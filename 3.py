import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def tr_translate(polygons, dx, dy):
    def translate(poly):
        return tuple((x + dx, y + dy) for x, y in poly)
    return list(map(translate, polygons))

def tr_rotate(polygons, angle_rad):
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    def rotate(poly):
        return tuple((
            x * cos_a - y * sin_a,
            x * sin_a + y * cos_a
        ) for x, y in poly)
    return list(map(rotate, polygons))

def tr_symmetry(polygons, axis='y'):
    if axis == 'y':
        def sym(poly):
            return tuple((-x, y) for x, y in poly)
    elif axis == 'x':
        def sym(poly):
            return tuple((x, -y) for x, y in poly)
    else:
        raise ValueError("axis must be 'x' or 'y'")
    return list(map(sym, polygons))

def tr_homothety(polygons, k):
    def scale(poly):
        return tuple((x * k, y * k) for x, y in poly)
    return list(map(scale, polygons))

def visualize_single(polygons, title):
    fig, ax = plt.subplots(figsize=(6,6))

    xs = [x for poly in polygons for x, y in poly]
    ys = [y for poly in polygons for x, y in poly]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)

    for poly in polygons:
        patch = Polygon(poly, closed=True, edgecolor='black', facecolor='none', lw=1.5)
        ax.add_patch(patch)

    ax.set_title(title)
    ax.set_xlim(xmin - 1, xmax + 1)
    ax.set_ylim(ymin - 1, ymax + 1)
    ax.set_aspect('equal')
    ax.grid(True)

    plt.show()

if __name__ == "__main__":
    def generate_squares(n, step=2):
        for i in range(n):
            x = i * step
            yield ((x,0), (x+1,0), (x+1,1), (x,1))

    original = list(generate_squares(5))
    steps = [original]

    t1 = tr_translate(steps[-1], 1, 1)
    steps.append(t1)
    t2 = tr_rotate(t1, math.pi/2)
    steps.append(t2)
    t3 = tr_symmetry(t2, 'y')
    steps.append(t3)
    t4 = tr_homothety(t3, 0.5)
    steps.append(t4)

    titles = [
        "Исходные полигоны",
        "После параллельного переноса",
        "После поворота на 90°",
        "После симметрии по Y",
        "После гомотетии (k=0.5)"
    ]

    for polys, title in zip(steps, titles):
        visualize_single(polys, title)
