"""This file contains the serializers for the files app."""

from rest_framework import serializers

from .models import Files


class FileDetailSerializer(serializers.ModelSerializer):
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
        # fields = ["id", "name", "size"]
        fields = "__all__"


class FileCreateSerializer(serializers.ModelSerializer):
    """Serializer for the files model."""

    class Meta:
        """Meta class for the serializer."""

        model = Files
        fields = ["name", "contents", "tags"]
