from django.contrib.auth import get_user_model
from django.test import TestCase


class DashboardAccessTests(TestCase):
    def test_anonymous_user_is_redirected(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/login/", response.url)

    def test_staff_user_can_open_overview(self):
        user = get_user_model().objects.create_user("owner", password="secure-test-pass", is_staff=True)
        self.client.force_login(user)
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total projects")
        self.assertContains(response, "css/dashboard-responsive.css")
