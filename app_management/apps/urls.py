from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AppViewSet, TaskViewSet

router = DefaultRouter()
router.register("apps", AppViewSet, basename="app")
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = [path("", include(router.urls))]
