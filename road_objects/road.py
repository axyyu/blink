"""
Road Object

"""
from dependencies import *
from person_objects import *

class Road():
    def __init__(self, name, length, lanes, inject_rate, exit_rate):
        self.id = uuid.uuid4()
        self.name = name

        self.length = length
        self.lanes = lanes
        self.inject_rate = inject_rate
        self.exit_rate = exit_rate
        self.queue = []

        self.init()

    def __str__(self):
        return "{} {}".format(self.name, self.queue)

    def __repr__(self):
        return "{}_{}".format(self.name, str(self.id)[:5])

    """
    Init
    """
    def init(self):
        if self.length:
            self.queue = [ [ 0 for b in range(self.length) ] for a in range(self.lanes) ]

    """
    Road Methods
    """
    def update(self):
        for lane in range(self.lanes):
            for slot in range(1, self.length):
                if self.queue[lane][slot] != 0:
                    for l in random.sample([lane, lane-1, lane+1], 3):
                        if l >= 0 and l < self.lanes:
                            if self.queue[l][slot-1] == 0:
                                self.queue[l][slot-1] = self.queue[lane][slot]
                                self.queue[lane][slot] == 0
                                break

    """
    Road Detection Info
    """
    def count_vehicles(self):
        count = 0
        if self.length:
            for lane in random.sample(range(self.lanes), self.lanes):
                if self.queue[lane][self.length-1] != 0:
                    count+=1
            return 0
        return 0

    """ Returns open lane """
    def detect_back(self):
        if self.length:
            for lane in random.sample(range(self.lanes), self.lanes):
                if self.queue[lane][self.length-1] == 0:
                    return lane
            return None
        return False
    
    """ Returns front lane """
    def detect_front(self):
        if self.length:
            for lane in random.sample(range(self.lanes), self.lanes):
                if self.queue[lane][0] != 0:
                    return lane
            return None
        return False

    """
    Vehicle Methods
    """
    def add_vehicle(self):
        if self.length:
            lane = self.detect_back()
            if lane:
                self.queue[lane][self.length-1] = Vehicle()

    def remove_vehicle(self):
        if self.length:
            for lane in random.sample(range(self.lanes), self.lanes):
                for slot in random.sample(range(self.length), self.length):
                    if self.queue[lane][slot] != 0:
                        self.queue[lane][slot] == 0
        return None
    
    def pass_vehicles(self, target):
        target_lane = target.detect_back()
        my_front = self.detect_front()
        if target_lane and my_front:
            target.queue[target_lane][target.length-1] = self.queue[my_front][0]
            self.queue[my_front][0] = 0
    
    """
    Vehicle Injection and Removal
    """
    def randomly_inject(self):
        if self.length:
            if random.random() < self.exit_rate:
                self.remove_vehicle()
            if random.random() < self.inject_rate:
                self.add_vehicle()