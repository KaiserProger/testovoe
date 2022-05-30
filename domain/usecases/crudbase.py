from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from domain.entities.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


ModelTypeVar = TypeVar("ModelTypeVar", bound=Base)


class CrudBase(Generic[ModelTypeVar]):
    def __init__(self, model_type: Type[ModelTypeVar]) -> None:
        self.model_cls = model_type

    async def _create_or_update(self, obj: ModelTypeVar,
                                session: AsyncSession) -> None:
        session.add(obj)

    async def read(self, uid: UUID, session: AsyncSession)\
            -> Optional[ModelTypeVar]:
        return await session.get(self.model_cls, uid)

    async def delete(self, uid: UUID, session: AsyncSession) -> bool:
        obj = await self.read(uid, session)
        if obj is None:
            return False
        await session.delete(obj)
        return True

    async def read_all(self, session: AsyncSession) -> list[ModelTypeVar]:
        res = await session.execute(select(self.model_cls))
        return res.scalars().all()
