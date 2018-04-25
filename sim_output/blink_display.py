from dependencies import *
from argparse import ArgumentParser
import matplotlib
import pickle

#####################################################################
#       Blink Display
# Displays simulation output. Provides the ability to open specific
# intersection graphs.
#####################################################################
"""
Reading in output file.
"""
ap = ArgumentParser()

with open(network_dir, "rb") as f:
    network = pickle.load(f)


"""
Initalizes and runs the simulation.

Edit under here to run the simulation multiple times.
"""
sim = BlinkSimulation(network, cp.get("DEFAULT","sim_length"), cp.get("DEFAULT","tick_delay"))
sim.start()
