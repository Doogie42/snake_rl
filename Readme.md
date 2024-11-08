# Snake RL
This is a simple snake game that uses reinforcement learning to play the game. The game is built using the Pygame library and the reinforcement learning is done using a Qlearning algorithm and a Qtable.

# Installation
```
git clone git@github.com:Doogie42/snake_rl.git
#python -m venv venv # optional
#source venv/bin/activate # optional
pip install -r requirements.txt
```

# Usage
To train the snake run the following command:
```
python main.py
```
Options for training:
```
-t: specify the number of training episodes
-f: save the Qtable to a file
-l: load the Qtable from a file
-g: display the game while training
-size: specify the size of the game default is 10*10 grid, minimum is 6*6
-prefill: prefills the Qtable with a value to teach the snake to avoid dying
```

To test a model without training add the `no-train` flag:
```
python main.py -no-train -l <model> -g
```

# Example
```
# train the snake for 10000 episodes and save the model to agent/model.mdl
python main.py -t 10000 -f agent/model.mdl
```
```
# Test the model:
python main.py -no-train -l agent/model.mdl -g
```
You can also play the game yourself by running the following command and using wasd to move the snake:
```
python play_main.py
```


