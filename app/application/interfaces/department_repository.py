from abc import ABC, abstractmethod

from ..entities import (NewDepartmentEntity,
                        DepartmentEntity,
                        UpdateDepartmentEntity)


class IDepartmentRepository(ABC):
    @abstractmethod
    async def create(self,
                     new_department: NewDepartmentEntity) -> DepartmentEntity:
        pass

    @abstractmethod
    async def read(self, id: int) -> DepartmentEntity:
        pass

    @abstractmethod
    async def read_tree(
            self,
            id: int,
            depth: int
    ) -> tuple[DepartmentEntity, list[DepartmentEntity]]:
        pass

    @abstractmethod
    async def update(
            self,
            id: int,
            new_department_data: UpdateDepartmentEntity
    ) -> DepartmentEntity:
        pass

    @abstractmethod
    async def delete(self, id: int):
        pass

    @abstractmethod
    async def remove_parent(self, parent_id: int):
        pass

    @abstractmethod
    async def is_looping(self, new_parent_id: int, child_id: int) -> bool:
        pass
