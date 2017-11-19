"""
Road Object

"""
from dependencies import *

class Road(queue.Queue):
    def __init__(self, tick, name, length=20, capacity=20):
        threading.Thread.__init__(self)

        self.id = uuid.uuid4()
        self.name = name
        self.length = length
        self.capacity = capacity

        self.tick = tick