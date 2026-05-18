from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.interfaces import IDepartmentRepository, \
    IEmployeeRepository
from app.application.logic.use_cases import GetDepartmentUseCase


@pytest.fixture
def department_repo_mock():
    return MagicMock(spec=IDepartmentRepository)


@pytest.fixture
def employee_repo_mock():
    return MagicMock(spec=IEmployeeRepository)

