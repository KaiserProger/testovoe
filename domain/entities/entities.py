from sqlalchemy import Column, Float, ForeignKey, String
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Currency(Base):
    __tablename__ = "Currency"
    tag = Column(String, unique=True)
    value = Column(Float)


class User(Base):
    __tablename__ = "User"
    phone_number = Column(String)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    last_name = Column(String)


class Account(Base):
    __tablename__ = "Account"
    currency_uuid = Column(UUID(as_uuid=True), ForeignKey("Currency.uuid"))
    currency: Currency = relationship("Currency", backref="Account")
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("User.uuid"),
                       nullable=True)
    amount = Column(Float)


class Transaction(Base):
    __tablename__ = "Transaction"
    sender_uuid = Column(UUID(as_uuid=True), ForeignKey("Account.uuid"))
    receiver_uuid = Column(UUID(as_uuid=True), ForeignKey("Account.uuid"))
    amount = Column(Float)
