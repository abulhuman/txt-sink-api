"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("admin/", admin.site.urls),
    path("files/", include("src.apps.files.urls")),
]
