"""Fixtures for the files app tests."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client(transactional_db):
    """Fixture to create an API client."""
    return APIClient(transactional_db)
