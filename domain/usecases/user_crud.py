from typing import Optional
from uuid import UUID, uuid4
from random import randint

from sqlalchemy import select

from status_codes.status_codes import StatusCodes
from .crudbase import CrudBase
from domain.entities.entities import User
from sqlalchemy.ext.asyncio import AsyncSession


class CrudUser(CrudBase[User]):
    temp_store: dict[UUID, User] = {}
    codes: dict[UUID, int] = {}

    def __init__(self) -> None:
        super().__init__(User)

    async def create(self, obj: User)\
            -> UUID:
        uuid = uuid4()
        self.temp_store[uuid] = obj
        self.codes[uuid] = randint(100000, 999999)
        return uuid

    async def confirm(self, uuid: UUID, code: int,
                      session: AsyncSession) -> StatusCodes:
        if code != self.codes[uuid]:
            return StatusCodes.INCORRECT_DATA
        obj = self.temp_store.get(uuid)
        if obj is None:
            return StatusCodes.NOT_FOUND
        await self._create_or_update(obj, session)
        return StatusCodes.OK

    async def read_by_email(self, email: str,
                            session: AsyncSession) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def read_by_phone(self, number: str,
                            session: AsyncSession) -> Optional[User]:
        result = await session.execute(select(User).where(User.phone_number ==
                                                          number))
        return result.scalar_one_or_none()
