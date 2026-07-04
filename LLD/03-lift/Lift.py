from enums import LiftStatus, Direction
from Request import Request
from collections import defaultdict
class Lift:
    def __init__(self, id):
        self.status = LiftStatus.Stationary
        self.id = id
        self.currentFloor = 0
        self.direction = None
        self.destinations = set()
        self.sources = set()
        self.destinationSourceMap = defaultdict(set)
    
    def getCurrentFloor(self):
        return self.getCurrentFloor
    
    def assign(self, request: Request):
        self.destinations.add(request.destination)
        self.sources.add(request.source)

        if self.status == LiftStatus.Stationary:
            if self.currentFloor > request.source:
                self.destinations = Direction.Down
            elif self.currentFloor < request.source:
                self.destinations = Direction.Up
            else:
                self.open()
    
    def open(self):
        if self.currentFloor in self.destinations:
            self.destinations.remove(self.currentFloor)
        if self.currentFloor in self.sources:
            self.sources.remove(self.currentFloor)

    def move(self):
        if len(self.destinations) == 0 and len(self.sources) == 0:
            self.direction = None
            self.status = LiftStatus.Stationary
            return
        
        if not self.direction or self.status == LiftStatus.Stationary:
            floor, direction = self.getClosestFLoor()
            self.direction = direction
            self.status = LiftStatus.Running

        if self.direction == Direction.Down:
            if self.currentFloor - 1 >= 0:
                self.currentFloor -= 1
            else:
                self.currentFloor = 0
        else:
            if self.currentFloor + 1 <= 9:
                self.currentFloor += 1
            else:
                self.currentFloor = 9
        
        if self.currentFloor == 9 or self.currentFloor == 0: