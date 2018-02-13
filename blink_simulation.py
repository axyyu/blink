"""
Blink Simulation

Not run on main thread
"""
from dependencies import *
from road_objects import *
import configparser

class BlinkSimulation(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.tick = 0
        self.road_network = {}
        self.inject_rate = .5
        self.length = 0
        self.GUI = True
        self.size = 0

    def init(self, window=None):
        for k in self.road_network:
            self.road_network[k].init(window)
        self.size = len(self.road_network)
        self.verify_network()
        self.start()

    def run(self):
        cprint("\nRunning Network...\n","yellow")
        while self.tick < self.length:
            self.thread_check()
            self.update_tick()
            self.verify_network()
            self.status()

        cprint("\nEnded Simulation\n","yellow")

    """
    Network
    """
    def configure(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.length = float(config["PARAMETERS"]["SimulationLength"])
        self.GUI = (float(config["PARAMETERS"]["GUI"]) == 1)
        self.tick_delay = float(config["PARAMETERS"]["TickDelay"])

    def create_network(self, network_file, window=None):
        content = []

        with open(network_file, 'r') as f:
            content = f.readlines()

        for c in content:
            b = c.lstrip().rstrip()
            if len(b) <= 0:
                continue
            if b[0] == "#":
                region = Region(queue.Queue(), b[1:])
                self.road_network[region.name] = region
            if b[0] == "-":
                int_info = b[1:].split(",")
                intersection = Intersection(queue.Queue(), int_info[0], region.id, region.int_com, int_info[1], int_info[2])
                self.road_network[intersection.name] = intersection
            if b[0] == "*":
                road_info = b[1:].split(",")
                for r in range(len(road_info[1:-3])):
                    road = Road(road_info[0], road_info[r+2], road_info[r+1], int(road_info[-2]), int(road_info[-1]))
                    self.road_network[road_info[r+1].rstrip()].attach_road("enter", road)
                    self.road_network[road_info[r+2].rstrip()].attach_road("exit", road)

                    road = Road(road_info[0], road_info[r+1], road_info[r+2], int(road_info[-2]), int(road_info[-1]))
                    self.road_network[road_info[r+2].rstrip()].attach_road("enter", road)
                    self.road_network[road_info[r+1].rstrip()].attach_road("exit", road)

    """
    Running the Simulation
    """
    def update_tick(self):
        cprint("{}".format(self.tick), "magenta")

        for k in self.road_network:
            self.road_network[k].tick.put(self.tick)
        
        time.sleep(self.tick_delay)
        self.tick += 1

    def thread_check(self):
        count = threading.active_count() - 1
        if self.size == count:
            cprint("\nThread count doesn't match: {} != {}\n".format(count, self.size), "yellow")

    def verify_network(self):
        for k in self.road_network:
            if k != self.road_network[k].verif.get():
                cprint("Error: Verication is incorrect for {} {}".format(k, self.road_network[k].name), "red")
                raise ValueError("Code broke")

    def status(self):
        for k in self.road_network:
            self.road_network[k].status()