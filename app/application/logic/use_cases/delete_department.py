from enum import Enum

from ..common import ApplicationError
from ...interfaces import IDepartmentRepository, IEmployeeRepository


class DeleteDepartmentMode(str, Enum):
    CASCADE = 'cascade'
    REASSIGN = 'reassign'


class DeleteDepartmentUseCase:
    def __init__(self,
                 department_repo: IDepartmentRepository,
                 employee_repo: IEmployeeRepository):
        self._department_repo = department_repo
        self._employee_repo = employee_repo

    async def execute(self,
                      id: int,
                      mode: DeleteDepartmentMode,
                      reassign_to_department_id: int = None):
        if id == reassign_to_department_id:
            raise ApplicationError(
                code=400,
                message='You can\'t transfer employees to '
                        'the department you\'re deleting'
            )
        elif mode == DeleteDepartmentMode.REASSIGN:
            if reassign_to_department_id is None:
                raise ApplicationError(
                    code=400,
                    message='"reassign_to_department_id" must be specified'
                )
            await self._employee_repo.reassign(
                old_department_id=id,
                new_department_id=reassign_to_department_id
            )
            await self._department_repo.remove_parent(parent_id=id)
        await self._department_repo.delete(id=id)
