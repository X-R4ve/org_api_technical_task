from sqlalchemy import insert, select, update

from app.application.entities import EmployeeEntity, NewEmployeeEntity
from app.application.interfaces import IEmployeeRepository
from app.repositories.common.base_repository import BaseRepository
from app.infrastructure.db.models import Employee
from app.repositories.common.err import translate_db_exceptions


class EmployeeRepository(BaseRepository, IEmployeeRepository):
    @translate_db_exceptions
    async def create(self,
                     department_id: int,
                     new_employee: NewEmployeeEntity) -> EmployeeEntity:
        query = (
            insert(Employee)
            .values({
                Employee.full_name: new_employee.full_name,
                Employee.position: new_employee.position,
                Employee.hired_at: new_employee.hired_at,
                Employee.department_id: department_id
            })
            .returning(*Employee.__mapper__.c)
        )
        created_row = (await self._session.execute(query)).mappings().one()
        return EmployeeEntity.from_attributes(created_row)

    @translate_db_exceptions
    async def read_by_department_id(self,
                                    department_id: int) -> list[EmployeeEntity]:
        query = (
            select(*Employee.__mapper__.c)
            .where(Employee.department_id == department_id)
            .order_by(Employee.full_name)
        )
        employee_rows = (await self._session.execute(query)).mappings().all()
        return [EmployeeEntity.from_attributes(row) for row in employee_rows]

    @translate_db_exceptions
    async def reassign(self, old_department_id: int, new_department_id: int):
        query = (
            update(Employee)
            .where(Employee.department_id == old_department_id)
            .values({Employee.department_id: new_department_id})
        )
        await self._session.execute(query)
