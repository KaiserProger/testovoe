from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.entities import Currency
from .crudbase import CrudBase


class CrudCurrency(CrudBase[Currency]):
    def __init__(self) -> None:
        super().__init__(Currency)

    async def create_or_update(self, obj: Currency) -> None:
        await self._create_or_update(obj)

    async def read_by_tag(self, tag: str, session: AsyncSession)\
            -> Optional[Currency]:
        result = await session.execute(select(Currency).where(Currency.tag ==
                                                              tag))
        cur: Currency = result.scalar_one_or_none()
        return cur
