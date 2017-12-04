"""
Road Object

"""
from dependencies import *

class Road(queue.PriorityQueue):
    def __init__(self, name, start_int, end_int, length=20, capacity=20):
        queue.PriorityQueue.__init__(self,capacity)

        self.id = uuid.uuid4()
        self.start_int = start_int
        self.end_int = end_int
        self.name = name
        self.length = length
        self.capacity = capacity

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}_{}".format(self.name, str(self.id)[:5])
    
    def randomly_inject():
        pass

    def randomly_remove():
        pass
    
    def update(self):
        for v in self.queue:
            v[0] -= 1
    
    def put(self,vehicle):
        super().put([self.length,vehicle])
