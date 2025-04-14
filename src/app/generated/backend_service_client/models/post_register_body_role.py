from enum import Enum


class PostRegisterBodyRole(str, Enum):
    EMPLOYEE = "employee"
    MODERATOR = "moderator"

    def __str__(self) -> str:
        return str(self.value)
