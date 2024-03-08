from datetime import date, datetime
from typing import Union


def datetime_encoder(obj: Union[date, datetime]) -> str:
    if isinstance(obj, date) or isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")
