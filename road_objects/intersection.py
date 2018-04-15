"""
Intersection Object

"""
from dependencies import *
from input_objects import intersection_control
from person_objects import *

class Intersection():
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name

        """ Communication """
        self.tick = 0
        self.verif = [] # Verification with sim
        self.region = {}

        self.inner_tick = 0
        self.roads = {}

        self.lights = {}
        self.cycle_times = {}
        self.light_dir = []
        self.yellow_clearance = {}

        self.light_dir = []
        self.current_cycle = 0

        """ Evaluation """
        self.data = {}
        self.metrics = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self):
        self.init_lights()
        self.init_data()
        self.init_eval()
        self.current_cycle = 0

        self.verif.append(self.name)

    def add_region(self, region_com):
        self.region = region_com

    def run(self):
        self.inner_tick+=1

        # Manages Cars
        self.update_lights()
        self.simulate_cars()
        self.update_cars()

        # Data Evaluation
        self.collect_data()
        self.eval()

        # Algorithm Control
        self.region_update()
        self.alter_times()

        # Verification
        self.status()
        self.verif.append(self.name)

    """
    Status
    Print out necessary information
    """
    def status(self):
        print(self.tick)
        pprint(self.data)
        pprint(self.metrics)

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
        self.cycle_times = {r:45 for r in self.roads}
        for k,r in self.roads.items():
            yellow_times = [3]
            for _,n in r.items():
                if n.yellow_clearance:
                    yellow_times.append(n.yellow_clearance)
            self.yellow_clearance[k] = max(yellow_times)

        self.light_dir = list(self.lights.keys())
        self.lights[ self.light_dir[self.current_cycle] ] = 1

    def update_lights(self):
        cycle = self.light_dir[self.current_cycle]
        new_cycle = (self.current_cycle + self.yellow_clearance[cycle]) % len(self.light_dir)

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
        self.data["DFR"].append(car_count)


    def simulate_cars(self):
        inject_total = 0
        for r in self.roads:
            if "enter" in self.roads[r]:
                inject, exit = self.roads[r]["enter"].randomly_inject(self.tick)
                inject_total += inject
        self.data["AFR"].append(inject_total)

    """
    Data Collection

    AFR - Arrival Flow Rate (veh/s)
    DFR - Departure Flow Rate (veh/s)
    C - Cycle Length
    Q - Queue Length
    """
    def init_data(self):
        fields = [
            "AFR",
            "DFR",
            "C",
            "Q"
        ]
        for f in fields:
            self.data[f] = []

    def collect_data(self):
        queue_length = 0
        for r in self.roads:
            if "enter" in self.roads[r]:
                queue_length = self.roads[r]["enter"].count_vehicles()
        self.data["Q"].append(queue_length)

        self.data["C"].append(sum([self.cycle_times[r] for r in self.cycle_times]))

    """
    Evaluation

    MA - Mean Number of Arrivals/Cycle
    MD - Mean Number of Departures/Cycle
    I - Variance of Number of Arrivals/MA

    FR - Flow Ratio (AFR/DFR)

    QO - Queue Overflow Estimate [(2x-1)I]/[2(1-x)] x>=.5

    SMAD - Simple Moving Average Departures
    SMAA - Simple Moving Average Arrivals
    """
    def init_eval(self):
        fields = [
            "MA",
            "MD",
            "I",
            "FR",
            "QO",
            "SMAD",
            "SMAA"
        ]
        for f in fields:
            self.metrics[f] = 0

    def eval(self):
        if len(self.data["Q"]) > self.data["C"][-1]:
            cycle_length = self.data["C"][-1]
            self.metrics["MA"] = self.data["AFR"][-cycle_length:]/cycle_length;
            self.metrics["MD"] = self.data["DFR"][-cycle_length:]/cycle_length;

            self.metrics["I"] = np.std(self.data["AFR"])/self.metrics["MA"]

            x = .6
            self.metrics["QO"] = ( (2*x-1)*self.metrics["I"] ) / (2*(1-x))

        if self.data["DFR"][-1] != 0:
            self.metrics["FR"] = self.data["AFR"][-1]/self.data["DFR"][-1]

    """
    Region Weights

    Change times from weights
    """
    def region_update(self):
        weight = self.region[self.id]

    """
    Intersection Control

    Times can't be < Yellow Clearance Interval
    """
    def alter_times(self):
        new_cycle_times = intersection_control.run(self.tick, self.data, self.metrics, self.cycle_times)
        try:
            if new_cycle_times.keys() != self.roads.keys():
                raise ValueError('Roads do not match.', set(new_cycle_times.keys()).symmetric_difference(set(self.roads.keys())))
            for r in new_cycle_times:
                if new_cycle_times[r] < self.yellow_clearance[r]:
                    raise ValueError('New cycle times are shorter than required yellow clearance time.', r, new_cycle_times[r])
            self.cycle_times = new_cycle_times
        except Exception as e:
            pass
            # print("ALTER TIMES ERROR ", e.args)
