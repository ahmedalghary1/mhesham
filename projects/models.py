from django.db import models
from django.urls import reverse
from core.models import OrderedModel


class Category(OrderedModel):
    name_ar = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name_en


class Project(OrderedModel):
    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    challenge_ar = models.TextField(blank=True)
    challenge_en = models.TextField(blank=True)
    direction_ar = models.TextField(blank=True)
    direction_en = models.TextField(blank=True)
    client = models.CharField(max_length=255, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    services_ar = models.CharField(max_length=300, blank=True)
    services_en = models.CharField(max_length=300, blank=True)
    cover_image = models.ImageField(upload_to="projects/covers/")
    behance_url = models.URLField(max_length=500, blank=True)
    external_url = models.URLField(max_length=500, blank=True)
    video_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    seo_title_ar = models.CharField(max_length=180, blank=True)
    seo_title_en = models.CharField(max_length=180, blank=True)
    seo_description_ar = models.CharField(max_length=320, blank=True)
    seo_description_en = models.CharField(max_length=320, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})


class ProjectImage(OrderedModel):
    LAYOUTS = (("full", "Full width"), ("half", "Half width"), ("portrait", "Portrait"), ("landscape", "Landscape"), ("grid", "Grid"))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="projects/gallery/")
    alt_ar = models.CharField(max_length=240, blank=True)
    alt_en = models.CharField(max_length=240, blank=True)
    layout_type = models.CharField(max_length=20, choices=LAYOUTS, default="full")

    def __str__(self):
        return f"{self.project} image {self.pk or ''}"
