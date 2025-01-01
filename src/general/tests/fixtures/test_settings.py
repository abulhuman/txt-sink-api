""" This file contains the test settings for the project. """

import pytest
from django.test import override_settings


@pytest.fixture(autouse=True)
def test_settings(settings):  # pylint: disable=W0613, W0621
    """Fixture to override the settings for the tests."""
    with override_settings(SECRET_KEY='b27c612c6cbeac10c8788fbc95b29f563cc0ea2eb7d6be08',):
        yield
