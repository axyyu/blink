import pickle
from pprint import pprint
from tqdm import tqdm

"""
SHAPEFILES

Ignores exits and highways are they are less likely to have traffic lights
Ignores intersections with the same road name as they are usually neighorhood roads without lights
"""
import shapefile
sf = shapefile.Reader("FCPS_shapefiles/Roadway_Centerlines")

records = sf.records()
shapes = sf.shapes()

"""
Finds Intersections between Road Vectors
"""
intersection_map = {}

road_types = [
    "LOCAL ROAD",
    "PRIMARY",
    "SECONDARY",
    "TERTIARY"
]

for r in tqdm(range(len(shapes)), desc="Finding Intersections"):
    road_name = records[r][11]
    road_type = records[r][19]

    if road_type in road_types: # REMOVES BAD ROADS
        for p in shapes[r].points:
            if p not in intersection_map:
                intersection_map[p] = {
                    "road_ids": set(),
                    "road_names": set()
                }

            intersection_map[p]["road_ids"].add(r)
            intersection_map[p]["road_names"].add(road_name)

"""
Filter Intersections by Names
"""
fake_intersections = set()
for key,value in tqdm(intersection_map.items(), desc="Filtering Intersections"):
    if len(value["road_names"]) < 2:
        fake_intersections.add(key)

for i in tqdm(list(fake_intersections), desc="Deleting Intersections") :
    del intersection_map[i]

"""
Locate Intersections and Corresponding Roads"
"""
for key,value in tqdm(intersection_map.items(), desc="Setting Up Roads"):
    intersection_name = "{}".format(str(value["road_names"]))
    value["name"] = intersection_name

    value["roads"] = []
    for r in value["road_ids"]:
        location_int = [p for p in shapes[r].points if p != key and p in intersection_map]

        if len(location_int) < 1:
            road = {
                "name": records[r][11],
                "length": None,
                "lanes": None,
                "am_inject_rate": None,
                "pm_exit_rate": None,
                "yellow_clearance": None,
                "end": None
            }
        else:
            end = location_int[0]

            speed_limit = records[r][42]
            road_length = (( (key[0]-end[0])**2 + (key[1]-end[1])**2 ) ** .5) * 69
            average_vehicle_length = 0.0029829545

            speed_limit = speed_limit / 3600 # CONVERT FROM MPH TO MPS
            delay_distance = speed_limit * 2 # DELAY TIME IS SPEED * 2 SECONDS
            car_distance = average_vehicle_length + delay_distance
            length = int(road_length / car_distance)
            yellow_clearance = max(3, int(1.4 + (1.47*speed_limit)/(2*10)) ) # Reaction time as 1.4s

            if length == 0:
                length = 1

            road_type = records[r][19]

            lanes = 1
            am_inject_rate = .64
            pm_exit_rate = .7
            if road_type == "PRIMARY":
                am_inject_rate = 0
                pm_exit_rate = 0
                lanes = 4
            if road_type == "SECONDARY":
                am_inject_rate = .1
                pm_exit_rate = .1
                lanes = 3
            if road_type == "TERTIARY":
                am_inject_rate = .13
                pm_exit_rate = .28
                lanes = 2

            road = {
                "name": records[r][11],
                "length": length,
                "lanes": lanes,
                "am_inject_rate": am_inject_rate,
                "pm_exit_rate": pm_exit_rate,
                "yellow_clearance": yellow_clearance,
                "end": end
            }
        value["roads"].append(road)

with open("fairfax", 'wb') as f:
    pickle.dump(intersection_map, f, protocol=pickle.HIGHEST_PROTOCOL)

# with open("fairfax.txt", 'w') as f:
#     f.write("#{}\n".format("Fairfax"))
#
#     f.write("\n")
#
#     for k,v in tqdm(intersection_map.items(), desc="Write Ints"):
#         f.write("-{}\n".format(v["name"]))
#         for r in v["roads"]:
#             if r["end"] is not None:
#                 r["end"] = intersection_map[r["end"]]["name"]
#             f.write("{},{},{},{}\n".format(r["name"], r["length"], r["lanes"], r["end"]))
