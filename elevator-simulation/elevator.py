from passenger import Passenger
from utilities import calc_direction, custom_max, custom_min

class Elevator(object):

    def __init__(self, n_floors, max_people = 10):
        self.calls = [] ## calls from people outside the elevator
        self.floor = 0 ## current floor
        self.n_floors = n_floors ## number of floors
        self.direction = 1 ## 1 if going up, -1 if going down, starts at 0 due to inital floor
        self.destinations = [] ## calls from people inside the elevator
        self.max_people = max_people ## maximum number of people allowed inside

    def move_FIFO(self, target):
        self.snapshot() ## prints current floor, direction, and destinations
        self.floor = target ## moves elevator to target

    def move_one(self):
        self.snapshot() ## prints current floor, direction, and destinations
        self.floor += self.direction ## moves one floor according to direction

    def pickup_dropoff(self):
        for call in self.calls: ## loops through all calls
            passenger = call[3] ## passenger that made the call
            ## picks up passenger if there is a call on their floor 
            ## that goes on current direction and if there is space left
            if call[0] == self.floor and call[2] == self.direction and len(self.destinations) < self.max_people:
                self.add_destination(passenger) ## if picks up passenger, add their destination to list
                self.calls.remove(call) ## if picks up, remove call from list
            passenger.time_cost += 1 ## increase cost by 1 to all passengers waiting for pickup

        # Check for dropoffs (destination) on this floor
        for dest in self.destinations:
            passenger = dest[1] ## passenger with the destination
            if dest[0] == self.floor: ## if there is a dest in the current floor, dropoff
                self.destinations.remove(dest) ## remove from dests list
            passenger.time_cost += 1 ## increase cost by 1 to all passengers waiting for dropoff

    def FIFO(self): ## first in, first out strategy
        first_call = self.calls[0] ## prioritizes call waiting for longest time
        passenger = first_call[3] ## passenger that made call
        ## distance ran by elevator with no one inside
        empty_elevator_dist = abs(self.floor - passenger.start_floor)
        self.move_FIFO(passenger.destination) ## move elevator to passenger destination
        distance = abs(passenger.start_floor - passenger.destination) ## distance travelled in elevator
        ## update everyone's wait time_cost
        for call in self.calls:
            call[3].time_cost += distance + empty_elevator_dist
        del self.calls[0] ## delete the call just attended

    def move_to_max_min(self):
        if self.direction == 1: ## if moving up
            ## destinations of people going up still outside elevator
            ## most elevators would not have this info in advance
            upwards_dropoffs_outside = [i[1] for i in self.calls if i[2] == 1]
            ## destinations of people going up inside elevator 
            upwards_dropoffs_inside = [i[0] for i in self.destinations if i[0] >= self.floor]
            ## set with all destinations
            upwards_dropoffs = set(upwards_dropoffs_outside + upwards_dropoffs_inside)
            ## all calls going down
            downwards_pickups = [i[0] for i in self.calls if i[2] == -1]
            ## finds max that the elevator will reach, defined as the max between the
            ## max destination, and the max downward call
            max_up_dest = custom_max(upwards_dropoffs,downwards_pickups)
            ## pickup/dropoff and move until reaching max point
            while self.floor < max_up_dest:
                self.pickup_dropoff()
                self.move_one()
        elif self.direction == -1: ## if moving down
            ## destinations of people going down still outside elevator
            downwards_dropoffs_outside = [i[1] for i in self.calls if i[2] == -1]
            ## destinations of people going down inside elevator
            downwards_dropoffs_inside = [i[0] for i in self.destinations if i[0] <= self.floor]
            ## set with all such destinations
            downwards_dropoffs = set(downwards_dropoffs_outside + downwards_dropoffs_inside)
            ## all calls going up
            upwards_pickups = [i[0] for i in self.calls if i[2] == 1]
            ## the converse of max_up_dest
            min_down_dest = custom_min(downwards_dropoffs,upwards_pickups)
            ## pickup/dropoff and move until reaching min point
            while self.floor > min_down_dest:
                self.pickup_dropoff()
                self.move_one()

    def max_floor_strategy(self):
        ## firstly, pickup-dropoff people in the initial state of elevator
        self.pickup_dropoff()
        ## while there are calls or destinations
        while self.calls or self.destinations:
            ## move to max/min point while picking up / dropping off
            self.move_to_max_min()
            ## change direction when point is reached
            self.direction = -self.direction
            self.pickup_dropoff()

    def add_call(self, call_floor, dest, Passenger):
        direction = calc_direction(call_floor, dest)
        self.calls.append([call_floor, dest, direction, Passenger])

    def add_destination(self, Passenger):
        self.destinations.append([Passenger.destination, Passenger])

    def snapshot(self):
        print "\nElevator Snapshot","\nCurrent Floor: ", self.floor, "\nDirection: ", self.direction, "\nDestinations: ", [i[0] for i in self.destinations]