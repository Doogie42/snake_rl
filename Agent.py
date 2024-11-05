from State import State
from Snake import SnakeDirection
import pickle
import random
import math


class Agent():
    def __init__(self) -> None:
        self.q_table = {}
        self.direction = None
        self.learning_rate = 0.01
        self.gamma = 0.9

    def choose_direction(self,
                         state: State,
                         no_train: bool,
                         current_iter: int) -> SnakeDirection:
        try:
            _ = self.q_table[state]
        except KeyError:
            self.q_table[state] = [0, 0, 0, 0]
        coef = math.log(current_iter + 1, 10)
        if coef == 0:
            coef = 1
        epsilon = 0.2 / coef
        if epsilon < 0.01:
            epsilon = 0.01
        epsilon = 0.2
        if no_train and random.uniform(0, 1) < epsilon:
            arg = random.randrange(0, 4)
        else:
            arg = self.q_table[state].index(max(self.q_table[state]))
        self.direction = SnakeDirection(arg).value
        return SnakeDirection(arg)

    def renforce(self, reward: int,
                 state: State, new_state: State) -> None:

        # Q(s,a) <- Q(s,a) + Alpha*(R+gamma*max Q(s',a') - Q(s,a))
        try:
            _ = self.q_table[new_state]
        except KeyError:
            self.q_table[new_state] = [0, 0, 0, 0]
        max_new_state = max(self.q_table[new_state])
        # no idea how to make it pretty
        self.q_table[state][self.direction] = \
            self.q_table[state][self.direction] +\
            self.learning_rate *\
            (reward + self.gamma * max_new_state -
             self.q_table[state][self.direction])

    def save(self, file_name: str) -> None:
        with open(file_name, 'wb') as handle:
            pickle.dump(self.q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, file_name: str) -> None:
        with open(file_name, 'rb') as handle:
            self.q_table = pickle.load(handle)
