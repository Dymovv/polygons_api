import matplotlib.pyplot as plt
import math
import numpy as np

def shift_polygon(polygon, dx=0, dy=0):
    return tuple((x+dx, y+dy) for x,y in polygon)

def plot_polygons_list(polygons_lists, titles):
    n = len(polygons_lists)
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
    axes = axes.flatten() if n > 1 else [axes]

    for ax in axes[n:]:
        ax.axis('off')

    for ax, polys, title in zip(axes, polygons_lists, titles):
        for i, poly in enumerate(polys):
            shifted = shift_polygon(poly, dx=i*2.5)
            x, y = zip(*shifted)
            ax.fill(x + (x[0],), y + (y[0],), alpha=0.5)
            ax.plot(x + (x[0],), y + (y[0],), 'k-')
        ax.set_title(title)
        ax.set_aspect('equal')
        ax.grid(True)
    plt.tight_layout()
    plt.show()

# --- вспомогательные функции ---

def is_convex(polygon):
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    signs = []
    n = len(polygon)
    for i in range(n):
        c = cross(polygon[i], polygon[(i+1)%n], polygon[(i+2)%n])
        signs.append(c > 0)
    return all(signs) or not any(signs)

def polygon_area(polygon):
    x = [p[0] for p in polygon]
    y = [p[1] for p in polygon]
    return 0.5*abs(sum(x[i]*y[(i+1)%len(polygon)] - x[(i+1)%len(polygon)]*y[i] for i in range(len(polygon))))

def polygon_sides(polygon):
    return [math.dist(polygon[i], polygon[(i+1)%len(polygon)]) for i in range(len(polygon))]

def point_eq(p1, p2, eps=1e-9):
    return abs(p1[0]-p2[0])<eps and abs(p1[1]-p2[1])<eps

# Фильтры из п.5

def flt_convex_polygon(polygons):
    return list(filter(is_convex, polygons))

def flt_angle_point(polygons, point):
    # Фильтрует фигуры с углом, совпадающим с point
    return [p for p in polygons if any(point_eq(corner, point) for corner in p)]

def flt_square(polygons, min_area=0.5):
    return [p for p in polygons if polygon_area(p) >= min_area]

def flt_short_side(polygons, min_length=0.3):
    def has_short_side(p):
        return any(side < min_length for side in polygon_sides(p))
    return [p for p in polygons if not has_short_side(p)]

def flt_point_inside(polygons, point):
    # Проверка, лежит ли point внутри выпуклого многоугольника (используем метод с углами)
    def inside(poly, pt):
        def angle(a, b, c):
            import math
            def vector(p1, p2):
                return (p2[0]-p1[0], p2[1]-p1[1])
            import math
            va = vector(pt, a)
            vb = vector(pt, b)
            dot = va[0]*vb[0]+va[1]*vb[1]
            cross = va[0]*vb[1]-va[1]*vb[0]
            return math.atan2(abs(cross), dot)
        total = 0
        n = len(poly)
        for i in range(n):
            total += angle(poly[i], poly[(i+1)%n], pt)
        return abs(total - 2*math.pi) < 1e-3
    return [p for p in polygons if is_convex(p) and inside(p, point)]

def flt_polygon_angles_inside(polygons, polygon):
    # Фильтрует выпуклые полигоны, у которых хотя бы один угол внутри polygon
    return [p for p in polygons if is_convex(p) and any(
        flt_point_inside([p], angle)[0] if flt_point_inside([p], angle) else False
        for angle in polygon)]

# --- Исходные полигоны для примера ---
polygons = [
    ((0,0),(1,0),(1,1),(0,1)),               # квадрат
    ((0,0),(2,0),(1,3)),                     # треугольник
    ((0,0),(1,0),(1,0.5),(0.5,1),(0,1)),    # выпуклый пятиугольник
    ((0,0),(1,0),(1,0.1),(0.5,0.5),(0,1)),  # невыпуклый
    ((0,0),(0.5,0),(0.5,0.4),(0,0.4)),      # маленький прямоугольник
    ((0,0),(0.3,0),(0.3,0.3),(0,0.3)),      # еще меньше
]

# Параметры для фильтров, которые требуют аргументы
point_for_angle = (0,0)
point_inside = (0.5, 0.5)
polygon_for_angles = polygons[0]

# Создаем списки фигур после фильтрации
filters_results = [
    flt_convex_polygon(polygons),
    flt_angle_point(polygons, point_for_angle),
    flt_square(polygons, min_area=0.5),
    flt_short_side(polygons, min_length=0.4),
    flt_point_inside(polygons, point_inside),
    flt_polygon_angles_inside(polygons, polygon_for_angles),
]

titles = [
    'Выпуклые многоугольники',
    'Все фигуры',
    'Площадь >= 0.5',
    'Без коротких сторон < 0.4',
    'Без невыпуклых',
    'Наибольшая площадь',
]

plot_polygons_list(filters_results, titles)
