"""
Blink Simulation
"""
from dependencies import *
from road_objects import *
import configparser

class BlinkSimulation():
    def __init__(self, network, tick_limit=60, tick_delay=1):
        """ Ticks """
        self.tick = 0
        self.tick_limit = tick_limit
        self.tick_delay = tick_delay

        """ Network """
        self.network = network
        self.threads = []
        self.size = 0

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

    def run(self):
        cprint("\nRunning Network...\n","yellow")

        while self.tick < self.tick_limit:
            self.update_tick()
            self.run_threads()
            self.verify_network()

        cprint("\nEnded Simulation\n","yellow")

    """
    Network
    """
    def create_network(self):
        region = Region()

        intersection_threads = {}
        for i,v in tqdm(self.network.items(), desc="Populating Intersections"):
            if i not in intersection_threads:
                intersection = Intersection(v["name"], region.intersection)
                intersection_threads[i] = intersection

        for i,v in tqdm(self.network.items(), desc="Populating Roads"):
            for r in v["roads"]:
                r.keys()
                road = Road(r["name"], r["length"], r["lanes"], r["yellow_clearance"], r["am_inject_rate"], r["pm_exit_rate"])

                intersection_threads[i].attach_road("exit", road)

                if r["end"]:
                    intersection_threads[r["end"]].attach_road("enter", road)

        self.threads.append(region)
        for i,v in tqdm(intersection_threads.items(), desc="Appending threads"):
            self.threads.append(v)

    """
    Running the Simulation
    """
    def update_tick(self):
        cprint("{}".format(self.tick), "magenta")

        for t in self.threads:
            t.tick = self.tick

        time.sleep(self.tick_delay)
        self.tick += 1

    def verify_network(self):
        for t in self.threads:
            if t.name != t.verif.pop():
                cprint("Error: Verication is incorrect for {}".format(t.name), "red")
                raise ValueError("Verification Error")
