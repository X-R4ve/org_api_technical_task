from typing import Annotated

from fastapi import Depends

from app.api.dependencies.logic import get_department_service
from app.api.schemas.requests.new_department import NewDepartmentRequestSchemaV1
from app.api.schemas.responses.department import DepartmentResponseSchemaV1
from app.application.logic.services import DepartmentService


async def create_department_v1(
        new_department: NewDepartmentRequestSchemaV1,
        department_service: Annotated[
            DepartmentService,
            Depends(get_department_service)
        ]
) -> DepartmentResponseSchemaV1:
    created_department_entity = await department_service.create_department(
        new_department=new_department.to_entity()
    )
    return DepartmentResponseSchemaV1.from_entity(
        entity=created_department_entity
    )