from sqlalchemy import select, or_
from domain.entities.entities import Account, Transaction
from .crudbase import CrudBase
from sqlalchemy.ext.asyncio import AsyncSession


class CrudTransaction(CrudBase[Transaction]):
    def __init__(self) -> None:
        super().__init__(Transaction)

    async def create_or_update(self, obj: Transaction,
                               session: AsyncSession) -> None:
        await self._create_or_update(obj, session)

    async def get_account_transactions(self, account: Account,
                                       session: AsyncSession)\
            -> list[Transaction]:
        result = await session.execute(select(Transaction).where(
            or_(Transaction.sender_uuid == account.uuid,
                Transaction.receiver_uuid == account.uuid)))
        return result.scalars().all()
