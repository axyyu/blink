"""
Region Object

"""
from dependencies import *
from input_objects import region_control

class Region(threading.Thread):
    def __init__(self, tick, name):
        threading.Thread.__init__(self)
        
        self.id = uuid.uuid4()
        self.name = name

        self.tick = tick
        self.com = queue.Queue()
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def run(self):
        while True:
            tick = self.tick.get()
            cprint("\t{}".format(tick),"magenta")
