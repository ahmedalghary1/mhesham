from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from projects.models import Project


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ["core:home", "core:about", "projects:list", "contact:contact"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
