from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from certificates.models import Certificate, Education
from contact.forms import ContactMessageForm
from experience.models import Experience, VolunteerRole
from projects.models import Project
from .models import HomeContent, Skill


def home(request):
    home_content, _ = HomeContent.objects.get_or_create(pk=1)
    context = {
        "home": home_content,
        "projects": Project.objects.filter(is_published=True, is_featured=True).select_related("category")[:6],
        "skills": Skill.objects.all(),
        "experiences": Experience.objects.all(),
        "volunteering": VolunteerRole.objects.all(),
        "certificates": Certificate.objects.all(),
        "education": Education.objects.all(),
        "contact_form": ContactMessageForm(),
    }
    return render(request, "pages/home.html", context)


def about(request):
    home_content, _ = HomeContent.objects.get_or_create(pk=1)
    return render(request, "pages/about.html", {
        "home": home_content,
        "experiences": Experience.objects.all(),
        "volunteering": VolunteerRole.objects.all(),
        "education": Education.objects.all(),
    })


def robots_txt(request):
    lines = ["User-agent: *", "Disallow: /dashboard/", "Disallow: /django-admin/", "Sitemap: " + request.build_absolute_uri("/sitemap.xml")]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def switch_language(request, language):
    allowed = {code for code, _ in settings.LANGUAGES}
    if language not in allowed:
        return redirect("core:home")
    target = request.GET.get("next", f"/{language}/")
    if not url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        target = f"/{language}/"
    response = redirect(target)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, max_age=365 * 24 * 60 * 60, samesite="Lax", secure=not settings.DEBUG)
    return response


def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)


def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
