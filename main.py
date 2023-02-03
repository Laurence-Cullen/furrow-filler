import matplotlib.pyplot as plt

from plot import plot_polygon
from svg_loader import load_polygon_from_svg

if __name__ == '__main__':
    left = load_polygon_from_svg('left.svg', 'r')
    plot_polygon(left)

    right = load_polygon_from_svg('right.svg', 'b')
    plot_polygon(right)

    # fused = fuse_polygons_concave_hull(left, right)
    # plot_polygon(fused)

    # invert y axis of plot
    plt.gca().invert_yaxis()

    plt.show()
