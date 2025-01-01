"""Fixtures for the tests."""
import os

# Set on the earliest possible moment
os.environ['PYTEST_RUNNING'] = 'true'

from src.apps.files.tests.fixtures import *  # noqa: E402, F401, F402, F403 # pylint: disable=W0401, W0614, C0413
from src.general.tests.fixtures import *  # noqa: E402, F401, F402, F403 # pylint: disable=W0401, W0614, C0413
