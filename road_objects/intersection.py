"""
Intersection Object

"""
from dependencies import *
from input_objects import intersection_control
from person_objects import *

class Intersection():
    def __init__(self, name, region_com):
        self.id = uuid.uuid4()
        self.name = name

        """ Communication """
        self.tick = 0
        self.verif = [] # Verification with sim
        self.region = region_com

        self.inner_tick = 0
        self.roads = {}

        self.lights = {}
        self.cycle_times = {}
        self.light_dir = []
        self.current_cycle = 0

        # Evaluation
        self.car_freq = [0 for x in range(30)] # SET TRAILING WINDOW AS SIMULATION PARAMETER
        self.metrics = {}
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self):
        self.init_lights()
        self.current_cycle = 0

        self.verif.append(self.name)

    def run(self):
        self.inner_tick+=1

        # Manages Cars
        self.update_lights()
        self.simulate_cars()
        cars_passing = self.update_cars()

        # Algorithm Control
        # self.region_update( self.region_com.get_nowait() )
        self.alter_times()

        # Data Collection
        self.update_car_freq(cars_passing)
        self.eval()

        # Verification
        self.status()
        self.verif.append(self.name) 

    """
    Status
    Print out necessary information
    """
    def status(self):
        cprint("\t{}\t{}\t".format(self.name, self.lights ), "blue")

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

    R = -1
    Y = 0
    G = 1
    """
    def init_lights(self):
        self.lights = {r: -1 for r in self.roads}
        self.cycle_times = {r:5 for r in self.roads}
        self.light_dir = list(self.lights.keys())

        self.lights[ self.light_dir[self.current_cycle] ] = 1

    def update_lights(self):
        cycle = self.light_dir[self.current_cycle]
        new_cycle = (self.current_cycle + 1) % len(self.light_dir)
        
        if self.inner_tick > self.cycle_times[self.light_dir[self.current_cycle]]:
            self.change_lights(self.current_cycle, new_cycle)

    def change_lights(self, old, new):
        if old != new:
            if self.lights[ self.light_dir[old] ] == 1:
                self.lights[ self.light_dir[old] ] = 0
            elif self.lights[ self.light_dir[old] ] == 0:
                self.lights[ self.light_dir[old] ] = -1
                self.lights[ self.light_dir[new] ] = 1
                self.inner_tick = 0
                self.current_cycle = new

    """
    Handle Cars
    """
    def update_cars(self):
        car_count = 0
        for r in self.roads:
            if "enter" in self.roads[r]:
                self.roads[r]["enter"].update()
                if self.lights[r] == 1 or self.lights[r] == 0:
                    if self.roads[r]["enter"].pass_vehicles(self.roads[r]["exit"]):
                        car_count += 1
        return car_count
        

    def simulate_cars(self):
        for r in self.roads:
            if "enter" in self.roads[r]:
                self.roads[r]["enter"].randomly_inject()

    """
    Evaluation
    """
    def update_car_freq(self, cars):
        self.car_freq.pop(0)
        self.car_freq.append(cars)

    def eval(self):
        stats = {}
        stats['SMA'] = sum(self.car_freq)/len(self.car_freq)
        return stats

    """
    Intersection Control
    """
    def alter_times(self):
        pass
        # self.cycle_times = intersection_control.run(self.metrics, self.roads, self.cycle_times)