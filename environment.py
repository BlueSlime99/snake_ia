import random

from assets.maps import *
from state import State

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'

ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVE = {ACTION_UP: (-1, 0),
               ACTION_DOWN: (1, 0),
               ACTION_LEFT: (0, -1),
               ACTION_RIGHT: (0, 1)}
REWARD_DEFAULT = -1


class Environment:
    def __init__(self, str_map):
        row = 0
        col = 0
        self.player_positions = {}
        self.__positions = {}
        str_map = str_map.strip()
        for line in str_map.strip().split('\n'):
            for item in line:
                self.__positions[row, col] = item
                if item == MAP_GOAL:
                    self.__apple_position = (row, col)
                elif item == MAP_PLAYER:
                    self.__start = (row, col)
                    self.player_position = self.__start
                    self.player_positions[row, col] = self.__start
                col += 1
            row += 1
            col = 0

        self.__rows = row
        self.__cols = len(line)

        self.__reward_goal = len(self.__positions)
        self.__reward_wall = -2 * self.__reward_goal

    def do(self, action):
        new_state = State()
        move = ACTION_MOVE[action]
        new_player_position = (self.player_position[0] + move[0], self.player_position[1] + move[1])

        if new_player_position not in self.__positions \
                or self.__positions[new_player_position] == MAP_WALL:
            reward = self.__reward_wall
            self.update_state(new_state, self.player_position)


        else:
            self.__positions[self.player_position] = MAP_NOTHING
            self.__positions[new_player_position] = MAP_PLAYER
            self.player_position = new_player_position
            self.update_state(new_state, new_player_position)
            if new_player_position == self.__apple_position:
                reward = self.__reward_goal
            else:
                reward = REWARD_DEFAULT

        return new_state, reward

    def update_state(self, state: State, new_player_position):
        up = (new_player_position[0] + ACTION_MOVE[ACTION_UP][0], new_player_position[1] + ACTION_MOVE[ACTION_UP][1])
        down = (
            new_player_position[0] + ACTION_MOVE[ACTION_DOWN][0], new_player_position[1] + ACTION_MOVE[ACTION_DOWN][1])
        left = (
            new_player_position[0] + ACTION_MOVE[ACTION_LEFT][0], new_player_position[1] + ACTION_MOVE[ACTION_LEFT][1])
        right = (
            new_player_position[0] + ACTION_MOVE[ACTION_RIGHT][0],
            new_player_position[1] + ACTION_MOVE[ACTION_RIGHT][1])

        state.headRadar.update(self.__positions[up], self.__positions[down], self.__positions[left],
                               self.__positions[right])
        state.appleRadar.update(new_player_position, self.__apple_position)

    @property
    def states(self):
        return list(self.__positions.keys())

    @property
    def start(self):
        return self.__start

    @property
    def apple_position(self):
        return self.__apple_position

    @property
    def height(self):
        return self.__rows

    @property
    def width(self):
        return self.__cols

    def is_wall(self, state):
        return self.__positions[state] == MAP_WALL


    def goal_reached(self):
        self.reset_apple()
        self.grow_snake()

    def grow_snake(self):
        pass

    def reset_apple(self):
        x = random.randint(1, self.__rows - 2)
        y = random.randint(1, self.__cols - 2)

        self.__positions[self.__apple_position] = MAP_NOTHING
        self.__apple_position = (x, y)
        self.__positions[self.__apple_position] = MAP_GOAL
