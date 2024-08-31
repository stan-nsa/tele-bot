from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(10))
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
