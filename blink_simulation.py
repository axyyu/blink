from dependencies import *
from road_objects import *
from pprint import pprint

#####################################################################
#       Blink Simulation
# Manager for the traffic simulation. Generates the road network and
# runs each intersection and region. Data is collected throughout the
# process and is displayed at the end of the run.
#####################################################################

class BlinkSimulation():
    """
    BlinkSimulation

    tick - time variable (represents 1 sec)
    objects - list of intersection and region objects that need to be run
    """

    def __init__(self, network, tick_limit, tick_delay):
        """
        Initializes a BlinkSimulation object

        Arguments:
        network - dictionary of intersections and roads (created using create_network)
        tick_limit - the number of ticks the simulation will run for
        tick_delay - delay in seconds between each loop of the simulation
        """
        # Tick Setup
        self.tick = 0
        self.tick_limit = int(tick_limit)
        self.tick_delay = int(tick_delay)

        # Network Setup
        self.network = network
        self.objects = []

    #####################################################################
    #      INITIALIZATION
    #####################################################################

    def start(self):
        """
        Begins the simulation.

        Returns:
        data - data from simulation
        """
        self.create_network()
        self.init()
        self.simulate()
        return self.output()

    def create_network(self):
        """
        Creates all intersection and region objects based on the network dictionary.
        """
        self.region = Region("DC")

        intersection_objects = {}
        for i,v in tqdm(self.network.items(), desc="Populating Intersections"):
            if i not in intersection_objects:
                intersection = Intersection(v["name"], i, self.region.intersection_weights)
                self.region.add_intersection(intersection.id,intersection)
                intersection_objects[i] = intersection

        for i,v in tqdm(self.network.items(), desc="Populating Roads"):

            for r in v["roads"]:
                r.keys()
                road = Road(r["name"], r["length"], r["lanes"], r["yellow_clearance"], r["am_inject_rate"], r["pm_exit_rate"])

                intersection_objects[i].attach_road("exit", road)

                if r["end"]:
                    intersection_objects[r["end"]].attach_road("enter", road)
                    road.set_intersection(intersection_objects[r["end"]])

            if "4th St SW" in v["name"] and "E St SW" in v["name"]:
                print("\n")
                print(v["name"])
                print(intersection_objects[i].roads)

        for i,v in tqdm(intersection_objects.items(), desc="Appending objects"):
            self.objects.append(v)

    def init(self):
        """
        Initializes every intersection and region under the simulation.
        """
        cprint("\nInitializing Network...\n","yellow")
        # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            # a = [executor.submit(t.init()) for t in self.objects]

        for t in self.objects:
            t.init()
        self.region.init()
        cprint("\nFinished initialization. Simulation\n","yellow")

    #####################################################################
    #      SIMULATION
    #####################################################################

    def simulate(self):
        """
        Simulates the traffic network.
        """
        cprint("\nRunning Network...\n","yellow")

        for self.tick in range(self.tick_limit):
            cprint("{}".format(self.tick), "magenta", flush=True)
            start_time = time.time()

            self.run()
            # self.eval()
            # self.process()
            # self.status()

            print("--- %s seconds ---" % (time.time() - start_time))

            time.sleep(self.tick_delay)

        cprint("\nEnded Simulation\n","yellow")

    def run(self):
        """
        Simulates the passage of vehicles and pedestrians in each intersection.
        """
        for t in self.objects:
            t.tick = self.tick
            t.run()
        self.region.tick = self.tick
        self.region.run()

    def eval(self):
        """
        Collects data and calculates key traffic metrics.
        """
        for t in self.objects:
            t.eval()
        self.region.eval()

    def process(self):
        """
        Runs the algorithms for traffic control within each object.
        """
        for t in self.objects:
            t.process()
        self.region.process()

    def status(self):
        """
        Prints the status of the simulation.
        """
        self.region.status()

    #####################################################################
    #      RESULTS
    #####################################################################

    def output(self):
        """
        Outputs the data from the simulation.

        Returns:
        data - data from simulation
        """
        data = {}
        data["tick_limit"] = self.tick_limit

        data["region"] = self.region.metrics;

        name_to_id = {} # TODO: what if two intersections with the same name appear?
        for t in self.objects:
            data[t.id] = (t.name, t.coords, t.data, t.metrics)

        return data
