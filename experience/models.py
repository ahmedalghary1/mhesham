from django.db import models
from core.models import OrderedModel


class Experience(OrderedModel):
    company = models.CharField(max_length=180)
    position_ar = models.CharField(max_length=180)
    position_en = models.CharField(max_length=180)
    location_ar = models.CharField(max_length=180, blank=True)
    location_en = models.CharField(max_length=180, blank=True)
    employment_type = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    company_logo = models.ImageField(upload_to="experience/", blank=True)

    def __str__(self):
        return self.company


class VolunteerRole(OrderedModel):
    organization = models.CharField(max_length=180)
    role_ar = models.CharField(max_length=180)
    role_en = models.CharField(max_length=180)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.organization} - {self.role_en}"
