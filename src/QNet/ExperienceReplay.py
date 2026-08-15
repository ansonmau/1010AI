import random 
from collections import deque

class ExperienceReplay:
    def __init__(self, replay_size):
        self._buffer = deque(maxlen=replay_size)
        self._size = replay_size

    def save(self, state, action, reward, next_state, can_play):
        self._buffer.append((state, action, reward, next_state, can_play))
    
    def sample(self, n_samples):
        batch = random.sample(self._buffer, n_samples)

        # batch = [(s1,r1,ns1,cp1), (s2,r2,ns2,cp2), ...]
        # want to return (s1,s2,...), (r1,r2,...), ...
        states, actions, rewards, next_states, can_plays = zip(*batch)

        return states, actions, rewards, next_states, can_plays

    def get_size(self):
        return len(self._buffer)
