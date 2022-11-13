import os

import arcade

from agent import Agent
from environment import *

SPRITE_SCALE = 0.33
SPRITE_SIZE = round(128 * SPRITE_SCALE)

FILE_AGENT = 'snakeQtable.data'


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
            = self.state_to_xy(self.__agent.environment.player_position)

        self.__goal = arcade.Sprite(':resources:images/enemies/bee.png', SPRITE_SCALE)
        self.__goal.center_x, self.__goal.center_y \
            = self.state_to_xy(self.__agent.environment.goal)

        self.__sound = arcade.Sound(':resources:sounds/rockHit2.wav')

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.__agent.environment.height - state[0] - 0.5) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__player.draw()
        self.__goal.draw()
        arcade.draw_text(
            f'#{self.__iteration} Score: {self.__agent.score} T°C: {round(self.__agent.temperature * 100, 2)}',
            10, 10,
            arcade.csscolor.WHITE, 20)

    def on_update(self, delta_time):
        if self.__agent.state != self.__agent.environment.goal:
            self.__agent.step()
        else:
            self.__agent.environment.reset_apple()
            self.__goal.center_x, self.__goal.center_y \
                = self.state_to_xy(self.__agent.environment.goal)
            self.__iteration += 1
            # self.__sound.play()

        self.__player.center_x, self.__player.center_y \
            = self.state_to_xy(self.__agent.environment.player_position)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.H:
            self.__agent.heat()


if __name__ == "__main__":
    env = Environment(MAP)
    agent = Agent(env)

    if os.path.exists(FILE_AGENT):
        agent.load(FILE_AGENT)
        # plt.plot(agent.history)
        # plt.show()

    window = MazeWindow(agent)
    window.setup()
    arcade.run()

    agent.save(FILE_AGENT)
