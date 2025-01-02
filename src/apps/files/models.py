""" This module contains the models for the files app. """

from django.db import models

from src.general.models import CreatedModified


class Files(CreatedModified):
    """Model for files"""
    id = models.AutoField(primary_key=True)  # noqa A003
    name = models.CharField(max_length=255)
    uri = models.URLField()
    size = models.IntegerField()
    contents = models.TextField()
    tags = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(f"📄; id={self.id} - {self.name} - tags={self.tags}")

    class Meta:
        """Meta class for the model"""
        db_table = "files"


class SearchTags(CreatedModified):
    """Model for search tags"""
    id = models.AutoField(primary_key=True)  # noqa A003
    tag_name = models.CharField(max_length=255)
    file = models.ForeignKey(Files, on_delete=models.CASCADE)

    class Meta:
        """Meta class for the model"""
        db_table = "search_tags"
