from enum import Enum


class SenderType(str, Enum):
    USER = "USER"
    AI = "AI"
    SYSTEM = "SYSTEM"
