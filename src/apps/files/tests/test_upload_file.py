"""Integration tests for the Files API."""

from unittest.mock import patch

import pytest
from botocore.exceptions import NoCredentialsError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from src.apps.files.models import Files, SearchTags


@pytest.mark.django_db
def test_create_file_should_respond_with_201(api_client: APIClient, s3_file_save):  # pylint: disable=W0613, W0621
    """Test creating a file."""
    url = reverse("upload")
    file = SimpleUploadedFile("test_file.txt", f"{'a' * 600}".encode("utf-8"), content_type="text/plain")
    file_json = {"file": file, "tags": "test_tag"}
    response = api_client.post(url, file_json, format="multipart")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "File uploaded successfully"
    # assert response.data["s3_object_URL"] == f"https://"
    assert Files.objects.count() == 1  # pylint: disable=E1101
    assert Files.objects.first().tags == "test_tag"  # pylint: disable=E1101
    assert Files.objects.first().size == 600  # pylint: disable=E1101
    assert Files.objects.first().name == "test_file.txt"  # pylint: disable=E1101
    assert Files.objects.first().contents == "a" * 600  # pylint: disable=E1101

    assert s3_file_save.called
    assert SearchTags.objects.count() == 1  # pylint: disable=E1101
    assert SearchTags.objects.first().tag_name == "test_tag"  # pylint: disable=E1101
    assert SearchTags.objects.first().file_id == Files.objects.first().id  # pylint: disable=E1101


@pytest.mark.django_db
def test_create_file_no_file_provided(api_client):
    """Test creating a file without providing a file."""
    url = reverse("upload")
    response = api_client.post(url, {}, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "No file provided"


@pytest.mark.django_db
def test_create_file_invalid_file_type(api_client):
    """Test creating a file with an invalid file type."""
    url = reverse("upload")
    file = SimpleUploadedFile("test_file.pdf", "test".encode("utf-8"), content_type="application/pdf")
    file_json = {"file": file, "tags": "test_tag"}
    response = api_client.post(url, file_json, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Only text('*.txt') files are allowed"


@pytest.mark.django_db
def test_create_file_size_too_small(api_client):
    """Test creating a file with a size that is too small."""
    url = reverse("upload")
    file = SimpleUploadedFile("test_file.txt", "test".encode("utf-8"), content_type="text/plain")
    file_json = {"file": file, "tags": "test_tag"}
    response = api_client.post(url, file_json, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "File size should be greater than 0.5KB"


@pytest.mark.django_db
def test_create_file_size_too_large(api_client):
    """Test creating a file with a size that is too large."""
    url = reverse("upload")
    file = SimpleUploadedFile("test_file.txt", f"{'a' * 3000}".encode("utf-8"), content_type="text/plain")
    file_json = {"file": file, "tags": "test_tag"}
    response = api_client.post(url, file_json, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "File size should be less than 2KB"


@pytest.mark.django_db
def test_create_file_no_credentials(api_client):
    """Test creating a file with no credentials available."""
    url = reverse("upload")
    file = SimpleUploadedFile("test_file.txt", f"{'a' * 600}".encode("utf-8"), content_type="text/plain")
    file_json = {"file": file, "tags": "test_tag"}
    with patch("src.apps.files.views.s3.put_object", side_effect=NoCredentialsError):
        response = api_client.post(url, file_json, format="multipart")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["error"] == "Credentials not available"
