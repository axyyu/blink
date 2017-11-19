"""
Intersection Object

"""
from dependencies import *
from input_objects import intersection_control

class Intersection(threading.Thread):
    def __init__(self, tick, name, region, region_com):
        threading.Thread.__init__(self)

        self.id = uuid.uuid4()
        self.name = name
        self.region = region
        self.region_com = region_com

        self.tick = tick
        self.com = queue.Queue()
        self.roads = []

    def attach_road(self,road):
        self.roads.append(road)