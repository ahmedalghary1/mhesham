from django.db import models
from core.models import OrderedModel


class Certificate(OrderedModel):
    title_ar = models.CharField(max_length=180)
    title_en = models.CharField(max_length=180)
    organization_ar = models.CharField(max_length=180, blank=True)
    organization_en = models.CharField(max_length=180, blank=True)
    year = models.PositiveIntegerField()
    certificate_image = models.ImageField(upload_to="certificates/images/", blank=True)
    certificate_pdf = models.FileField(upload_to="certificates/pdfs/", blank=True)
    verification_url = models.URLField(max_length=500, blank=True)
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title_en


class Education(OrderedModel):
    title_ar = models.CharField(max_length=240)
    title_en = models.CharField(max_length=240)
    institution_ar = models.CharField(max_length=180, blank=True)
    institution_en = models.CharField(max_length=180, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title_en
