from dependencies import *
import argparse
import pickle

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

"""
TERMINAL INPUT
"""
parser = argparse.ArgumentParser(description='{}{}{}'.format(bcolors.WARNING,
"Blink Traffic Simulation - This program simulates the passage of cars and pedestrians through a region."
,bcolors.ENDC))
parser.add_argument('network', help='{}{}{}'.format(bcolors.OKGREEN,'Network file.',bcolors.ENDC))
parser.add_argument('-t', help='Maximum number of ticks (seconds).')
parser.add_argument('-d', help='Delay in seconds between each tick (seconds).')
args = parser.parse_args()

f = open("{}".format(args.network), "rb")
network = pickle.load(f)

sim = BlinkSimulation(network)
sim.start()

print(args)
# tick_limit=args, tick_delay=1
