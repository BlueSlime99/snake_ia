from enum import Enum


class AppleRadar:

    def __init__(self) -> None:
        self.direction = ""
        self.distance = Distance.THREE_AND_MORE

    def update(self, player_position, apple_position):
        self.update_distance(player_position, apple_position)
        self.update_direction(player_position, apple_position)

    def update_distance(self, player_position, apple_position):
        self.distance = abs((apple_position[0] - player_position[0]) + (apple_position[1] - player_position[1]))
        # if dist <= 1:
        #     self.distance = Distance.ONE
        # elif dist <= 2:
        #     self.distance = Distance.TWO
        # else:
        #     self.distance = Distance.THREE_AND_MORE

    def update_direction(self, player_position, apple_position):
        result = ""
        if player_position[1] < apple_position[1]:
            result += "S"
        elif player_position[1] > apple_position[1]:
            result += "N"

        if player_position[0] < apple_position[0]:
            result += "E"
        elif player_position[0] > apple_position[0]:
            result += "W"

        self.direction = result


class Distance(Enum):
    ONE = 1
    TWO = 2
    THREE_AND_MORE = 3
