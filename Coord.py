import random


class Coord():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, value: object) -> bool:
        return self.x == value.x and self.y == value.y

    def __str__(self) -> str:
        return f"{self.x} {self.y}"

    def __repr__(self) -> str:
        return f"{self.x} {self.y}"

    def __add__(self, rhs: object) -> object:
        return Coord(self.x + rhs.x, self.y + rhs.y)


def make_random_coord(start=0, max_val=10) -> Coord:
    return Coord(random.randrange(start, max_val),
                 random.randrange(start, max_val))


def make_randome_coord_include(x_include: list[int] = [],
                               y_include: list[int] = []) -> Coord:
    x = random.choice(x_include)
    y = random.choice(y_include)
    return Coord(x, y)
