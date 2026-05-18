from ...entities import DetailedDepartmentEntity
from ...interfaces import IDepartmentRepository, IEmployeeRepository


class GetDepartmentUseCase:
    def __init__(self,
                 department_repo: IDepartmentRepository,
                 employee_repo: IEmployeeRepository):
        self._department_repo = department_repo
        self._employee_repo = employee_repo

    async def execute(self,
                      id: int,
                      depth: int,
                      include_employees: bool) -> DetailedDepartmentEntity:
        if depth > 0:
            root, children = await \
                self._department_repo.read_tree(id=id, depth=depth)
        else:
            root = await self._department_repo.read(id=id)
            children = []
        if include_employees:
            employees = await \
                self._employee_repo.read_by_department_id(department_id=id)
        else:
            employees = []
        return DetailedDepartmentEntity(
            department=root,
            employees=employees,
            children=children
        )
