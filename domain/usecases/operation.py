from typing import Optional
from .converter import Converter
from domain.entities.entities import Account, Transaction


class Operation:

    def __init__(self, sender: Account, receiver: Account, amount: float,
                 temp_account: Account):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.initial_amount = amount
        self.happened = False
        self.temp_account = temp_account
        self.status = "NEW"

    async def gen_transaction(self) -> Optional[Transaction]:
        first, second = None, None
        if self.sender is not None:
            first = self.sender.uuid
        if self.receiver is not None:
            second = self.receiver.uuid
        if self.status == "DONE":
            return Transaction(sender_uuid=first,
                               receiver_uuid=second,
                               amount=self.initial_amount)
        else:
            return None

    async def approve(self) -> bool:
        if self.sender is None:
            self.amount = await Converter.convert(self.receiver.currency,
                                                  self.temp_account.currency,
                                                  self.amount)
        elif self.sender.amount > self.amount:
            self.sender.amount -= self.amount
            self.amount = await Converter.convert(self.sender.currency,
                                                  self.temp_account.currency,
                                                  self.amount)
            if self.receiver is None:
                self.status = "DONE"
                return True
        else:
            self.status = "REJECTED"
            return False
        self.temp_account.amount += self.amount
        self.status = "APPROVED"
        return True

    async def go(self) -> None:
        if not await self.approve() or self.status == "DONE":
            return
        self.temp_account.amount -= self.amount
        receive_amount = await Converter.convert(self.temp_account.currency,
                                                 self.receiver.currency,
                                                 self.amount)
        self.receiver.amount += receive_amount
        self.status = "DONE"
