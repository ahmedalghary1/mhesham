from django.urls import path
from . import views

app_name = "projects"
urlpatterns = [
    path("", views.project_list, name="list"),
    path("filter/", views.filter_projects, name="filter"),
    path("<slug:slug>/", views.project_detail, name="detail"),
]
