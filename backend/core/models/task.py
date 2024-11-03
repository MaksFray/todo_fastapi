from sqlalchemy.orm import Mapped, mapped_column

from .mixins.int_id_pk import IntIdPkMixin
from .base import Base


class Task(IntIdPkMixin, Base):
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    completed: Mapped[bool] = mapped_column(nullable=False, default=False)