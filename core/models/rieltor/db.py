from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class RieltorDB(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    surname: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[str] = mapped_column(String(100))

    commission_present: Mapped[float | None] = mapped_column(Numeric(precision=5, scale=2))
