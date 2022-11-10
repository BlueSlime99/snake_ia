from enum import Enum


class HeadRadar:

    def __init__(self) :


        self.__upOfHead,self.__rightOfHead,self.__leftOfhead, self.__downOfHead = Threats
        
    @property
    def upOfHeadSnake(self):
        return self.__upOfHead

    @property
    def downOfHeadSnake(self):
        return self.__downOfHead

    @property
    def leftOfHeadSnake(self):
        return self.__leftOfhead

    @property
    def rightOfHeadSnake(self):
        return self.__rightOfHead


    def setDownOfHead(self, state):
        self.__downOfHead = state

    def setRightOfHead(self, state):
        self.__rightOfHead = state

    def setLeftOfHead(self, state):
        self.__leftOfhead = state

    def setUpOfHead(self, state):
        self.__upOfHead = state

   

class Threats (Enum):

    SNAKE = "snake"
    APPLE = "apple"
    WALL = "wall"
    NONE = "none"

