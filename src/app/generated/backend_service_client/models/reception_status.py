from enum import Enum


class ReceptionStatus(str, Enum):
    CLOSE = "close"
    IN_PROGRESS = "in_progress"

    def __str__(self) -> str:
        return str(self.value)
