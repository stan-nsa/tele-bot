from db.engine import db_session
from db.models import User, SkuLog
from sqlalchemy import select, delete, update

from aiogram.types import User as Tg_User


# Получить юзера из базы по telegram-id и статусу
async def get_user(tg_user: Tg_User, status: str = None):
    async with db_session() as session:
        query = select(User).where(User.id == tg_user.id)

        if status:
            query = query.where(User.status == status)

        user = await session.scalar(query)

        return user


# Получить список юзеров бота из базы по статусу
async def get_users(status: str = 'member'):
    async with db_session() as session:
        query = select(User)

        if status:
            query = query.where(User.status == status)

        users = await session.scalars(query)

        return users


# Удалить юзера из базы по telegram-id
async def delete_user(tg_user: Tg_User):
    async with db_session() as session:
        await session.execute(
            delete(User).
            where(User.id == tg_user.id)
        )
        await session.commit()


# Пометить юзера в базе как <not member> по telegram-id
async def delete_user_by_id(user_id: int):
    async with db_session() as session:
        await session.execute(
            update(User).
            where(User.id == user_id).
            values({'status': 'not member'})
        )
        await session.commit()


# Удалить юзера в базе по telegram-id
async def update_user(tg_user: Tg_User, status: str = 'member'):
    if await get_user(tg_user=tg_user):
        async with db_session() as session:
            update_values = {
                'first_name': tg_user.first_name,
                'last_name': tg_user.last_name,
                'username': tg_user.username,
                'full_name': tg_user.full_name,
                'status': status,
            }
            await session.execute(
                update(User).
                where(User.id == tg_user.id).
                values(update_values)
            )
            await session.commit()
    else:
        await add_user(tg_user=tg_user, status=status)


# Удалить юзера в базу
async def add_user(tg_user: Tg_User, status: str = 'member'):
    async with db_session() as session:
        user = User(
            id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            full_name=tg_user.full_name,
            status=status
        )
        session.add(user)
        await session.commit()


# Удалить лог действия в базу
async def add_log(user_id, user_name, sku, action, description):
    async with db_session() as session:
        event = SkuLog(
            user_id=user_id,
            user_name=user_name,
            sku=sku,
            action=action,
            description=description
        )
    session.add(event)
    await session.commit()
