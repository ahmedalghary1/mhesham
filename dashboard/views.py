from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from contact.models import ContactMessage
from projects.models import Project, ProjectImage
from certificates.models import Certificate
from .decorators import staff_required
from .forms import ProjectGalleryUploadForm, StaffAuthenticationForm
from .registry import MODEL_REGISTRY, get_registered_model


class DashboardLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = StaffAuthenticationForm
    redirect_authenticated_user = True


@require_POST
def dashboard_logout(request):
    logout(request)
    return redirect("dashboard:login")


@staff_required
def overview(request):
    projects = Project.objects.all()
    context = {
        "total_projects": projects.count(),
        "published_projects": projects.filter(is_published=True).count(),
        "draft_projects": projects.filter(is_published=False).count(),
        "certificate_count": Certificate.objects.count(),
        "message_count": ContactMessage.objects.count(),
        "unread_count": ContactMessage.objects.filter(status="unread").count(),
        "latest_projects": projects.order_by("-updated_at")[:5],
        "latest_messages": ContactMessage.objects.all()[:5],
    }
    return render(request, "dashboard/overview.html", context)


def _registry_or_404(key):
    registered = get_registered_model(key)
    if not registered:
        raise PermissionDenied
    return registered


@staff_required
def model_list(request, key):
    model, title, search_fields = _registry_or_404(key)
    items = model.objects.all()
    query = request.GET.get("q", "").strip()
    if query and search_fields:
        condition = Q()
        for field in search_fields:
            condition |= Q(**{f"{field}__icontains": query})
        items = items.filter(condition)
    display_fields = [f for f in model._meta.fields if f.name not in {"id"}][:5]
    rows = [{"object": item, "values": [getattr(item, f.name) for f in display_fields]} for item in items[:200]]
    return render(request, "dashboard/model_list.html", {
        "model_key": key, "model_title": title, "fields": display_fields, "rows": rows, "query": query,
    })


@staff_required
def model_form(request, key, pk=None):
    model, title, _ = _registry_or_404(key)
    obj = get_object_or_404(model, pk=pk) if pk else None
    exclude = [f.name for f in model._meta.fields if not f.editable or f.auto_created]
    Form = modelform_factory(model, exclude=exclude)
    form = Form(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        saved = form.save()
        messages.success(request, f"{title} saved successfully.")
        if key == "projects":
            return redirect("dashboard:project_gallery", pk=saved.pk)
        return redirect("dashboard:model_list", key=key)
    return render(request, "dashboard/model_form.html", {"form": form, "model_title": title, "model_key": key, "object": obj})


@staff_required
@require_POST
def model_delete(request, key, pk):
    model, title, _ = _registry_or_404(key)
    obj = get_object_or_404(model, pk=pk)
    obj.delete()
    messages.success(request, f"{title} item deleted.")
    return redirect("dashboard:model_list", key=key)


@staff_required
def project_gallery(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectGalleryUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        start = project.gallery.count()
        for offset, image in enumerate(request.FILES.getlist("images")):
            ProjectImage.objects.create(project=project, image=image, sort_order=start + offset)
        messages.success(request, "Gallery images uploaded.")
        return redirect("dashboard:project_gallery", pk=pk)
    return render(request, "dashboard/project_gallery.html", {"project": project, "form": form})


@staff_required
def project_preview(request, pk):
    project = get_object_or_404(Project.objects.select_related("category").prefetch_related("gallery"), pk=pk)
    return render(request, "projects/project_detail.html", {"project": project, "previous_project": None, "next_project": None, "is_preview": True})


@staff_required
@require_POST
def reorder(request, key):
    model, _, _ = _registry_or_404(key)
    if not any(f.name == "sort_order" for f in model._meta.fields):
        return JsonResponse({"ok": False}, status=400)
    ids = request.POST.getlist("ids[]")
    for position, pk in enumerate(ids):
        model.objects.filter(pk=pk).update(sort_order=position)
    return JsonResponse({"ok": True})


@staff_required
@require_POST
def message_status(request, pk, status):
    if status not in {"unread", "read", "archived"}:
        return JsonResponse({"ok": False}, status=400)
    message = get_object_or_404(ContactMessage, pk=pk)
    message.status = status
    message.save(update_fields=["status"])
    return redirect("dashboard:model_list", key="messages")
