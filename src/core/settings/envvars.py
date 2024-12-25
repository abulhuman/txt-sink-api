"""
This takes the environment variables with a matching prefix,
 strips the prefix, and updates the global.

For example,
export TXT_SINK_SETTINGS_IN_DOCKER=true (environment variable)

Could then be referenced as a global setting:
IN_DOCKER=True
"""

import os
import sys

from src.general.utils.setting_collections import deep_update
from src.general.utils.settings import get_settings_from_environment

# globals() is a dictionary that holds all the global variables
deep_update(
    globals(),
    get_settings_from_environment(ENV_VAR_SETTINGS_PREFIX),  # type: ignore # noqa: F821 # pylint: disable=E0602
)

try:
    if os.path.exists(LOCAL_SETTINGS_PATH):  # type: ignore # noqa: F821 # pylint: disable=E0602
        if DEBUG and not LOCAL_SETTINGS_PATH.split(".")[1] == "dev":  # type: ignore # noqa: F821,E501 # pylint: disable=E0602
            raise ValueError(
                """Local settings path file name must have 'dev' in it, \
when running in DEBUG=True; eg. 'local/settings.dev.py'"""
            )
        if not DEBUG and not LOCAL_SETTINGS_PATH.split(".")[1] == "prod":  # type: ignore # noqa: F821,E501 # pylint: disable=E0602
            raise ValueError(
                """Local settings path file name must have 'prod' in it, \
when running in DEBUG=False; eg. 'local/settings.prod.py'"""
            )
except AssertionError as e:
    print(e)
    sys.exit(1)
except ValueError as e:
    print(e)
    sys.exit(1)
