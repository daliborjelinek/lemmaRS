from rest_framework import serializers

from .models import Resource, Tag


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'description', 'created_at')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'description', 'created_at')