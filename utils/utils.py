from typing import Any
from domain.config.read import ConfigReader
from domain.entities.base import Base
from domain.entities.entities import User
from domain.usecases.user_crud import CrudUser
from sqlalchemy.ext.asyncio import AsyncSession
from traceback import print_exc
import jwt
from hashlib import sha256
import re


config = ConfigReader()


def model_to_dict(obj: Base) -> dict[str, Any]:
    x = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    x['uuid'] = str(x['uuid'])   # Just to serialize UUID
    return x


def compare_optional(fields: list[str], first: dict[str, Any],
                     second: dict[str, Any]) -> bool:
    for i in fields:
        x, y = first.get(i), second.get(i)
        if all([x, y]):
            if x != y:
                return False
    return True


def compare_required(fields: list[str], first: dict[str, Any],
                     second: dict[str, Any]) -> bool:
    for i in fields:
        x, y = first.get(i), second.get(i)
        if not all([x, y]):
            return False
        if x != y:
            return False
    return True


def compare(fields: dict[str, list[str]], first: Base, second: Base) -> bool:
    first_dict = model_to_dict(first)
    second_dict = model_to_dict(second)
    for i in fields:
        match i:
            case "optional":
                if not compare_optional(fields["optional"],
                                        first_dict,
                                        second_dict):
                    return False
            case "required":
                if not compare_required(fields["required"],
                                        first_dict,
                                        second_dict):
                    return False
    return True


def create_jwt(u: User) -> str:
    u_dict = model_to_dict(u)
    return jwt.encode(u_dict, config.model.secret_key)


async def verify_jwt(token: str, crud: CrudUser,
                     session: AsyncSession) -> User | None:
    try:
        decoded = jwt.decode(token, config.model.secret_key, ["HS256"])
        uzver = User(**decoded)  # UZVER COMES BACK!!!
        u = await crud.read(uzver.uuid, session)
        if u is None:
            print("CANT FIND USER")
            return None
        if not compare({'required': ['email', 'phone_number', 'password',
                        'name', 'surname', 'last_name']}, uzver, u):
            print("COMPARE ERROR")
            return None
        return u
    except jwt.PyJWTError:
        print_exc()
        return None


def refresh_jwt(u: User) -> str:
    return create_jwt(u)


async def get_sha_hash(password: str) -> str:
    return sha256(password.encode('utf-8')).hexdigest()


async def pass_validator(password: str) -> bool:
    pattern = '^(?=.*[A-Z])(?=.*[0-9]).{8,}$'
    x = re.search(pattern, password)
    if x is None:
        return False
    return True
