from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from domain.deps.deps import dummy, get_service_collection
from domain.entities.entities import Account, Currency, Transaction
from domain.usecases.bank_service import BankService
from domain.usecases.user_crud import CrudUser
from domain.usecases.currency_crud import CrudCurrency
from utils.utils import verify_jwt
from domain.config.read import ConfigReader


account_router = APIRouter(prefix="/account")
service_collection_ref = get_service_collection()
config = ConfigReader()


@account_router.post("/")
async def create_account(token: str,
                         tag: str,
                         session: AsyncSession =
                         Depends(dummy)) -> UUID | None:
    async with session.begin():
        crud_user: CrudUser = service_collection_ref.crud_cache[CrudUser]
        user = await verify_jwt(token, crud_user, session)
        if user is None:
            print("NO USER FOUND")
            return None
        service: BankService = service_collection_ref.\
            service_cache[BankService]
        account = await service.create_account(user.uuid, tag.lower(), session)
        if account is None:
            print("ERROR CREATING ACCOUNT")
            return None
    return account.uuid


@account_router.delete("/")
async def delete_account(token: str,
                         uid: UUID,
                         session: AsyncSession = Depends(dummy)) -> bool:
    async with session.begin():
        crud_user: CrudUser = service_collection_ref.crud_cache[CrudUser]
        user = await verify_jwt(token, crud_user, session)
        if user is None:
            return False
        service: BankService = service_collection_ref.\
            service_cache[BankService]
        return await service.delete(uid, user.uuid, session)


@account_router.post("/deposit")
async def deposit(token: str,
                  uid: UUID,
                  amount: float,
                  session: AsyncSession = Depends(dummy)) -> bool:
    async with session.begin():
        service: BankService = service_collection_ref.\
            service_cache[BankService]
        value = await service.deposit(uid, amount, session)
    return value


@account_router.post("/withdraw")
async def withdraw(token: str,
                   uid: UUID,
                   amount: float,
                   session: AsyncSession = Depends(dummy)) -> bool:
    async with session.begin():
        crud = service_collection_ref.crud_cache[CrudUser]
        user = await verify_jwt(token, crud, session)
        if user is None:
            return False
        service: BankService = service_collection_ref.\
            service_cache[BankService]
        value = await service.withdraw(user.uuid, uid, amount, session)
    return value


@account_router.post("/transfer")
async def transfer(token: str,
                   from_uuid: UUID,
                   to_uuid: UUID,
                   amount: float,
                   session: AsyncSession = Depends(dummy)) -> bool:
    async with session.begin():
        crud = service_collection_ref.crud_cache[CrudUser]
        user = await verify_jwt(token, crud, session)
        if user is None:
            return False
        service: BankService = service_collection_ref.\
            service_cache[BankService]
        value = await service.transfer(from_uuid, to_uuid, user.uuid, amount,
                                       session)
    return value


@account_router.get("/transactions/all")
async def get_user_account_transactions(token: str,
                                        session: AsyncSession =
                                        Depends(dummy))\
        -> list[Transaction] | None:
    crud = service_collection_ref.crud_cache[CrudUser]
    user = await verify_jwt(token, crud, session)
    if user is None:
        return None
    service: BankService = service_collection_ref.\
        service_cache[BankService]
    return await service.get_user_account_transactions(user.uuid, session)


@account_router.get("/transactions")
async def get_acc_transactions(token: str,
                               acc_id: UUID,
                               session: AsyncSession =
                               Depends(dummy)) -> list[Transaction] | None:
    crud = service_collection_ref.crud_cache[CrudUser]
    user = await verify_jwt(token, crud, session)
    if user is None:
        return None
    service: BankService = service_collection_ref.service_cache[BankService]
    return await service.get_account_transactions(acc_id, session)


@account_router.get("/{uid}")
async def get_account(token: str,
                      uid: UUID,
                      session: AsyncSession = Depends(dummy))\
            -> Account | None:
    crud_user: CrudUser = service_collection_ref.crud_cache[CrudUser]
    user = await verify_jwt(token, crud_user, session)
    if user is None:
        return None
    service: BankService = service_collection_ref.service_cache[BankService]
    account = await service.get_account(user.uuid, uid, session)
    return account


@account_router.get("/")
async def get_user_accounts(token: str,
                            session: AsyncSession
                            = Depends(dummy)) -> list[Account]:
    crud: CrudUser = service_collection_ref.crud_cache[CrudUser]
    user = await verify_jwt(token, crud, session)
    if user is None:
        return []
    service: BankService = service_collection_ref.service_cache[BankService]
    return await service.get_user_accounts(user.uuid, session)


@account_router.get("/currency")
async def get_currencies(secret_key: str,
                         session: AsyncSession =
                         Depends(dummy)) -> list[Currency]:
    if not secret_key == config.model.secret_key:
        return []
    crud: CrudCurrency = service_collection_ref.crud_cache[CrudCurrency]
    return await crud.read_all(session)


@account_router.post("/currency/value")
async def set_currency_value(secret_key: str,
                             tag: str,
                             value: float,
                             session: AsyncSession =
                             Depends(dummy)) -> bool:
    async with session.begin():
        if not secret_key == config.model.secret_key:
            return False
        crud: CrudCurrency = service_collection_ref.crud_cache[CrudCurrency]
        cur = await crud.read_by_tag(tag)
        if cur is None:
            return False
        cur.value = value
    return True
