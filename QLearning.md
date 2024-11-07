# Q-Learning

Qlearning is a machime learning algorithm that is used to solve reinforcement learning problems. It is a model-free algorithm that learns the optimal policy from interaction with the environment. The agent learns the optimal policy by exploring the environment and updating the Q-values of the state-action pairs.

## Q-Learning Algorithm

The Q-Learning algorithm updates the Q-value, which represents the expected utility of taking a given action in a given state and following the optimal policy thereafter. The update rule for Q-Learning is the Bellman equation:

Q(s, a) = Q(s, a) + lr * [reward + discount * max(Q(s', a')) - Q(s, a)]

Where:
- \( s \) is the current state
- \( a \) is the action taken
- \( r \) is the reward received after taking action \( a \)
- \( s' \) is the next state
- 0 < learning rate (or alpha) < 1 
- 0 < discount factor (or gamma) < 1

We can resume the Q-Learning algorithm in the following steps:
1. Get the current state of the board
2. Choose an action based on the current state
3. Take the action and get the reward
4. Get the new state of the board
5. Update the Q-Table using the Q-Learning update rule

## State

The state is a representation of the board.
In our case the snake only see the 4 directions around it's head.
The state is a tuple of 12 elements:
- 4 elements for an immediate danger in each next cell around the head
- 4 elements for the green apple direction (up, down, left, right) but with the distance to the food
- 4 elements for the red apple direction (up, down, left, right) but with the distance to the food

## Choosing an Action

There is 4 possible actions the snake can take: up, down, left, right.
To choose an action during the training phase, the agent uses an epsilon-greedy policy. With probability epsilon, the agent chooses a random action, and with probability 1-epsilon, the agent chooses the action with the highest Q-value for the current state.
As time passes epsilon decreases, so the agent becomes more likely to choose the action with the highest Q-value.

## Q-Table
The q-table is a dictionary where the key is the Q-State and the value is a list of 4 elements representing the Q-Value of each action.
Example:
```
"State1" : [0.1, 0.2, 0.3, 0.4]
"State2" : [0.5, 0.6, 0.7, 0.8]
...
"SateN" : [0.9, 0.1, 0.2, 0.3]
```
At the start of the training, the Q-Table is empty. Whenever the agent encounters a new state, it adds the state to the Q-Table with Q-Values initialized to 0.
To optimize the Q-Table, we can prefill it with some values. => For example we can fill it with negative values for every danger states.
