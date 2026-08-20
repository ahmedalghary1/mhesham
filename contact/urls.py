from django.urls import path
from . import views

app_name = "contact"
urlpatterns = [path("", views.contact, name="contact"), path("send/", views.quick_contact, name="send")]
