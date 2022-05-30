from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from domain.config.read import ConfigReader
from domain.entities.entities import Account
from sqlalchemy.ext.asyncio import AsyncSession
from .crudbase import CrudBase


class CrudAccount(CrudBase[Account]):
    def __init__(self) -> None:
        self.super = super().__init__(Account)
        self.temp_uuid = ConfigReader().model.temp_acc_id

    async def get_temp_account(self, session: AsyncSession)\
            -> None:
        result = await session.execute(select(Account)
                                       .where(Account.uuid ==
                                              self.temp_uuid)
                                       .options(selectinload(Account.
                                                             currency)))
        return result.scalar_one()

    async def read(self, uid: UUID, session: AsyncSession)\
            -> Account | None:
        return await session.get(self.model_cls, uid,
                                 options=[selectinload(Account.currency)])

    async def create_or_update(self, obj: Account,
                               session: AsyncSession) -> None:
        await self._create_or_update(obj, session)

    async def get_user_accounts(self, u: UUID,
                                session: AsyncSession) -> list[Account]:
        result = await session.execute(select(Account).where(Account.
                                                             user_uuid == u)
                                       .options(selectinload(Account.
                                                             currency)))
        x = result.scalars().all()
        return x
