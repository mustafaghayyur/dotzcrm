from django.urls import include, path
from rest_framework import routers

from .restviews import users

# REST API; register all SiewSets...
router = routers.DefaultRouter()
router.register(r"users", users.UserViewSet)
router.register(r"groups", users.GroupViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),  # Additionally, we include login URLs for the browsable API.
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
