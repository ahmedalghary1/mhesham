from django.test import TestCase
from django.contrib.staticfiles import finders
from .models import HomeContent, SiteSetting


class PublicPageTests(TestCase):
    def setUp(self):
        SiteSetting.objects.create(pk=1)
        HomeContent.objects.create(pk=1)

    def test_arabic_home_is_rtl(self):
        response = self.client.get("/ar/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="ar" dir="rtl"')
        self.assertContains(response, "محمد هشام")

    def test_english_home_is_ltr(self):
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="en" dir="ltr"')
        self.assertContains(response, "Mohamed Hesham")

    def test_responsive_assets_and_safe_area_viewport_are_present(self):
        response = self.client.get("/en/")
        self.assertContains(response, "viewport-fit=cover")
        self.assertContains(response, "css/responsive-pro.css")

    def test_hero_uses_real_software_logo_assets(self):
        response = self.client.get("/en/")
        for filename in ("photoshop.svg", "illustrator.svg", "figma.svg", "canva.svg", "indesign.svg", "premiere-pro.svg"):
            self.assertIsNotNone(finders.find(f"icons/software/{filename}"))
            self.assertContains(response, f"icons/software/{filename}")

    def test_robots_protects_dashboard(self):
        response = self.client.get("/robots.txt")
        self.assertContains(response, "Disallow: /dashboard/")
