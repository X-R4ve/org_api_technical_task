from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Self


@dataclass(slots=True)
class NewEmployeeEntity:
    full_name: str
    position: str
    hired_at: date | None


@dataclass(slots=True)
class EmployeeEntity:
    id: int
    full_name: str
    position: str
    hired_at: date | None
    created_at: datetime
    department_id: int

    @classmethod
    def from_attributes(cls, obj: Any) -> Self:
        return cls(
            id=obj.id,
            full_name=obj.full_name,
            position=obj.position,
            hired_at=obj.hired_at,
            created_at=obj.created_at,
            department_id=obj.department_id
        )
