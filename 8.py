import math
from functools import reduce

def polygon_area(polygon):
    x = [pt[0] for pt in polygon]
    y = [pt[1] for pt in polygon]
    return 0.5 * abs(sum(x[i]*y[(i+1)%len(polygon)] - x[(i+1)%len(polygon)]*y[i] for i in range(len(polygon))))

def polygon_sides(polygon):
    return [math.dist(polygon[i], polygon[(i+1)%len(polygon)]) for i in range(len(polygon))]

def dist_to_origin(point):
    return math.sqrt(point[0]**2 + point[1]**2)


def agr_origin_nearest_reduce(polygons):
    '''Функция, выбирающая полигон с углом ближе к началу координат'''
    def reducer(poly1, poly2):
        nearest1 = min(poly1, key=dist_to_origin)
        nearest2 = min(poly2, key=dist_to_origin)
        return poly1 if dist_to_origin(nearest1) < dist_to_origin(nearest2) else poly2
    return reduce(reducer, polygons)

def agr_max_side_reduce(polygons):
    '''Выбирает максимум длины стороны среди всех полигонов'''
    def reducer(max_side, polygon):
        current_max = max(polygon_sides(polygon)) if polygon else 0
        return max(max_side, current_max)
    return reduce(reducer, polygons, 0)

def agr_min_area_reduce(polygons):
    '''Выбирает полигон с минимальной площадью'''
    def reducer(poly1, poly2):
        return poly1 if polygon_area(poly1) < polygon_area(poly2) else poly2
    return reduce(reducer, polygons)

# проверка

square = ((1,1),(1,3),(3,3),(3,1))
triangle = ((-1,-1),(0,2),(2,0))
pentagon = ((0,0),(2,1),(3,3),(1,4),(-1,3))

polygons = [square, triangle, pentagon]

nearest_polygon = agr_origin_nearest_reduce(polygons)
nearest_point = min(nearest_polygon, key=dist_to_origin)
print("Полигоны с вершиной ближайшей к началу координат:", nearest_polygon)
print("Самая близкая вершина:", nearest_point)

max_side_length = agr_max_side_reduce(polygons)
print("Максимальная длина стороны среди всех полигонов:", max_side_length)

min_area_polygon = agr_min_area_reduce(polygons)
print("Полигон с минимальной площадью:", min_area_polygon)
print("Площадь этого полигона:", polygon_area(min_area_polygon))
