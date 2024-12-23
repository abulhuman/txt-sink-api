"""
URL configuration for core project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("files/", include("files.urls")),
]
