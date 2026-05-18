from typing import Annotated

from fastapi import Depends

from app.api.dependencies.logic import get_department_service
from app.api.schemas.requests.update_department import \
    UpdateDepartmentRequestSchemaV1
from app.api.schemas.responses.department import DepartmentResponseSchemaV1
from app.application.logic.services import DepartmentService


async def update_department_v1(
        id: int,
        new_department_data: UpdateDepartmentRequestSchemaV1,
        department_service: Annotated[
            DepartmentService,
            Depends(get_department_service)
        ]
):
    updated_department = await department_service.update_department(
        id=id,
        new_department_data=new_department_data.to_entity()
    )
    return DepartmentResponseSchemaV1.from_entity(entity=updated_department)
