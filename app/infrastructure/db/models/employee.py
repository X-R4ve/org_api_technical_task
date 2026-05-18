from datetime import date, datetime

from sqlalchemy import BigInteger, ForeignKey, String, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.core.base import Base
from app.infrastructure.settings.constants import Limits


class Employee(Base):
    __tablename__ = 'employees'

    id: Mapped[int] = \
        mapped_column(BigInteger(), primary_key=True, autoincrement=True)

    full_name: Mapped[str] = \
        mapped_column(String(Limits.Employee.FullName.max_length))
    position: Mapped[str] = \
        mapped_column(String(Limits.Employee.Position.max_length))
    hired_at: Mapped[date | None] = mapped_column()
    created_at: Mapped[datetime] = \
        mapped_column(DateTime(timezone=True), server_default=func.now())

    department_id: Mapped[int] = \
        mapped_column(BigInteger(), ForeignKey('departments.id'))

    __table_args__ = (
        Index('idx_employees_department_id',
              department_id),
    )
