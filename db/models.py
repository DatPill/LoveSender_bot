from typing import Annotated, Optional

from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from data.config import DB_URL


engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine)

pkint = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[pkint]
    tg_id = mapped_column(BigInteger, unique=True)
    animal: Mapped[Optional[str]]
    send_daily = mapped_column(Boolean, default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
