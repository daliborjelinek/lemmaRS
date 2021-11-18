from django.db.models import Q, Prefetch
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_api_key.permissions import HasAPIKey
from url_filter.integrations.drf import DjangoFilterBackend

from . import serializers
from .models import User, Project, ProjectGroup, Resource, PermissionLevel, Tag, Image, PermissionRequest, Reservation, \
    ReservedResource
from .permissions import UserPermission, ProjectPermission, CommonReadAdminAndProviderAll, IsAdmin
from .serializers import ProjectSerializer, ProjectGroupSerializer, ResourceSerializer, PermissionLevelSerializer, \
    TagSerializer, PermissionRequestFullSerializer, PermissionRequestCreateSerializer, \
    PermissionRequestResolveSerializer, ReservationSerializer, ReservationCreateSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin, GenericViewSet):
    permission_classes = [UserPermission | HasAPIKey]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['role']

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.UserUpdateSerializer
        return serializers.UserReadSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserViewSet, self).get_object()


@extend_schema_view(
    list=extend_schema(parameters=[
        OpenApiParameter(name='uco', description='filter projects by UCO', required=False, type=str),
    ])
)
class ProjectViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin, GenericViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission | HasAPIKey]
    queryset = Project.objects.order_by('-created_at').all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Project.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(Q(members__username=username) | Q(owner__username=username))
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='userId', description='member ID', required=True, type=str),

        ],
        request=None,

    )
    @action(detail=True, methods=['PUT'], name='Add member')
    def add_member(self, request, pk=None):
        project = self.get_object()

        project.members.add(User.objects.get(pk=request.query_params['userId']))

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'], name='Remove member')
    def remove_member(self, request, pk=None):
        project = self.get_object()
        user = project.members.get(pk=request.query_params['userId'])
        project.members.remove(user)
        return Response(status=status.HTTP_202_ACCEPTED)


class ProjectGroupViewSet(viewsets.ModelViewSet):
    queryset = ProjectGroup.objects.all()
    permission_classes = [CommonReadAdminAndProviderAll]
    serializer_class = ProjectGroupSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    # queryset = Resource.objects.order_by('name').all().prefetch_related('tags')
    queryset = Resource.objects.order_by('name').all().prefetch_related('tags', Prefetch(
        'reservations',
        queryset=ReservedResource.objects.filter(
            (Q(reservation__approved=True) | Q(reservation__approved=None)) &  # exclude declined reservations
            (Q(reservation__return_date_time__gt=timezone.now()) |  # include upcoming and ongoing reservations
              (Q(real_pickup_date__isnull=False) & Q(real_return_date__isnull=True))))  # include picked up reservations
        .select_related('reservation', ),
        to_attr='blocking_reservations'
    )
                                                                        )

    permission_classes = [CommonReadAdminAndProviderAll | HasAPIKey]
    serializer_class = ResourceSerializer


class PermissionLevelViewSet(viewsets.ModelViewSet):
    queryset = PermissionLevel.objects.all()
    permission_classes = [CommonReadAdminAndProviderAll]
    serializer_class = PermissionLevelSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [CommonReadAdminAndProviderAll]
    serializer_class = TagSerializer


