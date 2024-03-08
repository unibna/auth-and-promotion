from typing import Type
from pydantic import BaseModel


def tortoise_to_pydantic(tortoise_object, pydantic_model: Type[BaseModel]):
    pydantic_dict = {field: getattr(tortoise_object, field) for field in pydantic_model.__annotations__}
    return pydantic_model(**pydantic_dict)
