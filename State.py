from enum import IntEnum
from Apple import AppleType
from Snake import Snake


class direction(IntEnum):
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
            self.death[direction.Left.value] = 1
        if snake.head.x == snake.board_width - 1:
            self.death[direction.Right.value] = 1
        if snake.head.y == 0:
            self.death[direction.Top.value] = 1
        if snake.head.y == snake.board_height - 1:
            self.death[direction.Down.value] = 1

        for body in snake.body:
            if body.y == snake.head.y:
                if snake.head.x == body.x - 1:
                    self.death[direction.Right.value] = 1
                if snake.head.x == body.x + 1:
                    self.death[direction.Left.value] = 1
            if body.x == snake.head.x:
                if snake.head.y == body.y - 1:
                    self.death[direction.Down.value] = 1
                if snake.head.y == body.y + 1:
                    self.death[direction.Top.value] = 1

        for apple in snake.apple:
            if apple.coord.y == snake.head.y:
                if apple.coord.x > snake.head.x:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[direction.Right.value] = 1
                    else:
                        self.red_apple[direction.Right.value] = 1
                else:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[direction.Left.value] = 1
                    else:
                        self.red_apple[direction.Left.value] = 1
            if apple.coord.x == snake.head.x:
                if apple.coord.y > snake.head.y:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[direction.Down.value] = 1
                    else:
                        self.red_apple[direction.Down.value] = 1
                else:
                    if apple.type == AppleType.GREEN:
                        self.green_apple[direction.Top.value] = 1
                    else:
                        self.red_apple[direction.Top.value] = 1

    def normalize(self) -> str:
        s = ""
        for i in self.death:
            s += str(i)
        for i in self.red_apple:
            s += str(i)
        for i in self.green_apple:
            s += str(i)
        return s
