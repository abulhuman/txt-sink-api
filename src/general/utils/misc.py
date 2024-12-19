import yaml


def yaml_coerce(value):
    """
    Coerce a string value to its corresponding YAML data type.

    This function takes a string value and attempts to convert it to its
    corresponding YAML data type using the PyYAML library. If the value is
    not a string, it is returned as-is.

    Args:
        value (any): The value to be coerced.

    Returns:
        any: The coerced value if it is a string, otherwise the original value.
    """
    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', Loader=yaml.SafeLoader)['dummy']

    return value
