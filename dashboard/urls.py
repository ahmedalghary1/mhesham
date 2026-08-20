from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", views.dashboard_logout, name="logout"),
    path("", views.overview, name="overview"),
    path("content/<slug:key>/", views.model_list, name="model_list"),
    path("content/<slug:key>/new/", views.model_form, name="model_create"),
    path("content/<slug:key>/<int:pk>/edit/", views.model_form, name="model_edit"),
    path("content/<slug:key>/<int:pk>/delete/", views.model_delete, name="model_delete"),
    path("projects/<int:pk>/gallery/", views.project_gallery, name="project_gallery"),
    path("projects/<int:pk>/preview/", views.project_preview, name="project_preview"),
    path("reorder/<slug:key>/", views.reorder, name="reorder"),
    path("messages/<int:pk>/<slug:status>/", views.message_status, name="message_status"),
]
