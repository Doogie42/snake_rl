import pygame
from Coord import Coord
from Apple import AppleType
from Snake import Snake
from enum import Enum
import time

SQUARE_SIZE = 30
OFFSET_TOP_X = 100
OFFSET_TOP_Y = 100


class Action(Enum):
    QUIT = 1,
    RESTART = 2,
    CONTINUE = 3,
    LEFT = 4,
    DOWN = 5,
    RIGHT = 6,
    TOP = 7


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
        self.action = Action.CONTINUE
        self.old_tick = -1
        self.higscore = 0
        self.higduration = 0

    def clean_up(self):
        pygame.quit()

    def render(self, snake: Snake,
               game_number: int,
               score: int,
               duration: int,
               q_table: dict,
               state: str = "") -> None:
        self.higscore = max(score, self.higscore)
        self.higduration = max(duration, self.higduration)
        self.get_input()
        self.clock.tick(self.tick)
        self.screen.fill("black")
        self.draw_border(snake)
        self.draw_snake(snake)
        self.draw_apple(snake)
        self.top_statistics(game_number, score, duration,
                            known_state=len(q_table.keys()))
        if state:
            self.display_state(q_table[state], state, snake)

        pygame.display.flip()

    def top_statistics(self, game_number: int, score: int,
                       duration: int, known_state: int):
        text_surface = self.my_font.render(f'fps {self.tick}', False, "green")
        self.screen.blit(text_surface, (0, 0))
        text_surface = self.my_font.render(f'# game {game_number}',
                                           False,
                                           "green")
        self.screen.blit(text_surface, (0, 20))
        text_surface = self.my_font.render(f'known state {known_state}',
                                           False,
                                           "green")
        self.screen.blit(text_surface, (0, 40))

        text_surface = self.my_font.render(f'score {score}', False, "green")
        self.screen.blit(text_surface, (self.screen_width / 2, 0))
        text_surface = self.my_font.render(f'highscore {self.higscore}',
                                           False,
                                           "green")
        self.screen.blit(text_surface, (self.screen_width / 2, 20))

        text_surface = self.my_font.render(f'duration {duration}',
                                           False,
                                           "green")
        self.screen.blit(text_surface, (self.screen_width - 180, 0))
        text_surface = self.my_font.render(f'highduration {self.higduration}',
                                           False,
                                           "green")
        self.screen.blit(text_surface, (self.screen_width - 180, 20))

    def display_state(self,
                      state_value: list[float],
                      state: str,
                      snake: Snake) -> None:
        offset_bottom_y = OFFSET_TOP_Y + snake.board_height * SQUARE_SIZE
        text_surface = self.my_font.render(f'State {state}', False, "green")
        self.screen.blit(text_surface, (0, offset_bottom_y + 10))
        text_surface = self.my_font.render(
            f'value {[int(i) for i in state_value]}', False, "green"
        )
        self.screen.blit(text_surface, (0, offset_bottom_y + 30))

    def board_to_screen_coord(self, coord: Coord) -> Coord:
        offset_x = OFFSET_TOP_X
        offset_y = OFFSET_TOP_Y
        new_x = offset_x + (coord.x) * SQUARE_SIZE
        new_y = offset_y + (coord.y) * SQUARE_SIZE
        return Coord(new_x, new_y)

    def get_input(self):
        self.action = Action.CONTINUE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.action = Action.QUIT

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.action = Action.QUIT

        elif keys[pygame.K_r]:
            self.action = Action.RESTART
        elif keys[pygame.K_w]:
            self.action = Action.TOP
        elif keys[pygame.K_d]:
            self.action = Action.RIGHT
        elif keys[pygame.K_a]:
            self.action = Action.LEFT
        elif keys[pygame.K_s]:
            self.action = Action.DOWN

        elif keys[pygame.K_g]:
            self.tick += 1
        elif keys[pygame.K_f]:
            if self.tick > 0:
                self.tick -= 1
        if keys[pygame.K_SPACE]:
            time.sleep(0.4)
            while True:
                _ = pygame.event.get()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    time.sleep(0.4)
                    break

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

    def get_user_action(self) -> Action:
        return self.action
