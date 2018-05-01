from dependencies import *
from blink_simulation import BlinkSimulation
from random_seed import blink_generate
from configparser import ConfigParser
import pickle

#####################################################################
#       Blink Configuration and Initialization
# Configure and run objects of the traffic simulation.
#####################################################################
"""
Reading in config file and loading the network object.

Should only use one configuration for all simulations run at one time.
"""
cp = ConfigParser()
cp.read("config.ini")
network_dir = cp.get("DEFAULT","network_file")

with open(network_dir, "rb") as f:
    network = pickle.load(f)

blink_generate.setup_generator() # Used for random number access to speed up the simulation

"""
Initalizes and runs the simulation.

Edit under here to run the simulation multiple times.
"""
sim = BlinkSimulation(network, cp.get("DEFAULT","sim_length"), cp.get("DEFAULT","tick_delay"))
output = sim.start()
with open("./sim_output/output.pickle", "wb") as f:
    pickle.dump(output, f, protocol=pickle.HIGHEST_PROTOCOL)

cprint("Data saved.", "yellow")
