from ...entities import (NewDepartmentEntity,
                         DepartmentEntity,
                         UpdateDepartmentEntity)
from ..common import ApplicationError
from .common import BaseService
from ...entities.departments import UNSET
from ...interfaces import IDepartmentRepository


class DepartmentService(BaseService[IDepartmentRepository]):
    async def create_department(
            self,
            new_department: NewDepartmentEntity
    ) -> DepartmentEntity:
        return await self._repo.create(new_department=new_department)

    async def update_department(
            self,
            id: int,
            new_department_data: UpdateDepartmentEntity
    ) -> DepartmentEntity:
        if id == new_department_data.parent_id:
            raise ApplicationError(
                code=400,
                message='department can\'t be a parent of itself'
            )
        elif new_department_data.is_empty():
            raise ApplicationError(
                code=400,
                message='new data not transferred'
            )
        new_parent_id = new_department_data.parent_id
        if new_parent_id is not UNSET:
            is_looping = await self._repo.is_looping(
                new_parent_id=new_parent_id,
                child_id=id
            )
            if is_looping:
                raise ApplicationError(
                    code=409,
                    message='departments hierarchy must not contain loops'
                )
        return await self._repo.update(id=id,
                                       new_department_data=new_department_data)
