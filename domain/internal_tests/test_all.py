import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from usecases.account_crud import CrudAccount
import sys
sys.path.append("..")
sys.path.append("../..")
from usecases.auth_service import AuthService
from usecases.bank_service import BankService
from usecases.currency_crud import CrudCurrency
from usecases.transaction_crud import CrudTransaction
from usecases.user_crud import CrudUser


@pytest.mark.asyncio
async def test_all(create_session: AsyncSession):
    crud_user = CrudUser()
    crud_acc = CrudAccount()
    crud_cur = CrudCurrency()
    crud_trans = CrudTransaction()
    auth_service = AuthService(crud_user)
    bank_service = BankService(crud_acc, crud_cur, crud_trans)
    async with create_session.begin():
        uuid = await auth_service.register({
            "phone_number": "+77002221337",
            "email": "uzbek@mail.ru",
            "password": "PythonNotCool123#./",
            "name": "Roman",
            "last_name": "Uzbek",
            "surname": "Kaiser"
        })
        code = crud_user.codes.get(uuid)
        assert code is not None
        assert await auth_service.confirm(uuid, code, create_session)
    # ------- SO HERE WE GO! REGISTER PASSED -------
    async with create_session.begin():
        rub_acc = await bank_service.create_account({
            "user_uuid": uuid,
            "amount": 150,
        }, "rub", create_session)
        usd_acc = await bank_service.create_account({
            "user_uuid": uuid,
            "amount": 100,
        }, "usd", create_session)
        eur_acc = await bank_service.create_account({
            "user_uuid": uuid,
            "amount": 50,
        }, "eur", create_session)
        assert all([rub_acc, usd_acc, eur_acc])
    # ------- ACCOUNT CREATION PASSED! -------
