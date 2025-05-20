import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def extend_line_both_sides(angle_deg, length=50):
    rad = math.radians(angle_deg)
    dx = length * math.cos(rad)
    dy = length * math.sin(rad)
    return (-dx, -dy), (dx, dy)

def vector_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def vector_mul(v, scalar):
    return (v[0] * scalar, v[1] * scalar)

def vector_len(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)

def vector_norm(v):
    length = vector_len(v)
    return (v[0] / length, v[1] / length)

def trapezoids_between_lines(angle1_deg, angle2_deg, count=6, base_length=2.0, height=1.0, spacing=1.0):
    v1 = (math.cos(math.radians(angle1_deg)), math.sin(math.radians(angle1_deg)))
    v2 = (math.cos(math.radians(angle2_deg)), math.sin(math.radians(angle2_deg)))
    bisect = vector_norm(vector_add(v1, v2))
    trapezoids = []
    for i in range(count):
        dist = spacing + i * (base_length + spacing)
        p_bottom1 = vector_mul(v1, dist)
        p_bottom2 = vector_mul(v2, dist)
        p_top_offset = vector_mul(bisect, height)
        p_top1 = vector_add(p_bottom1, p_top_offset)
        p_top2 = vector_add(p_bottom2, p_top_offset)
        trapezoids.append((p_bottom1, p_bottom2, p_top2, p_top1))
    return trapezoids

# Функция для отрисовки трапеций на оси
def draw_trapezoids(ax, trapezoids, color, alpha=0.7):
    for poly in trapezoids:
        patch = Polygon(poly, closed=True, facecolor=color, edgecolor='black', alpha=alpha)
        ax.add_patch(patch)

# Генерация линий
def plot_lines(ax):
    # Линии 30° и 60°
    line1_start, line1_end = extend_line_both_sides(30, length=50)
    line2_start, line2_end = extend_line_both_sides(60, length=50)
    ax.plot([line1_start[0], line1_end[0]], [line1_start[1], line1_end[1]], 'r-', lw=2)
    ax.plot([line2_start[0], line2_end[0]], [line2_start[1], line2_end[1]], 'b-', lw=2)

    # Линии 210° и 240°
    line3_start, line3_end = extend_line_both_sides(210, length=50)
    line4_start, line4_end = extend_line_both_sides(240, length=50)
    ax.plot([line3_start[0], line3_end[0]], [line3_start[1], line3_end[1]], 'r--', lw=2)
    ax.plot([line4_start[0], line4_end[0]], [line4_start[1], line4_end[1]], 'b--', lw=2)

# Создание трапеций
traps_1 = trapezoids_between_lines(30, 60, count=6, base_length=2, height=1, spacing=1)
traps_2 = trapezoids_between_lines(210, 240, count=6, base_length=2, height=1, spacing=1)

# Объединяем для удобства фильтрации
all_traps = traps_1 + traps_2

# Фильтрация — оставим по 3 трапеции в каждой группе (итого 6)
filtered_traps = traps_1[:3] + traps_2[:3]

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# До фильтра
axes[0].set_title('До фильтрации (все трапеции)')
plot_lines(axes[0])
draw_trapezoids(axes[0], all_traps[:6], 'orange')
draw_trapezoids(axes[0], all_traps[6:], 'green')
axes[0].legend()
axes[0].set_xlim(-60, 60)
axes[0].set_ylim(-60, 60)
axes[0].set_aspect('equal')
axes[0].grid(True)
axes[0].axhline(0, color='gray', lw=0.5)
axes[0].axvline(0, color='gray', lw=0.5)

# После фильтра
axes[1].set_title('После фильтрации (6 трапеций)')
plot_lines(axes[1])
draw_trapezoids(axes[1], filtered_traps[:3], 'orange')
draw_trapezoids(axes[1], filtered_traps[3:], 'green')
axes[1].legend()
axes[1].set_xlim(-60, 60)
axes[1].set_ylim(-60, 60)
axes[1].set_aspect('equal')
axes[1].grid(True)
axes[1].axhline(0, color='gray', lw=0.5)
axes[1].axvline(0, color='gray', lw=0.5)

plt.show()
