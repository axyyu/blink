"""
Intersection Object

"""
from dependencies import *
from input_objects import intersection_control

class Intersection(threading.Thread):
    def __init__(self, tick, name, region, region_com, directions = 4):
        threading.Thread.__init__(self)

        self.id = uuid.uuid4()
        self.name = name
        self.region = region
        self.region_com = region_com
        self.directions = directions

        self.tick = tick
        self.inner_tick = 0
        self.com = queue.Queue()
        self.input_road = [False for d in range(directions)]
        self.exit_road = [False for d in range(directions)]

        self.lights = [False for d in range(directions)]
        self.cycle_times = [10 for d in range(directions)]
        self.current_cycle = 0
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def init(self):
        self.initLights()
        self.start()

    def run(self):
        while True:
            tick = self.tick.get()
            self.updateLights(tick)
            cprint("\t{}\t{}".format(self.name, self.lights),"blue")

    """
    Attaching Roads
    Attempts to find a road in the opposite direction thats already been attached
    If not, then attaches to the end of the array
    """
    def search(self, road, road_list):
        ind = -1
        for r in range(len(road_list)):
            if road_list[r] and road.id == road_list[r].id:
                ind = r
        return ind

    def attach_road(self, option, road):
        if option:
            self.add_road(road, self.input_road, self.exit_road)
        else:
            self.add_road(road, self.exit_road, self.input_road)

    def add_road(self,road, one, two):
        if road in one:
            cprint("WARNING: Attempted to add preexisting road to intersection.",'yellow')
            return
        
        dir = self.search(road, two)
        if dir > -1:
            temp = None
            if dir < len(one):
                temp = one.pop(dir)
                one.insert(dir, road)
                road = temp
                
            return
        
        for d in range(len(one)):
            if one[d] == 0:
                one[d] = road
                break

    """
    Light management
    """
    """
    def updateCycles(self, tick):
        currentCycle = tick%sum(self.cycleTimes)
        for x in range(self.effCycleTimes):
            if(currentCycle<self.effCycleTimes[x]):
                currentGreenLight = self.lights[x]
        return currentGreenLight

    def changeCycleTimes(self, newLights):
        self.cycleTimes = newLights
        self.effCycleTimes = [sum(self.cycleTimes[0,x+1]) for x in range(len(self.cycleTimes))]
    """
    def initLights(self):
        self.lights = [1 if a != 0 else False for a in self.input_road]
        self.cycle_times = [10 if a > -1 else False for a in self.lights ]

    def updateLights(self, tick):
        print(self.input_road)
        print(self.exit_road)
        # one = self.lights.index(1)
        # two = one + int(self.directions/2)
