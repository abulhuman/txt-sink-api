""" Settings module for the TXT_SINK_API project. """

import os.path
from pathlib import Path

from split_settings.tools import include, optional

# from src.general.utils.pytest import is_pytest_running

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Namespacing our env vars to avoid conflicts
ENV_VAR_SETTINGS_PREFIX = "TXT_SINK_SETTINGS_"
# The path to the local settings file
LOCAL_SETTINGS_PATH = os.getenv(f"{ENV_VAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    # We dedicate local/settings.unittests.py to have reproducible unittest runs
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"
    # LOCAL_SETTINGS_PATH = f'local/settings{".unittests" if is_pytest_running() else ".dev"}.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    "base.py",
    "setting_logging.py",
    optional(LOCAL_SETTINGS_PATH),
    "aws.py",
    "rest_framework.py",
    "custom.py",
    # "docker.py",
    "envvars.py",
    "rds_db.py",
)

# if not is_pytest_running():
# 	 assert SECRET_KEY is not NotImplemented  # type: ignore # noqa: F821
