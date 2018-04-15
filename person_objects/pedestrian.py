"""
Pedestrian Object

Determines pedestrian position and probable destination

"""
from dependencies import *

class Pedestrian():
    def __init__(self):
        self.id = uuid.uuid4()
        self.current_lane = -1
        self.projected_destinations = set()
        self.movement_history = []

    """
    Calculate the remaining possible destinations using the movement history
    """
    def update_destinations(self):
        destination_control.pedestrian_destinations(self.movement_history, self.current_lane, self.projected_destinations)

    """
    Move to new lane and update
    """
    def change_lane(self, end):
        self.movement_history.append(self.current_lane)
        self.current_lane = end
        self.update_destinations()
