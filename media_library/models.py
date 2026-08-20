from pathlib import Path
from django.core.exceptions import ValidationError
from django.db import models

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".pdf"}


def validate_media(upload):
    ext = Path(upload.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Unsupported file type.")
    if upload.size > 20 * 1024 * 1024:
        raise ValidationError("Files must be 20 MB or smaller.")


class MediaAsset(models.Model):
    title = models.CharField(max_length=160)
    file = models.FileField(upload_to="library/%Y/%m/", validators=[validate_media])
    alt_ar = models.CharField(max_length=240, blank=True)
    alt_en = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title
