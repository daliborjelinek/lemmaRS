from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, permissions

from .serializers import ResourceSerializer
from .models import Resource


class HeroViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Resource.objects.all().order_by('name')
    serializer_class = ResourceSerializer