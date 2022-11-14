from enum import Enum


class Threats(Enum):
    SNAKE = "snake"
    APPLE = "apple"
    WALL = "wall"
    NONE = "none"


CHAR_TO_THREAT = {
    " ": Threats.NONE,
    "*": Threats.APPLE,
    ".": Threats.SNAKE,
    "#": Threats.WALL
}


class HeadRadar:

    def __init__(self):
        self.up = Threats.NONE
        self.down = Threats.NONE
        self.left = Threats.NONE
        self.right = Threats.NONE

    def update(self, up, down, left, right):
        self.up = CHAR_TO_THREAT[up]
        self.down = CHAR_TO_THREAT[down]
        self.left = CHAR_TO_THREAT[left]
        self.right = CHAR_TO_THREAT[right]
