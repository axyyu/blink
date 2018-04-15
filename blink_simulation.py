"""
Blink Simulation
"""
from dependencies import *
from road_objects import *


class BlinkSimulation():
    def __init__(self, network, tick_limit, tick_delay):
        """ Ticks """
        self.tick = 0
        self.tick_limit = int(tick_limit)
        self.tick_delay = int(tick_delay)

        """ Network """
        self.network = network
        self.threads = []
        self.size = 0

        """ Data """
        self.data = []

    def start(self):
        self.create_network()
        self.init()
        self.run()

    def init(self):
        for t in self.threads:
            t.init()
        self.verify_network()

    def run_threads(self):
        for t in self.threads:
            t.run()
            t.status()

    def run(self):
        cprint("\nRunning Network...\n","yellow")

        for self.tick in range(self.tick_limit):
            self.update_tick()
            self.run_threads()
            self.verify_network()
            self.data.append({k:v for k,v in self.region.metrics.items()})
            # self.region.status()
        self.status()

        cprint("\nEnded Simulation\n","yellow")

    """
    Network
    """
    def create_network(self):
        self.region = Region()

        intersection_threads = {}
        for i,v in tqdm(self.network.items(), desc="Populating Intersections"):
            if i not in intersection_threads:
                intersection = Intersection(v["name"])
                intersection.add_region(self.region.add_intersection(intersection.id,intersection))
                intersection_threads[i] = intersection

        for i,v in tqdm(self.network.items(), desc="Populating Roads"):
            for r in v["roads"]:
                r.keys()
                road = Road(r["name"], r["length"], r["lanes"], r["yellow_clearance"], r["am_inject_rate"], r["pm_exit_rate"])

                intersection_threads[i].attach_road("exit", road)

                if r["end"]:
                    intersection_threads[r["end"]].attach_road("enter", road)

        self.threads.append(self.region)
        for i,v in tqdm(intersection_threads.items(), desc="Appending objects"):
            self.threads.append(v)

    """
    Running the Simulation
    """
    def time_multiplier(self, sec):
        return np.sin(sec * (np.pi/1800))

    def update_tick(self):
        cprint("{}".format(self.tick), "magenta", flush=True)

        for t in self.threads:
            t.tick = self.time_multiplier(self.tick)

        time.sleep(self.tick_delay)

    def verify_network(self):
        for t in self.threads:
            if t.name != t.verif.pop():
                cprint("Error: Verication is incorrect for {}".format(t.name), "red")
                raise ValueError("Verification Error")

    """
    Compiling Results
    """
    def status(self):
        pass
