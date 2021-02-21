from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Resource

User = get_user_model()

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'description', 'created_at')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'description', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fullname')
