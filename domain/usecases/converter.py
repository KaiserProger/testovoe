from domain.entities.entities import Currency


class Converter:
    @staticmethod
    async def convert(first: Currency, second: Currency,
                      amount: float) -> float:
        return (amount * first.value / second.value)
