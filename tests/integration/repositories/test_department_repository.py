from collections.abc import Generator
from itertools import permutations
from string import ascii_letters

import pytest
from sqlalchemy import insert

from app.application.entities import DepartmentEntity, EmployeeEntity
from app.infrastructure.db.models import Department, Employee


def strings_generator(length: int) -> Generator[str]:
    for letters in permutations(ascii_letters, length):
        yield ''.join(letters)


async def gen_departments_tree(async_session,
                               depth: int) -> list[DepartmentEntity]:
    cur_depth = 0
    names_gen = strings_generator(length=10)
    created_departments = []
    last_level: list[DepartmentEntity] = []
    while cur_depth <= depth:
        if last_level:
            values = [
                {Department.name: next(names_gen),
                 Department.parent_id: department.id}

                for department in last_level
                for _ in range(2)
            ]
        else:
            values = [{Department.name: next(names_gen),
                       Department.parent_id: None}]
        query = (
            insert(Department)
            .values(values)
            .returning(*Department.__mapper__.c)
        )
        created_rows = (await async_session.execute(query)).mappings().all()
        await async_session.commit()
        last_level = [DepartmentEntity.from_attributes(obj=row)
                      for row in created_rows]
        created_departments.extend(last_level)
        cur_depth += 1
    return created_departments


async def gen_employees_for_departments(
        async_session,
        departments: list[DepartmentEntity]
) -> list[EmployeeEntity]:
    names_gen = strings_generator(length=9)
    positions_gen = strings_generator(length=10)
    values = [
        {Employee.full_name: next(names_gen),
         Employee.position: next(positions_gen),
         Employee.department_id: department.id}

        for department in departments
        for _ in range(5)
    ]
    query = insert(Employee).values(values).returning(*Employee.__mapper__.c)
    created_rows = (await async_session.execute(query)).mappings().all()
    await async_session.commit()
    return [EmployeeEntity.from_attributes(obj=row)
            for row in created_rows]


@pytest.mark.integration
@pytest.mark.usefixtures('build_database')
class TestDepartmentRepository:
    @pytest.mark.parametrize(
        ('depth', 'gen_depth'),
        (
            (0, 2),
            (2, 0),
            (2, 1),
            (2, 3),
            (4, 4),
            (5, 7),
            (7, 5)
        )
    )
    async def test_read_tree(
            self,
            depth: int,
            gen_depth: int,
            *,
            async_session,
            department_repo,
            get_new_department_entity
    ):
        departments = await gen_departments_tree(async_session=async_session,
                                                 depth=gen_depth)
        root_department = next(d for d in departments if d.parent_id is None)

        result_root, result_children = await department_repo.read_tree(
            id=root_department.id,
            depth=depth
        )

        expected_children_ids_set = {root_department.id}
        for _ in range(depth):
            expected_children_ids_set |= {
                d.id
                for d in departments
                if d.parent_id in expected_children_ids_set
            }
        expected_children_ids_set.remove(root_department.id)

        assert isinstance(result_root, DepartmentEntity)
        assert all(isinstance(c, DepartmentEntity) for c in result_children)
        assert result_root.id == root_department.id
        assert expected_children_ids_set == {c.id for c in result_children}
