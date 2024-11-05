from State import State
from Snake import SnakeDirection


class Agent():
    def __init__(self, q_table: dict) -> None:
        self.q_table = dict

    def choose_direction(self, state: State) -> SnakeDirection:
        return SnakeDirection(1)

    def renforce(self, reward: int,
                 prev_state: State, new_state: State) -> None:
        pass
