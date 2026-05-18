from typing import Any

from pydantic import field_validator


def trim_before_validating(field: str, *fields: str):
    @field_validator(field, *fields, mode='before')
    def _validator(cls, value: Any):
        return str(value).strip()
    return _validator
