from uuid import UUID
import pytest
import requests


@pytest.fixture(scope="session")
def register_user() -> str:
    '''If you're running tests,
       please disable verify_on_register
       in domain/config/config.json,
       OTHERWISE IT WILL NOT WORK.'''
    response = requests.post("/register", json={
        "phone_number": "+77002221337",
        "email": "kaisergrobe@gmail.com",
        "password": "PythonNotCool123#./",
        "name": "Roman",
        "last_name": "Uzbek",
        "surname": "Kaiser"
    })
    assert response.status_code == 200
    response = requests.post("/login", json={
        "phone_number": "+77002221337",
        "password": "PythonNotCool123#./"
    })
    assert response.status_code == 200
    token = response.json()["token"]
    return token


@pytest.fixture(scope="session")
def create_accounts(register_user: str) -> None:
    response = requests.post("/account/", json={
        "token": register_user,
        "tag": "RUB"
    })
    assert response.status_code == 200
    response = requests.post("/account/", json={
        "token": register_user,
        "tag": "USD"
    })
    assert response.status_code == 200


@pytest.fixture(scope="session")
def get_user_accounts(register_user: str,
                      create_accounts: None) -> dict[str, UUID]:
    acc_uuids: dict[str, UUID] = {}
    response = requests.get("/account", json={
        "token": register_user
    })
    assert response.status_code == 200
    x = response.json()
    for i in x:
        acc_uuids[i["currency"]["tag"]] = UUID(i["uuid"])
    return acc_uuids
