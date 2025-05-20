import math
from functools import wraps
from collections.abc import Iterable

# --- Вспомогательные функции ---

def polygon_area(polygon):
    # Площадь многоугольника по формуле Гаусса (положительная)
    x = [pt[0] for pt in polygon]
    y = [pt[1] for pt in polygon]
    area = 0.5 * abs(sum(x[i]*y[(i+1)%len(polygon)] - x[(i+1)%len(polygon)]*y[i] for i in range(len(polygon))))
    return area

def polygon_sides(polygon):
    # Длины сторон многоугольника
    sides = []
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1)%len(polygon)]
        sides.append(math.dist((x1,y1),(x2,y2)))
    return sides

def is_convex(polygon):
    # Проверка выпуклости многоугольника
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    n = len(polygon)
    signs = []
    for i in range(n):
        signs.append(cross(polygon[i], polygon[(i+1)%n], polygon[(i+2)%n]) > 0)
    return all(signs) or not any(signs)

def point_equals(p1, p2, eps=1e-9):
    return abs(p1[0]-p2[0]) < eps and abs(p1[1]-p2[1]) < eps

# --- Фильтры ---

def flt_convex_polygon(polygons):
    return filter(is_convex, polygons)

def flt_angle_point(point):
    def inner(polygons):
        return filter(lambda p: any(point_equals(v, point) for v in p), polygons)
    return inner

def flt_square(min_area):
    def inner(polygons):
        return filter(lambda p: polygon_area(p) >= min_area, polygons)
    return inner

def flt_short_side(max_len):
    def inner(polygons):
        return filter(lambda p: min(polygon_sides(p)) < max_len, polygons)
    return inner

def flt_point_inside(point):
    # Для выпуклых: проверяем, что точка внутри многоугольника
    def inside(polygon):
        def sign(p1, p2, p3):
            return (p1[0]-p3[0])*(p2[1]-p3[1])-(p2[0]-p3[0])*(p1[1]-p3[1])
        n = len(polygon)
        pos = neg = False
        for i in range(n):
            s = sign(point, polygon[i], polygon[(i+1)%n])
            if s > 0:
                pos = True
            elif s < 0:
                neg = True
            if pos and neg:
                return False
        return True
    def inner(polygons):
        return filter(lambda p: is_convex(p) and inside(p), polygons)
    return inner

def flt_polygon_angles_inside(reference_polygon):
    def inner(polygons):
        ref_points = reference_polygon
        def any_angle_inside(polygon):
            return any(flt_point_inside(pt)([polygon]) for pt in ref_points)
        return filter(lambda p: is_convex(p) and any_angle_inside(p), polygons)
    return inner

# --- Трансформации ---

def tr_translate(polygon, dx, dy):
    return tuple((x+dx, y+dy) for (x,y) in polygon)

def tr_rotate(polygon, angle_deg, center=(0,0)):
    angle_rad = math.radians(angle_deg)
    cx, cy = center
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    def rot_point(p):
        x, y = p
        x -= cx
        y -= cy
        x_new = x*cos_a - y*sin_a + cx
        y_new = x*sin_a + y*cos_a + cy
        return (x_new, y_new)
    return tuple(rot_point(p) for p in polygon)

def tr_symmetry(polygon, axis='x'):
    if axis == 'x':
        return tuple((x, -y) for (x,y) in polygon)
    elif axis == 'y':
        return tuple((-x, y) for (x,y) in polygon)
    else:
        raise ValueError("axis must be 'x' or 'y'")

def tr_homothety(polygon, scale, center=(0,0)):
    cx, cy = center
    return tuple(((x-cx)*scale+cx, (y-cy)*scale+cy) for (x,y) in polygon)

# --- Декораторы ---

def filter_polygons_in_args(filter_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            new_args = [filter_func(arg) if isinstance(arg, Iterable) and not isinstance(arg, (str, bytes)) else arg for arg in args]
            new_kwargs = {k: filter_func(v) if isinstance(v, Iterable) and not isinstance(v, (str, bytes)) else v for k,v in kwargs.items()}
            return func(*new_args, **new_kwargs)
        return wrapper
    return decorator

def transform_polygons_in_args(transform_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            new_args = [map(transform_func, arg) if isinstance(arg, Iterable) and not isinstance(arg, (str, bytes)) else arg for arg in args]
            new_kwargs = {k: map(transform_func, v) if isinstance(v, Iterable) and not isinstance(v, (str, bytes)) else v for k,v in kwargs.items()}
            return func(*new_args, **new_kwargs)
        return wrapper
    return decorator

# --- Демонстрация ---

@filter_polygons_in_args(flt_convex_polygon)
@filter_polygons_in_args(flt_square(1.5))
def print_filtered_polygons(polygons):
    print("Отфильтрованные полигоны:")
    for p in polygons:
        print(p)

@transform_polygons_in_args(lambda p: tr_translate(p, 10, 10))
def print_translated_polygons(polygons):
    print("Трансформированные полигоны (сдвиг на (10,10)):")
    for p in polygons:
        print(p)

# --- Примерные полигоны ---

square = ((0,0),(0,2),(2,2),(2,0))
small_square = ((0,0),(0,1),(1,1),(1,0))
triangle = ((0,0),(2,0),(1,2))
concave = ((0,0),(2,0),(1,1),(2,2),(0,2))

polygons = [square, small_square, triangle, concave]

# --- Запуск ---

print_filtered_polygons(polygons)
print()
print_translated_polygons(polygons)
