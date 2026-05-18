from pydantic import BaseModel, Field

from app.infrastructure.settings.constants import Limits


class GetDepartmentQueryParamsV1(BaseModel):
    depth: int = Field(1,
                       ge=Limits.QueryParams.GetDepartment.min_depth,
                       le=Limits.QueryParams.GetDepartment.max_depth)
    include_employees: bool = True
