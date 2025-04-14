from enum import Enum


class PVZCity(str, Enum):
    КАЗАНЬ = "Казань"
    МОСКВА = "Москва"
    САНКТ_ПЕТЕРБУРГ = "Санкт-Петербург"

    def __str__(self) -> str:
        return str(self.value)
