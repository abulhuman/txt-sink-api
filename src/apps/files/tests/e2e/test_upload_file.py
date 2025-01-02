"""Integration tests for the Files API."""

from unittest.mock import patch

import pytest
from botocore.exceptions import NoCredentialsError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from src.apps.files.models import Files, SearchTags


@pytest.mark.django_db
class TestUploadFile:
    """Test class for the upload file endpoint."""

    def test_should_201(self, api_client: APIClient, upload_url, s3_file_save):  # pylint: disable=W0613, W0621
        """Test creating a file."""
        file = SimpleUploadedFile("test_file.txt", f"{'a' * 600}".encode("utf-8"), content_type="text/plain")
        file_json = {"file": file, "tags": "test_tag"}
        response = api_client.post(upload_url, file_json, format="multipart")
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

    def test_should_400_when_no_file_provided(self, api_client, upload_url):
        """Test creating a file without providing a file."""
        response = api_client.post(upload_url, {}, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "No file provided"

    def test_should_400_when_invalid_file_type(self, api_client, upload_url):
        """Test creating a file with an invalid file type."""
        file = SimpleUploadedFile("test_file.pdf", "test".encode("utf-8"), content_type="application/pdf")
        file_json = {"file": file, "tags": "test_tag"}
        response = api_client.post(upload_url, file_json, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Only text('*.txt') files are allowed"

    def test_should_400_when_size_too_small(self, api_client, upload_url):
        """Test creating a file with a size that is too small."""
        file = SimpleUploadedFile("test_file.txt", "test".encode("utf-8"), content_type="text/plain")
        file_json = {"file": file, "tags": "test_tag"}
        response = api_client.post(upload_url, file_json, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "File size should be greater than 0.5KB"

    def test_should_400_when_size_too_large(self, api_client, upload_url):
        """Test creating a file with a size that is too large."""
        file = SimpleUploadedFile("test_file.txt", f"{'a' * 3000}".encode("utf-8"), content_type="text/plain")
        file_json = {"file": file, "tags": "test_tag"}
        response = api_client.post(upload_url, file_json, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "File size should be less than 2KB"

    def test_should_500_when_no_credentials(self, api_client, upload_url):
        """Test creating a file with no credentials available."""
        file = SimpleUploadedFile("test_file.txt", f"{'a' * 600}".encode("utf-8"), content_type="text/plain")
        file_json = {"file": file, "tags": "test_tag"}
        with patch("src.apps.files.views.s3.put_object", side_effect=NoCredentialsError):
            response = api_client.post(upload_url, file_json, format="multipart")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Credentials not available"
