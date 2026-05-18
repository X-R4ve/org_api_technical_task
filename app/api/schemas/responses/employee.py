from datetime import date, datetime
from typing import Self

from pydantic import BaseModel

from app.application.entities.employees import EmployeeEntity


class EmployeeResponseSchemaV1(BaseModel):
    id: int
    full_name: str
    position: str
    hired_at: date | None
    created_at: datetime
    department_id: int

    @classmethod
    def from_entity(cls, entity: EmployeeEntity) -> Self:
        return cls(
            id=entity.id,
            full_name=entity.full_name,
            position=entity.position,
            hired_at=entity.hired_at,
            created_at=entity.created_at,
            department_id=entity.department_id
        )
