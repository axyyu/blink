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
        self.verif = queue.Queue() #Verification with sim
        self.int_com = queue.Queue() #Communication with int
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self, window=None):
        self.start()

    def run(self):
        while True:
            tick = self.tick.get()

            self.verif.put(self.name) #Verification
            # cprint("\t{}".format(tick),"magenta")
    
    """
    Status
    Print out necessary information
    """
    def status(self):
        pass