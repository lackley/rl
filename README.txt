RL- reinforcement learning readme

Implementation of Q-learning and Rmax algorithm on two worlds.

To run:
python game.py {Q or R} -world {stan or frank}

Flags you can set:
-level <x.lev>: sets the level for Stan to play. (e.g. -level 2.lev runs the 2.lev level) (default=1.lev)
-eps <value>: sets value for epsilon (default=.01)
-m <value>: sets number of visits to a state before Rmax begins learning
(default=2)
-iters : sets number of actions taken in a run (default=10000)
-nographics: runs code without displaying graphics
-silent: doesn't print stats during the run

Explanation of worlds:

Stan's world can be modeled as a Markov Decision Process. It has four types of grid squares: solid ground (black square), trapdoor (green square), air (white square), ladder (blue rectangle), start, and end of tunnel (purple rectangle). Each time Stan steps on a trapdoor, with some probability it acts as air. Otherwise it acts as solid ground.
Stan can take the five actions: left, right, jump left, jump right, and climb up. Each time Stan gets to the end of the tunnel, he gets some large positive reward. Then he finds himself back at the start square. Every other step is penalized and incurs a small negative reward.

Frank's problem of how to program Curiosity (based on the inverted pendulum problem) can also be modeled as an MDP. However, unlike Stan, Frank lives in a continuous world where the states are defined by both the position and velocity of both Curiosity and the pole (four values per state). In order to model a continuous world with an MDP the state space needs to be discretized. A state consists of four values: cart location, cart velocity, pole angle and pole velocity. Because this is a continuous space, each of these values is represented by a bin, not the true value. For example, the MDP cannot tell the difference between cart location .01 and .02 as they are both placed in the same bin.  Curiosity has two actions, "left" or "right".

Both algorithms work by calling update on the current state, action take, reward received, and resultant state. Next the get_action method is called to get the next action that the agent should take. 

