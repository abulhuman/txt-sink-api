import os

from .misc import yaml_coerce


def get_settings_from_environment(prefix):
    """
    Retrieve settings from environment variables with a given prefix.

    This function scans the environment variables for keys that start with the specified prefix,
    strips the prefix from the keys, and returns a dictionary where the keys are the stripped
    environment variable names and the values are the corresponding environment variable values
    coerced using the `yaml_coerce` function.

    Args:
        prefix (str): The prefix to look for in environment variable keys.

    Returns:
        dict: A dictionary containing the settings derived from the environment variables.
    """
    prefix_len = len(prefix)
    return {
        key[prefix_len:]: yaml_coerce(value)
        for key, value in os.environ.items()
        if key.startswith(prefix)
    }
