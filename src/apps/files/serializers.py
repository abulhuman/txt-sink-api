"""This file contains the serializers for the files app."""

from rest_framework import serializers

from src.general.serializers import CreatedModifiedSerializer

from .models import Files


class FileDetailSerializer(CreatedModifiedSerializer):
    """Serializer for the files model."""

    class Meta:
        """Meta class for the serializer."""

        model = Files
        fields = "__all__"


class FileListSerializer(serializers.ModelSerializer):
    """Serializer for the files model."""

    class Meta:
        """Meta class for the serializer."""

        model = Files
        fields = ["id", "modified_date", "name", "size", "tags", "url"]


class FileCreateSerializer(serializers.ModelSerializer):
    """Serializer for the files model.

    fields:
    name: str
    contents: str
    tags: str
    """

    class Meta:
        """Meta class for the serializer."""

        model = Files
        fields = ["name", "contents", "tags"]
