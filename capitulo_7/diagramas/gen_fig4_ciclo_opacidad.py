import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')

# Title
ax.text(0, 1.65, 'Ciclo de opacidad financiera', fontsize=18, fontweight='bold',
        ha='center', va='center', color='#1b4332')
ax.text(0, 1.45, 'Deficiencias interrelacionadas en la gestión financiera de Rústico Pizza y Pan',
        fontsize=10, ha='center', va='center', color='#555555')

# 6 nodes in a circle
labels = [
    'Registros de ventas\nincompletos',
    'Gastos sin\ncategorizar',
    'Costeo\ndesactualizado',
    'Efectivo no\nbancarizado',
    'Sin reportes\nfinancieros',
    'Decisiones\npor intuición'
]

details = [
    '8 días sin registro\n65% cobertura por producto',
    '9 compras no registradas\n$7,430 subregistro',
    '8 meses sin actualizar\nQueso +23.8%, Harina +25%',
    '40-50% fuera del banco\n$2,370 sin conciliar',
    'Sin estado de resultados\nSin flujo de caja formal',
    '"Mucho en el instinto\ny en la experiencia"'
]

colors = ['#2d6a4f', '#40916c', '#52b788', '#e9c46a', '#f4a261', '#e76f51']
text_colors = ['white', 'white', '#1b4332', '#1b4332', '#1b4332', 'white']

n = 6
angles = [np.pi/2 - i * 2 * np.pi / n for i in range(n)]
radius = 1.1
node_radius = 0.38

positions = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

# Draw arrows between consecutive nodes (circular)
for i in range(n):
    x1, y1 = positions[i]
    x2, y2 = positions[(i + 1) % n]
    dx = x2 - x1
    dy = y2 - y1
    dist = np.sqrt(dx**2 + dy**2)
    shrink = node_radius / dist
    ax.annotate('', xy=(x2 - dx * shrink, y2 - dy * shrink),
                xytext=(x1 + dx * shrink, y1 + dy * shrink),
                arrowprops=dict(arrowstyle='->', color='#666666', lw=2,
                                connectionstyle='arc3,rad=0.15'))

# Draw nodes
for i, (x, y) in enumerate(positions):
    circle = plt.Circle((x, y), node_radius, facecolor=colors[i],
                         edgecolor='#333333', linewidth=2, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y + 0.05, labels[i], fontsize=9, fontweight='bold',
            ha='center', va='center', color=text_colors[i], zorder=6)
    detail_radius = 1.7
    dx, dy = detail_radius * np.cos(angles[i]), detail_radius * np.sin(angles[i])
    ax.text(dx, dy, details[i], fontsize=7, ha='center', va='center',
            color='#444444', style='italic', zorder=6,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f9fa',
                      edgecolor='#cccccc', alpha=0.9))

# Center label
ax.text(0, 0, 'CICLO DE\nOPACIDAD', fontsize=12, fontweight='bold',
        ha='center', va='center', color='#e76f51')

plt.tight_layout()
plt.savefig('/mnt/c/Users/HG_Co/OneDrive/Documents/Github/rustico/capitulo_7/diagramas/fig4_ciclo_opacidad.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fig4 generated successfully")
