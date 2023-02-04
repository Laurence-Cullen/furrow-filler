import matplotlib.pyplot as plt

from classes import Polygon, Point
from plot import plot_polygon
from svg_loader import load_polygon_from_svg


def closest_points(polygon1: Polygon, polygon2: Polygon) -> tuple[Point, Point]:
    """Identify the closest approach between two polygons."""
    distance = float('inf')
    closest_point1 = polygon1.points[0]
    closest_point2 = polygon2.points[0]

    for point1 in polygon1.points:
        for point2 in polygon2.points:
            if point1.distance_to(point2) < distance:
                distance = point1.distance_to(point2)
                closest_point1 = point1
                closest_point2 = point2

    return closest_point1, closest_point2


def n_closest_point_pairs(polygon1: Polygon, polygon2: Polygon, n: int) -> list[tuple[Point, Point]]:
    """Identify the n closest point pairs between two polygons."""
    # create a dict with a key of the distance between two points and a value of the two points
    distances = {}
    for point1 in polygon1.points:
        for point2 in polygon2.points:
            distances[point1.distance_to(point2)] = (point1, point2)

    # extract the n closest points from the dict
    closest_points = []
    for distance in sorted(distances)[:n]:
        closest_points.append(distances[distance])
    return closest_points


def find_unique_points(point_pairs: list[tuple[Point, Point]]) -> (set[Point], set[Point]):
    """Find the unique points in a list of point pairs."""
    unique_points1 = set()
    unique_points2 = set()
    for point1, point2 in point_pairs:
        unique_points1.add(point1)
        unique_points2.add(point2)
    return unique_points1, unique_points2


def sort_points_by_index(points: list[Point]) -> list[Point]:
    """Sort a list of points by their index."""
    return sorted(points, key=lambda point: point.index)


def fuse_polygons(polygon1: Polygon, polygon2: Polygon) -> Polygon:
    """Fuse two polygons together."""
    # find the closest points between the two polygons
    closest_point_pairs = n_closest_point_pairs(polygon1, polygon2, 25)
    unique_points1, unique_points2 = find_unique_points(closest_point_pairs)

    # sort unique points
    unique_points1 = sort_points_by_index(unique_points1)
    unique_points2 = sort_points_by_index(unique_points2)

    # combine unique points
    unique_points = unique_points1 + unique_points2

    # create a new polygon from the unique points
    return Polygon(unique_points, 'g')


if __name__ == '__main__':
    left = load_polygon_from_svg('left.svg', 'r')
    plot_polygon(left)

    right = load_polygon_from_svg('right.svg', 'b')
    plot_polygon(right)

    # create a new polygon from the unique points
    fused = fuse_polygons(left, right)
    plot_polygon(fused)

    # invert y axis of plot
    plt.gca().invert_yaxis()

    plt.show()
