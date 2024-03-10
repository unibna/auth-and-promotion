async def filter_none_fields(value: dict, fields: list = []) -> dict:
    """
    This function removes None fields from dict value

    Parameters:
    ----------
    - value: dict
        value as dict
    - fields: list
        if fields is passed, only remove key name in fields
        else, remove all keys have None value
    """
    if not fields:
        fields = list(value.keys())
    for field in fields:
        if value[field] is None:
            del value[field]
    return value