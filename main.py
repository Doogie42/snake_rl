import argparse
from Snake import Snake, GameState
from Graphic import Graphic
from State import State
from Agent import Agent
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", type=int, help="train", nargs="?", const=1000)
    parser.add_argument(
        "-g", help="graphic mode", action='store_true')
    parser.add_argument(
        "-f", help="file to save", type=str)
    parser.add_argument(
        "-l", help="file to load", type=str)
    parser.add_argument(
        "-no-train", help="no-train", action='store_true')
    args = parser.parse_args()
    snake = Snake()
    agent = Agent()
    if args.l:
        agent.load(args.l)
    reward_val = {
        GameState.ALIVE: -1,
        GameState.DEAD: -50,
        GameState.GREEN: 20,
        GameState.RED: -20
    }
    if args.g:
        graphic = Graphic(tick=10)
    for i in tqdm(range(args.t)):
        while True:
            if args.g:
                graphic.render(snake)
            state = State(snake)
            direction = agent.choose_direction(state,
                                               no_train=not args.no_train,
                                               current_iter=i)
            game_state = snake.move(direction)
            new_state = State(snake)
            agent.renforce(reward_val[game_state], state, new_state)
            if game_state == GameState.DEAD:
                snake = Snake()
                break
    if args.f:
        agent.save(args.f)


if __name__ == "__main__":
    main()
