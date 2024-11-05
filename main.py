import argparse
from Snake import Snake, GameState
from Graphic import Graphic
from State import State
from Agent import Agent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", type=int, help="train", nargs="?", const=1000)
    parser.add_argument(
        "-g", help="graphic mode", action='store_true')
    parser.add_argument(
        "-f", help="file to save", type=str)
    parser.add_argument(
        "-no-learn", help="no-learn", action='store_true')
    args = parser.parse_args()
    snake = Snake()
    agent = Agent(None)
    reward_val = {
        GameState.ALIVE: -1,
        GameState.DEAD: -100,
        GameState.GREEN: 30,
        GameState.RED: -30
    }
    if args.g:
        graphic = Graphic(tick=10)
    while True:
        if args.g:
            graphic.render(snake)
        state = State(snake)
        direction = agent.choose_direction(state)
        game_state = snake.move(direction)
        new_state = State(snake)
        agent.renforce(reward_val[game_state], state, new_state)
        if game_state == GameState.DEAD:
            snake = Snake()
            continue


if __name__ == "__main__":
    main()
