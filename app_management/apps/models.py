from django.conf import settings
from django.db import models


class App(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100, blank=True)
    points = models.PositiveIntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="tasks")
    screenshot = models.ImageField(upload_to="task_screenshots/")
    completed = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}: {self.app}"
