from sqlalchemy import insert, select, literal, update, delete

from app.application.entities import (NewDepartmentEntity,
                                      DepartmentEntity,
                                      UpdateDepartmentEntity)
from app.application.entities.departments import UNSET
from app.application.interfaces import IDepartmentRepository
from app.repositories.common.base_repository import BaseRepository
from app.infrastructure.db.models import Department
from app.repositories.common.err import DBError, translate_db_exceptions


class DepartmentRepository(BaseRepository, IDepartmentRepository):
    @translate_db_exceptions
    async def create(self,
                     new_department: NewDepartmentEntity) -> DepartmentEntity:
        query = (
            insert(Department)
            .values({
                Department.name: new_department.name,
                Department.parent_id: new_department.parent_id
            })
            .returning(*Department.__mapper__.c)
        )
        created_department_row = (
            await self._session.execute(query)
        ).mappings().one()
        return DepartmentEntity.from_attributes(obj=created_department_row)

    @translate_db_exceptions
    async def read(self, id: int) -> DepartmentEntity:
        query = select(*Department.__mapper__.c).where(Department.id == id)
        department_row = (await self._session.execute(query)).mappings().one()
        return DepartmentEntity.from_attributes(obj=department_row)

    @translate_db_exceptions
    async def read_tree(
            self,
            id: int,
            depth: int
    ) -> tuple[DepartmentEntity, list[DepartmentEntity]]:
        cte = (
            select(*Department.__mapper__.c, literal(0).label('cur_depth'))
            .where(Department.id == id)
            .cte(name='root', recursive=True)
        )
        cte_alias = cte.alias()
        cte = cte.union_all(
            select(*Department.__mapper__.c, cte_alias.c.cur_depth + 1)
            .join(cte_alias, Department.parent_id == cte_alias.c.id)
            .where(cte_alias.c.cur_depth < depth)
        )
        query = select(cte)

        rows = (await self._session.execute(query)).mappings().all()

        root_row = next((r for r in rows if r.id == id), None)

        if not rows or root_row is None:
            raise DBError(code=404,
                          message='department not found')

        return (DepartmentEntity.from_attributes(obj=root_row),
                [DepartmentEntity.from_attributes(obj=row)
                 for row in rows
                 if row.id != id])

    @translate_db_exceptions
    async def update(
            self,
            id: int,
            new_department_data: UpdateDepartmentEntity
    ) -> DepartmentEntity:
        query_values = {Department.name: new_department_data.name,
                        Department.parent_id: new_department_data.parent_id}
        query_values = {k: v for k, v in query_values.items() if v is not UNSET}
        query = (
            update(Department)
            .where(Department.id == id)
            .values(query_values)
            .returning(*Department.__mapper__.c)
        )
        updated_row = (await self._session.execute(query)).mappings().one()

        return DepartmentEntity.from_attributes(obj=updated_row)

    @translate_db_exceptions
    async def delete(self, id: int):
        query = delete(Department).where(Department.id == id)
        await self._session.execute(query)

    @translate_db_exceptions
    async def remove_parent(self, parent_id: int):
        query = (update(Department)
                 .where(Department.parent_id == parent_id)
                 .values({Department.parent_id: None}))
        await self._session.execute(query)

    @translate_db_exceptions
    async def is_looping(self, new_parent_id: int, child_id: int) -> bool:
        cte = (
            select(Department.id, Department.parent_id)
            .where(Department.id == new_parent_id)
            .cte(name='ancestors', recursive=True)
        )
        cte_alias = cte.alias()
        cte = cte.union_all(
            select(Department.id, Department.parent_id)
            .where(Department.id == cte_alias.c.parent_id,
                   Department.id != new_parent_id)
        )
        query = select(
            literal(child_id).in_(select(cte.c.id))
        )
        return (await self._session.execute(query)).scalar()
