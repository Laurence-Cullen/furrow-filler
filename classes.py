class Point:
    """Represents a point in 2-D space."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Polygon:
    """Represents a polygon in 2-D space."""

    def __init__(self, points: list[Point], colour: str):
        self.points = points
        self.colour = colour
