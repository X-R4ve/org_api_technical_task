from typing import Annotated

from fastapi import Depends, params

from app.api.dependencies.logic import get_get_department_uc
from app.api.schemas.parameters.get_department import \
    GetDepartmentQueryParamsV1
from app.api.schemas.responses.detailed_department import \
    DetailedDepartmentResponseSchemaV1
from app.application.logic.use_cases import GetDepartmentUseCase


async def get_department_v1(
        id: int,
        query_params: Annotated[GetDepartmentQueryParamsV1, Depends()],
        get_department_uc: Annotated[
            GetDepartmentUseCase,
            Depends(get_get_department_uc)
        ]
) -> DetailedDepartmentResponseSchemaV1:
    detailed_department = await get_department_uc.execute(
        id=id,
        depth=query_params.depth,
        include_employees=query_params.include_employees
    )
    return DetailedDepartmentResponseSchemaV1.from_entity(
        entity=detailed_department
    )
