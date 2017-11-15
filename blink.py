from dependencies import *
from person_objects import *
from road_objects import *

colors = colors.Colors()
"""
Helper
"""
def displayNetwork(road_network):
    for rid in road_network:
        # print("\n{}{}{}".format(colors.PURPLE + colors.BOLD, rid, colors.ENDC))
        cprint("\n{}".format(rid), 'magenta', attrs=['bold'])
        for iid in road_network[rid].intersections:
            print("\n---> {}{}{}".format(colors.GREEN, iid, colors.ENDC))
            print("-------> {}Entering Lanes{}".format(colors.UNDERLINE, colors.ENDC))
            for slid in road_network[rid].intersections[iid].startLanes:
                print("-------> {}{}{}".format(colors.BLUE,slid, colors.ENDC))
            print("-------> {}Exiting Lanes{}".format(colors.UNDERLINE, colors.ENDC))
            for elid in road_network[rid].intersections[iid].endLanes:
                if road_network[rid].intersections[iid].endLanes[elid].ped:
                    print("-------> {}{}{}".format(colors.BLUE + colors.BOLD,elid,colors.ENDC))
                print("-------> {}{}{}".format(colors.BLUE,elid,colors.ENDC))

"""
Generate road networks
"""

"""
Randomly generates road network
1 Region
3-5 Intersections
2-3 Lanes To Each Intersection
"""
def randomly_generate():
    # road_network = {}
    root = Region()
    road_network = {root.id:root}

    for i in range(random.randint(3,5)):
        int_obj = Intersection(root.id)
        int_id = int_obj.id
        root.intersections[int_id] = int_obj

    #Vehicle Lanes
    l_est = len(root.intersections)*4
    for l in range(l_est): 
        start = random.choice( list(root.intersections.keys()) )
        end = start
        while end == start:
            end = random.choice( list(root.intersections.keys()) )

        lane_obj = Lane(root.id, start, end)
        root.intersections[start].startLanes[lane_obj.id] = lane_obj
        root.intersections[end].endLanes[lane_obj.id] = lane_obj

    #Pedestrian Lanes
    l_est = len(root.intersections)*2
    for l in range(l_est): 
        start = random.choice( list(root.intersections.keys()) )
        end = start
        while end == start:
            end = random.choice( list(root.intersections.keys()) )

        lane_obj = Lane(root.id, start, end, True)
        root.intersections[start].startLanes[lane_obj.id] = lane_obj
        root.intersections[end].endLanes[lane_obj.id] = lane_obj

    return road_network

road_network = randomly_generate()
displayNetwork(road_network)
# road_network[0].start()
# regions[0].start()