import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from itertools import islice, cycle


def gen_rectangle():
    w, h = 2, 1
    while True:
        yield ((0, 0), (w, 0), (w, h), (0, h))


def gen_triangle():
    side = 2
    h = math.sqrt(3) / 2 * side
    while True:
        yield ((0, 0), (side, 0), (side / 2, h))


def gen_hexagon():
    side = 1
    h = math.sqrt(3) * side
    while True:
        yield (
            (0, 0), (side, 0),
            (1.5 * side, h / 2),
            (side, h),
            (0, h),
            (-0.5 * side, h / 2),
        )


def tr_homothety(polygon, k):
    return tuple((x * k, y * k) for x, y in polygon)


def flt_short_side(polygon, threshold):
    def side_length(a, b):
        return math.dist(a, b)

    n = len(polygon)
    shortest = min(side_length(polygon[i], polygon[(i + 1) % n]) for i in range(n))
    return shortest < threshold


def shift_polygon(polygon, dx=0, dy=0):
    return tuple((x + dx, y + dy) for x, y in polygon)


def plot_polygons(polygons, title):
    fig, ax = plt.subplots(figsize=(14, 10))
    colors = ['red', 'green', 'blue', 'orange', 'purple']

    all_x = [x for poly in polygons for (x, y) in poly]
    all_y = [y for poly in polygons for (x, y) in poly]
    margin = 1
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

    for i, poly in enumerate(polygons):
        poly_patch = Polygon(poly, closed=True, fill=True, alpha=0.6, color=colors[i % len(colors)], edgecolor='black')
        ax.add_patch(poly_patch)
        cx = sum(x for x, y in poly) / len(poly)
        cy = sum(y for x, y in poly) / len(poly)
        ax.text(cx, cy, str(i + 1), ha='center', va='center', fontsize=10, weight='bold')

    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True)
    plt.show()


# --- Основная логика ---

rects = gen_rectangle()
tris = gen_triangle()
hexs = gen_hexagon()

base_polygons = list(islice(rects, 5)) + list(islice(tris, 5)) + list(islice(hexs, 5))
scales = [0.5, 0.7, 1.0, 1.5, 2.0]

# Параметры сетки
cols = 5  # количество фигур в ряду
rows = 3  # количество рядов
spacing_x = 6
spacing_y = 6

scaled_polygons = []

for idx, (poly, scale) in enumerate(zip(base_polygons, cycle(scales))):
    scaled = tr_homothety(poly, scale)
    col = idx % cols
    row = idx // cols
    dx = col * spacing_x
    dy = -row * spacing_y  # минус, чтобы идти вниз по оси Y
    shifted = shift_polygon(scaled, dx=dx, dy=dy)
    scaled_polygons.append(shifted)

plot_polygons(scaled_polygons, "15 фигур разного масштаба в сетке")

threshold = 1.0
filtered = list(filter(lambda p: flt_short_side(p, threshold), scaled_polygons))
filtered = filtered[:4]

plot_polygons(filtered, f"Фигуры с кратчайшей стороной < {threshold} (не более 4)")
