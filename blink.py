from dependencies import *
from blink_simulation import BlinkSimulation
from configparser import ConfigParser
import pickle

cp = ConfigParser()
cp.read("config.ini")
network_dir = cp.get("DEFAULT","network_file")

with open(network_dir, "rb") as f:
    network = pickle.load(f)

sim = BlinkSimulation(network, cp.get("DEFAULT","sim_length"), cp.get("DEFAULT","tick_delay"))
sim.start()
