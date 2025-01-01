"""Fixtures for the files app tests."""

from io import BytesIO
from unittest.mock import patch

import pytest
from model_bakery import baker


@pytest.fixture
def txt_file():
    """Fixture to create a File instance."""
    return baker.make(
        "files.Files",
        _fill_optional=True,
        name="test_file.txt",
        size=0,
        contents="",
        tags="test",
    )


@pytest.fixture(scope="function")
def file_with_tags():
    """Fixture to create a File instance with tags."""
    file = baker.make(
        "apps.files.Files",
        _fill_optional=True,
        name="test_file.txt",
        size=1000,
        contents="test file contents",
        tags="tag1,tag2",
    )
    baker.make("apps.files.SearchTags", file=file, tag_name="tag1")
    baker.make("apps.files.SearchTags", file=file, tag_name="tag2")
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
