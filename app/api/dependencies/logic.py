from typing import Annotated

from fastapi import Depends

from app.api.dependencies.db import get_department_repository, \
    get_employee_repository
from app.application.logic.services import DepartmentService, EmployeeService
from app.application.logic.use_cases import DeleteDepartmentUseCase, \
    GetDepartmentUseCase
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository


DepartmentRepoDependency = Annotated[
    DepartmentRepository,
    Depends(get_department_repository)
]
EmployeeRepoDependency = Annotated[
    EmployeeRepository,
    Depends(get_employee_repository)
]


def get_department_service(
        department_repository: DepartmentRepoDependency
) -> DepartmentService:
    return DepartmentService(repo=department_repository)


def get_employee_service(
        employee_repository: EmployeeRepoDependency
) -> EmployeeService:
    return EmployeeService(repo=employee_repository)


def get_delete_department_uc(
        department_repository: DepartmentRepoDependency,
        employee_repository: EmployeeRepoDependency
):
    return DeleteDepartmentUseCase(
        department_repo=department_repository,
        employee_repo=employee_repository
    )


def get_get_department_uc(
        department_repository: DepartmentRepoDependency,
        employee_repository: EmployeeRepoDependency
):
    return GetDepartmentUseCase(
        department_repo=department_repository,
        employee_repo=employee_repository
    )