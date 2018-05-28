import pickle
import uuid


"""
Global Params

Edit file inputs and outputs here.
"""
output_file = "sample"
length = 10
lanes = 3
inject_rate = .5
yellow_clearance = 2

width = 2 # Dimensions of returned network
height = 2

"""
Sample Network Generation
"""
intersection_map = {}

def valid_point(x, y):
    if x >= 0 and x < width and y >= 0 and y < height:
        return True
    return False

def add_road(name, start, end):
    if valid_point(*end):
        one = start
        two = end
        if one[0] < two[0] or one[1] < two[1]:
            one = end
            two = start

        return {
                    "id": uuid.uuid4(),
                    "name": "Road {}".format(name),
                    "length": length,
                    "lanes": lanes,
                    "am_inject_rate": inject_rate,
                    "pm_exit_rate": inject_rate,
                    "yellow_clearance": yellow_clearance,
                    "start": start,
                    "end": end
                }
    else:
        return {
                    "id": uuid.uuid4(),
                    "name": "Road {}".format(name),
                    "length": None,
                    "lanes": None,
                    "am_inject_rate": None,
                    "pm_exit_rate": None,
                    "yellow_clearance": None,
                    "start": start,
                    "end": end
                }

for x in range(width):
    for y in range(height):
        intersection_map[(x,y)] = {
            "id": uuid.uuid4(),
            "name": "{},{}".format(x,y),
            "roads":[]
        }

        start = (x,y)

        for a in [-1, 1]:
            end = (x+a, y)
            intersection_map[(x,y)]["roads"].append(add_road("Y{}".format(y), start, end))

            end = (x, y+a)
            intersection_map[(x,y)]["roads"].append(add_road("X{}".format(x), start, end))

with open(output_file, 'wb') as f:
    pickle.dump(intersection_map, f, protocol=pickle.HIGHEST_PROTOCOL)