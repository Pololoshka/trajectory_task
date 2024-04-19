from dataclasses import dataclass
from typing import Self


@dataclass
class Vehicle:
    name: str
    model: str
    year: int
    color: str
    price: int
    latitude: float
    longitude: float
    id: int | None = None

    @classmethod
    def parse(cls, data: dict) -> Self:
        return cls(**data)
