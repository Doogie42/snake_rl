import argparse
from Snake import Snake, GameState
from Graphic import Graphic, Action
from State import State
from Agent import Agent
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
import numpy as np
import Config
from argparse import RawTextHelpFormatter


def show_vision(state: State):
    print(f"state :{state}")
    state.dump()


def main():
    random.seed(12)
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-t", type=int, help="number of training sessions", nargs="?",
        const=Config.DEFAULT_LEN, default=Config.DEFAULT_LEN)
    parser.add_argument(
        "-g", help="graphic mode\n" +
        "AVAILABLE COMMAND:\n" +
        "\tf: slow fps\n" +
        "\tg: speed up fps\n" +
        "\tspace: pause/continue",
        action='store_true')
    parser.add_argument(
        "-f", help="file to save", type=str)
    parser.add_argument(
        "-l", help="file to load", type=str)
    parser.add_argument(
        "-no-train", help="don't train the model, useful for testing models",
        action="store_true")
    parser.add_argument(
        "-size", type=int,
        help="size of snake square", nargs="?",
        const=Config.DEFAULT_SIZE, default=Config.DEFAULT_SIZE)
    parser.add_argument(
        "-prefill", help="prefill q_table with proper value to avoid death",
        action="store_true")
    parser.add_argument(
        "-show-vision", help="show snake vision in terminal",
        action="store_true")
    parser.add_argument(
        "-step",
        help="wait for user input before moving",
        action="store_true")
    args = parser.parse_args()
    if args.size:
        assert args.size > 6, "map need to be at leat 7 square wide (big value will result in weird graphical game)"
    reward_val = {
        GameState.ALIVE: -1,
        GameState.DEAD: -50,
        GameState.GREEN: 20,
        GameState.RED: -20
    }
    agent = Agent(prefill=args.prefill, reward_val=reward_val)
    score_history = []
    duration_history = []
    green_apple_eaten = []
    red_apple_eaten = []
    state_history = []
    running = True

    if args.l:
        agent.load(args.l)
    if args.g:
        graphic = Graphic(tick=Config.DEFAULT_TICK)
    latest_apple_eaten = 0
    for i in tqdm(range(args.t), disable=(args.g or
                                          args.show_vision or
                                          args.step)):
        if not running:
            break
        snake = Snake(board_height=args.size, board_width=args.size)
        latest_apple_eaten = 0

        while True:
            state = State(snake)
            direction = agent.choose_direction(state,
                                               allow_random=not args.no_train)
            game_state = snake.move(direction)
            new_state = State(snake)
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
            if args.show_vision:
                show_vision(new_state)

            latest_apple_eaten += 1
            if game_state == GameState.RED or game_state == GameState.GREEN:
                latest_apple_eaten = 0
            if args.no_train and latest_apple_eaten >\
                    Config.DURATION_KILL_NO_FOOD_EATEN:
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
            if args.step:
                if args.g:
                    graphic.wait_input()
                else:
                    _ = input()

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
    print(f"max score = {max(score_history)} ",
          f"average score = {np.mean(score_history):.2f}")
    print(f"max duration = {max(duration_history)} ",
          f"average duration = {np.mean(duration_history):.2f}")


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
