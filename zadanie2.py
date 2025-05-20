import itertools
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def gen_rectangle(start_x=0, side=1, gap=0.3):
    width = side
    height = side
    x = start_x
    while True:
        poly = ((x, 0), (x, height), (x + width, height), (x + width, 0))
        yield poly
        x += width + gap

def gen_triangle(start_x=0, side=1, gap=0.3):
    height = math.sqrt(3)/2 * side
    x = start_x
    while True:
        poly = ((x, 0), (x + side/2, height), (x + side, 0))
        yield poly
        x += side + gap

def gen_hexagon(start_x=0, side=0.577, gap=0.3):
    angle_step = math.pi / 3
    width = 2 * side * math.cos(math.pi / 6)  # ~1
    x = start_x
    while True:
        points = []
        for i in range(6):
            px = x + side * math.cos(angle_step * i)
            py = side * math.sin(angle_step * i)
            points.append((px, py))
        min_y = min(p[1] for p in points)
        points = [(px, py - min_y) for px, py in points]  # выравнивание по нижней грани y=0
        yield tuple(points)
        x += width + gap

def visualize_polygons(polygons, count=10):
    fig, ax = plt.subplots()
    for poly in itertools.islice(polygons, count):
        patch = Polygon(poly, closed=True, edgecolor='black', facecolor='none', lw=1.5)
        ax.add_patch(patch)
    ax.set_aspect('equal')
    ax.autoscale_view()
    plt.grid(True)
    plt.show()

def combined_sequence():
    gap = 0.3
    side_rect = 1
    side_tri = 1
    side_hex = 0.577

    rects = gen_rectangle(start_x=0, side=side_rect, gap=gap)
    start_x_tris = 2 * (side_rect + gap)
    tris = gen_triangle(start_x=start_x_tris, side=side_tri, gap=gap)
    start_x_hex = start_x_tris + 2 * (side_tri + gap) + gap
    hexes = gen_hexagon(start_x=start_x_hex, side=side_hex, gap=gap)

    return itertools.chain(
        itertools.islice(rects, 2),
        itertools.islice(tris, 2),
        itertools.islice(hexes, 3)
    )

if __name__ == "__main__":
    seq = combined_sequence()
    visualize_polygons(seq, count=7)
