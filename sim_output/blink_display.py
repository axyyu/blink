from argparse import ArgumentParser
import matplotlib.pyplot as plt
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
ap.add_argument('filename')
args = ap.parse_args()

with open(args.filename, "rb") as f:
    data = pickle.load(f)

"""
Display data.
"""
tick_limit = data["tick_limit"]
region_metrics = data["region"]

x = [t for t in range(tick_limit)]

for k,v in region_metrics.items():
    plt.plot(x, v)

plt.rcParams["figure.figsize"] = [20, 40]
plt.legend(list(region_metrics.keys()), loc='upper left')
# plt.title("Baseline")
plt.xlabel("Ticks (seconds)")
plt.ylabel("Ratio")
plt.show()
