from typing import Any
from uuid import UUID
from domain.entities.entities import User
from domain.mail.mailer import Mailer
from status_codes.status_codes import StatusCodes
from .user_crud import CrudUser
from sqlalchemy.ext.asyncio import AsyncSession

from utils.utils import compare, create_jwt, get_sha_hash, pass_validator


class AuthService:
    def __init__(self, crud: CrudUser) -> None:
        self.crud = crud

    async def login(self, session: AsyncSession,
                    values: dict[str, Any]) -> str:
        u = User(**values)
        u.password = await get_sha_hash(u.password)
        email = False
        if u.email is not None and u.email != "":
            email = True
            print(u.email)
        obj = await self.crud.read_by_email(u.email, session) if email\
            else await self.crud.read_by_phone(u.phone_number, session)
        if obj is None:
            return ""
        if not compare({"required": ["password"], "optional": ["email",
                        "phone_number"]}, u, obj):
            print("{} and {}".format(u.password, obj.password))
            return ""
        return create_jwt(obj)

    async def register(self, values: dict[str, Any],
                       session: AsyncSession) -> UUID | None:
        u = User(**values)
        if not await pass_validator(u.password):
            return None
        if await self.crud.read_by_email(u.email, session)\
                or await self.crud.read_by_phone(u.phone_number, session):
            return None
        print("!!!", u.password)
        u.password = await get_sha_hash(u.password)
        result = await self.crud.create(u)
        code = self.crud.codes.get(result)
        await Mailer.send(code, u.email)
        return result

    async def confirm(self, uid: UUID, code: int,
                      session: AsyncSession) -> StatusCodes:
        return await self.crud.confirm(uid, code, session)

    async def change_data(self,
                          email: str,
                          password: str,
                          data_dict: dict[str, Any],
                          session: AsyncSession) -> bool:
        if not self.login(session, {"email": email,
                                    "password": password}):
            return False
        u = await self.crud.read_by_email(email, session)
        if u is None:
            return False
        for i in data_dict:
            if i is not None or i != "":
                setattr(u, i, data_dict[i])
        return True
