"""
Lane Object

"""
from dependencies import *

class Lane(threading.Thread):
    def __init__(self, region_id, s_int_id, e_int_id, ped=False):
        self.id = uuid.uuid4()
        self.region = region_id
        self.start_intersection = s_int_id
        self.end_intersection = e_int_id
        self.ped = ped

        self.objects = []
        self.light = 0
        
        threading.Thread.__init__(self)
        self.stoprequest = threading.Event()

    """
    Detects objects
    """
    def detect(self):
        pass

    """
    Adds objects
    """
    def add(self, object):
        pass

    """
    Threading
    """
    def verify(self):
        return self.isAlive()

    def run(self):
        self.stoprequest.clear()
        while not self.stoprequest.isSet():
            try:
                pass
            except queue.Empty:
                print("Empty")
    
    def join(self, timeout=None):
        self.stoprequest.set()
        super(Lane, self).join(timeout)