"""
Road Object

"""
from dependencies import *
from person_objects import *

angle_error = .1

class Road:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

        self.end_intersection = None
        self.queue = []
        self.lane_dir = []

        self.directions = {}

    def __str__(self):
        return "{} {}".format(self.name, self.queue)

    def __repr__(self):
        return "{}_{}".format(self.name, str(self.id)[:5])
        # return "{}_{}, {}, {}".format(self.name, str(self.id)[:5], self.directions, self.lane_dir)

    def set_intersection(self, i):
        self.end_intersection = i

    def set_lane(self, road):
        if self.end == road.start and self.start == road.end:
            return

        a = np.subtract(self.end, self.start)
        b = np.subtract(road.end, road.start)

        a = a / np.linalg.norm(a)
        b = b / np.linalg.norm(b)

        dot = a[0]*-b[1] + a[1]*b[0]

        if dot > 0+angle_error:
            self.directions["right"] = road
        elif dot < 0-angle_error:
            self.directions["left"] = road
        self.directions["straight"] = road

    """
    Init
    """
    def init(self):
        if self.end_intersection:
            self.queue = [ [ 0 for b in range(self.length) ] for a in range(self.lanes) ]
            self.lane_dir = [ [] for b in range(self.lanes)]

            straight_start = 0
            straight_end = self.lanes

            if "right" in self.directions:
                self.lane_dir[-1].append("right")
                straight_end -= 1
            
            if "left" in self.directions:
                self.lane_dir[0].append("left")
                straight_start += 1

            for l in range(straight_start, straight_end):
                if "straight" in self.directions:
                    self.lane_dir[l].append("straight")
                elif "left" in self.directions:
                    self.lane_dir[l].append("left")
                elif "right" in self.directions:
                    self.lane_dir[l].append("right")

            if self.lanes < 3:
                if "straight" in self.directions:
                    self.lane_dir[-1].append("straight")



    """
    Road Methods
    """
    def update(self):
        for lane in range(self.lanes):
            for slot in range(1, self.length):
                if self.queue[lane][slot] != 0:
                    for l in random.sample([lane, lane-1, lane+1], 3):
                        if l >= 0 and l < self.lanes:
                            if self.queue[l][slot-1] == 0:
                                self.queue[l][slot-1] = self.queue[lane][slot]
                                self.queue[lane][slot] = 0
                                break

    def setup_ratios(self, day):
        """
        1 - Night
        0 - Day
        """
        if day >= 0:
            self.inject_rate = self.am_inject_rate * day
            self.exit_rate = .01 * day
        else:
            self.inject_rate = .01 * abs(day)
            self.exit_rate = self.pm_exit_rate * abs(day)

    """
    Road Detection Info
    """
    def count_vehicles(self):
        count = 0
        if self.end_intersection:
            for lane in range(self.lanes):
                for slot in range(self.length):
                    if self.queue[lane][slot] != 0:
                        count+=1
            return count
        return 0

    """ Returns open lane """
    def detect_back(self):
        if self.end_intersection:
            for lane in random.sample(range(self.lanes), self.lanes):
                if self.queue[lane][-1] == 0:
                    return lane
            return None
        return False

    """
    Vehicle Methods
    """
    def add_vehicle(self):
        if self.end_intersection:
            lane = self.detect_back()
            if lane:
                self.queue[lane][-1] = Vehicle()

    def remove_vehicle(self):
        if self.end_intersection:
            for lane in random.sample(range(self.lanes), self.lanes):
                for slot in random.sample(range(self.length), self.length):
                    if self.queue[lane][slot] != 0:
                        self.queue[lane][slot] == 0
        return None

    def pass_vehicles(self):
        car_count = 0
        if self.end_intersection:
            for l in range(len(self.queue)):
                if self.queue[l][0] != 0:
                    if len(self.lane_dir[l]) > 0:
                        direction = random.choice(self.lane_dir[l])
                        target = self.directions[direction]
                        target_lane = target.detect_back()
                        if target_lane:
                            target.queue[target_lane][-1] = self.queue[l][0]
                            self.queue[l][0] = 0
                            if target.end_intersection:
                                target.end_intersection.alert(1)
                            car_count += 1
        return car_count

    """
    Vehicle Injection and Removal
    """
    def randomly_inject(self, day):
        self.setup_ratios(day)

        inject = exit = 0
        if self.end_intersection:
            if random.random() < self.exit_rate:
                self.remove_vehicle()
                exit+=1
            if random.random() < self.inject_rate:
                self.add_vehicle()
                inject+=1
        return inject, exit
