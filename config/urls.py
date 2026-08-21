from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve as serve_media

from core.sitemaps import ProjectSitemap, StaticViewSitemap

sitemaps = {"static": StaticViewSitemap, "projects": ProjectSitemap}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("language/<str:language>/", __import__("core.views", fromlist=["switch_language"]).switch_language, name="switch_language"),
    path("robots.txt", __import__("core.views", fromlist=["robots_txt"]).robots_txt, name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("projects/", include("projects.urls")),
    path("contact/", include("contact.urls")),
    prefix_default_language=True,
)

if settings.SERVE_MEDIA:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve_media, {"document_root": settings.MEDIA_ROOT}),
    ]

handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"
