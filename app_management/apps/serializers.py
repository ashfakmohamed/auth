from rest_framework import serializers

from .models import App, Task


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ("id", "name", "link", "category", "sub_category", "points")


class TaskSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    app_name = serializers.CharField(source="app.name", read_only=True)
    screenshot = serializers.ImageField(write_only=True)
    screenshot_uploaded = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "user",
            "username",
            "app",
            "app_name",
            "screenshot",
            "screenshot_uploaded",
            "completed",
            "approved_at",
            "created_at",
        )
        read_only_fields = ("id", "user", "completed", "approved_at", "created_at")

    def get_screenshot_uploaded(self, instance):
        return bool(instance.screenshot)

    def validate_screenshot(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Screenshots must be 5 MB or smaller.")
        allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        content_type = getattr(value, "content_type", "")
        if content_type not in allowed_types:
            raise serializers.ValidationError("Upload a JPEG, PNG, WebP, or GIF image.")
        return value
