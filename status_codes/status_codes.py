from enum import Enum


class StatusCodes(Enum):
    EXPIRED_TOKEN = "EXPIRED_TOKEN"
    INCORRECT_DATA = "INCORRECT_DATA"
    OK = "OK"
    FAIL = "FAIL"
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
