from dependencies import *
from person_objects import *
from road_objects import *
from pprint import pprint

import argparse
import configparser

"""
NEEDED LATER FOR TERMINAL INPUT

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('network', metavar='N', type=argparse.FileType('r'), help='A file containing a road network.')
# parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum, default=max, help='sum the integers (default: find the max)')
args = parser.parse_args()
print(args.network)
"""

"""
For Simulation Purposes
"""
tick = 0
road_network = {}
inject_rate = .5

"""
Helper
"""
def check_input():
    if len(sys.argv) < 2:
        cprint("\nUsage: blink.py <network> <ticks> \n", 'yellow')
        sys.exit()

"""
Configure
Reads configuration settings
"""
def configure():
    global inject_rate
    config = configparser.ConfigParser()
    config.read('blink_conf.conf')
    inject_rate = float(config["PARAMETERS"]["InjectRate"])

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
            intersection = Intersection(queue.Queue(), b[1:], region.id, region.com, inject_rate)
            road_network[intersection.name] = intersection
        if b[0] == "*":
            road_info = b[1:].split(",")
            for r in range(len(road_info[1:-3])):
                road = Road(road_info[0], road_info[r+2], road_info[r+1], int(road_info[-2]), int(road_info[-1]))
                road_network[road_info[r+1].rstrip()].attach_road("enter", road)
                road_network[road_info[r+2].rstrip()].attach_road("exit", road)

                road = Road(road_info[0], road_info[r+1], road_info[r+2], int(road_info[-2]), int(road_info[-1]))
                road_network[road_info[r+2].rstrip()].attach_road("enter", road)
                road_network[road_info[r+1].rstrip()].attach_road("exit", road)

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
        cprint("\t{}".format(tick),"magenta")

        for k in road_network:
            road_network[k].tick.put(tick)
        time.sleep(1)
        tick+=1
    pass

configure()
check_input()
create_network()
init_network()
# display_network()
run_network()