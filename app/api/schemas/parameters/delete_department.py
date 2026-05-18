from pydantic import BaseModel, model_validator

from app.application.logic.use_cases.delete_department import DeleteDepartmentMode


class DeleteDepartmentQueryParamsV1(BaseModel):
    mode: DeleteDepartmentMode
    reassign_to_department_id: int | None = None

    @model_validator(mode='after')
    def _validate_args_combination(self):
        if (
                self.mode == DeleteDepartmentMode.REASSIGN and
                self.reassign_to_department_id is None
        ):
            raise ValueError
        return self
