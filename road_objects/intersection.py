"""
Intersection Object

"""
from dependencies import *
from input_objects import intersection_control

class Intersection(threading.Thread):
    def __init__(self, region_id=None):
        self.id = uuid.uuid4()
        self.region = region_id
        self.startLanes = {}
        self.endLanes = {}
        self.efficiency = 0

        self.region_q = None
        
        threading.Thread.__init__(self)
        self.stoprequest = threading.Event()

    """
    Threading
    """
    def verify(self):
        pass

    def run(self):
            # self.lane_q.append(queue.Queue())
            # self.lanes[l].int_q = self.lane_q[l]
            # self.lanes[l].start()

        self.stoprequest.clear()
        while not self.stoprequest.isSet():
            try:
                pass
            except queue.Empty:
                print("Empty")
    
    def join(self, timeout=None):
        self.stoprequest.set()
        super(Intersection, self).join(timeout)