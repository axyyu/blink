"""
Where you input region control methods
"""

"""
Main Method - Do Not Edit Headers

Returns dict with cycle times
Keys - Road Name
Value - Cycle Time
{'RoadNameN_S': 5, 'RoadNameE_W': 5}
"""
def congestion(lane):
    cars = 0
    if len(lane) != 0:
        for x in lane:
            if x != 0:
                cars+=1
        return cars/len(lane)
def run(time, intersection):
    mRoads = intersection.roads
    compare = {}
    for x in mRoads:
        sum = 0
        for y in mRoads[x]['enter']:
            for i in y.queue:
                sum+=congestion(i)
                #print(x, congestion(i))
        for z in mRoads[x]['exit']:
            for i in z.queue:
                sum+=congestion(i)
                #print(x, congestion(i))
        compare[x] = sum
    list = []
    for x in mRoads:
        list.append(x)
    x, y = list[0], list[1]
    arr = []
    if compare[x] > compare[y]:
        arr.append(intersection.cycle_times[x] + 1)
        arr.append(intersection.cycle_times[y] - 1)
    if compare[y] > compare[x]:
        arr.append(intersection.cycle_times[x] - 1)
        arr.append(intersection.cycle_times[y] + 1)
    print(intersection.cycle_times, arr)
    return arr
