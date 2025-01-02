"""Test module for the get files endpoint"""

from datetime import datetime

import pytest
from rest_framework import status

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"  # pylint: disable=C0103


@pytest.mark.django_db
class TestGetFiles:
    """Test class for the get files endpoint"""

    def test_should_200_when_no_tags(self, api_client, txt_file):
        """Test getting files."""
        response = api_client.get("/files/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == txt_file.name
        assert response.data[0]["size"] == txt_file.size
        assert response.data[0]["tags"] == txt_file.tags
        assert response.data[0]["id"] == txt_file.id
        txt_file_formatted_modified_date = txt_file.modified_date.strftime(DATE_FORMAT)
        response_formatted_modified_date = datetime.fromisoformat(response.data[0]["modified_date"]
                                                                  ).strftime(DATE_FORMAT)
        assert response_formatted_modified_date == txt_file_formatted_modified_date
        assert response.data[0]["uri"] == txt_file.uri

    def test_should_200_when_with_tags(self, api_client, txt_file_with_tags):
        """Test getting files."""
        response = api_client.get("/files/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == txt_file_with_tags.name
        assert response.data[0]["size"] == txt_file_with_tags.size
        assert response.data[0]["tags"] == txt_file_with_tags.tags
        assert response.data[0]["id"] == txt_file_with_tags.id
        txt_file_formatted_modified_date = txt_file_with_tags.modified_date.strftime(DATE_FORMAT)
        response_formatted_modified_date = datetime.fromisoformat(response.data[0]["modified_date"]
                                                                  ).strftime(DATE_FORMAT)
        assert response_formatted_modified_date == txt_file_formatted_modified_date
        assert response.data[0]["uri"] == txt_file_with_tags.uri

    def test_should_200_when_search_by_is_tags_and_q_exists(self, api_client, txt_file_with_tags):
        """Test getting files."""
        response = api_client.get("/files/?search_by=tags&q=tag-one")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == txt_file_with_tags.name
        assert response.data[0]["size"] == txt_file_with_tags.size
        assert response.data[0]["tags"] == txt_file_with_tags.tags
        assert response.data[0]["id"] == txt_file_with_tags.id
        txt_file_formatted_modified_date = txt_file_with_tags.modified_date.strftime(DATE_FORMAT)
        response_formatted_modified_date = datetime.fromisoformat(response.data[0]["modified_date"]
                                                                  ).strftime(DATE_FORMAT)
        assert response_formatted_modified_date == txt_file_formatted_modified_date
        assert response.data[0]["uri"] == txt_file_with_tags.uri

    def test_should_200_when_search_by_is_tags_and_q_does_not_exist(
        self,
        api_client,
    ):
        """Test getting files."""
        response = api_client.get("/files/?search_by=tags&q=tag-three")
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_should_200_when_search_by_is_name_and_q_exists(self, api_client, txt_file_with_tags):
        """Test getting files."""
        response = api_client.get("/files/?search_by=name&q=test_file.txt")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == txt_file_with_tags.name
        assert response.data[0]["size"] == txt_file_with_tags.size
        assert response.data[0]["tags"] == txt_file_with_tags.tags
        assert response.data[0]["id"] == txt_file_with_tags.id
        txt_file_formatted_modified_date = txt_file_with_tags.modified_date.strftime(DATE_FORMAT)
        response_formatted_modified_date = datetime.fromisoformat(response.data[0]["modified_date"]
                                                                  ).strftime(DATE_FORMAT)
        assert response_formatted_modified_date == txt_file_formatted_modified_date
        assert response.data[0]["uri"] == txt_file_with_tags.uri

    def test_should_200_when_search_by_is_name_and_q_does_not_exist(
        self,
        api_client,
    ):
        """Test getting files."""
        response = api_client.get("/files/?search_by=name&q=test_file_two.txt")
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_should_200_when_search_by_is_contents_and_q_exists(self, api_client, txt_file_with_tags):
        """Test getting files."""
        response = api_client.get("/files/?search_by=contents&q=test file contents")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == txt_file_with_tags.name
        assert response.data[0]["size"] == txt_file_with_tags.size
        assert response.data[0]["tags"] == txt_file_with_tags.tags
        assert response.data[0]["id"] == txt_file_with_tags.id
        txt_file_formatted_modified_date = txt_file_with_tags.modified_date.strftime(DATE_FORMAT)
        response_formatted_modified_date = datetime.fromisoformat(response.data[0]["modified_date"]
                                                                  ).strftime(DATE_FORMAT)
        assert response_formatted_modified_date == txt_file_formatted_modified_date
        assert response.data[0]["uri"] == txt_file_with_tags.uri

    def test_should_200_when_search_by_is_contents_and_q_does_not_exist(
        self,
        api_client,
    ):
        """Test getting files."""
        response = api_client.get("/files/?search_by=contents&q=test file contents two")
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_should_400_when_search_by_is_invalid(self, api_client):
        """Test getting files."""
        response = api_client.get("/files/?search_by=invalid")
        assert response.status_code == 400
        assert response.data == {"error": "Invalid search_by parameter provided. Specify tags, name, or contents"}

    def test_should_400_when_search_by_is_tags_and_no_q(self, api_client):
        """Test getting files."""
        response = api_client.get("/files/?search_by=tags")
        assert response.status_code == 400
        assert response.data == {"error": "No tags provided"}

    def test_should_400_when_search_by_is_name_and_no_q(self, api_client):
        """Test getting files."""
        response = api_client.get("/files/?search_by=name")
        assert response.status_code == 400
        assert response.data == {"error": "No name provided"}

    def test_should_400_when_search_by_is_contents_and_no_q(
        self,
        api_client,
    ):
        """Test getting files."""
        response = api_client.get("/files/?search_by=contents")
        assert response.status_code == 400
        assert response.data == {"error": "No contents provided"}
