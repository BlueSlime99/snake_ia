from enum import Enum


class AppleRadar:

    def __init__(self) -> None:

        self.direction = Direction #Enum
        self.distance = Distance #Enum

    @property
    def Appledirection(self):
        return self.direction    

    @property
    def Appledistance(self):
        return self.distance

    def setDirection(self, newDirection):
        self.direction = newDirection

    def setDistance(self, newDistance):
        self.distance = newDistance  

class Direction (Enum):
    NORTH = "N"
    WEST = "W"
    EAST = "E"
    SOUTH = "S"
    NORTH_WEST = "NW"
    SOUTH_WEST = "SW"
    NORTH_EAST = "NE"
    SOUTH_EAST = "SE"

   

class Distance (Enum):
    ONE = 1
    TWO = 2
    THREE_AND_MORE = 3


