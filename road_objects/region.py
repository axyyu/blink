"""
Region Object

"""
from dependencies import *
from input_objects import region_control

class Region():
    def __init__(self, name="Region"):
        self.id = uuid.uuid4()
        self.name = name

        self.tick = 0 # Receive ticks from simulation
        self.verif = [] # Verification with sim
        self.intersection = [] # Communication with int
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self):
        self.verif.append(self.name)

    def run(self):
        self.process_intersection_data()
        self.verif.append(self.name) # Verification
    
    """
    Status
    Print out necessary information
    """
    def status(self):
        pass

    """
    Region Control
    """
    def process_intersection_data(self):
        pass