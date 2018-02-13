"""
Intersection Object

"""
from dependencies import *
from input_objects import intersection_control
from person_objects import *

class Intersection(threading.Thread):
    def __init__(self, tick, name, region, region_com, inject_rate, loss_rate):
        threading.Thread.__init__(self)

        self.id = uuid.uuid4()
        self.name = name

        self.region = region
        self.region_com = region_com

        self.inject_rate = float(inject_rate) # Inject rate for vehicles
        self.loss_rate = float(loss_rate)

        self.tick = tick # Communication with simulation
        self.verif = queue.Queue() # Verification with simulation

        self.inner_tick = 0
        self.roads = {}

        self.lights = {}
        self.cycle_times = {}
        self.light_dir = []
        self.current_cycle = False

        # Evaluation
        self.car_freq = [0 for x in range(30)] # SET TRAILING WINDOW AS SIMULATION PARAMETER
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self, window=None):
        self.init_lights()
        self.current_cycle = 0

        self.panel = window.addIntersection(self.name, self.roads)

        self.verif.put(self.name)
        self.start()

    def run(self):
        while True:
            tick = self.tick.get()
            self.inner_tick+=1

            self.update_lights()
            self.simulate_cars()
            cars_passing = self.update_cars()

            self.update_car_freq(cars_passing)
            self.eval()
            
            self.panel.updateStatus(self)

            self.verif.put(self.name) # Verification

    """
    Status
    Print out necessary information
    """
    def status(self):
        cprint("\t{}\t{}\t{}".format(self.name, self.cars_in_roads(), self.lights ), "blue")

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

    def update_lights(self):
        cycle = self.light_dir[self.current_cycle]
        new_cycle = (self.current_cycle + 1) % len(self.light_dir)

        if self.inner_tick > self.cycle_times[self.light_dir[self.current_cycle]]:
            self.inner_tick = 0
            self.change_lights(self.current_cycle, new_cycle)
            self.current_cycle = new_cycle
        elif self.inner_tick == self.cycle_times[self.light_dir[self.current_cycle]]:
            if self.lights[ cycle] == 1 and new_cycle != self.current_cycle:
                self.lights[ cycle ] = 0

    def change_lights(self, old, new):
        self.lights[ self.light_dir[old] ] = -1
        self.lights[ self.light_dir[new] ] = 1

    """
    Handle Cars
    """

    # def road_status(self):
    #     for r in self.roads:
    #         print(self.roads[r]["enter"])
    
    def cars_in_roads(self):
        return { r:len(self.roads[r]["enter"].queue) for r in self.roads}   

    def update_cars(self):
        car_count = 0
        for r in self.roads:
            self.roads[r]["enter"].update()
            if self.lights[r] == 1 or self.lights[r] == 0:
                if self.roads[r]["enter"].pass_vehicles(self.roads[r]["exit"], self.name):
                    car_count += 1
        return car_count
        

    def simulate_cars(self):
        for r in self.roads:
            if random.random() < self.inject_rate:
                self.roads[r]["enter"].randomly_inject()
            if random.random() < self.loss_rate:
                self.roads[r]["enter"].randomly_remove()

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