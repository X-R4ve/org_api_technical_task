from ...entities.employees import NewEmployeeEntity, EmployeeEntity
from ...interfaces import IEmployeeRepository
from .common.base_service import BaseService


class EmployeeService(BaseService[IEmployeeRepository]):
    async def create_employee(
            self,
            department_id: int,
            new_employee: NewEmployeeEntity
    ) -> EmployeeEntity:
        return await self._repo.create(department_id=department_id,
                                       new_employee=new_employee)
