from dependencies import *
from person_objects import *
from road_objects import *
from pprint import pprint

"""
For Simulation Purposes
"""
tick = 0
road_network = {}

"""
Helper
"""
def check_input():
    if len(sys.argv) < 2:
        cprint("\nUsage: blink.py <network>\n", 'yellow')
        sys.exit()
def display_network(road_network):
    for rid in road_network:
        # print("\n{}{}{}".format(colors.PURPLE + colors.BOLD, rid, colors.ENDC))
        cprint("\n{}".format(rid), 'magenta', attrs=['bold'])
        for iid in road_network[rid].intersections:
            pass

"""
Input Road Network
Generates the network based on the file input
"""
def create_network():
    content = []
    with open(sys.argv[1], 'r') as f:
        content = f.readlines()

    for c in content:
        b = c.lstrip().rstrip()
        if len(b) <= 0:
            continue
        if b[0] == "#":
            region = Region(queue.Queue(), b[1:])
            road_network[region.name] = region
        if b[0] == "-":
            intersection = Intersection(queue.Queue(), b[1:], region.id, region.com)
            road_network[intersection.name] = intersection
        if b[0] == "*":
            road_info = b[1:].split(",")
            pprint(road_info)
            for r in range(len(road_info[1:-3])):
                road = Road(road_info[0], road_info[r+2], road_info[r+1], int(road_info[-2]), int(road_info[-1]))
                road_network[road_info[r+1].rstrip()].attach_road(True, road)
                road_network[road_info[r+2].rstrip()].attach_road(False, road)

                road = Road(road_info[0], road_info[r+1], road_info[r+2], int(road_info[-2]), int(road_info[-1]))
                road_network[road_info[r+2].rstrip()].attach_road(True, road)
                road_network[road_info[r+1].rstrip()].attach_road(False, road)

"""
Initialize Network
Starts all the threads
"""
def init_network():
    for k in road_network:
        road_network[k].init()

def run_network():
    global tick
    while True:
        count = threading.active_count()
        cprint("\nActive Threads: {}\n".format(threading.active_count()),"green")

        for k in road_network:
            road_network[k].tick.put(tick)
        time.sleep(1)
        tick+=1
    pass

check_input()
create_network()
init_network()
# run_network()
pprint(road_network["IntC"].input_road)
pprint(road_network["IntC"].exit_road)
pprint(road_network["IntC"].lights)