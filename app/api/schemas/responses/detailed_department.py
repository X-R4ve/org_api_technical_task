from typing import Self

from pydantic import BaseModel, Field

from app.api.schemas.responses.department import DepartmentResponseSchemaV1
from app.api.schemas.responses.employee import EmployeeResponseSchemaV1
from app.application.entities.departments import DetailedDepartmentEntity


class DetailedDepartmentResponseSchemaV1(BaseModel):
    department: DepartmentResponseSchemaV1
    employees: list[EmployeeResponseSchemaV1] = Field(default_factory=list)
    children: list[DepartmentResponseSchemaV1] = Field(default_factory=list)

    @classmethod
    def from_entity(cls, entity: DetailedDepartmentEntity) -> Self:
        return cls(
            department=DepartmentResponseSchemaV1.from_entity(
                entity=entity.department
            ),
            employees=[
                EmployeeResponseSchemaV1.from_entity(entity=employee)
                for employee in entity.employees
            ],
            children=[
                DepartmentResponseSchemaV1.from_entity(entity=department)
                for department in entity.children
            ]
        )
