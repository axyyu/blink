"""
Where you input destination control methods
"""

"""
Calculate the remaining possible destinations using the movement history

Args:
* history
* current
* destinations

Returns:
* set of destinations
"""
def pedestrian_destinations(history,current,destinations):
    pass

def vehicle_destinations(history,current,destinations):
    for h in history:
        destinations.discard(h)