import numpy as np 

#code adapted from:
#https://www.upgrad.com/blog/markov-chain-in-python-tutorial/

class MarkovChain():
    def __init__(self, transition_prob):
        """
        Initialize MarkovChain objecct

        Parameters:
        transition_prob (dict): A dict object representing transition
        probabilities in Markov Chain.
        Example:
            {state1: {state1:0.1, state2:0.9},
            {state2: {...}}
        """

        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())

    def next_state(self, current_state):
        """
        Returns state an next position based on transition probabilities.

        Parameters:
        current_state (int): label at current position.
        """

        return np.random.choice(
                                self.states,
                                p=[self.transition_prob[current_state][next_state]
                                    for next_state in self.states]
                                )

    def generate_states(self, len=10):
        """
        Generates a sequence of states of length len.

        Parameters:
        len (int): The number of states in returned sequence.

        Returns:
        states (ndarray): 1D array containing data of 'int' type.
        """
        states = []
        current_state = np.random.choice(self.states) 
        for i in range(len):
            next_state = self.next_state(current_state)
            states.append(next_state)
            current_state = next_state
        
        return np.array(states)


                            
