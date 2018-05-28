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

    def __init__(self, network, tick_limit, tick_delay, verbose):
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
        self.tick_delay = float(tick_delay)

        # Network Setup
        self.network = network
        self.objects = []

        self.verbose = True if int(verbose) == 1 else False

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
                intersection = Intersection(v["id"], v["name"], i, self.region.intersection_weights)
                self.region.add_intersection(intersection.id,intersection)
                intersection_objects[i] = intersection

        for i,v in tqdm(self.network.items(), desc="Populating Roads"):

            for r in v["roads"]:
                r.keys()
                road = Road(**r)

                intersection_objects[i].attach_road("exit", road)

                if r["end"] in self.network:
                    intersection_objects[r["end"]].attach_road("enter", road)
                    road.set_intersection(intersection_objects[r["end"]])

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

    def time_multiplier(self, tick):
        period = np.pi/(self.tick_limit/4)
        return np.sum([ (2*np.sin(k*period*tick)) / (k*np.pi*(-1)**(k+1)) for k in range(1,5)])
        
    def simulate(self):
        """
        Simulates the traffic network.
        """
        cprint("\nRunning Network...\n","yellow")

        for self.tick in tqdm(range(self.tick_limit), desc="Simulation Progress"):
            cprint("{}".format(self.tick), "magenta", flush=True) if self.verbose else 0
            start_time = time.time()

            self.run()
            self.eval()
            self.process()
            self.status()

            print("--- %s seconds ---" % (time.time() - start_time)) if self.verbose else 0

            time.sleep(self.tick_delay)

        cprint("\nEnded Simulation\n","yellow")

    def run(self):
        """
        Simulates the passage of vehicles and pedestrians in each intersection.
        """
        time = self.time_multiplier(self.tick)
        for t in self.objects:
            t.tick = self.tick
            t.time = time
            t.run()
        self.region.tick = self.tick
        self.region.run()

        # print(time)
        # for t in self.objects:
        #     print(t)
        #     for _,r in t.roads.items():
        #         for _,roads in r.items():
        #             for road in roads:
        #                 print(road.queue)
            # print(t.data["Q"][-10:])

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
        self.region.status() if self.verbose else 0

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
