# TD3 applied to the Bittle robot in Isaac Sim

Attempting to train the Bittle robot dog to walk with reinforcement learning.
Current model performance:
<img src="./bittlebots.gif" height="500">

**Forked TD3 benchmarking with a few files added:**

These files are modified to work with the Isaac Sim env for the Bittle robot. More info on all of this can be found on the videos that cover my attempts here:
1. Can we simulate a real robot?: https://www.youtube.com/watch?v=phTnbmXM06g


There are probably mistakes/errors/redundant/useless bits of code, I am just sharing where I am so far JIC anyone wishes to try their hand :P PRs welcome. 

To actually run, you need to use the Omni version of Python. You can either do this via shebang at the top or by placing my 2 edited files in the omniverse directory. For example, my files are located in here: `/home/h/.local/share/ov/pkg/isaac_sim-2021.1.1/TD3-Bittle-9/`

1. `TD3-Bittle-16-1.py` This is the main training file. 
2. `TD3_4.py` This is the modified version of the TD3 model. Just a larger model.
3. `Models` directory, this contains the best TD3 model so far. You can run it, or attempt to train from here.
4. `20-Bittles-very-long-6.usd` One version of a scene that's used to play the model. Feel free to make your own from here in the sim. Should be located in the `Isaac` directory of the omniverse directory.
5. `20-Bittles-very-long.usd` Used for training, mostly so Bittles don't run into eachother in training. There's a way to make them clip eachother, I just don't know it ATM. Should be located in the `Isaac` directory of the omniverse directory.
6. `Play-TD3-Bittle-MANY.py` This is used to play models, essentially just keep exploiting.
7. `graph_reward.py` Used to graph the rewards of the exploration and exploiting agents live while training.

