from dataclasses import replace
from datetime import datetime

import pytest

from app.application.entities import DepartmentEntity, EmployeeEntity, \
    NewDepartmentEntity


@pytest.fixture
def get_new_department_entity():
    def func(**kwargs):
        entity = NewDepartmentEntity(
            name='Microsoft',
            parent_id=None
        )
        return replace(entity, **kwargs)
    return func


@pytest.fixture
def get_department_entity():
    def func(**kwargs):
        entity = DepartmentEntity(
            id=1,
            name='Main Department',
            parent_id=None,
            created_at=datetime(2012, 12, 21)
        )
        return replace(entity, **kwargs)
    return func


@pytest.fixture
def get_employee_entity():
    def func(**kwargs):
        entity = EmployeeEntity(
            id=1,
            full_name='John Doe',
            position='maniac',
            hired_at=None,
            created_at=datetime(1995, 9, 22),
            department_id=1
        )
        return replace(entity, **kwargs)
    return func
