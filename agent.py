from __future__ import division # makes 1/2 equal float 0.5 and not integer 0
import random
from collections import defaultdict
import copy


class Qlearner:
    """ The QLearner agent.
    Attributes:
        alpha:      learning rate
        gamma:      future rate discount
        actions:    actions available to the agent (a list of general "action" objects)
        epsilon:    exploration parameter
    """

    def __init__(self, alpha, gamma, actions, epsilon):
        """ Inits Qlearner agent with parameters
        Args:
            alpha, gamma, epsilon:  see above
            actions:                actions available to the agent (a list of general actions)
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = actions
        # TODO
        # you may add structures here as necessary
        self.Q = {} #empty dictionary storing Q values for actions and states

    def update(self, s, a, r, s_):
        """ Updates the agent's knowledge.
        Args:
            s:  previous state (general "state")
            a:  action taken (general action)
            r:  reward received
            s_: resultant state
        """
        # TODO
        # does not return anything

        #find max Q value for s_
        q = []
        for a_ in self.actions:
            if (s_,a_) in self.Q:
                q.append(self.Q[s_,a_])
            else:
                q.append(0)
        max_Q = max(q)

        #update the Q value at (s,a)
        if (s,a) in self.Q:
            self.Q[(s,a)] = (1-self.alpha)*self.Q[(s,a)] + self.alpha*(r + self.gamma*max_Q)
        else:
            self.Q[(s,a)] = 0


    
    def get_action(self, s):
        """ Gets the best action based on the agent's knowledge and algorithm.

        Breaks ties randomly.
        
        Args:
            s:  current state
        """
        # TODO 
        # returns an action (default actions must be randomized)
        q = []
        for a in self.actions:
            if (s,a) in self.Q:
                q.append(self.Q[s,a])
            else:
                q.append(0)

        best_Q = max(q)

        if random.random() < self.epsilon:
            all_list = [i for i in range(len(self.actions))]
            selected_action_index = random.choice(all_list)
        else:
            max_list = [i for i in range(len(self.actions)) if q[i] == best_Q]
            selected_action_index = random.choice(max_list)


        return self.actions[selected_action_index]


    
    def get_Q_val(s, a):
        """ Gets the Q value of a given state and action if it is in dictionary. 
            Initialiezs it to 0 and adds it to dictionary if it is not already existing.

            Args:
                s: state
                a: action 
        """
        if (s,a) in self.Q:
            return self.Q[(s,a)]
        else:
            self.Q[(s,a)] = 0
            return 0


class Rmax:
    """ The Rmax agent.
    Attributes:
        rmax:       reward for going to or from the absorbing state
        gamma:      future rate discount
        m:          number of times a (state, action) pair needs to be attempted before it
                    computes a reward other than rmax
        actions:    actions available to the agent (a list of actions)
        s_r:        absorbing state
    """

    def __init__(self, rmax, gamma, m, actions):
        """ Inits Rmax agent with parameters.
        Args:
            rmax, gamma,m, actions: see above
        """
        self.rmax = rmax
        self.gamma = gamma
        self.m = m
        self.actions = actions
        self.s_r = "absorbing state"
        # TODO
        self.c = {} #dict of key=(s,a) val = num times (s,a) has been visited
        self.rsum = {} #dict of key = (s,a) val=accumulated rewards
        self.r = {} #dict of key = (s,a) val = reward
        self.T = {} #dict of key = (s,a,s') val = transistion probability
        self.cs = {} #dict of key=(s,a,s') val=number of times agent reached s' from s taking action a
        self.V = {} #dict of key=s val= (value at state s, action that got you there
        for a in actions:
            self.r[(self.s_r, a)] = rmax
            self.T[(self.s_r,a, self.s_r)] = 1
    
    

    def update(self, s, a, r, s_):
        """ Updates the agent's knowledge.
        Args:
            s:  previous state
            a:  action taken
            r:  reward received
            s_: resultant state
        """
        # TODO
        # does not return anything
        
        #increment number of times (s,a) has been visited
        if (s,a) in self.c:
            self.c[(s,a)] = self.c[(s,a)]+1
        else:
            self.c[(s,a)] = 1
        
        #update the reward at (s,a)
        if (s,a) in self.rsum:
            self.rsum[(s,a)] = self.rsum[(s,a)] + r
        else:
            self.rsum[(s,a)] = r
                
        #increment number of times agent reached s' from s taking action a
        if (s,a,s_) in self.cs:
            self.cs[(s,a,s_)] = self.cs[(s,a,s_)] + 1
        else:
            self.cs[(s,a,s_)] = 1
        
        if (s,a) in self.r:
            old_r = self.r[(s,a)]
        else:
            self.r[(s,a)] = 0
            old_r = 0
        if (s,a,s_) in self.T:
            old_T = self.T[(s,a,s_)]
        else:
            self.T[(s,a,s_)] = 0
            old_T = 0


        


#loop1 while none of the values changed more than 1/rmax
#loop2 loop over all thes states in v
#loop3 loop over all the actions

        #if you are on the mth iteration or 1st iteration
        # or (s,a) takes you to a state that you've never been to before
        # then you should run value itration
        if (self.c[(s,a)] < self.m):
            self.r[(s,a)] = self.rmax
            self.T[(s,a,self.s_r)] = 1

            self.V[s] = ((self.rmax / (1-self.gamma)), a)

        else:
            self.r[(s,a)] = self.rsum[(s,a)]/float(self.c[(s,a)])
            for state in self.V:
                if (s,a,state) in self.cs:
                    self.T[(s,a,state)] = self.cs[(s,a,state)]/float(self.c[(s,a)])
                else:
                    self.T[(s,a,state)] = 0

       


        if self.c[(s,a)] >= self.m:
            still_looping = True
            while still_looping:
                none_changed = True
                last_copy = copy.deepcopy(self.V)
                
                for state in self.V:
                    max_val = -99999999
                    max_actions = []
                    for action in self.actions:
                        if (state, action) in self.r:
                            v_s = self.r[(state,action)]
                        else:
                            v_s = 0
                        sum_term = 0
                        for (state_, (v0, a1)) in self.V.iteritems():
                            if (state, action, state_) in self.T:
                                sum_term += self.T[(state, action, state_)] * v0
                        sum_term = sum_term*self.gamma
                        v_s += sum_term
                        if v_s == max_val:
                            max_val = v_s
                            max_actions.append(action)
                        if v_s > max_val:
                            max_actions = [action]
                            max_val = v_s
                    max_action = random.choice(max_actions)
                    self.V[state] = (max_val, max_action)

                    if state in last_copy:
                        #if all the values are less than 1/rmax quit looping 
                        if (abs ((last_copy[state])[0] - max_val)) > 1/float(self.rmax):
                             none_changed = False
                    else:
                        none_changed = False

            
                still_looping = not none_changed
                
                




    

    def get_action(self, s):
        """ Gets the best action based on the agent's knowledge and algorithm.
        
        Returns whatever action has the highest reward associated with it.
        
        Breaks ties randomly.

        Args:
            s:  current state
        """
        # TODO
        # returns an action (default actions must be randomized)
        if s in self.V:
            return (self.V[s])[1]
        else:
            return random.choice(self.actions)


