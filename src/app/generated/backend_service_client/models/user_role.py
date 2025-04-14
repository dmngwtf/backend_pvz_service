from enum import Enum


class UserRole(str, Enum):
    EMPLOYEE = "employee"
    MODERATOR = "moderator"

    def __str__(self) -> str:
        return str(self.value)
