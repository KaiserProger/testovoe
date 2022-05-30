from domain.usecases.account_crud import CrudAccount
from domain.usecases.auth_service import AuthService
from domain.usecases.bank_service import BankService
from domain.usecases.currency_crud import CrudCurrency
from domain.usecases.transaction_crud import CrudTransaction
from domain.usecases.user_crud import CrudUser


# Может быть, это и не лучшее решение,
# зато более-менее конфигурируемое.
# В случае появления нового сервиса/CRUDа достаточно
# добавить его в crud_cache или service_cache
# соответственно.
class ServiceCollection:
    crud_cache = {CrudUser: CrudUser(),
                  CrudAccount: CrudAccount(),
                  CrudTransaction: CrudTransaction(),
                  CrudCurrency: CrudCurrency()}
    service_cache = {AuthService: AuthService(crud_cache[CrudUser]),
                     BankService: BankService(crud_cache[CrudAccount],
                                              crud_cache[CrudCurrency],
                                              crud_cache[CrudTransaction],
                                              crud_cache[CrudUser])}

    def __init__(self) -> None:
        self.lambdas = {i: lambda _: self.crud_cache[i]
                        for i in self.crud_cache}
        self.lambdas.update({i: lambda _: self.service_cache[i]
                            for i in self.service_cache})


_service_collection = ServiceCollection()  # Так нельзя делать, но
# Depends не хочет нормально работать, поэтому...


def get_service_collection() -> ServiceCollection:
    return _service_collection


async def dummy() -> None:
    pass
