from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ClientDB(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    surname: Mapped[str | None] = mapped_column(String(100))
    name: Mapped[str | None] = mapped_column(String(100))
    patronymic: Mapped[str | None] = mapped_column(String(100))

    phone: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(100))
