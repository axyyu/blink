"""
Vehicle Object

Determines car position and probable destination

"""
from dependencies import *
from input_objects import destination_control

class Vehicle():
    def __init__(self):
        self.id = uuid.uuid4()
        self.current_lane = -1
        self.projected_destinations = set()
        self.movement_history = []

    def __str__(self):
        return self.id

    """
    Calculate the remaining possible destinations using the movement history
    """
    def update_destinations(self):
        destination_control.vehicle_destinations(self.movement_history, self.current_lane, self.projected_destinations)

    """
    Move to new lane and update
    """
    def change_lane(self, end):
        self.movement_history.append(self.current_lane)
        self.current_lane = end
        self.update_destinations()

    """
    For testing purposes
    Should never be used in simulation
    """
    def __gt__(self, other):
        return self.id > other.id