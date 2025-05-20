import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def triangle_at(i):
    base_x = i * 1.2
    return ((base_x, 0), (base_x + 0.3, 1.2), (base_x + 0.6, 0))

def tr_translate(poly, dx, dy):
    return tuple((x+dx, y+dy) for x,y in poly)

def tr_symmetry(poly):
    return tuple((x, -y) for x,y in poly)

def visualize(polygons_sequences, colors, labels, title):
    plt.figure(figsize=(10,6))
    ax = plt.gca()
    for polys, color, label in zip(polygons_sequences, colors, labels):
        for poly in polys:
            patch = Polygon(poly, closed=True, edgecolor=color, facecolor='none', lw=2)
            ax.add_patch(patch)
        patch = Polygon(polys[0], closed=True, edgecolor=color, facecolor='none', lw=3, label=label)
        ax.add_patch(patch)
    ax.set_aspect('equal')
    ax.set_xlim(-5, 15)
    ax.set_ylim(-3, 5)
    ax.grid(True)
    ax.legend()
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    indices = range(-7, 8)

    tris1 = [triangle_at(i) for i in indices]

    offset_y = 3  # расстояние между лентами
    tris2 = [tr_translate(tr_symmetry(triangle_at(i)), 0, offset_y) for i in indices]

    visualize(
        [tris1, tris2],
        ['blue', 'red'],
        ['Лента 1', 'симметричная лента 2'],
        'задание с симметрией'
    )
