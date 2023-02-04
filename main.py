import matplotlib.pyplot as plt
import shapely.geometry as sg
from shapely.geometry import Polygon, Point

from plot import plot_polygon
from svg_loader import load_polygon_from_svg


def n_shortest_connector_lines(p1: Polygon, p2: Polygon, n: int) -> list[tuple[sg.LineString, int, int]]:
    """Identify the n closest connecting lines between two Polygon objects."""
    # create a dict with a key of the distance between two points and a value of a tuple
    # of an sg.Line object between the two points and the index of the point in polygon1 and polygon2
    lines = {}
    for i, point1 in enumerate(p1.exterior.coords):
        for j, point2 in enumerate(p2.exterior.coords):
            line = sg.LineString([point1, point2])
            distance = line.length
            lines[distance] = (line, i, j)

    # extract the n shortest lines
    shortest_lines = []
    for i, (distance, (line, i1, i2)) in enumerate(sorted(lines.items())):  # sort the dict by key
        if i < n:
            shortest_lines.append((line, i1, i2))
        else:
            break

    return shortest_lines


def find_unique_points(lines: list[tuple[sg.LineString, int, int]]) -> tuple[
    list[tuple[int, Point]], list[tuple[int, Point]]]:
    """Find the unique points indices from a list of shapely LineString objects and index integers."""
    # create a set of unique i and j indices
    unique_i = set()
    unique_j = set()
    for line, i, j in lines:
        unique_i.add((i, Point(line.xy[0][0], line.xy[1][0])))
        unique_j.add((j, Point(line.xy[0][1], line.xy[1][1])))

    return list(unique_i), list(unique_j)


def sort_points_by_index(points: list[tuple[int, Point]]) -> list[Point]:
    """Sort a list of points by their index."""
    # sort points by index
    points.sort(key=lambda x: x[0])

    # remove the index from the tuple
    points = [point for _, point in points]

    return points


def point_at_line_end(line: sg.LineString, point: Point) -> bool:
    """Check if a point is at the end of a line."""
    # check if point matches the start of the line
    if point.x == line.coords[0][0] and point.y == line.coords[0][1]:
        return True

    # check if point matches the end of the line
    if point.x == line.coords[1][0] and point.y == line.coords[1][1]:
        return True
    return False


def remove_lines_intersecting_with_polygon(polygon: Polygon, lines: list[tuple[sg.LineString, int, int]]) -> list[
    tuple[sg.LineString, int, int]]:
    """Remove any shapely LineString objects that intersect with the edges of Polygon."""
    # for each line determine the intersection with the polygon
    return_lines = []
    for line, i, j in lines:
        intersection = polygon.intersection(line)

        # if intersection is of type LineString, GeometryCollection or MultiLineString then continue
        if not isinstance(intersection, Point):
            print(intersection)
            continue

        # Check if intersection has the same value as either point in LineString
        if point_at_line_end(line, point=intersection):
            return_lines.append((line, i, j))
        elif intersection.is_empty:
            return_lines.append((line, i, j))

    return return_lines


def fuse_polygons(polygon1: Polygon, polygon2: Polygon) -> Polygon:
    """Fuse two polygons together."""
    # find the closest points between the two polygons
    closest_lines = n_shortest_connector_lines(polygon1, polygon2, 25)

    # remove intersecting lines
    # closest_lines = remove_lines_intersecting_with_polygon(polygon1, closest_lines)
    closest_lines = remove_lines_intersecting_with_polygon(polygon2, closest_lines)

    unique_points1, unique_points2 = find_unique_points(closest_lines)

    # sort unique points
    unique_points1 = sort_points_by_index(unique_points1)
    unique_points2 = sort_points_by_index(unique_points2)

    # combine unique points
    unique_points = unique_points1 + unique_points2

    # create a new polygon from the unique points
    return Polygon(unique_points)


if __name__ == '__main__':
    left = load_polygon_from_svg('left0.svg')
    plot_polygon(left, 'r')

    right = load_polygon_from_svg('right0.svg')
    plot_polygon(right, 'b')

    # create a new polygon from the unique points
    fused = fuse_polygons(left, right)
    fused = fused.convex_hull
    plot_polygon(fused, 'g')

    # invert y axis of plot
    plt.gca().invert_yaxis()

    plt.show()
