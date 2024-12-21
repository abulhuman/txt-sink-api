""" This file is used to register the Files model in the admin panel."""

from django.contrib import admin

from .models import Files, SearchTags

admin.site.register(Files)
admin.site.register(SearchTags)
