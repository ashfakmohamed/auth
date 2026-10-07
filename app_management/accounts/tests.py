from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class AccountPageTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')

    def test_profile_shows_authenticated_user(self):
        user = CustomUser.objects.create_user(
            username="ashfak",
            email="ashfak@example.com",
            password="Strong-password-2026!",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("profile"))
        self.assertContains(response, "ashfak@example.com")
