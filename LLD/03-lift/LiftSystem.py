from Lift import Lift
from enums import Direction
from Request import Request
class LiftSystem:
    def __init__(self, liftCt, floorCt):
        self.lifts = [Lift(i+1) for i in range(liftCt)]
        self.totalFloors = floorCt
        self.floors = [i for i in range(floorCt+1)]
        self.requests = []

    def request(self, source, destination):
        req = Request(source, destination)
        minSteps = float('inf')
        closestLift = None
        for lift in self.lifts:
            if lift.direction == Direction.Down:
                if lift.currentFloor >- source:
                    steps = lift.currentFloor - source
                else:
                    steps = lift.currentFloor + source
            elif lift.direction == Direction.Up:
                if lift.currentFloor <= source:
                    steps = source - lift.currentFloor 
                else:
                    steps = (self.totalFloors-  lift.currentFloor) + (self.self.totalFloors - source)
            else:
                steps = abs(lift.currentFloor - source)
        
            closestLift = lift if steps < minSteps else closestLift
        closestLift.assign(req)

    def step():
        
            
        