class PermissionRequestViewSet(viewsets.ModelViewSet):
    queryset = PermissionRequest.objects.order_by('-created_at').all()
    permission_classes = [CommonReadAdminAndProviderAll]
    serializer_class = PermissionRequestFullSerializer

    @extend_schema(
        request=PermissionRequestCreateSerializer,
        responses={204: None}
    )
    @action(methods=['PUT'], detail=False, name='Send request for higher permissions',
            permission_classes=[IsAuthenticated])
    def send_request(self, request):
        serializer = PermissionRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            reason = serializer.validated_data.get('reason')
            applicant = request.user
            # requested_level = PermissionLevel.objects.get(pk=serializer.validated_data.get('requested_level'))
            PermissionRequest.objects.create(reason=reason, applicant=applicant,
                                             requested_level=serializer.validated_data.get('requested_level'))
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=PermissionRequestResolveSerializer,
        responses={204: None}
    )
    @action(methods=['PUT'], detail=True, name='Send result of permission request', permission_classes=[IsAdmin])
    def resolve_request(self, request, pk):
        serializer = PermissionRequestResolveSerializer(data=request.data)
        if serializer.is_valid():
            approved = serializer.validated_data.get('approved')
            approved_by = request.user
            response = serializer.validated_data.get('response')
            expiration_date = serializer.validated_data.get('expiration_date')
            PermissionRequest.objects.filter(pk=pk).update(approved=approved, approved_by=approved_by,
                                                           response=response,
                                                           expiration_date=expiration_date)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationViewSet(viewsets.ModelViewSet):
    # todo: exlude porvider from
    queryset = Reservation.objects.all().order_by('-created_at')
    permission_classes = [CommonReadAdminAndProviderAll]
    serializer_class = ReservationSerializer

    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.picked_up:
            return Response("delete of picked up reservation is not allowed", status=status.HTTP_400_BAD_REQUEST)
        if reservation.return_date_time < timezone.now():
            return Response("delete of ended reservation is not allowed", status=status.HTTP_400_BAD_REQUEST)
        reservation.delete()
        return Response(data='delete success')

    @extend_schema(
        request=ReservationCreateSerializer,
        responses={204: None}
    )
    @action(methods=['PUT'], detail=False, name='CreateReservation')
    def create_reservation(self, request):
        serializer = ReservationCreateSerializer(data=request.data)
        if serializer.is_valid():
            pickup_date_time = serializer.validated_data.get('pickup_date_time')
            approval_required = serializer.validated_data.get('approval_required')
            return_date_time = serializer.validated_data.get('return_date_time')
            resources = serializer.validated_data.get('resources')
            applicant = request.user
            project = serializer.validated_data.get('project')

            reservation = Reservation.objects.create(project=project, pickup_date_time=pickup_date_time,
                                                     return_date_time=return_date_time,
                                                     applicant=applicant, approved=None if approval_required else True)

            for resource_id in resources:
                resource = Resource.objects.get(pk=resource_id)
                ReservedResource.objects.create(resource=resource, reservation=reservation)

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True, name='TransmitReservation')
    def transmit_reservation(self, request, pk):
        reservation = self.get_object()
        if not reservation.approved:
            return Response('This reservation needs to be approved first.', status=status.HTTP_400_BAD_REQUEST)
        if reservation.picked_up:
            return Response('Reservation has been already transmitted', status=status.HTTP_400_BAD_REQUEST)
        if reservation.pickup_date_time > timezone.now():
            return Response("Transmit before claimed pickup date not allowed", status=status.HTTP_400_BAD_REQUEST)
        if reservation.return_date_time < timezone.now():
            return Response("Transmit after claimed return date not allowed", status=status.HTTP_400_BAD_REQUEST)

        ReservedResource.objects.filter(reservation_id=pk).update(real_pickup_date=timezone.now())
        reservation.picked_up = True
        reservation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=True, name='resolve_reservation_request')
    def resolve_reservation_request(self, request, pk):
        reservation = self.get_object()
        print(reservation.approved_by)
        if reservation.approved_by is None:
            reservation.approved_by = request.user
            reservation.approved = request.data['approved']
            reservation.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Reservation has been already approved", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True, name='')
    def take_up_resources(self, request, pk):
        reservation = self.get_object()
        if not reservation.picked_up:
            return Response("Cant take up reservation which was not picked up", status=status.HTTP_400_BAD_REQUEST)
        ids = request.data['resources']
        print(ids)
        already_returned_resources = ReservedResource.objects.filter(pk__in=ids).filter(
            real_return_date__isnull=False).values_list('id', flat=True)
        print(already_returned_resources)
        if len(already_returned_resources) > 0:
            return Response('ids ' + ', '.join(map(str, already_returned_resources)) + ' was already returned',
                            status=status.HTTP_400_BAD_REQUEST)
        ReservedResource.objects.filter(pk__in=ids).update(real_return_date=timezone.now())
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    parser_classes = (MultiPartParser,)

    def post(self, request, ):
        file = request.data['file']
        image = Image.objects.create(file=file)
        print(image.file.url)
        return Response(image.file.url, status=200)
