from enum import Enum


class ProductType(str, Enum):
    ОБУВЬ = "обувь"
    ОДЕЖДА = "одежда"
    ЭЛЕКТРОНИКА = "электроника"

    def __str__(self) -> str:
        return str(self.value)
