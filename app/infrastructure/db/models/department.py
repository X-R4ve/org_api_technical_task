from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, String, DateTime, func, Index, \
    CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.core.base import Base
from app.infrastructure.settings.constants import Limits


class Department(Base):
    __tablename__ = 'departments'

    id: Mapped[int] = \
        mapped_column(BigInteger(), primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(Limits.Department.Name.max_length))
    created_at: Mapped[datetime] = \
        mapped_column(DateTime(timezone=True), server_default=func.now())

    parent_id: Mapped[int | None] = mapped_column(
        BigInteger(),
        ForeignKey('departments.id', ondelete='CASCADE')
    )

    __table_args__ = (
        Index('idx_departments_parent_id',
              parent_id,
              postgresql_where=parent_id.is_not(None)),
        UniqueConstraint(name, parent_id,
                         name='uq_departments_name_parent_id')
    )
