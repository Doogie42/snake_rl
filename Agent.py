from State import State
from Snake import SnakeDirection
import pickle
import random
import math


class Agent():
    def __init__(self) -> None:
        self.q_table = {}
        self.q_table = prefill_q_table(self.q_table)
        self.direction = None
        self.learning_rate = 0.001
        self.gamma = 0.5

    def handle_new_state(self, state: State) -> None:
        try:
            _ = self.q_table[state]
        except KeyError:
            self.q_table[state] = [0, 0, 0, 0]

    def update_epsilon(self, current_iter) -> float:
        coef = math.log(current_iter + 1, 10)
        if coef == 0:
            coef = 1
        epsilon = 0.2 / coef
        if epsilon < 0.01:
            epsilon = 0.01
        return epsilon

    def choose_direction(self,
                         state: State,
                         allow_random: bool,
                         current_iter: int) -> SnakeDirection:
        epsilon = self.update_epsilon(current_iter)
        self.handle_new_state(state)
        if allow_random and random.uniform(0, 1) < epsilon:
            arg = random.randrange(0, 4)
        else:
            try:
                arg = self.q_table[state].index(max(self.q_table[state]))
            except KeyError:
                self.q_table[state] = [0, 0, 0, 0]
                arg = random.randrange(0, 4)
        self.direction = SnakeDirection(arg).value
        return SnakeDirection(arg)

    def renforce(self, reward: int,
                 state: State, new_state: State) -> None:
        # Q(s,a) <- Q(s,a) + Alpha*(R+gamma*max Q(s',a') - Q(s,a))
        self.handle_new_state(new_state)
        max_new_state = max(self.q_table[new_state])
        delta = reward + self.gamma * max_new_state
        delta -= self.q_table[state][self.direction]

        self.q_table[state][self.direction] = \
            self.q_table[state][self.direction] + self.learning_rate * delta

    def save(self, file_name: str) -> None:
        with open(file_name, 'wb') as handle:
            pickle.dump(self.q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, file_name: str) -> None:
        with open(file_name, 'rb') as handle:
            self.q_table = pickle.load(handle)


def permutation(s, i, d):
    if i >= len(s):
        return
    permutation(s, i + 1, d)
    if s[i] == "0":
        s[i] = "1"
    else:
        s[i] = "0"
    d[''.join(s)] = [0, 0, 0, 0]
    permutation(s, i + 1, d)
    d[''.join(s)] = [0, 0, 0, 0]


def prefill_q_table(q_table: dict) -> dict:
    s = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
    permutation(s, 0, q_table)
    for key, value in q_table.items():
        if key[0] == "1":
            value[0] = -50
        if key[1] == "1":
            value[1] = -50
        if key[2] == "1":
            value[2] = -50
        if key[3] == "1":
            value[3] = -50
    return q_table
