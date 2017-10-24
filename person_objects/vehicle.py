"""
Vehicle Object

Determines car position and probable destination

"""
from dependencies import *

class Vehicle():
    def __init__(self):
        self.id = uuid.uuid4() # or licence plate number
        self.current_lane = -1
        self.projected_destinations = set()
        self.movement_history = []

    """
    Calculate the remaining possible destinations using the movement history
    """
    def update_destinations(self):
        # all_intersections = []
        for m in self.movement_history:
            self.projected_destinations.discard(m)

    """
    Move to new lane and update
    """
    def change_lane(self, end):
        self.movement_history.append(self.current_lane)
        self.current_lane = end
        self.update_destinations()