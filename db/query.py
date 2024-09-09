from db.engine import db_session
from db.models import User, SkuLog
from sqlalchemy import select, delete, update

from aiogram.types import User as Tg_User


# Получить юзера из базы по telegram-id и статусу
async def get_user(tg_user: Tg_User, status: str = None):
    async with db_session() as session:
        query = select(User).where(User.id == tg_user.id)

        if status:
            query.where(User.status == status)

        user = await session.scalar(query)

        return user


# Удалить юзера из базы по telegram-id
async def delete_user(tg_user: Tg_User):
    async with db_session() as session:
        await session.execute(delete(User).where(User.id == tg_user.id))
        await session.commit()


# Удалить юзера в базе по telegram-id
async def update_user(tg_user: Tg_User, status: str = 'member'):
    async with db_session() as session:
        await session.execute(update(User).where(User.id == tg_user.id).values({'status': status}))
        await session.commit()


# Удалить юзера в базу
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


# Удалить лог действия в базу
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
