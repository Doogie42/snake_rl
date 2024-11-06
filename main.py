import argparse
from Snake import Snake, GameState
from Graphic import Graphic, Action
from State import State
from Agent import Agent
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
import numpy as np


def main():
    random.seed(12)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", type=int, help="train", nargs="?", const=1000, default=1000)
    parser.add_argument(
        "-g", help="graphic mode", action='store_true')
    parser.add_argument(
        "-f", help="file to save", type=str)
    parser.add_argument(
        "-l", help="file to load", type=str)
    parser.add_argument(
        "-no-train", help="no-train", action="store_true")
    parser.add_argument(
        "-size", type=int,
        help="size of square", nargs="?",
        const=10, default=10)
    parser.add_argument(
        "-prefill", help="prefill q_table with custom value",
        action="store_true")
    args = parser.parse_args()

    reward_val = {
        GameState.ALIVE: -1,
        GameState.DEAD: -50,
        GameState.GREEN: 20,
        GameState.RED: -20
    }
    agent = Agent(prefill=args.prefill)
    score_history = []
    duration_history = []
    green_apple_eaten = []
    red_apple_eaten = []
    state_history = []
    running = True

    if args.l:
        agent.load(args.l)
    if args.g:
        graphic = Graphic(tick=21)
    latest_apple_eaten = 0
    for i in tqdm(range(args.t), disable=args.g):
        if not running:
            break
        snake = Snake(board_height=args.size, board_width=args.size)
        latest_apple_eaten = 0

        while True:
            state = State(snake).normalize()
            direction = agent.choose_direction(state,
                                               allow_random=not args.no_train,
                                               current_iter=i)
            game_state = snake.move(direction)
            new_state = State(snake).normalize()
            if not args.no_train:
                agent.renforce(reward_val[game_state], state, new_state)

            if args.g:
                graphic.render(snake, i,
                               snake.get_score(), snake.get_duration(),
                               agent.q_table, state)
                action = graphic.get_user_action()
                if action == Action.QUIT:
                    running = False
                    break
                if action == Action.RESTART:
                    break

            latest_apple_eaten += 1
            if game_state == GameState.RED or game_state == GameState.GREEN:
                latest_apple_eaten = 0
            if args.no_train and latest_apple_eaten > 200:
                game_state = GameState.DEAD
                latest_apple_eaten = 0

            if game_state == GameState.DEAD:
                score_history.append(snake.get_score())
                duration_history.append(snake.get_duration())
                green_apple_eaten.append(snake.get_green_apple_eaten())
                red_apple_eaten.append(snake.get_red_apple_eaten())
                if not args.prefill:
                    state_history.append(len(agent.q_table.keys()))
                latest_apple_eaten = 0
                break

    if args.f:
        agent.save(args.f)

    if args.g:
        graphic.clean_up()

    plt.subplot(3, 2, 1)
    plt.title("rolling score average")
    plt.plot(moving_average(score_history))
    plt.subplot(3, 2, 2)
    plt.plot(moving_average(duration_history))
    plt.title("rolling duration average")

    plt.subplot(3, 2, 3)
    plt.plot(moving_average(green_apple_eaten))
    plt.title("rolling green apple eaten average")
    plt.subplot(3, 2, 4)
    plt.plot(moving_average(red_apple_eaten))
    plt.title("rolling red apple eaten average")

    plt.subplot(3, 2, 5)
    plt.plot(state_history)
    plt.title("state discovery")
    plt.show()
    print(f"max score = {max(score_history)}")

    print(f"average score = {np.mean(score_history)}")


def moving_average(value: list, k=100):
    current_sum = 0
    average = []
    index = 0
    for val in value:
        current_sum += val
        if index > k:
            current_sum -= value[index - k]
            average.append(current_sum / k)
        else:
            average.append(current_sum / (index + 1))

        index += 1
    return average


if __name__ == "__main__":
    main()
