from django.utils import timezone
from rest_framework import serializers
from datetime import datetime
from django.utils.timezone import make_aware

from .models import Resource, Project, ProjectGroup, PermissionLevel, Tag, User, PermissionRequest, Reservation, \
    ReservedResource


class UserHolidaySerializer(serializers.JSONField):
    def to_representation(self, data):
        data = list(
            filter(lambda x: make_aware(datetime.strptime((x['to']), "%Y-%m-%dT%H:%M:%S.%fZ")) >= timezone.now(), data))
        return super().to_representation(data)


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname']


class UserReadSerializer(serializers.ModelSerializer):
    holidays = UserHolidaySerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'fullname', 'permission_level', 'role', 'role_display', 'email',
                  'phone', 'address', 'calendar_data', 'holidays', 'room']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role_display', 'email', 'phone', 'address', 'calendar_data', 'room', 'holidays']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BlockingIntervalSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(source='reservation.pickup_date_time')
    end = serializers.DateTimeField(source='blocking_end')
    reservation_id = serializers.IntegerField(source='reservation.id')
    reservation_name = serializers.StringRelatedField(source='reservation.project')

    class Meta:
        model = ReservedResource
        # fields = ('id', 'start', 'end')
        fields = ('id', 'start', 'end', 'reservation_name', 'reservation_id')


class ResourceSerializer(serializers.ModelSerializer):
    # tag_str = serializers.CharField(source='tags', read_only=True)
    tags_str = serializers.StringRelatedField(source='tags', many=True, read_only=True)
    blocking_reservations = BlockingIntervalSerializer(read_only=True, many=True)
    inv_numbers = serializers.JSONField()

    class Meta:
        model = Resource
        fields = ('not_returned',
            'id', 'active', 'name', 'description', 'internal_notes', 'cost', 'image_url', 'provider',
            'tags', 'tags_str', 'required_permission_level', 'blocking_reservations', 'inv_numbers')


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
        fields = ('id', 'expiration_date', 'approved', 'response')


class PermissionRequestFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionRequest
        depth = 1
        fields = '__all__'


class ReservedResourceSerializer(serializers.ModelSerializer):
    resource_str = serializers.StringRelatedField(source='resource', read_only=True)

    class Meta:
        model = ReservedResource
        fields = ('id', 'real_return_date', 'real_pickup_date', 'comment', 'resource_str', 'reservation')


class ReservationSerializer(serializers.ModelSerializer):
    resources = ReservedResourceSerializer(many=True)
    applicant = SimpleUserSerializer(read_only=True)
    project = serializers.StringRelatedField(read_only=True)
    fully_returned = serializers.BooleanField(read_only=True)

    class Meta:
        depth = 1
        model = Reservation
        fields = (
            'id', 'pickup_date_time', 'return_date_time', 'picked_up', 'applicant', 'approved', 'approved_by',
            'resources', 'project', 'created_at', 'fully_returned',)


class ReservationCreateSerializer(serializers.ModelSerializer):
    resources = serializers.ListField(
        child=serializers.IntegerField()
    )
    approval_required = serializers.BooleanField(allow_null=True)

    class Meta:
        model = Reservation
        fields = ('pickup_date_time', 'return_date_time', 'resources', 'approval_required', 'project')
