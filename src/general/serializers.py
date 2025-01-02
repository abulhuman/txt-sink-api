"""Serializers for the general app."""

from rest_framework import serializers


class CreatedModifiedSerializer(serializers.ModelSerializer):
    """Serializer for the CreatedModified model."""

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        """Meta class for the serializer."""

        fields = "__all__"
