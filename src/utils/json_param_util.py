import json
from typing import Any, TypeVar, cast

from fastapi import Depends, HTTPException, Query
from pydantic import Json, TypeAdapter, ValidationError


T = TypeVar("T")


def json_param(param_name: str, model: type[T], **query_kwargs: Any) -> T:
    """
    Parse JSON-encoded query parameters as pydantic models.

    The function returns a `Depends()` instance that takes the JSON-encoded value from the query parameter `param_name` and converts it to a Pydantic model, defined by the `model` attribute.
    """

    def get_parsed_dictionary(
        value: Json[str] = Query(alias=param_name, **query_kwargs)
    ) -> T:
        try:
            return TypeAdapter(model).validate_python(json.loads(value))
        except ValidationError as err:
            raise HTTPException(400, detail=err.errors())

    return cast(T, Depends(get_parsed_dictionary))
