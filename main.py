import argparse
from Snake import Snake, GameState
from Graphic import Graphic, Action
from State import State
from Agent import Agent
from tqdm import tqdm
import matplotlib.pyplot as plt
import random


def main():
    random.seed(12)
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

    reward_val = {
        GameState.ALIVE: -1,
        GameState.DEAD: -50,
        GameState.GREEN: 20,
        GameState.RED: -20
    }
    agent = Agent()
    score_history = []
    duration_history = []
    green_apple_eaten = []
    red_apple_eaten = []
    running = True

    if args.l:
        agent.load(args.l)
    if args.g:
        graphic = Graphic(tick=21)

    for i in tqdm(range(args.t), disable=args.g):
        if not running:
            break
        snake = Snake()
        while True:
            state = State(snake).normalize()
            direction = agent.choose_direction(state,
                                               allow_random=False,
                                               current_iter=i)
            game_state = snake.move(direction)
            new_state = State(snake).normalize()
            agent.renforce(reward_val[game_state], state, new_state)

            if args.g:
                graphic.render(snake, agent.q_table[state], state)
                action = graphic.get_user_action()
                if action == Action.QUIT:
                    running = False
                    break
                if action == Action.RESTART:
                    break

            if game_state == GameState.DEAD:
                score_history.append(snake.get_score())
                duration_history.append(snake.get_duration())
                green_apple_eaten.append(snake.get_green_apple_eaten())
                red_apple_eaten.append(snake.get_red_apple_eaten())
                break

    if args.f:
        agent.save(args.f)

    if args.g:
        graphic.clean_up()

    plt.subplot(2, 2, 1)
    plt.title("Score average")
    plt.plot(moving_average(score_history))
    plt.subplot(2, 2, 2)

    plt.plot(moving_average(duration_history))
    plt.title("Duration average")
    plt.subplot(2, 2, 3)
    plt.plot(moving_average(green_apple_eaten))
    plt.title("Green apple eaten")
    plt.subplot(2, 2, 4)
    plt.plot(moving_average(red_apple_eaten))
    plt.title("red apple eaten")

    plt.show()

    print(len(agent.q_table))


def moving_average(value: list):
    current_sum = 0
    average = []
    index = 0
    for val in value:
        current_sum += val
        average.append(current_sum / (index + 1))
        index += 1
    return average


if __name__ == "__main__":
    main()
