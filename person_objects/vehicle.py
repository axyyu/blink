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
        
        # For GUI Purposes
        r = lambda: random.randint(0,255)
        self.color = '#%02X%02X%02X'.format(r(),r(),r())

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self.id)[:5]

    """
    Calculate the remaining possible destinations using the movement history
    """
    def add_location(self, intersection):
        self.movement_history.append(intersection)

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
    """
    def __gt__(self, other):
        return self.id > other.id