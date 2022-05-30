from typing import AsyncIterator
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from domain.entities.entities import Account, Currency
from domain.entities.base import Base
from sqlalchemy.exc import SQLAlchemyError


class Db:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url, echo=True, future=True)
        self.sessionmaker = sessionmaker(self.engine, class_=AsyncSession,
                                         expire_on_commit=False)

    async def create_session(self) -> AsyncIterator[AsyncSession]:
        async with self.sessionmaker() as session:
            yield session

    async def init_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def init_app_values(self, acc_id: UUID) -> None:
        rub = Currency(tag="rub", value=1/70)
        usd = Currency(tag="usd", value=1)
        eur = Currency(tag="eur", value=1/0.85)
        async with self.sessionmaker() as session:
            try:
                async with session.begin():
                    await session.merge(rub)
                    await session.merge(usd)
                    await session.merge(eur)
            except SQLAlchemyError:
                await session.rollback()
                async with session.begin():
                    res = await session.execute(select(Currency).
                                                where(Currency.tag == "rub"))
                    rub = res.scalar_one()
                    res = await session.execute(select(Currency).
                                                where(Currency.tag == "usd"))
                    usd = res.scalar_one()
                    res = await session.execute(select(Currency).
                                                where(Currency.tag == "eur"))
                    eur = res.scalar_one()
        async with self.sessionmaker() as session:
            try:
                async with session.begin():
                    temp = Account(uuid=acc_id, user_uuid=None,
                                   currency_uuid=usd.uuid, amount=1000000)
                    await session.merge(temp)
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
