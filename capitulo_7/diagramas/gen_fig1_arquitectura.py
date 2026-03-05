import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(5, 6.6, 'Arquitectura del sistema de gestión financiera modular',
        fontsize=14, fontweight='bold', ha='center', color='#1b4332')

def draw_mod(ax, x, y, title, subtitle, color, tc='white'):
    w, h = 2.6, 1.1
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle='round,pad=0.15', facecolor=color,
                           edgecolor='#1b4332', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y + 0.15, title, fontsize=9, fontweight='bold',
            ha='center', va='center', color=tc)
    ax.text(x, y - 0.2, subtitle, fontsize=7.5,
            ha='center', va='center', color=tc)

# Top row: POS centered
draw_mod(ax, 5, 5.5, 'Módulo 1: Punto de Venta', '(POS)', '#2d6a4f')

# Middle row: Costos + Tesorería + Nómina
draw_mod(ax, 1.8, 3.5, 'Módulo 2: Costos', 'e Inventario', '#40916c')
draw_mod(ax, 5, 3.5, 'Módulo 3: Flujo de Caja', 'y Tesorería', '#52b788', '#1b4332')
draw_mod(ax, 8.2, 3.5, 'Módulo 4: Nómina', 'Simplificada', '#74c69d', '#1b4332')

# Bottom row: Reportes centered
draw_mod(ax, 5, 1.5, 'Módulo 5: Reportes', 'y Dashboard', '#95d5b2', '#1b4332')

# Arrows: simple, clean
def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1.8))

# POS -> 3 middle modules
arrow(ax, 3.8, 5.0, 2.2, 4.1)   # POS -> Costos
arrow(ax, 5.0, 4.95, 5.0, 4.1)  # POS -> Tesorería
arrow(ax, 6.2, 5.0, 7.8, 4.1)   # POS -> (skip, not direct)

# Middle -> Reportes
arrow(ax, 2.2, 2.95, 3.8, 2.1)  # Costos -> Reportes
arrow(ax, 5.0, 2.95, 5.0, 2.1)  # Tesorería -> Reportes
arrow(ax, 7.8, 2.95, 6.2, 2.1)  # Nómina -> Reportes

# Cross connections (middle row)
arrow(ax, 3.1, 3.5, 3.7, 3.5)   # Costos -> Tesorería
arrow(ax, 6.7, 3.5, 6.3, 3.5)   # Nómina -> Tesorería

# Labels on arrows
ax.text(3.3, 4.7, 'Ventas del día', fontsize=6.5, ha='center', color='#666', rotation=25)
ax.text(4.6, 4.5, 'Ingresos', fontsize=6.5, ha='center', color='#666')
ax.text(3.4, 3.7, 'Costo MP', fontsize=6, ha='center', color='#666')
ax.text(6.5, 3.7, 'Nómina', fontsize=6, ha='center', color='#666')

plt.tight_layout()
plt.savefig('/mnt/c/Users/HG_Co/OneDrive/Documents/Github/rustico/capitulo_7/diagramas/fig1_arquitectura_sistema.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fig1 generated successfully")
