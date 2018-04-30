from tqdm import tqdm
import shapefile
import pickle

#####################################################################
#       Blink - Create Network
# Generates a network file readable by the Blink simulation. Requires
# a shapefile.
#####################################################################

"""
Global Params

Edit file inputs and outputs here.
"""
input_files = "DC_shapefile/Street_Centerlines"
output_file = "washington"
permitted_road_types = [
    "STREET",
    "ROAD",
    "AVENUE",
    "DRIVE",
]
name_index = 9
type_index = 14
dir_index = 16
len_index = -1
quad_index = 15

#####################################################################
#       SHAPEFILES
#####################################################################

def obtain_shapefile_data():
    """
    Retrieves records (vector-assigned data) and shapes (vectors) from the
    shapefiles.
    """
    sf = shapefile.Reader(input_files)
    return sf.records(), sf.shapes()

#####################################################################
#       INTERSECTIONS
#####################################################################

def add_point(int_map, p, r):
    road_name = records[r][name_index] + " " + records[r][quad_index]
    if p not in int_map:
        int_map[p] = {
            "road_ids": set(),
            "road_names": set(),
            "roads": []
        }

    int_map[p]["road_ids"].add(r)
    int_map[p]["road_names"].add(road_name)

def find_intersections():
    """
    Finds intersections between road vectors.
    """
    int_map = {}
    for r in tqdm(range(len(shapes)), desc="Finding Intersections"):
        road_type = records[r][type_index]
        dir_type = records[r][dir_index]

        if road_type in permitted_road_types:
            # if dir_type == "One way (Against digitizing direction)":
            #     add_point(int_map, shapes[r].points[-1],r)
            # elif dir_type == "One way (Digitizing direction)":
            #     add_point(int_map, shapes[r].points[0],r)
            # else:
            for p in shapes[r].points:
                add_point(int_map, p, r)

    return int_map

def filter_intersections(int_map):
    """
    Filters intersections by the number of road names. An intersection with
    less than 2 unique road names is assumed to lead beyond the scope of the
    algorithm.
    """
    filtered_map = {}
    for key,value in tqdm(int_map.items(), desc="Filtering Intersections"):
        if len(value["road_names"]) > 1:
            filtered_map[key] = value

    return filtered_map

#####################################################################
#       ROADS
#####################################################################

def add_road(filtered_map, road_id, start, end):
    if not end:
        road = {
            "name": records[road_id][name_index],
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        }
    else:
        speed_limit = (25 + 10) / 3600 # in meters per second
        road_length = records[road_id][len_index] # In meters
        average_vehicle_length = 4.5 # In meters

        delay_distance = speed_limit * 2 # meters
        car_interval = average_vehicle_length + delay_distance # meters
        length = max(1, int(road_length / car_interval))
        yellow_clearance = max(3, int(1.4 + (1.47*speed_limit)/(2*10)) ) # seconds

        road_type = records[road_id][type_index]

        lanes = 1
        am_inject_rate = .64
        pm_exit_rate = .7

        road = {
            "name": records[road_id][name_index],
            "length": length,
            "lanes": lanes,
            "am_inject_rate": am_inject_rate,
            "pm_exit_rate": pm_exit_rate,
            "yellow_clearance": yellow_clearance,
            "end": end
        }
    filtered_map[start]["roads"].append(road)

def find_end(int_map, filtered_map, start_id, road_id, count):
    """
    Finds the end of the road.
    """
    if count > 3:
        return None

    # p_index = shapes[road_id].index(start_id)
    # if p_index == 0:
    #     if shapes[road_id][-1] in filtered_map:
    #         return p
    # elif p_index == len(shapes[road_id])-1:
    #     if shapes[road_id][0] in filtered_map:
    #         return p

    for p in shapes[road_id].points:
        if p != start_id:
            if p in filtered_map:
                return p

    road_name = records[road_id][name_index]
    for p in shapes[road_id].points:
        if p != start_id:

            possible_roads = [r for r in int_map[p]["road_ids"]
                if records[r][name_index] == road_name and r != road_id]

            for r in possible_roads:
                possible_end = find_end(int_map, filtered_map, start_id, r, count+1)
                if possible_end:
                    return possible_end
    return None

def define_roads(int_map, filtered_map):
    """
    Adds data for each road to the intersections.
    """
    for key,value in tqdm(filtered_map.items(), desc="Setting Up Roads"):
        intersection_name = "{}".format(str(value["road_names"]))
        value["name"] = intersection_name

        for r in value["road_ids"]:
            try:
                end = find_end(int_map, filtered_map, key, r, 0)
            except:
                end = None

            add_road(int_map, r, key, end)

#####################################################################
#       SAVING
#####################################################################

def write_to_file(filtered_map):
    """
    Pickles intersection map. This is the network object.
    """
    with open(output_file, 'wb') as f:
        pickle.dump(filtered_map, f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    records, shapes = obtain_shapefile_data()
    int_map = find_intersections()
    filtered_map = filter_intersections(int_map)
    define_roads(int_map, filtered_map)
    write_to_file(filtered_map)
