from enum import Enum


class AuthCode(Enum):
    Ok = 0,
    Exists = 1,
    Exception = 2
