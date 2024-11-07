from Apple import Apple, AppleType
from Coord import Coord, make_random_coord
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
        assert nb_green_apple + nb_red_apple < board_height + board_width + size_start
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
        self.duration = 0
        self.apple_eaten = []
        for i in range(0, size_start - 1):
            new_body = self.body[i] - self.direction_move[self.direction]
            self.body.append(new_body)

        for i in range(0, nb_green_apple):
            self.apple.append(self.make_apple(apple_type=AppleType.GREEN))
        for i in range(0, nb_red_apple):
            self.apple.append(self.make_apple(apple_type=AppleType.RED))

    def make_apple(self, apple_type: AppleType) -> Apple:
        coord = make_random_coord(0, self.board_height)
        while coord in self.body or coord in self.apple:
            coord = make_random_coord(0, self.board_height)
        return Apple(apple_type, coord)

    def move(self, direction: SnakeDirection) -> GameState:
        self.duration += 1
        self.direction = direction
        new_coord = self.head + self.direction_move[self.direction]
        if new_coord in self.body:
            return GameState.DEAD
        if new_coord.x < 0 or new_coord.x >= self.board_width:
            return GameState.DEAD
        if new_coord.y < 0 or new_coord.y >= self.board_height:
            return GameState.DEAD
        self.body.insert(0, new_coord)
        self.head = new_coord
        ret_state = GameState.ALIVE
        try:
            apple_idx = self.apple.index(self.head)
            self.apple_eaten.append(
                Apple(self.apple[apple_idx].type, self.apple[apple_idx].coord)
            )
            if self.apple[apple_idx].type == AppleType.RED:
                ret_state = GameState.RED
                if len(self.body) <= 2:
                    return GameState.DEAD
                self.body.pop()
                self.body.pop()
            if self.apple[apple_idx].type == AppleType.GREEN:
                ret_state = GameState.GREEN
            if len(self.body) < self.board_height * self.board_width - len(self.apple) - 1:
                self.apple[apple_idx] = self.make_apple(self.apple[apple_idx].type)
            else:
                del self.apple[apple_idx]
        except ValueError:
            self.body.pop()
            pass
        return ret_state

    def _safe_del(self, my_list: list, val) -> list:
        try:
            my_list.remove(val)
        except ValueError:
            pass
        return my_list

    def get_score(self) -> int:
        return len(self.body)

    def get_duration(self) -> int:
        return self.duration

    def get_green_apple_eaten(self) -> int:
        return len([a for a in self.apple_eaten if a.type == AppleType.GREEN])

    def get_red_apple_eaten(self) -> int:
        return len([a for a in self.apple_eaten if a.type == AppleType.RED])
