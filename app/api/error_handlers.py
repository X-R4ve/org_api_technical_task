from pydantic import ValidationError
from fastapi import Request
from fastapi.responses import JSONResponse

from app.application.logic.common.err import BaseError


def base_error_handler(request: Request, error: BaseError):
    return JSONResponse(
        content={'message': error.message},
        status_code=error.code
    )


def pydantic_validation_error_handler(request: Request, error: ValidationError):
    return JSONResponse(
        content={'message': 'bad request'},
        status_code=400
    )


def unexpected_error_handler(request: Request, error: Exception):
    return JSONResponse(
        content={'message': 'unexpected error'},
        status_code=500
    )
