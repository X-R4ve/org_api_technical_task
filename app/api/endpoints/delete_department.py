from typing import Annotated

from fastapi import Depends

from app.api.dependencies.logic import get_delete_department_uc
from app.api.schemas.parameters.delete_department import \
    DeleteDepartmentQueryParamsV1
from app.application.logic.use_cases import DeleteDepartmentUseCase


async def delete_department_v1(
        id: int,
        query_params: Annotated[DeleteDepartmentQueryParamsV1, Depends()],
        delete_department_uc: Annotated[
            DeleteDepartmentUseCase,
            Depends(get_delete_department_uc)
        ]
):
    await delete_department_uc.execute(
        id=id,
        mode=query_params.mode,
        reassign_to_department_id=query_params.reassign_to_department_id
    )
