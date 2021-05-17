from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import FileUploadView

router = routers.DefaultRouter()
router.register('user', views.UserViewSet, 'current')
router.register('project', views.ProjectViewSet)
router.register('project-group', views.ProjectGroupViewSet)
router.register('resource', views.ResourceViewSet)
router.register('permission-level', views.PermissionLevelViewSet)
router.register('permission-request', views.PermissionRequestViewSet)
router.register('reservation', views.ReservationViewSet)
router.register('tag', views.TagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', include('rest_social_auth.urls_jwt_pair')),
    path('image/', FileUploadView.as_view()),
    # path("django_query_profiler/", include("django_query_profiler.client.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
