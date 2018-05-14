"""
Region Object

"""
from dependencies import *
from input_objects import region_control

class Region:
    def __init__(self, name="Region"):
        self.id = uuid.uuid4()
        self.name = name
        self.time = 0

        self.tick = 0 # Receive ticks from simulation
        self.intersections = {} # Communication with int
        self.intersection_weights = {}

        # Evaluation
        self.metrics = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self):
        self.init_eval()

    def add_intersection(self, int_id, obj):
        self.intersections[int_id] = obj
        self.intersection_weights[int_id] = 0
        return self.intersection_weights

    def run(self):
        pass

    def eval(self):
        # Data Evaluation
        self.evaluate_data()

    def process(self):
        # Algorithm Control
        self.alter_weights()

    """
    Status
    Print out necessary information
    """
    def status(self):
        for f,v in self.metrics.items():
            print(f,v[-1])

    """
    Evalutation

    AMA - Average MA
    AMD - Average MD
    AFR - Average FR
    AQO - Average QO
    ASMAD - Average SMAD
    ASMAA - Average SMAA

    HVI - Number of high density intersections
    """
    def init_eval(self):
        fields = [
        "AMA",
        "AMD",
        "AFR",
        "AQO",
        "AQ",
        "HVI",
        ]
        for f in fields:
            self.metrics[f] = []

    def evaluate_data(self):
        self.size = len(self.intersections)
        for f in self.metrics:
            value = 0
            for id, intersection in self.intersections.items():
                if f == "AQ":
                    if len(intersection.data["Q"]) > 0:
                        # print(intersection.data["Q"][-1])
                        value+= intersection.data["Q"][-1]
                elif f == "HVI":
                    if len(intersection.data["Q"]) > 0:
                        # print(intersection.data["Q"][-1])
                        if intersection.data["Q"][-1] > 20:
                            value += 1
                else:
                    if len(intersection.metrics[f[1:]]) > 0:
                        value += intersection.metrics[f[1:]][-1]
                    
            if f != "HVI":
                self.metrics[f].append(value / self.size)
            else:
                self.metrics[f].append(value)

    """
    Region Control

    Weight output (user sets the scale)
    """
    def alter_weights(self):
        intersection_weights = region_control.run(self.time, self)

        try:
            if intersection_weights.keys() != self.intersection_weights.keys():
                raise ValueError('Intersections do not match.', set(intersection_weights.keys()).symmetric_difference(set(self.intersection_weights.keys())))
            for intersection_id, weight in intersection_weights.items():
                try:
                    float(weight)
                except:
                    raise ValueError('Intersection weights are not numbers.', intersection_id, weight)
            self.intersection_weights = intersection_weights
        except Exception as e:
            pass
            # print("ALTER TIMES ERROR ", e.args)
