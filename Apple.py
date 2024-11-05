from enum import Enum
from Coord import Coord


class AppleType(Enum):
    RED = 1,
    GREEN = 2


class Apple():
    def __init__(self, type: AppleType, coord: Coord) -> None:
        self.type = type
        self.coord = coord

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Apple):
            return self.coord == value.coord
        if isinstance(value, Coord):
            return self.coord == value

    def __hash__(self):
        return hash((self.coord.x, self.coord.y, self.type))
