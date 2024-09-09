from sqlalchemy import select, update
from sqlalchemy.dialects.sqlite import insert

from db.models import User, async_session

async def create_user(tg_id: int, send_daily: bool, animal: str | None) -> None:
    async with async_session() as session:
        insert_stmt = (
            insert(User).
            values(tg_id=tg_id, send_daily=send_daily, animal=animal).
            on_conflict_do_nothing()
        )

        await session.execute(insert_stmt)
        await session.commit()


async def change_daily(tg_id: int) -> bool:
    async with async_session() as session:
        select_stmt = (
            select(User).
            filter_by(tg_id=tg_id)
        )
        user = (await session.execute(select_stmt)).scalar_one()    # TODO: if user is not in db

        if user.send_daily is False:
            daily_status = True
            user.send_daily = daily_status
        else:
            daily_status = False
            user.send_daily = daily_status

        await session.commit()
        return daily_status


async def get_daily_userdata() -> list[dict]:
    """Returns list of dictionaries with data for every user

    Return format: :code:`[{'tg_id': user.tg_id, 'animal': user.animal}]`
    """
    async with async_session() as session:
        select_stmt = (
            select(User).
            where(User.send_daily == True)
        )

        user_list = (await session.execute(select_stmt)).scalars()
        userdata_list: list[dict] = []

        for user in user_list:
            userdata_list.append({'tg_id': user.tg_id, 'animal': user.animal})

        return userdata_list


async def get_user_animal(tg_id: int) -> str | None:
    """Returns user's animal"""
    async with async_session() as session:
        select_stmt = (
            select(User.animal).
            where(User.tg_id==tg_id)
        )

        user_animal: str | None = (await session.execute(select_stmt)).scalar_one()

        return user_animal


async def change_user_animal(tg_id: int, animal: str | None) -> None:
    async with async_session() as session:
        update_stmt = (
            update(User).
            where(User.tg_id==tg_id).
            values(animal=animal)
        )

        await session.execute(update_stmt)
        await session.commit()
