import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def rectangle_at(i):
    base_x = i * 1.2
    return ((base_x, 0), (base_x + 1, 0), (base_x + 1, 1), (base_x, 1))

def triangle_at(i):
    base_x = i * 1.2
    return ((base_x, 0), (base_x + 0.3, 1.2), (base_x + 0.6, 0))

def tr_translate(poly, dx, dy):
    return tuple((x+dx, y+dy) for x,y in poly)

def tr_rotate(poly, angle_rad):
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    return tuple((x*cos_a - y*sin_a, x*sin_a + y*cos_a) for x,y in poly)

def visualize(polygons_sequences, colors, labels, title):
    plt.figure(figsize=(10,8))
    ax = plt.gca()
    for polys, color, label in zip(polygons_sequences, colors, labels):
        for poly in polys:
            patch = Polygon(poly, closed=True, edgecolor=color, facecolor='none', lw=2)
            ax.add_patch(patch)
        patch = Polygon(polys[0], closed=True, edgecolor=color, facecolor='none', lw=3, label=label)
        ax.add_patch(patch)
    ax.set_aspect('equal')
    ax.set_xlim(-10, 20)
    ax.set_ylim(-10, 20)
    ax.grid(True)
    ax.legend()
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    angle_rect_deg = 30
    angle_tri_deg = 15
    angle_rect = math.radians(angle_rect_deg)
    angle_tri = math.radians(angle_tri_deg)

    intersection_point = (5, 2)

    indices = range(-7, 8)

    rects = []
    for i in indices:
        poly = rectangle_at(i)
        poly_rot = tr_rotate(poly, angle_rect)
        poly_shift = tr_translate(poly_rot, intersection_point[0], intersection_point[1])
        rects.append(poly_shift)

    tris = []
    for i in indices:
        poly = triangle_at(i)
        poly_rot = tr_rotate(poly, angle_tri)
        poly_shift = tr_translate(poly_rot, intersection_point[0], intersection_point[1])
        tris.append(poly_shift)

    visualize(
        [rects, tris],
        ['blue', 'green'],
        ['лента 1', 'лента 2'],
        'Две пересекающиеся ленты под разными углами'
    )
