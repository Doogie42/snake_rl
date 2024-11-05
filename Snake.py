from Apple import Apple, AppleType
from Coord import Coord, make_random_coord, make_randome_coord_include
import random
from enum import Enum


BOARD_WIDTH = 10
BOARD_HEIGHT = 10


class SnakeDirection(Enum):
    LEFT = 0
    UP = 1
    DOWN = 2
    RIGHT = 3

    def __int__(self):
        return self.value


class GameState(Enum):
    DEAD = 1,
    ALIVE = 2,
    RED = 3,
    GREEN = 4,


class Snake():
    def __init__(self,
                 board_width=10,
                 board_height=10,
                 size_start=3,
                 nb_green_apple=2,
                 nb_red_apple=1) -> None:
        self.head = make_random_coord(0 + 3, board_width - 3)
        self.body = [self.head]
        self.direction = random.choice(list(SnakeDirection))
        self.direction_move = {
            SnakeDirection.LEFT: Coord(-1, 0),
            SnakeDirection.UP: Coord(0, -1),
            SnakeDirection.DOWN: Coord(0, 1),
            SnakeDirection.RIGHT: Coord(1, 0),
        }
        self.board_width = board_width
        self.board_height = board_height
        self.apple = []

        for i in range(0, size_start - 1):
            new_body = self.body[i] + self.direction_move[self.direction]
            self.body.append(new_body)

        for i in range(0, nb_green_apple):
            self.apple.append(self.make_apple(apple_type=AppleType.GREEN))
        for i in range(0, nb_red_apple):
            self.apple.append(self.make_apple(apple_type=AppleType.RED))

    def make_apple(self, apple_type: AppleType) -> Apple:
        x_possible = list(range(0, self.board_width))
        y_possible = list(range(0, self.board_height))
        for body_piece in self.body:
            x_possible = self._safe_del(x_possible, body_piece.x)
            y_possible = self._safe_del(y_possible, body_piece.y)
        for apple in self.apple:
            x_possible = self._safe_del(x_possible, apple.coord.x)
            y_possible = self._safe_del(y_possible, apple.coord.y)
        apple_coord = make_randome_coord_include(x_possible, y_possible)
        return Apple(apple_type, apple_coord)

    def choose_direction(self) -> None:
        self.direction = SnakeDirection((self.direction.value + 1) % 4)

    def move(self, direction: SnakeDirection) -> GameState:
        self.direction = direction
        new_coord = self.head + self.direction_move[self.direction]
        if new_coord in self.body:
            return GameState.DEAD
        if new_coord.x < 0 or new_coord.x >= self.board_width:
            return GameState.DEAD
        if new_coord.y < 0 or new_coord.y >= self.board_height:
            return GameState.DEAD
        self.body.insert(0, new_coord)
        self.body.pop()
        self.head = new_coord
        ret_state = GameState.ALIVE
        try:
            apple_idx = self.apple.index(self.head)
            if self.apple[apple_idx].type == AppleType.RED:
                ret_state = GameState.RED
                if len(self.body) <= 1:
                    return GameState.DEAD
                self.body.pop()
            if self.apple[apple_idx].type == AppleType.GREEN:
                ret_state = GameState.GREEN
            self.apple[apple_idx] = self.make_apple(self.apple[apple_idx].type)
        except ValueError:
            pass
        return ret_state

    def _safe_del(self, my_list: list, val) -> list:
        try:
            my_list.remove(val)
        except ValueError:
            pass
        return my_list
