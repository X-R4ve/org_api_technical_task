from typing import Annotated

from fastapi import Depends

from app.api.dependencies.logic import get_employee_service
from app.api.schemas.requests.new_employee import NewEmployeeRequestSchemaV1
from app.api.schemas.responses.employee import EmployeeResponseSchemaV1
from app.application.logic.services import EmployeeService


async def create_employee_v1(
        id: int,
        new_employee: NewEmployeeRequestSchemaV1,
        employee_service: Annotated[
            EmployeeService,
            Depends(get_employee_service)
        ]
):
    created_employee_entity = await employee_service.create_employee(
        department_id=id,
        new_employee=new_employee.to_entity()
    )
    return EmployeeResponseSchemaV1.from_entity(entity=created_employee_entity)
