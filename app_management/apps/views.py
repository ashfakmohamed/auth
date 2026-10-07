from pathlib import Path

from django.db import transaction
from django.db.models import F
from django.http import FileResponse
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import App, Task
from .serializers import AppSerializer, TaskSerializer


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = Task.objects.select_related("user", "app")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], url_path="screenshot")
    def download_screenshot(self, request, pk=None):
        task = self.get_object()
        filename = Path(task.screenshot.name).name
        return FileResponse(task.screenshot.open("rb"), as_attachment=True, filename=filename)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAdminUser],
    )
    def approve(self, request, pk=None):
        with transaction.atomic():
            task = Task.objects.select_for_update().select_related("app", "user").get(pk=pk)
            if not task.completed:
                task.completed = True
                task.approved_at = timezone.now()
                task.save(update_fields=["completed", "approved_at"])
                type(task.user).objects.filter(pk=task.user_id).update(
                    points=F("points") + task.app.points
                )
                task.user.refresh_from_db(fields=["points"])
        return Response(TaskSerializer(task, context={"request": request}).data, status=status.HTTP_200_OK)
