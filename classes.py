class Point:
    """Represents a point in 2-D space."""

    def __init__(self, x: float, y: float, index: int = None):
        self.x = x
        self.y = y
        self.index = index

    def distance_to(self, other: 'Point') -> float:
        """Calculate the distance between two points."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Polygon:
    """Represents a polygon in 2-D space."""

    def __init__(self, points: list[Point], colour: str):
        self.points = points
        self.colour = colour
