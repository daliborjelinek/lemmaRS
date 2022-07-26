from django.db import transaction
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
from lemma_rs_be.Mailer import Mailer

from . import serializers
from .models import User, Project, ProjectGroup, Resource, PermissionLevel, Tag, Image, PermissionRequest, Reservation, \
    ReservedResource
from .permissions import UserPermission, ProjectPermission, CommonReadAdminAndProviderAll, IsAdmin, IsProvider, \
    IsReservationOwner
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
            ~Q(real_return_date__isnull=False) &  # exclude already returned resources
            ~Q(reservation__approved=False) &  # exclude declined reservations
            (Q(reservation__return_date_time__gt=timezone.now()) |  # include upcoming and ongoing reservations
             Q(real_pickup_date__isnull=False)))  # include picked up reservations before declared pickup date
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
            pr = PermissionRequest.objects.create(reason=reason, applicant=applicant,
                                                  requested_level=serializer.validated_data.get('requested_level'))
            Mailer.send_new_permission_request_email(pr)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=PermissionRequestResolveSerializer,
        responses={204: None}
    )
    @action(methods=['PUT'], detail=True, name='Send result of permission request',
            permission_classes=[IsAdmin | IsProvider])
    def resolve_request(self, request, pk):
        serializer = PermissionRequestResolveSerializer(data=request.data)
        if serializer.is_valid():
            approved = serializer.validated_data.get('approved')
            approved_by = request.user
            response = serializer.validated_data.get('response')
            expiration_date = serializer.validated_data.get('expiration_date')
            pr = PermissionRequest.objects.get(pk=pk)
            pr.approved = approved
            pr.approved_by = approved_by
            pr.response = response
            pr.expiration_date = expiration_date
            pr.save()
            print(pr.applicant.email)
            Mailer.send_permission_request_result_email(pr)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationViewSet(viewsets.ModelViewSet):
    # todo: exlude porvider from
    queryset = Reservation.objects.all().order_by('-created_at')
    permission_classes = [IsReservationOwner | CommonReadAdminAndProviderAll]
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
    @action(methods=['PUT'], detail=False, name='CreateReservation', permission_classes=[IsAuthenticated])
    def create_reservation(self, request):
        serializer = ReservationCreateSerializer(data=request.data)
        if serializer.is_valid():
            pickup_date_time = serializer.validated_data.get('pickup_date_time')
            approval_required = serializer.validated_data.get('approval_required')
            return_date_time = serializer.validated_data.get('return_date_time')
            resources = serializer.validated_data.get('resources')
            applicant = request.user
            project = serializer.validated_data.get('project')
            provider = serializer.validated_data.get('provider')

            reservation = Reservation(project=project, pickup_date_time=pickup_date_time,
                                      return_date_time=return_date_time,
                                      applicant=applicant, provider=provider,
                                      approved=None if approval_required else True)
            resources_objects = []
            for resource_id in resources:
                resource = Resource.objects.get(pk=resource_id)
                conflict = ReservedResource.objects.filter(
                    Q(resource_id=resource_id) &  # same id
                    ~Q(reservation__approved=False) &  # approved
                    (
                            (
                                    Q(
                                        reservation__return_date_time__gt=timezone.now()) &  # reservation end is in future
                                    Q(real_return_date__isnull=True)  # not returned yet
                            ) &  # exclude reservation which already ended or being returned
                            (
                                #  https://www.mssqltips.com/sqlservertip/5854/using-tsql-to-find-events-that-overlap-or-dont-in-sql-server/
                                    Q(reservation__pickup_date_time__lt=reservation.return_date_time)
                                    #  res. which started before end of this reservation
                                    &
                                    Q(reservation__return_date_time__gt=reservation.pickup_date_time)
                                    #  res. which ending after start of this reservation
                            )  # time overlaps (pickup and return at the same time is allowed)
                    )
                ).exists()
                if conflict:
                    return Response(f'Resource {resource.name} is already reserved in selected period.',
                                    status=status.HTTP_400_BAD_REQUEST)
                resources_objects.append(ReservedResource(resource=resource, reservation=reservation))
            reservation.save()
            ReservedResource.objects.bulk_create(resources_objects)
            Mailer.send_new_reservation_email(reservation)
            if reservation.approved is None:
                Mailer.send_reservation_approval_request_email(reservation)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True, name='TransmitReservation', permission_classes=[IsAdmin | IsProvider])
    def transmit_reservation(self, request, pk):
        reservation = self.get_object()
        if not reservation.approved:
            return Response('This reservation needs to be approved first.', status=status.HTTP_400_BAD_REQUEST)
        if reservation.picked_up:
            return Response('Reservation has been already transmitted', status=status.HTTP_400_BAD_REQUEST)
        # if reservation.pickup_date_time > timezone.now():
        #    return Response("Transmit before claimed pickup date not allowed", status=status.HTTP_400_BAD_REQUEST)
        if reservation.return_date_time < timezone.now():
            return Response("Transmit after claimed return date not allowed", status=status.HTTP_400_BAD_REQUEST)

        ReservedResource.objects.filter(reservation_id=pk).update(real_pickup_date=timezone.now())
        reservation.picked_up = True
        reservation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=True, name='resolve_reservation_request', permission_classes=[IsAdmin | IsProvider])
    def resolve_reservation_request(self, request, pk):
        reservation = self.get_object()
        print(reservation.approved_by)
        if reservation.approved_by is None:
            reservation.approved_by = request.user
            reservation.approved = request.data['approved']
            reservation.save()
            Mailer.send_reservation_approval_request_result_email(reservation)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Reservation has been already approved", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True, name='take_up_resources', permission_classes=[IsAdmin | IsProvider])
    def take_up_resources(self, request, pk):
        reservation = self.get_object()
        if not reservation.picked_up:
            return Response("Cant take up reservation which was not picked up", status=status.HTTP_400_BAD_REQUEST)
        selected_resources = request.data['resources']
        already_returned_resources = ReservedResource.objects.filter(pk__in=selected_resources.keys()).filter(
            real_return_date__isnull=False).values_list('id', flat=True)
        if len(already_returned_resources) > 0:
            return Response('ids ' + ', '.join(map(str, already_returned_resources)) + ' was already returned',
                            status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            for res_id, comment in selected_resources.items():
                ReservedResource.objects.filter(pk=res_id).update(real_return_date=timezone.now(), comment=comment)

        return Response(status=status.HTTP_204_NO_CONTENT)


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated | HasAPIKey]
    parser_classes = (MultiPartParser,)

    def post(self, request, ):
        file = request.data['file']
        image = Image.objects.create(file=file)
        print(image.file.url)
        return Response(image.file.url, status=200)
