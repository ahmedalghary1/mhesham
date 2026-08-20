import tempfile
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from .models import Project


def image_upload():
    stream = BytesIO()
    Image.new("RGB", (24, 24), "#3b3b8e").save(stream, "PNG")
    return SimpleUploadedFile("cover.png", stream.getvalue(), content_type="image/png")


class ProjectVisibilityTests(TestCase):
    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        self.media.cleanup()

    def test_only_published_project_is_public(self):
        Project.objects.create(title_ar="منشور", title_en="Published", slug="published", cover_image=image_upload(), is_published=True)
        Project.objects.create(title_ar="مسودة", title_en="Draft", slug="draft", cover_image=image_upload(), is_published=False)
        self.assertEqual(self.client.get("/en/projects/published/").status_code, 200)
        self.assertEqual(self.client.get("/en/projects/draft/").status_code, 404)
