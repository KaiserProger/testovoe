from typing import Any
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from domain.deps.deps import dummy, get_service_collection
from domain.schemas.schemas import ConfirmUser, Login, RegisterUser
from domain.usecases.auth_service import AuthService
from domain.usecases.user_crud import CrudUser
from status_codes.status_codes import StatusCodes
from domain.config.read import ConfigReader


auth_router = APIRouter()
service_collection_ref = get_service_collection()
config = ConfigReader()


@auth_router.post("/register")
async def register(model: RegisterUser,
                   session: AsyncSession = Depends(dummy)) -> Any:
    service: AuthService = service_collection_ref.service_cache[AuthService]
    crud: CrudUser = service_collection_ref.crud_cache[CrudUser]
    uuid = await service.register(model.dict(), session)
    if not config.model.verify_on_register:
        '''To disable verification,
           just find config.json in domain/config and set
           verify_on_register to False,
           so no need to send email.
           WARN: UNTESTED!!!'''
        if uuid is None:
            return None
        code = crud.codes[uuid]
        await service.confirm(uuid, code, session)
    return jsonable_encoder(uuid)


@auth_router.post("/confirm")
async def confirm(model: ConfirmUser,
                  session: AsyncSession = Depends(dummy)) -> StatusCodes:
    async with session.begin():
        service: AuthService = service_collection_ref.\
            service_cache[AuthService]
        return await service.confirm(model.uuid, model.code, session)


@auth_router.post("/login")
async def login(model: Login, session: AsyncSession = Depends(dummy)) -> Any:
    async with session.begin():
        service: AuthService = service_collection_ref.\
            service_cache[AuthService]
        token = await service.login(session, model.dict())
        return token
