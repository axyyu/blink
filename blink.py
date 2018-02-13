from dependencies import *
import argparse

from blink_simulation import BlinkSimulation

"""
grey
red - error messages
green - productivity
yellow - warning messages
blue
magenta - tick
cyan - intersection
white
"""

"""
NEEDED LATER FOR TERMINAL INPUT

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('network', metavar='N', type=argparse.FileType('r'), help='A file containing a road network.')
# parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum, default=max, help='sum the integers (default: find the max)')
args = parser.parse_args()
print(args.network)
"""

"""
Helper
"""
def check_input():
    if len(sys.argv) < 2:
        cprint("\nUsage: blink.py <network> <ticks> \n", 'yellow')
        sys.exit()

check_input()
network_file = sys.argv[1]
config_file = "blink_conf.conf"


sim = BlinkSimulation()
sim.configure(config_file)
sim.create_network(network_file)
sim.init()