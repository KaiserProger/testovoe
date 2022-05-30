from uuid import UUID
import requests

URL = "http://localhost:8080"
uuid = ""


def test_deposit_money(register_user: str,
                       get_user_accounts: dict[str, UUID]) -> None:
    response = requests.post("/account/deposit", json={
        "token": register_user,
        "uuid": get_user_accounts["rub"],
        "amount": 100
    })
    assert response.status_code == 200
    assert response.json()


def test_withdraw_money(register_user: str,
                        get_user_accounts: dict[str, UUID]) -> None:
    response = requests.post("/account/withdraw", json={
        "token": register_user,
        "uuid": get_user_accounts["rub"],
        "amount": 20
    })
    assert response.status_code == 200
    assert response.json()


def test_transfer(register_user: str,
                  get_user_accounts: dict[str, UUID]) -> None:
    response = requests.post("/account/transfer", json={
        "token": register_user,
        "from_uuid": get_user_accounts["rub"],
        "to_uuid": get_user_accounts["eur"],
        "amount": 50
    })
    assert response.status_code == 200
    assert response.json()
