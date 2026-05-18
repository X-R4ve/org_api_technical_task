from datetime import date

from pydantic import BaseModel, Field

from app.api.schemas.common.validators import trim_before_validating
from app.application.entities.employees import NewEmployeeEntity
from app.infrastructure.settings.constants import Limits


class NewEmployeeRequestSchemaV1(BaseModel):
    full_name: str = Field(...,
                           min_length=Limits.Employee.FullName.min_length,
                           max_length=Limits.Employee.FullName.max_length)
    position: str = Field(...,
                          min_length=Limits.Employee.Position.min_length,
                          max_length=Limits.Employee.Position.max_length)
    hired_at: date | None = None

    _trim = trim_before_validating('full_name', 'position')

    def to_entity(self) -> NewEmployeeEntity:
        return NewEmployeeEntity(
            full_name=self.full_name,
            position=self.position,
            hired_at=self.hired_at
        )