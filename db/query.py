from db.engine import db_session
from db.models import User, SkuLog
from sqlalchemy import select, delete

from aiogram.types import User as Tg_User


async def get_user(tg_user: Tg_User):
    async with db_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_user.id))
        return user


async def delete_user(tg_user: Tg_User):
    async with db_session() as session:
        await session.execute(delete(User).where(User.id == tg_user.id))
        await session.commit()


async def add_user(tg_user: Tg_User):
    async with db_session() as session:
        user = User(
            id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            status='member'
        )
        session.add(user)
        await session.commit()


async def add_log(user_id, sku, action, description):
    async with db_session() as session:
        event = SkuLog(
            user_id=user_id,
            sku=sku,
            action=action,
            description=description
        )
    session.add(event)
    await session.commit()
