import pickle


"""
Global Params

Edit file inputs and outputs here.
"""
output_file = "sample"
length = 5
lanes = 2
inject_rate = .7

"""
Hardcoded Network
"""
intersection_map = {}

intersection_map[(0,0)] = {
    "road_ids": {},
    "road_names": {"Road 0,0 to 1,0", "Road 0,0 to 0,1", "Road 0,0 to Nowhere", "Road 0,0 to Nowhere 2"},
    "roads":[
        {
            "name": "Road 0,0 to 1,0",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (1,0)
        },
        {
            "name": "Road 0,0 to 0,1",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (0,1)
        },
        {
            "name": "Road 0,0 to Nowhere",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        },
        {
            "name": "Road 0,0 to Nowhere 2",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        }
    ]
}

intersection_map[(0,1)] = {
    "road_ids": {},
    "road_names": {"Road 0,1 to 1,1", "Road 0,1 to 0,0", "Road 0,1 to Nowhere", "Road 0,1 to Nowhere 2"},
    "roads":[
        {
            "name": "Road 0,1 to 1,1",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (1,1)
        },
        {
            "name": "Road 0,1 to 0,0",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (0,0)
        },
        {
            "name": "Road 0,1 to Nowhere",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        },
        {
            "name": "Road 0,1 to Nowhere 2",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        }
    ]
}

intersection_map[(1,0)] = {
    "road_ids": {},
    "road_names": {"Road 1,0 to 1,1", "Road 1,0 to 0,0", "Road 1,0 to Nowhere", "Road 1,0 to Nowhere 2"},
    "roads":[
        {
            "name": "Road 1,0 to 1,1",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (1,1)
        },
        {
            "name": "Road 1,0 to 0,0",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (0,0)
        },
        {
            "name": "Road 1,0 to Nowhere",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        },
        {
            "name": "Road 1,0 to Nowhere 2",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        }
    ]
}

intersection_map[(1,1)] = {
    "road_ids": {},
    "road_names": {"Road 1,1 to 0,1", "Road 1,1 to 1,0", "Road 1,1 to Nowhere", "Road 1,1 to Nowhere 2"},
    "roads":[
        {
            "name": "Road 1,1 to 0,1",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (0,1)
        },
        {
            "name": "Road 1,1 to 1,0",
            "length": length,
            "lanes": lanes,
            "am_inject_rate": inject_rate,
            "pm_exit_rate": inject_rate,
            "yellow_clearance": 2,
            "end": (1,0)
        },
        {
            "name": "Road 1,1 to Nowhere",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        },
        {
            "name": "Road 1,1 to Nowhere 2",
            "length": None,
            "lanes": None,
            "am_inject_rate": None,
            "pm_exit_rate": None,
            "yellow_clearance": None,
            "end": None
        }
    ]
}

with open(output_file, 'wb') as f:
    pickle.dump(intersection_map, f, protocol=pickle.HIGHEST_PROTOCOL)