from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.db.core.sessions import get_async_session_maker
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository


async def get_async_session(
        async_session_maker: Annotated[
            async_sessionmaker,
            Depends(get_async_session_maker)
        ]
):
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_department_repository(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> DepartmentRepository:
    return DepartmentRepository(session=async_session)


def get_employee_repository(
        async_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> EmployeeRepository:
    return EmployeeRepository(session=async_session)
