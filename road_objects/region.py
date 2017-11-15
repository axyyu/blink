"""
Region Object
"""
from dependencies import *
from input_objects import region_control

class Region(threading.Thread):
    def __init__(self):
        self.id = uuid.uuid4()
        self.intersections = {}
        self.efficiency = 0

        self.total_threads = 0

        threading.Thread.__init__(self)
        self.stoprequest = threading.Event()

    """
    Threading Methods
    """
    def verify(self):
        pass

    def monitor(self):
        print("{}/{} Threads Active".format(threading.active_count(), self.total_threads))

    def run(self):
        print('{} initiated'.format(self.id))
        for i in tqdm(range(len(self.intersections))):
            print("")

        # self.verify()
        self.total_threads = threading.active_count() 
        
        self.stoprequest.clear()
        while not self.stoprequest.isSet():
            try:
                self.monitor()
                time.sleep(1)
            except queue.Empty:
                print("Empty")
    
    def join(self, timeout=None):
        self.stoprequest.set()
        super(Region, self).join(timeout)