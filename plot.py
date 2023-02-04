import shapely.geometry as sg
from matplotlib import pyplot as plt


def plot_polygon(polygon: sg.Polygon, colour: str) -> None:
    """Plot a Polygon object into a closed polygon using matplotlib."""
    x, y = polygon.exterior.xy
    plt.fill(x, y, colour)
