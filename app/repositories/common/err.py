from functools import wraps

from sqlalchemy.exc import (IntegrityError,
                            NoResultFound,
                            OperationalError,
                            ProgrammingError,
                            DBAPIError,
                            SQLAlchemyError)

from app.application.logic.common.err import BaseError


class DBError(BaseError):
    pass


def translate_db_exceptions(async_method):
    @wraps(async_method)
    async def wrapper(*args, **kwargs):
        try:
            return await async_method(*args, **kwargs)
        except IntegrityError as e:
            raise DBError(code=409,
                          message='data conflict') from e
        except NoResultFound as e:
            raise DBError(code=404,
                          message='data not found') from e
        except OperationalError as e:
            raise DBError(code=503,
                          message='error connecting to database') from e
        except (ProgrammingError, DBAPIError, SQLAlchemyError) as e:
            raise DBError(code=500,
                          message='database error') from e
    return wrapper
