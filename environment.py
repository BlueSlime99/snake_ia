

import random
from assets.maps import *


ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'

ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVE = {ACTION_UP : (-1, 0),
               ACTION_DOWN : (1, 0),
               ACTION_LEFT : (0, -1),
               ACTION_RIGHT : (0, 1)}
REWARD_DEFAULT = -1


class Environment:
    def __init__(self, str_map):
        row = 0
        col = 0
        self.__states = {}
        str_map = str_map.strip()
        for line in str_map.strip().split('\n'):
            for item in line:
                self.__states[row, col] = item
                if item == MAP_GOAL:
                    self.__goal = (row, col)
                elif item == MAP_START:
                    self.__start = (row, col)
                col += 1
            row += 1
            col = 0

        self.__rows = row
        self.__cols = len(line)

        self.__reward_goal = len(self.__states)
        self.__reward_wall = -2 * self.__reward_goal

    def do(self, state, action):
        move = ACTION_MOVE[action]
        new_state = (state[0] + move[0], state[1] + move[1])

        if new_state not in self.__states \
           or self.__states[new_state] in [MAP_WALL, MAP_START]:
            reward = self.__reward_wall
        else:
            state = new_state
            if new_state == self.__goal:
                reward = self.__reward_goal
            else:
                reward = REWARD_DEFAULT

        return state, reward

    @property
    def states(self):
        return list(self.__states.keys())

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal


    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

    def is_wall(self, state):
        return self.__states[state] == MAP_WALL

    def print(self, agent):
        res = ''
        for row in range(self.__rows):
            for col in range(self.__cols):
                state = (row, col)
                if state == agent.state:
                    res += 'A'
                else:
                    res += self.__states[(row, col)]
                
            res += '\n'
        print(res)              

    def reset_apple(self):
          x = random.randint(1, self.__rows -2)
          y = random.randint(1, self.__cols -2)

          self.__goal = (x,y)
