from dependencies import *
from input_objects import intersection_control
from person_objects import *

#####################################################################
#       Intersection
# Manages traffic flow between intersections and maintains cycle
# times. Tracks data on the departures and arrivals.
#####################################################################

class Intersection:
    """
    Intersection

    tick - in seconds, set by the BlinkSimulation, used to obtain time of day
    region - intersection weights determined by Region object
    roads - dictionary of roads
        roads [ road name ] [ type(enter|exit) ] = road object

    lights - dictionary of light status
        lights [ road name ] = type(-1|0|1)
    light_dir - list of road names (used for identifing current green light)
    yellow_clearance - dictionary of yellow clearance times for each road
        yellow_clearance [ road name ] = float (seconds)

    inner_tick - ticks elapsed in current cycle
    cycle_times - current cycle times for each road
        cycle_times [ road name ] = int (ticks for each cycle)
    current_cycle - the current cycle (index in light_dir)

    arrivals - number of arrivals per tick
    departures - number of departures per tick
    data - dictionary of various data points
    metrics - dictionary of various calculations
    """

    def __init__(self, int_id, name, coords, region_com):
        """
        Initializes the intersection.

        Arguments:
        name - name of the intersection
        """
        self.id = int_id
        self.coords = coords
        self.name = name
        self.time = 0

        # Communication with simulation and regions
        self.tick = 0
        self.region = region_com

        # Road Setup
        self.roads = {}

        # Light Setup
        self.lights = {}
        self.light_dir = []
        self.yellow_clearance = {}

        # Cycle Setup
        self.inner_tick = 0
        self.cycle_times = {}
        self.current_cycle = 0

        # Data Setup
        self.arrivals = 0
        self.departures = 0
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
        self.init_roads()
        self.current_cycle = 0

    def run(self):
        self.inner_tick+=1

        # Manages Cars
        self.update_lights()
        self.simulate_cars()
        self.update_cars()

    def eval(self):
        # Data Evaluation
        self.collect_data()
        self.evaluate_data()

    def process(self):
        # Algorithm Control
        self.region_update()
        self.alter_times()

    """
    Status
    Print out necessary information
    """
    def status(self):
        print(self.tick)
        for r in self.roads:
            if "enter" in self.roads[r]:
                print(self.roads[r]["enter"].length)

    """
    Attaching Roads
    Attempts to find a road in the opposite direction thats already been attached
    """
    def attach_road(self, option, road):
        if road.name not in self.roads:
            self.roads[road.name] = {}

        if option not in self.roads[road.name]:
            self.roads[road.name][option] = []

        self.roads[road.name][option].append(road)

    def init_roads(self):
        for _,r in self.roads.items():
            if "enter" in r:
                for enter_road in r["enter"]:
                    for k,r in self.roads.items():
                        if "exit" in r:
                            for exit_road in r["exit"]:
                                enter_road.set_lane(exit_road)
                    enter_road.init()

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
                if _ == "enter":
                    for road in n:
                        if road.yellow_clearance:
                            yellow_times.append(road.yellow_clearance)
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
    def alert(self, num):
        self.arrivals += num

    def update_cars(self):
        for r in self.roads:
            if "enter" in self.roads[r]:
                for road in self.roads[r]["enter"]:
                    road.update()
                    if self.lights[r] == 1 or self.lights[r] == 0:
                        passed_count = road.pass_vehicles()
                        self.departures += passed_count

    def simulate_cars(self):
        for r in self.roads:
            if "enter" in self.roads[r]:
                for road in self.roads[r]["enter"]:
                    inject, exit = road.randomly_inject(self.time)
                    self.arrivals += inject
                    self.departures += exit

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
        self.data["AFR"].append(self.arrivals)
        self.data["DFR"].append(self.departures)
        self.arrivals = 0
        self.departures = 0

        queue_length = 0
        for r in self.roads:
            if "enter" in self.roads[r]:
                for road in self.roads[r]["enter"]:
                    queue_length += road.count_vehicles()
        self.data["Q"].append(queue_length)
        self.data["C"].append(sum([self.cycle_times[r] for r in self.cycle_times]))

    """
    Evaluation

    MA - Number of Arrivals/Cycle
    MD - Number of Departures/Cycle

    I - Variance of Number of Arrivals/MA

    AFR - Flow Ratio (AFR/DFR)
    DFR - Flow Ratio (DFR/AFR)

    QO - Queue Overflow Estimate [(2x-1)I]/[2(1-x)] x>=.5
    """
    def init_eval(self):
        fields = [
            "MA",
            "MD",
            "I",
            "FR",
            "QO"
        ]
        for f in fields:
            self.metrics[f] = []

    def evaluate_data(self):
        # if len(self.data["Q"]) > self.data["C"][-1]:
        cycle_length = self.data["C"][-1]
        self.metrics["MA"].append(sum(self.data["AFR"][-cycle_length:]));
        self.metrics["MD"].append(sum(self.data["DFR"][-cycle_length:]));

        if self.metrics["MA"][-1] != 0:
            self.metrics["I"].append(np.std(self.data["AFR"])/self.metrics["MA"][-1])

            x = .6
            self.metrics["QO"].append(( (2*x-1)*self.metrics["I"][-1] ) / (2*(1-x)))
        else:
            self.metrics["I"].append(0)
            self.metrics["QO"].append(0)

        if self.metrics["MD"][-1] != 0:
            self.metrics["FR"].append(self.metrics["MA"][-1]/self.metrics["MD"][-1])
        else:
            self.metrics["FR"].append(0)

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
        new_cycle_times = intersection_control.run(self.time, self)
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
