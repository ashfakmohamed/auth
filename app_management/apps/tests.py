import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from .models import App, Task


GIF_BYTES = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==")


@override_settings(MEDIA_ROOT="/tmp/app-management-test-media")
class ApiPermissionTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("user", password="Strong-password-2026!")
        self.other = CustomUser.objects.create_user("other", password="Strong-password-2026!")
        self.admin = CustomUser.objects.create_superuser("admin", "admin@example.com", "Strong-password-2026!")
        self.app = App.objects.create(
            name="Example App",
            link="https://example.com",
            category="Utility",
            sub_category="",
            points=10,
        )

    def screenshot(self, name="proof.gif"):
        return SimpleUploadedFile(name, GIF_BYTES, content_type="image/gif")

    def test_regular_user_can_list_apps_but_cannot_create_them(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get(reverse("app-list")).status_code, status.HTTP_200_OK)
        response = self.client.post(
            reverse("app-list"),
            {"name": "Blocked", "link": "https://example.com", "category": "Test", "points": 1},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tasks_are_scoped_to_current_user_and_hide_file_url(self):
        own = Task.objects.create(user=self.user, app=self.app, screenshot=self.screenshot("own.gif"))
        Task.objects.create(user=self.other, app=self.app, screenshot=self.screenshot("other.gif"))
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("task-list"))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], own.id)
        self.assertNotIn("screenshot", response.data[0])

    def test_non_owner_cannot_download_screenshot(self):
        task = Task.objects.create(user=self.other, app=self.app, screenshot=self.screenshot())
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("task-download-screenshot", args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_admin_can_approve_and_points_are_awarded_once(self):
        task = Task.objects.create(user=self.user, app=self.app, screenshot=self.screenshot())
        self.client.force_authenticate(self.user)
        self.assertEqual(
            self.client.post(reverse("task-approve", args=[task.id])).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(self.admin)
        self.assertEqual(
            self.client.post(reverse("task-approve", args=[task.id])).status_code,
            status.HTTP_200_OK,
        )
        self.client.post(reverse("task-approve", args=[task.id]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.points, 10)
