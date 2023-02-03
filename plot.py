from matplotlib import pyplot as plt

from classes import Polygon


def plot_polygon(polygon: Polygon) -> None:
    """Plot a Polygon object into a closed polygon using matplotlib."""
    x = [point.x for point in polygon.points]
    y = [point.y for point in polygon.points]
    x.append(x[0])
    y.append(y[0])

    # Plot the polygon
    plt.plot(x, y, polygon.colour)
