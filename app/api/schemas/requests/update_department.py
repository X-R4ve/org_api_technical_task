from pydantic import BaseModel

from app.api.schemas.common.validators import trim_before_validating
from app.application.entities.departments import UpdateDepartmentEntity


class UpdateDepartmentRequestSchemaV1(BaseModel):
    name: str = None
    parent_id: int | None = None

    _trim = trim_before_validating('name')

    def to_entity(self) -> UpdateDepartmentEntity:
        entity = UpdateDepartmentEntity()
        new = self.model_dump(exclude_unset=True)
        if 'name' in new:
            entity.name = self.name
        if 'parent_id' in new:
            entity.parent_id = self.parent_id
        return entity
