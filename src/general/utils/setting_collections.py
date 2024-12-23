""" This module contains utility functions for setting collections. """


def deep_update(base_dict, update_with):
    """
    Recursively updates a dictionary with another dictionary.

    This function takes two dictionaries, `base_dict` and `update_with`, and updates
    `base_dict` with the values from `update_with`. If a value in `update_with` is a
    dictionary and the corresponding value in `base_dict` is also a dictionary, the
    function will recursively update the nested dictionaries. Otherwise, it will
    overwrite the value in `base_dict` with the value from `update_with`.

    Args:
        base_dict (dict): The dictionary to be updated.
        update_with (dict): The dictionary with values to update `base_dict`.

    Returns:
        dict: The updated `base_dict`.
    """
    for key, value in update_with.items():
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)

            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            else:
                base_dict[key] = value
        else:
            base_dict[key] = value

    return base_dict
