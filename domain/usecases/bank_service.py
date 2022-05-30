from typing import Optional
from uuid import UUID

from domain.entities.entities import Account, Transaction
from .account_crud import CrudAccount
from .currency_crud import CrudCurrency
from .user_crud import CrudUser
from .transaction_crud import CrudTransaction
from sqlalchemy.ext.asyncio import AsyncSession
from .operation import Operation


class BankService:
    def __init__(self, acc_crud: CrudAccount,
                 cur_crud: CrudCurrency,
                 trans_crud: CrudTransaction,
                 user_crud: CrudUser) -> None:
        self.acc_crud = acc_crud
        self.cur_crud = cur_crud
        self.trans_crud = trans_crud
        self.user_crud = user_crud

    async def create_account(self, user_uuid: UUID,
                             tag: str,
                             session: AsyncSession) -> Account | None:
        check: list[Account] = await self.acc_crud.get_user_accounts(user_uuid,
                                                                     session)
        cur = await self.cur_crud.read_by_tag(tag, session)
        if cur is None:
            return None
        if len(check) > 0:
            print("CHECK STARTED")
            for i in check:
                if i.currency_uuid == cur.uuid:
                    print("GOT CHECK YOPTA")
                    return None
        a = Account(user_uuid=user_uuid, currency_uuid=cur.uuid, amount=0)
        await self.acc_crud.create_or_update(a, session)
        return a

    async def delete(self, uid: UUID, u: UUID,
                     session: AsyncSession) -> bool:
        if not self.check_user_owns_account(u, uid, session):
            return False
        return await self.acc_crud.delete(uid, session)

    async def deposit(self, to: UUID,
                      amount: float,
                      session: AsyncSession) -> bool:
        second = await self.acc_crud.read(to, session)
        if second is None:
            return False
        return await self.commit_operation(None, second, amount,
                                           session)

    async def withdraw(self, user_uuid: UUID,
                       to: UUID,
                       amount: float,
                       session: AsyncSession) -> bool:
        if not self.check_user_owns_account(user_uuid, to,
                                            session):
            return False
        first = await self.acc_crud.read(to, session)
        if first is None:
            return False
        return await self.commit_operation(first, None, amount,
                                           session)

    async def get_account_transactions(self, account_id: UUID,
                                       user_id: UUID,
                                       session: AsyncSession)\
            -> list[Transaction] | None:
        if not self.check_user_owns_account(user_id, account_id,
                                            session):
            return None
        account = await self.acc_crud.read(account_id, session)
        if account is None:
            return []
        return await self.trans_crud.get_account_transactions(account, session)

    async def commit_operation(self, first: Optional[Account],
                               second: Optional[Account],
                               amount: float,
                               session: AsyncSession) -> bool:
        temp = await self.acc_crud.get_temp_account(session)
        o = Operation(first, second, amount, temp)
        await o.go()
        transaction = await o.gen_transaction()
        if transaction is None:
            return False
        print("Printing transaction...")
        await self.trans_crud.create_or_update(transaction, session)
        return True

    async def check_user_owns_account(self, user_uuid: UUID,
                                      acc_uuid: UUID,
                                      session: AsyncSession) -> bool:
        acc = await self.acc_crud.read(acc_uuid, session)
        if acc is None or acc.user_uuid != user_uuid:
            return False
        return True

    async def transfer(self, from_uuid: UUID,
                       to_uuid: UUID,
                       user_uuid: UUID,
                       amount: float,
                       session: AsyncSession) -> bool:
        if not await self.check_user_owns_account(user_uuid, from_uuid,
                                                  session):
            return False
        first, second = await self.acc_crud.read(from_uuid, session),\
            await self.acc_crud.read(to_uuid, session)
        return await self.commit_operation(first, second, amount, session)

    async def get_account(self, user: UUID, acc: UUID,
                          session: AsyncSession) -> Account | None:
        if not self.check_user_owns_account(user, acc, session):
            return None
        return await self.acc_crud.read(acc, session)

    async def get_user_account_transactions(self,
                                            user_uuid: UUID,
                                            session: AsyncSession)\
            -> list[Transaction]:
        accounts = await self.acc_crud.get_user_accounts(user_uuid, session)
        transactions = []
        for i in accounts:
            objs = await self.get_account_transactions(i.uuid,
                                                       user_uuid,
                                                       session)
            if objs is None:
                continue
            transactions.append(objs)
        return transactions

    async def get_user_accounts(self,
                                user_uuid: UUID,
                                session: AsyncSession) -> list[Account]:
        return await self.acc_crud.get_user_accounts(user_uuid, session)
