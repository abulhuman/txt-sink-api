"""Model for created and modified fields."""

from django.db import models


class CreatedModified(models.Model):
    """Abstract model for created and modified fields."""

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class for the model."""

        abstract = True
