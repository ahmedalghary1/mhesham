from django.contrib import admin
from .models import Category, Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title_en", "category", "year", "is_featured", "is_published", "sort_order")
    list_filter = ("is_published", "is_featured", "category")
    search_fields = ("title_en", "title_ar", "client")
    prepopulated_fields = {"slug": ("title_en",)}
    inlines = [ProjectImageInline]

admin.site.register(Category)
