from rest_framework import serializers

from .models import Resource, Project, ProjectGroup, PermissionLevel, Tag, User, PermissionRequest, Reservation, \
    ReservedResource


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname']


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'fullname', 'permission_level', 'role', 'role_display', 'email',
                  'phone', 'address', 'calendar_data', 'room']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role_display', 'email', 'phone', 'address', 'calendar_data', 'room']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ResourceSerializer(serializers.ModelSerializer):
    # tag_str = serializers.CharField(source='tags', read_only=True)
    tags_str = serializers.StringRelatedField(source='tags', many=True, read_only=True)
    required_permission_level_str = serializers.StringRelatedField(source='required_permission_level', read_only=True)
    provider_str = serializers.StringRelatedField(source='provider', read_only=True)

    class Meta:
        model = Resource
        provider = SimpleUserSerializer(read_only=True)
        fields = (
            'id', 'active', 'name', 'description', 'internal_notes', 'cost', 'image_url', 'provider', 'provider_str',
            'tags', 'tags_str', 'required_permission_level', 'required_permission_level_str')


class ProjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    members = UserReadSerializer(many=True, read_only=True)
    owner = UserReadSerializer(read_only=True)

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['group'] = ProjectGroupSerializer(instance.group).data
    #     return response

    class Meta:
        model = Project
        fields = '__all__'


class PermissionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionLevel
        fields = '__all__'


# PERMISSION REQUESTS
class PermissionRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionRequest
        fields = ('requested_level', 'reason')


class PermissionRequestResolveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionRequest
        fields = ('expiration_date', 'approved', 'response')


class PermissionRequestFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionRequest
        fields = '__all__'


class ReservedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedResource
        fields = ('real_return_date', 'real_pickup_date', 'comment', 'resource')


class ReservationSerializer(serializers.ModelSerializer):
    resources = ReservedResourceSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ('pickup_date_time', 'return_date_time', 'picked_up', 'applicant', 'approved', 'approved_by','resources')


class ReservationCreateSerializer(serializers.ModelSerializer):
    resources = serializers.ListField(
        child=serializers.IntegerField()
    )

    class Meta:
        model = Reservation
        fields = ('pickup_date_time', 'return_date_time', 'resources')
