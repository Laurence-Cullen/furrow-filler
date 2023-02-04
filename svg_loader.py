import re

from shapely.geometry import Polygon, Point


def load_polygon_from_svg(filename: str) -> Polygon:
    """Load a Polygon from an SVG file."""

    svg_regex = r"points=\"((.|\n)*)\"/>"

    with open(filename, 'r') as f:
        svg = f.read()
    points_string = re.findall(svg_regex, svg)[0][0]

    # remove newline characters
    points_string = points_string.replace('\n', '')

    # remove all non space whitespace characters
    points_string = re.sub(r'\s+', ' ', points_string)

    # remove double quote characters
    points_string = points_string.replace('"', '')

    # remove trailing space
    points_string = points_string.strip()

    # split points_string into a list of strings
    points_string_list = points_string.split(' ')
    # convert each string in points_string_list into a Point object
    points = [Point(*map(float, point_string.split(','))) for i, point_string in enumerate(points_string_list)]
    return Polygon(points)
