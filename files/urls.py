""" URLs for the files app """

from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_files, name="list_files"),
    path("upload/", views.upload, name="upload"),
    path("search/", views.search_files, name="search_files"),
    path("<int:file_id>/", views.get_file, name="get_file"),
    path("<int:file_id>/delete/", views.delete_file, name="delete_file"),
]
