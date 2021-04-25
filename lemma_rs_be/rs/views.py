from django.db.models import Q
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from . import serializers
from .permissions import UserPermission, ProjectPermission, ProjectGroupPermission, ResourcePermission, \
    PermissionLevelPermission, TagPermission
from .models import User, Project, ProjectGroup, Resource, PermissionLevel, Tag
from .serializers import ProjectSerializer, ProjectGroupSerializer, ResourceSerializer, PermissionLevelSerializer, \
    TagSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin, GenericViewSet):
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']

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
            queryset = queryset.filter(Q(members__username=username) | Q(owner=username))
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
    permission_classes = [ProjectGroupPermission]
    serializer_class = ProjectGroupSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    permission_classes = [ResourcePermission]
    serializer_class = ResourceSerializer


class PermissionLevelViewSet(viewsets.ModelViewSet):
    queryset = PermissionLevel.objects.all()
    permission_classes = [PermissionLevelPermission]
    serializer_class = PermissionLevelSerializer


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    permission_classes = [TagPermission]
    serializer_class = TagSerializer
