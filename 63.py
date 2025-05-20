import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from itertools import islice, cycle
from shapely.geometry import Polygon as ShPolygon


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


def tr_translate(polygon, dx=0, dy=0):
    return tuple((x + dx, y + dy) for x, y in polygon)


def plot_polygons(polygons, title):
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = ['red', 'green', 'blue', 'orange', 'purple']

    all_x = [x for poly in polygons for (x, y) in poly]
    all_y = [y for poly in polygons for (x, y) in poly]
    margin = 2
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

    for i, poly in enumerate(polygons):
        poly_patch = Polygon(poly, closed=True, fill=True, alpha=0.5, color=colors[i % len(colors)], edgecolor='black')
        ax.add_patch(poly_patch)
        cx = sum(x for x, y in poly) / len(poly)
        cy = sum(y for x, y in poly) / len(poly)
        ax.text(cx, cy, str(i + 1), ha='center', va='center', fontsize=10, weight='bold')

    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True)
    plt.show()


def polygons_intersect(p1, p2):
    sp1 = ShPolygon(p1)
    sp2 = ShPolygon(p2)
    return sp1.intersects(sp2)


# Создаем 15 фигур с пересечениями

rects = gen_rectangle()
tris = gen_triangle()
hexs = gen_hexagon()

base_polygons = list(islice(rects, 5)) + list(islice(tris, 5)) + list(islice(hexs, 5))
scales = [1, 0.8, 1.2, 0.6, 1.0]  # разные масштабы

# Создаем фигуры с пересечениями, сдвигая их близко друг к другу (меньший шаг сдвига)
polygons = []
x_offset = 0
y_offset = 0
dx = 1.5  # меньше ширины, чтобы пересекались
dy = 1.2
for idx, (poly, scale) in enumerate(zip(base_polygons, cycle(scales))):
    scaled = tr_homothety(poly, scale)
    shifted = tr_translate(scaled, dx=x_offset, dy=y_offset)
    polygons.append(shifted)
    x_offset += dx
    y_offset += dy

plot_polygons(polygons, "15 фигур с пересечениями")


# Фильтрация пересекающихся фигур — оставляем только те, которые не пересекаются с предыдущими

def filter_non_intersecting(polygons):
    filtered = []
    for poly in polygons:
        if all(not polygons_intersect(poly, fp) for fp in filtered):
            filtered.append(poly)
    return filtered


filtered_polygons = filter_non_intersecting(polygons)

plot_polygons(filtered_polygons, "Отфильтрованные непересекающиеся фигуры")
print(f"Было фигур: {len(polygons)}, осталось после фильтрации: {len(filtered_polygons)}")
