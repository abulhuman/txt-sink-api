"""Fixtures for the files app tests."""

from io import BytesIO
from unittest.mock import patch

import pytest
from model_bakery import baker
from rest_framework.reverse import reverse


@pytest.fixture
def upload_url():
    """Fixture to create an upload URL."""
    return reverse("upload")


@pytest.fixture
def txt_file():
    """Fixture to create a File instance."""
    return baker.make(
        "files.Files",
        _fill_optional=True,
        name="test_file.txt",
        size=0,
        contents="",
        tags="",
    )


@pytest.fixture(scope="function")
def txt_file_with_tags():
    """Fixture to create a File instance with tags."""
    file = baker.make(
        "files.Files",
        _fill_optional=True,
        name="test_file.txt",
        size=1000,
        contents="test file contents",
        tags="tag-one,tag-two",
    )
    baker.make("files.SearchTags", file=file, tag_name="tag-one")
    baker.make("files.SearchTags", file=file, tag_name="tag-two")
    return file


@pytest.fixture(scope="function")
def s3_file_save():
    """Mock the s3 file save function."""
    with patch("src.apps.files.views.s3.put_object") as mock:
        yield mock


@pytest.fixture(scope="function")
def txt_file_json():  # pylint: disable=W0613, W0621
    """Fixture to create a File instance in JSON format."""
    file = BytesIO(("a" * 600).encode("utf-8"))
    file.name = "test_file.txt"
    file.content_type = "text/plain"
    file.size = 600
    yield {"file": file, "tags": "test"}
