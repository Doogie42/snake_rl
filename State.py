from enum import IntEnum
from Apple import AppleType
from Snake import Snake


class Direction(IntEnum):
    Top = 1
    Down = 2
    Right = 3
    Left = 0

    def __int__(self):
        return self.value


class State():
    def __init__(self, snake: Snake):
        self.death = [0, 0, 0, 0]
        self.red_apple = [0, 0, 0, 0]
        self.green_apple = [0, 0, 0, 0]
        if snake.head.x == 0:
            self.death[Direction.Left.value] = 1
        if snake.head.x == snake.board_width - 1:
            self.death[Direction.Right.value] = 1
        if snake.head.y == 0:
            self.death[Direction.Top.value] = 1
        if snake.head.y == snake.board_height - 1:
            self.death[Direction.Down.value] = 1

        for body in snake.body:
            if body.y == snake.head.y:
                if snake.head.x == body.x - 1:
                    self.death[Direction.Right.value] = 1
                if snake.head.x == body.x + 1:
                    self.death[Direction.Left.value] = 1
            if body.x == snake.head.x:
                if snake.head.y == body.y - 1:
                    self.death[Direction.Down.value] = 1
                if snake.head.y == body.y + 1:
                    self.death[Direction.Top.value] = 1

        for apple in snake.apple:
            if apple.coord.y == snake.head.y:
                if apple.coord.x > snake.head.x:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[Direction.Right.value] = 1
                    else:
                        self.red_apple[Direction.Right.value] = 1
                else:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[Direction.Left.value] = 1
                    else:
                        self.red_apple[Direction.Left.value] = 1
            if apple.coord.x == snake.head.x:
                if apple.coord.y > snake.head.y:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[Direction.Down.value] = 1
                    else:
                        self.red_apple[Direction.Down.value] = 1
                else:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[Direction.Top.value] = 1
                    else:
                        self.red_apple[Direction.Top.value] = 1

    def normalize(self) -> str:
        s = ""
        for i in self.death:
            s += str(i)
        for i in self.red_apple:
            s += str(i)
        for i in self.green_apple:
            s += str(i)
        return s

    def _get_line(self, direction: Direction) -> list:
        return ["D" if self.death[direction] else "x",
                "R" if self.red_apple[direction] else "x",
                "G" if self.green_apple[direction] else "x"
                ]

    def dump(self) -> None:
        top_char = self._get_line(Direction.Top)
        bot_char = self._get_line(Direction.Down)
        right_char = self._get_line(Direction.Right)
        left_char = self._get_line(Direction.Left)

        right_char = reversed(right_char)
        bot_char = reversed(bot_char)

        for char in top_char:
            print((len(left_char) - 1) * " ", char)
        print(''.join(left_char), end='')
        print("H", end='')
        print(''.join(right_char))
        for char in bot_char:
            print((len(left_char) - 1) * " ", char)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, State):
            return self.normalize() == value.normalize()
        if isinstance(value, str):
            return self.normalize() == value

    def __hash__(self) -> int:
        return hash(self.normalize())

    def __str__(self) -> str:
        return self.normalize()
