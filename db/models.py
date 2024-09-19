from sqlalchemy import BigInteger, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(String(150), nullable=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(20))
    date_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class SkuLog(Base):
    __tablename__ = 'sku_log'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.id'), index=True)
    user_name: Mapped[str] = mapped_column(String(50))
    sku: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(10))
    description: Mapped[str] = mapped_column(Text)
    date_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
