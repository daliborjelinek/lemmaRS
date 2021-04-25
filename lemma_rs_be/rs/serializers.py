from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Resource, Project, ProjectGroup, PermissionLevel, Tag, User


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname']


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'fullname', 'role', 'role_display', 'email', 'phone', 'address',
                  'calendar_data', 'room']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role_display', 'email', 'phone', 'address', 'calendar_data', 'room']


class ResourceFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'description', 'created_at')


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        provider = SimpleUserSerializer(read_only=True)
        tags = serializers.SlugRelatedField(
            many=True,
            slug_field='name',
            queryset=Tag.objects.all()
        )
        fields = ('name', 'description', 'price', 'image', 'provider', 'tags')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


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
