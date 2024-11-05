import pygame
from Coord import Coord
from Apple import AppleType
from Snake import Snake

SQUARE_SIZE = 30
OFFSET_TOP_X = 100
OFFSET_TOP_Y = 100


class Graphic():
    def __init__(self,
                 screen_width=800,
                 screen_height=800,
                 tick=42) -> None:
        self.screen_height = screen_height
        self.screen_width = screen_width
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_height,
                                               self.screen_width))
        self.clock = pygame.time.Clock()
        self.tick = tick
        pygame.font.init()
        self.my_font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.snake_body_color = "blue"
        self.snake_head_color = "green"
        self.red_apple_color = "red"
        self.green_apple_color = "green"

    def render(self, snake: Snake) -> None:
        self.clock.tick(self.tick)
        self.screen.fill("black")
        self.draw_border(snake)
        self.draw_snake(snake)
        self.draw_apple(snake)
        pygame.display.flip()

    def board_to_screen_coord(self, coord: Coord) -> Coord:
        offset_x = OFFSET_TOP_X
        offset_y = OFFSET_TOP_Y
        new_x = offset_x + (coord.x) * SQUARE_SIZE
        new_y = offset_y + (coord.y) * SQUARE_SIZE
        return Coord(new_x, new_y)

    def draw_snake(self, snake: Snake) -> None:
        projected = self.board_to_screen_coord(snake.body[0])
        pygame.draw.rect(self.screen, self.snake_head_color, pygame.Rect(
                            projected.x,
                            projected.y,
                            SQUARE_SIZE,
                            SQUARE_SIZE))
        for piece in snake.body[1:]:
            projected = self.board_to_screen_coord(piece)
            pygame.draw.rect(self.screen, self.snake_body_color, pygame.Rect(
                            projected.x,
                            projected.y,
                            SQUARE_SIZE,
                            SQUARE_SIZE))

    def draw_apple(self, snake: Snake) -> None:
        for apple in snake.apple:
            projected = self.board_to_screen_coord(apple.coord)
            if apple.type == AppleType.RED:
                color = self.red_apple_color
            else:
                color = self.green_apple_color
            pygame.draw.rect(self.screen, color, pygame.Rect(
                            projected.x,
                            projected.y,
                            SQUARE_SIZE,
                            SQUARE_SIZE))

    def draw_border(self, snake: Snake) -> None:

        pygame.draw.line(self.screen,
                         "green",
                         (OFFSET_TOP_X, OFFSET_TOP_Y),
                         (OFFSET_TOP_X,
                          OFFSET_TOP_Y + snake.board_width * SQUARE_SIZE))
        pygame.draw.line(self.screen,
                         "green",
                         (OFFSET_TOP_X, OFFSET_TOP_Y),
                         (OFFSET_TOP_X + snake.board_width * SQUARE_SIZE,
                          OFFSET_TOP_Y))
        pygame.draw.line(self.screen,
                         "green",
                         (OFFSET_TOP_X + snake.board_width * SQUARE_SIZE,
                          OFFSET_TOP_Y),
                         (OFFSET_TOP_X + snake.board_width * SQUARE_SIZE,
                          OFFSET_TOP_Y + snake.board_height * SQUARE_SIZE))
        pygame.draw.line(self.screen,
                         "green",
                         (OFFSET_TOP_X,
                          OFFSET_TOP_Y + snake.board_height * SQUARE_SIZE),
                         (OFFSET_TOP_X + snake.board_width * SQUARE_SIZE,
                          OFFSET_TOP_Y + snake.board_height * SQUARE_SIZE))
