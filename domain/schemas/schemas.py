from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ConfigSchema(BaseModel):
    temp_acc_id: UUID
    verify_on_register: bool
    secret_key: str


class RegisterUser(BaseModel):
    phone_number: str
    email: str
    password: str
    name: str
    surname: str
    last_name: str


class ConfirmUser(BaseModel):
    uuid: UUID
    code: int


class Login(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: str


class CreateAccount(BaseModel):
    user_uuid: UUID
    currency_tag: str


class ResetUser(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
