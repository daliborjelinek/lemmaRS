from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
from oauth2_provider.contrib.rest_framework import TokenHasScope

from rest_framework import viewsets, permissions, mixins
from rest_framework.views import APIView

from .serializers import ResourceSerializer, UserSerializer
from .models import Resource, User


class HeroViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Resource.objects.all().order_by('name')
    serializer_class = ResourceSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserViewSet, self).get_object()
