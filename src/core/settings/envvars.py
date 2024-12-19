"""
This takes the environment variables with a matching prefix,
 strips the prefix, and updates the global.

For example,
export TXT_SINK_SETTINGS_IN_DOCKER=true (environment variable)

Could then be referenced as a global setting:
IN_DOCKER=True
"""

from src.general.utils.collections import deep_update
from src.general.utils.settings import get_settings_from_environment

# globals() is a dictionary that holds all the global variables
deep_update(
    globals(), get_settings_from_environment(ENV_VAR_SETTINGS_PREFIX))  # type: ignore # noqa: F821
