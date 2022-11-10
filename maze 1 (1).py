import arcade
import os
import pickle
import time
import matplotlib.pyplot as plt

from random import *

MAZE = """
#.##############
#     #        #
###   #   #    #
#     #   #    #
#         #    #
#  #####  #    #
#      #  #    #
#      #  #    #
#         #    #
########  #    #
#         #    #
##############*#
"""

MAP_WALL = '#'
MAP_START = '.'
MAP_GOAL = '*'

REWARD_DEFAULT = -1

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'

ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

ACTION_MOVE = {ACTION_UP : (-1, 0),
               ACTION_DOWN : (1, 0),
               ACTION_LEFT : (0, -1),
               ACTION_RIGHT : (0, 1)}

SPRITE_SCALE = 0.33
SPRITE_SIZE = round(128 * SPRITE_SCALE)

FILE_AGENT = 'agent.al1'

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

class Agent:
    def __init__(self, env, alpha = 1, gamma = 0.8, cooling_rate = 0.999):
        self.__qtable = {}
        for state in env.states:
            self.__qtable[state] = {}
            for action in ACTIONS:
                self.__qtable[state][action] = 0.0
        
        self.__env = env
        self.__alpha = alpha
        self.__gamma = gamma
        self.__history = []
        self.__cooling_rate = cooling_rate
        self.reset(False)

    def reset(self, store_history = True):
        if store_history:
            self.__history.append(self.__score)
        self.__state = env.start
        self.__score = 0
        self.__temperature = 0

    def heat(self):
        self.__temperature = 1

    def best_action(self):
        if random() < self.__temperature:
            self.__temperature *= self.__cooling_rate
            return choice(ACTIONS)
        else:
            q = self.__qtable[self.__state]
            return max(q, key = q.get)

    def step(self):
        action = self.best_action()
        state, reward = self.__env.do(self.__state, action)
        
        maxQ = max(self.__qtable[state].values())
        delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.__state][action])
        self.__qtable[self.__state][action] += delta
        
        self.__state = state
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

    def __repr__(self):
        res = f'Agent {agent.state}\n'
        res += str(self.__qtable)
        return res

class MazeWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(SPRITE_SIZE * agent.environment.width,
                         SPRITE_SIZE * agent.environment.height, "Sortie d'urgence")

        self.__agent = agent
        self.__iteration = 0

    def setup(self):
        self.__walls = arcade.SpriteList()
        for state in filter(self.__agent.environment.is_wall,
                            self.__agent.environment.states):
            sprite = arcade.Sprite(':resources:images/tiles/boxCrate.png', SPRITE_SCALE)
            sprite.center_x, sprite.center_y = self.state_to_xy(state)
            self.__walls.append(sprite)

        self.__player = arcade.Sprite(':resources:images/enemies/wormPink.png', SPRITE_SCALE)
        self.__player.center_x, self.__player.center_y \
                                = self.state_to_xy(self.__agent.state)

        self.__goal = arcade.Sprite(':resources:images/enemies/bee.png', SPRITE_SCALE)
        self.__goal.center_x, self.__goal.center_y \
                                = self.state_to_xy(self.__agent.environment.goal)

        self.__sound = arcade.Sound(':resources:sounds/rockHit2.wav')
        
    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE,\
               (self.__agent.environment.height - state[0] - 0.5) * SPRITE_SIZE
    
    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__player.draw()
        self.__goal.draw()
        arcade.draw_text(f'#{self.__iteration} Score: {self.__agent.score} T°C: {round(self.__agent.temperature * 100, 2)}',
                         10, 10,
                         arcade.csscolor.WHITE, 20)

    def on_update(self, delta_time):
        if self.__agent.state != self.__agent.environment.goal:
            self.__agent.step()
        else:
            self.__agent.reset()
            self.__iteration += 1
            #self.__sound.play()
        
        self.__player.center_x, self.__player.center_y \
                                = self.state_to_xy(self.__agent.state)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.H:
            self.__agent.heat()

if __name__ == "__main__":
    env = Environment(MAZE)
    agent = Agent(env)

    if os.path.exists(FILE_AGENT):
        agent.load(FILE_AGENT)
        #plt.plot(agent.history)
        #plt.show()

    window = MazeWindow(agent)
    window.setup()
    arcade.run()

    agent.save(FILE_AGENT)
