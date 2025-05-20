import matplotlib.pyplot as plt
import math
from matplotlib.patches import Polygon

def point_on_ray(angle_deg, dist):
    rad = math.radians(angle_deg)
    return dist * math.cos(rad), dist * math.sin(rad)

def create_trapezoid(angle1, angle2, r1, r2):
    p1 = point_on_ray(angle1, r1)
    p2 = point_on_ray(angle2, r1)
    p3 = point_on_ray(angle2, r2)
    p4 = point_on_ray(angle1, r2)
    return [p1, p2, p3, p4]

def reflect_polygon(polygon):
    return [(-x, -y) for (x, y) in polygon]

angle1 = 30
angle2 = 60

num_trapezoids = 5
start_r = 2
thickness = 3.5
step = 4.0

fig, ax = plt.subplots(figsize=(8, 8))

for i in range(num_trapezoids):
    r1 = start_r + i * step
    r2 = r1 + thickness
    trap = create_trapezoid(angle1, angle2, r1, r2)
    ax.add_patch(Polygon(trap, closed=True, edgecolor='black', facecolor='black'))

    mirrored_trap = reflect_polygon(trap)
    ax.add_patch(Polygon(mirrored_trap, closed=True, edgecolor='black', facecolor='black'))

L = 40
for angle in [angle1, angle2, 210, 240]:
    x = [-L * math.cos(math.radians(angle)), L * math.cos(math.radians(angle))]
    y = [-L * math.sin(math.radians(angle)), L * math.sin(math.radians(angle))]
    ax.plot(x, y, color='gray', linestyle='--', linewidth=1)

ax.set_xlim(-40, 40)
ax.set_ylim(-40, 40)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("задание 4.4")
plt.show()
