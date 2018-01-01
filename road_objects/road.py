"""
Road Object

"""
from dependencies import *
from person_objects import *

class Road(queue.PriorityQueue):
    def __init__(self, name, start_int, end_int, length=20, capacity=2):
        queue.PriorityQueue.__init__(self,capacity)

        self.id = uuid.uuid4()
        self.start_int = start_int
        self.end_int = end_int
        self.name = name
        self.length = length
        self.capacity = capacity

    def __str__(self):
        return "{} {}".format(self.name, self.queue)

    def __repr__(self):
        return "{}_{}".format(self.name, str(self.id)[:5])

    """
    Basic Road Info
    Vehicles are added as tuples (distance_from_front, Vehicle Object)
    """
    def count_freq(self):
        freq = [0 for a in range(self.length)]
        for v in self.queue:
            freq[v[0]]+=1
        return freq

    def detect_availible(self):
        if self.count_freq()[self.length-1] < self.capacity:
            return True
        return False
    
    def detect_front(self):
        if len(self.queue) > 0 and self.queue[0][0] == 0:
            return True
        return False

    """
    Road Methods
    """
    def add_vehicle(self, vehicle):
        super().put([self.length-1,vehicle])

    def update(self):
        if not self.detect_front():
            for v in self.queue:
                v[0] -= 1

    def pass_vehicles(self, target):
        if target.detect_availible():
            if self.detect_front:
                target.add_vehicle(super().get()[1])
                cprint("\t\t{} -> {}".format( self.end_int, target.end_int ),"yellow")
    
    """
    Vehicle Injection
    """
    def randomly_inject(self):
        if self.detect_availible():
            self.add_vehicle(Vehicle())

    """
    Vehicle Removal
    """
    def randomly_remove(self):
        v = random.randint(0,len(self.queue))
        self.queue.pop(v)