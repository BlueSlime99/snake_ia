import pickle

from environment import *
from state import State


class Agent:
    def __init__(self, env, alpha=1, gamma=0.9, cooling_rate=0.999):
        self.__qtable = {}
        self.__env = env
        self.__alpha = alpha
        self.__gamma = gamma
        self.__history = []
        self.__cooling_rate = cooling_rate
        self.reset(False)

    def reset(self, store_history=True):
        if store_history:
            self.__history.append(self.__score)
        self.__state = State()
        self.__env.update_state(self.__state, self.__env.snake.get_head_position())
        self.__score = 0
        self.__temperature = 0

    def heat(self):
        self.__temperature = 1

    def best_action(self):
        if random.random() < self.__temperature:
            self.__temperature *= self.__cooling_rate
            return random.choice(ACTIONS)
        else:
            q = self.get_or_create(self.__qtable, self.__state)
            return max(q, key=q.get)

    def get_or_create(self, q_table, state):
        json_state = state.tojson()
        if json_state not in q_table:
            q_table[json_state] = {}
            for action in ACTIONS:
                q_table[json_state][action] = 0.0

        return q_table[json_state]

    def step(self):
        action = self.best_action()
        new_state, reward = self.__env.do(action)

        new_state_actions = self.get_or_create(self.__qtable, new_state)
        maxQ = max(new_state_actions.values())
        delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.__state.tojson()][action])
        self.__qtable[self.__state.tojson()][action] += delta

        self.__state = new_state
        self.__score += reward
        return action, reward

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable, self.__history = pickle.load(file)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def environment(self):
        return self.__env

    @property
    def history(self):
        return self.__history

    @property
    def temperature(self):
        return self.__temperature
