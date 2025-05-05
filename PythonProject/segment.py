from node import Distance
from node import Node
class Segment:
    def __init__(self, name, origin, destination) :
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)

    def __repr__(self):
        return f"Segment({self.name}, Origin: {self.origin.name}, Destination: {self.destination.name}, Cost: {self.cost})"

