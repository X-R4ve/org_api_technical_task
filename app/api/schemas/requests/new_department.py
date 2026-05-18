from pydantic import BaseModel, Field, model_validator, field_validator

from app.api.schemas.common.validators import trim_before_validating
from app.application.entities.departments import NewDepartmentEntity
from app.infrastructure.settings.constants import Limits


class NewDepartmentRequestSchemaV1(BaseModel):
    name: str = Field(...,
                      min_length=Limits.Department.Name.min_length,
                      max_length=Limits.Department.Name.max_length)
    parent_id: int | None = None

    _trim = trim_before_validating('name')

    def to_entity(self) -> NewDepartmentEntity:
        return NewDepartmentEntity(
            name=self.name,
            parent_id=self.parent_id,
        )