from Snake import Snake, GameState, SnakeDirection
from Graphic import Graphic, Action
import random


def main():
    random.seed()
    graphic = Graphic(tick=10)
    snake = Snake(board_height=20, board_width=20)
    game_number = 0
    duration = 0
    while True:
        direction = snake.direction
        game_state = snake.move(direction)

        action = graphic.get_user_action()
        if action == Action.QUIT:
            break
        if action == Action.RESTART:
            break
        if action == Action.LEFT:
            snake.direction = SnakeDirection(0)
        if action == Action.TOP:
            snake.direction = SnakeDirection(1)
        if action == Action.DOWN:
            snake.direction = SnakeDirection(2)
        if action == Action.RIGHT:
            snake.direction = SnakeDirection(3)

        graphic.render(snake, game_number, snake.get_score(), duration, {}, 0)
        if game_state == GameState.DEAD:
            snake = Snake(board_height=20, board_width=20)
            duration = 0
            game_number += 1
            continue
    graphic.clean_up()


if __name__ == "__main__":
    main()
