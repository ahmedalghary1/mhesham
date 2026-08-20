from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Category, Project


def project_list(request):
    projects = Project.objects.filter(is_published=True).select_related("category")
    category = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()
    if category:
        projects = projects.filter(category__slug=category)
    if query:
        projects = projects.filter(Q(title_ar__icontains=query) | Q(title_en__icontains=query) | Q(description_ar__icontains=query) | Q(description_en__icontains=query))
    return render(request, "projects/project_list.html", {"projects": projects, "categories": Category.objects.all(), "active_category": category})


def filter_projects(request):
    projects = Project.objects.filter(is_published=True).select_related("category")
    category = request.GET.get("category")
    if category:
        projects = projects.filter(category__slug=category)
    lang = "ar" if request.LANGUAGE_CODE == "ar" else "en"
    return JsonResponse({"projects": [{
        "title": getattr(p, f"title_{lang}"), "description": getattr(p, f"description_{lang}"),
        "category": getattr(p.category, f"name_{lang}", "") if p.category else "", "year": p.year,
        "url": p.get_absolute_url(), "image": p.cover_image.url,
    } for p in projects]})


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.select_related("category").prefetch_related("gallery"), slug=slug, is_published=True)
    ordered = list(Project.objects.filter(is_published=True).order_by("sort_order", "pk"))
    idx = ordered.index(project)
    previous = ordered[idx - 1] if idx > 0 else None
    following = ordered[idx + 1] if idx < len(ordered) - 1 else None
    return render(request, "projects/project_detail.html", {"project": project, "previous_project": previous, "next_project": following})
