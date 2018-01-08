"""
Blink Simulation

Not run on main thread
"""
from dependencies import *
from input_objects import intersection_control
from person_objects import *

class Intersection(threading.Thread):
    def __init__(self, tick, name, region, region_com, inject_rate):
        threading.Thread.__init__(self)

        self.id = uuid.uuid4()
        self.name = name
        self.com = queue.Queue()
        self.region = region
        self.region_com = region_com
        self.inject_rate = inject_rate

        self.tick = tick
        self.inner_tick = 0
        self.roads = {}

        self.lights = {}
        self.cycle_times = {}
        self.light_dir = []
        self.current_cycle = False
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self, window):
        self.init_lights()
        self.current_cycle = 0
        self.start()

    def run(self):
        while True:
            tick = self.tick.get()
            self.inner_tick+=1
            self.update_lights()
            self.simulate_cars()
            self.update_cars()
            self.com.put(self.name)

    """
    Status
    Print out necessary information
    """
    def status(self):
        cprint("\t{}\t{}\t{}".format(self.name,self.car_freq(), self.lights ),"blue")

    """
    Attaching Roads
    Attempts to find a road in the opposite direction thats already been attached
    """
    def attach_road(self, option, road):
        if road.name not in self.roads:
            self.roads[road.name] = {}
        self.roads[road.name][option] = road

    """
    Light management
    """
    def init_lights(self):
        self.lights = {r: False for r in self.roads}
        self.cycle_times = {r:5 for r in self.roads}
        self.light_dir = list(self.lights.keys())

    def update_lights(self):
        cycle = self.light_dir[self.current_cycle]
        if self.inner_tick > self.cycle_times[self.light_dir[self.current_cycle]]:
            self.inner_tick = 0
            new_cycle = (self.current_cycle + 1) % len(self.light_dir)
            self.change_lights(self.current_cycle, new_cycle)
            self.current_cycle = new_cycle
        elif self.inner_tick == self.cycle_times[self.light_dir[self.current_cycle]]:
            if self.lights[ cycle] == True :
                self.lights[ cycle ] = 0

    def change_lights(self, old, new):
        self.lights[ self.light_dir[old] ] = False
        self.lights[ self.light_dir[new] ] = True

    """
    Handle Cars
    """

    # def road_status(self):
    #     for r in self.roads:
    #         print(self.roads[r]["enter"])
    
    def car_freq(self):
        return { r:len(self.roads[r]["enter"].queue) for r in self.roads}
            

    def update_cars(self):
        for r in self.roads:
            self.roads[r]["enter"].update()
            if self.lights[r]:
                self.roads[r]["enter"].pass_vehicles(self.roads[r]["exit"])

    def simulate_cars(self):
        for r in self.roads:
            if random.random() < self.inject_rate:
                self.roads[r]["enter"].randomly_inject()