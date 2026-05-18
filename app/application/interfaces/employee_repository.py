from abc import ABC, abstractmethod

from ..entities import NewEmployeeEntity, EmployeeEntity


class IEmployeeRepository(ABC):
    @abstractmethod
    async def create(self,
                     department_id: int,
                     new_employee: NewEmployeeEntity) -> EmployeeEntity:
        pass

    @abstractmethod
    async def read_by_department_id(self,
                                    department_id: int) -> list[EmployeeEntity]:
        pass

    @abstractmethod
    async def reassign(self, old_department_id: int, new_department_id: int):
        pass
