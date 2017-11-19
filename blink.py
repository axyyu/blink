from dependencies import *
from person_objects import *
from road_objects import *
from pprint import pprint

"""
For Simulation Purposes
"""
tick = queue.Queue()
road_network = {}

"""
Helper
"""
def display_network(road_network):
    for rid in road_network:
        # print("\n{}{}{}".format(colors.PURPLE + colors.BOLD, rid, colors.ENDC))
        cprint("\n{}".format(rid), 'magenta', attrs=['bold'])
        for iid in road_network[rid].intersections:
            pass

"""
Input Road Network
"""
def create_network():
    content = []
    with open(sys.argv[1], 'r') as f:
        content = f.readlines()

    for c in content:
        b = c.lstrip().rstrip()
        if(b[0] == "#"):
            region = Region(tick, b[1:])
            if region.name not in road_network:
                road_network[region.name] = region
        if(b[0] == "-"):
            intersection = Intersection(tick, b[1:], region.id, region.com)
            if intersection.name not in road_network:
                road_network[intersection.name] = intersection
        if(b[0] == "*"):
            road_info = b[1:].split(",")
            int1, int2 = road_info[1].split("-")

            road = Road(tick, road_info[0])
            road_network[int1].attach_road(road)
            road_network[int2].attach_road(road)

            if road.name not in road_network:
                road_network[road.name] = road

create_network()
pprint(road_network)