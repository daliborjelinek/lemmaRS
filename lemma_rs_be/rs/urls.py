from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet, 'current')
router.register('project', views.ProjectViewSet)
router.register('project-group', views.ProjectGroupViewSet)
router.register('resource', views.ResourceViewSet)
router.register('permissionLevel', views.PermissionLevelViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
