class Passenger(object):

    def __init__(self, start_floor, destination):
        self.start_floor = start_floor
        self.destination = destination
        self.time_cost = 0

    def increment_timecost(self, cost = 1):
        self.time_cost += cost
