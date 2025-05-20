import math
import itertools
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def gen_rectangle():
    i = 0
    while True:
        yield ((i*1.2, 0), (i*1.2 + 1, 0), (i*1.2 + 1, 1), (i*1.2, 1))
        i += 1

def gen_triangle():
    i = 0
    while True:
        yield ((i*1.2, 0), (i*1.2 + 0.5, 1), (i*1.2 + 1, 0))
        i += 1

def gen_hexagon():
    i = 0
    side = 0.5
    h = math.sqrt(3)*side
    while True:
        x0 = i * (side*3)
        yield (
            (x0 + side, 0),
            (x0 + 2*side, 0),
            (x0 + 3*side, h/2),
            (x0 + 2*side, h),
            (x0 + side, h),
            (x0, h/2)
        )
        i += 1

def tr_translate(polygons, dx, dy):
    return map(lambda poly: tuple((x+dx, y+dy) for x,y in poly), polygons)

def tr_rotate(polygons, angle_rad):
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    def rotate_poly(poly):
        return tuple((x*cos_a - y*sin_a, x*sin_a + y*cos_a) for x,y in poly)
    return map(rotate_poly, polygons)

def visualize(polygons_sequences, colors, labels, title):
    plt.figure(figsize=(10,6))
    ax = plt.gca()
    max_polygons = 15
    for polys, color, label in zip(polygons_sequences, colors, labels):
        polys_list = list(itertools.islice(polys, max_polygons))
        for poly in polys_list:
            patch = Polygon(poly, closed=True, edgecolor=color, facecolor='none', lw=2)
            ax.add_patch(patch)
        patch = Polygon(polys_list[0], closed=True, edgecolor=color, facecolor='none', lw=3, label=label)
        ax.add_patch(patch)
    ax.set_aspect('equal')
    ax.set_xlim(-1, 20)
    ax.set_ylim(-5, 10)
    ax.grid(True)
    ax.legend()
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    angle_deg = 30
    angle = math.radians(angle_deg)

    rects = gen_rectangle()
    tris = gen_triangle()
    hexs = gen_hexagon()

    rects_rot = tr_rotate(rects, angle)
    tris_rot = tr_rotate(tris, angle)
    hexs_rot = tr_rotate(hexs, angle)

    dir_vec = (math.cos(angle), math.sin(angle))
    # вектор для смещения
    normal_vec = (-math.sin(angle), math.cos(angle))
    spacing = 1.5

    # смещение лент
    rects_shifted = tr_translate(rects_rot, normal_vec[0]*spacing*0, normal_vec[1]*spacing*0)
    tris_shifted = tr_translate(tris_rot, normal_vec[0]*spacing*1, normal_vec[1]*spacing*1)
    hexs_shifted = tr_translate(hexs_rot, normal_vec[0]*spacing*2, normal_vec[1]*spacing*2)

    visualize(
        [rects_shifted, tris_shifted, hexs_shifted],
        ['blue', 'green', 'orange'],
        ['Прямоугольники', 'Треугольники', 'Шестиугольники'],
        f'Три параллельных ленты под углом {angle_deg}°'
    )
