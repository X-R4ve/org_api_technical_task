from fastapi import FastAPI, status, APIRouter
from pydantic import ValidationError

from app.api.endpoints.create_department import create_department_v1
from app.api.endpoints.create_employee import create_employee_v1
from app.api.endpoints.delete_department import delete_department_v1
from app.api.endpoints.get_department import get_department_v1
from app.api.endpoints.update_department import update_department_v1
from app.api.error_handlers import (unexpected_error_handler,
                                    base_error_handler,
                                    pydantic_validation_error_handler)
from app.application.logic.common.err import BaseError

app_v1 = FastAPI()

router = APIRouter(prefix='/departments')

router.add_api_route(
    path='/',
    endpoint=create_department_v1,
    status_code=status.HTTP_201_CREATED,
    methods=['POST']
)
router.add_api_route(
    path='/{id}/employees/',
    endpoint=create_employee_v1,
    status_code=status.HTTP_201_CREATED,
    methods=['POST']
)
router.add_api_route(
    path='/{id}',
    endpoint=get_department_v1,
    methods=['GET']
)
router.add_api_route(
    path='/{id}',
    endpoint=update_department_v1,
    methods=['PATCH']
)
router.add_api_route(
    path='/{id}',
    endpoint=delete_department_v1,
    status_code=status.HTTP_204_NO_CONTENT,
    methods=['DELETE']
)

app_v1.include_router(router)


app_v1.add_exception_handler(
    exc_class_or_status_code=BaseError,
    handler=base_error_handler # type: ignore
)
app_v1.add_exception_handler(
    exc_class_or_status_code=ValidationError,
    handler=pydantic_validation_error_handler # type: ignore
)
app_v1.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=unexpected_error_handler
)
