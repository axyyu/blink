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
        self.intersections = {} # Communication with int

        # Evaluation
        self.data = {}
        self.metrics = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self):
        self.verif.append(self.name)

    def add_intersection(self, int_id, obj):
        self.intersections[int_id] = obj
        return self.intersections[int_id]

    def run(self):
        # Data Evaluation
        self.collect_data()
        self.eval()

        # Algorithm Control
        self.process_intersection_data()

        # Verification
        self.verif.append(self.name)

    """
    Status
    Print out necessary information
    """
    def status(self):
        pass

    """
    Data Collection
    """
    def init_data(self):
        fields = [
        ]
        for f in fields:
            self.data[f] = []

    def collect_data(self):
        pass

    def init_eval(self):
        fields = [
        ]
        for f in fields:
            self.eval[f] = None

    def eval(self):
        pass

    """
    Region Control
    """
    def process_intersection_data(self):
        # multipliers = region_control.run(self.day, self.metrics, self.intersections.keys())
        pass
