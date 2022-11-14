import jsonpickle
from appleRadar import AppleRadar
from headRadar import HeadRadar


class State:
    def __init__(self):
        self.headRadar = HeadRadar()
        self.appleRadar = AppleRadar()

    def tojson(self):
        return jsonpickle.encode(self)
