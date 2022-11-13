from collections import namedtuple

from appleRadar import AppleRadar
from headRadar import HeadRadar


class State:
    def __init__(self):
        self.headRadar = HeadRadar()
        # self.appleRadar = AppleRadar

    def __hash__(self) -> int:
        return hash((self.headRadar))
