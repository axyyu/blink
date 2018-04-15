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
        self.intersection_weights = {}

        # Evaluation
        self.metrics = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self):
        self.init_eval()
        self.verif.append(self.name)

    def add_intersection(self, int_id, obj):
        self.intersections[int_id] = obj
        self.intersection_weights[int_id] = 0
        return self.intersection_weights

    def run(self):
        # Data Evaluation
        self.eval()

        # Algorithm Control
        self.alter_weights()

        # Verification
        self.verif.append(self.name)

    """
    Status
    Print out necessary information
    """
    def status(self):
        pprint(self.metrics)

    """
    Evalutation

    AMA - Average MA
    AMD - Average MD
    AFR - Average FR
    AQO - Average QO
    ASMAD - Average SMAD
    ASMAA - Average SMAA

    HDI - Number of high density intersections
    """
    def init_eval(self):
        fields = [
        "AMA",
        "AMD",
        "AFR",
        "AQO",
        "ASMAD",
        "ASMAA",
        "HDI"
        ]
        for f in fields:
            self.metrics[f] = 0

    def eval(self):
        for f in self.metrics:
            self.metrics[f] = 0
            for id, intersection in self.intersections.items():
                if f != "HDI":
                    self.metrics[f] += intersection.metrics[f[1:]]
                else:
                    if intersection.metrics["FR"] > 1:
                        self.metrics["HDI"] += 1
            if f != "HDI":
                self.metrics[f] /= 2

    """
    Region Control

    Weight output (user sets the scale)
    """
    def alter_weights(self):
        intersection_weights = region_control.run(self.tick, self.metrics, self.intersections)

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
