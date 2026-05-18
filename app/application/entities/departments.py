from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from .employees import EmployeeEntity


UNSET = object()


@dataclass(slots=True)
class NewDepartmentEntity:
    name: str
    parent_id: int | None


@dataclass(slots=True)
class DepartmentEntity:
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    @classmethod
    def from_attributes(cls, obj: Any) -> Self:
        return cls(
            id=obj.id,
            name=obj.name,
            parent_id=obj.parent_id,
            created_at=obj.created_at
        )


@dataclass(slots=True)
class UpdateDepartmentEntity:
    name: str = UNSET
    parent_id: int | None = UNSET

    def is_empty(self):
        return self.name is UNSET and self.parent_id is UNSET


@dataclass(slots=True)
class DetailedDepartmentEntity:
    department: DepartmentEntity
    employees: list[EmployeeEntity]
    children: list[DepartmentEntity]
