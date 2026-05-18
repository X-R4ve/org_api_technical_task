from datetime import datetime
from typing import Self

from pydantic import BaseModel

from app.application.entities.departments import DepartmentEntity


class DepartmentResponseSchemaV1(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: DepartmentEntity) -> Self:
        return cls(
            id=entity.id,
            name=entity.name,
            parent_id=entity.parent_id,
            created_at=entity.created_at
        )