from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.entities import DetailedDepartmentEntity
from app.application.logic.use_cases import GetDepartmentUseCase


@pytest.mark.parametrize(
    ('depth', 'include_employees'),
    (
        (0, True),
        (0, False),
        (1, True),
        (1, False),
    )
)
async def test_get_department_use_case(
        depth: int,
        include_employees: bool,
        *,
        department_repo_mock: MagicMock,
        employee_repo_mock: MagicMock,
        get_department_entity,
        get_employee_entity
):
    root_department_id = 1

    root_department = get_department_entity(id=root_department_id)
    children = [get_department_entity(id=i) for i in range(2, 7)]
    employees = [get_employee_entity(id=i, department_id=root_department_id)
                 for i in range(1, 10)]
    department_repo_mock.read_tree = AsyncMock(
        return_value=(root_department, children)
    )
    department_repo_mock.read = AsyncMock(return_value=root_department)
    employee_repo_mock.read_by_department_id = AsyncMock(
        return_value=employees
    )

    repo = GetDepartmentUseCase(
        department_repo=department_repo_mock,
        employee_repo=employee_repo_mock
    )

    result = await repo.execute(id=root_department_id,
                                depth=depth,
                                include_employees=include_employees)

    assert isinstance(result, DetailedDepartmentEntity)
    assert result.department == root_department

    if depth > 0:
        assert result.children == children
        department_repo_mock.read_tree.assert_called_once_with(
            id=root_department_id,
            depth=depth
        )
    else:
        assert result.children == []
        department_repo_mock.read.assert_called_once_with(
            id=root_department_id
        )

    if include_employees:
        employee_repo_mock.read_by_department_id.assert_called_once_with(
            department_id=root_department_id
        )
        assert result.employees == employees
    else:
        employee_repo_mock.read_by_department_id.assert_not_called()
        assert result.employees == []

