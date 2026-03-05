import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(6, 8.5, 'Arquitectura del sistema de gestión financiera modular',
        fontsize=16, fontweight='bold', ha='center', color='#1b4332')
ax.text(6, 8.1, 'Rústico Pizza y Pan — 5 módulos interconectados',
        fontsize=11, ha='center', color='#555555')

# Module positions and info
modules = [
    {'name': 'Módulo 1\nPunto de Venta\n(POS)', 'x': 2, 'y': 6.5, 'color': '#2d6a4f', 'tc': 'white'},
    {'name': 'Módulo 2\nControl de Costos\ne Inventario', 'x': 6, 'y': 6.5, 'color': '#40916c', 'tc': 'white'},
    {'name': 'Módulo 3\nFlujo de Caja\ny Tesorería', 'x': 6, 'y': 4, 'color': '#52b788', 'tc': '#1b4332'},
    {'name': 'Módulo 4\nNómina\nSimplificada', 'x': 2, 'y': 4, 'color': '#74c69d', 'tc': '#1b4332'},
    {'name': 'Módulo 5\nReportes y\nDashboard', 'x': 10, 'y': 5.25, 'color': '#95d5b2', 'tc': '#1b4332'},
]

box_w = 2.8
box_h = 1.5

for m in modules:
    rect = FancyBboxPatch((m['x'] - box_w/2, m['y'] - box_h/2), box_w, box_h,
                           boxstyle='round,pad=0.15', facecolor=m['color'],
                           edgecolor='#1b4332', linewidth=2)
    ax.add_patch(rect)
    ax.text(m['x'], m['y'], m['name'], fontsize=10, fontweight='bold',
            ha='center', va='center', color=m['tc'])

# Arrows with labels
arrows = [
    # POS -> Costos
    {'from': (2 + box_w/2, 6.5), 'to': (6 - box_w/2, 6.5),
     'label': 'Ventas del día\n(productos, cantidades)', 'lx': 4, 'ly': 7.0},
    # POS -> Tesorería
    {'from': (2 + box_w/2, 6.5 - box_h/4), 'to': (6 - box_w/2, 4 + box_h/4),
     'label': 'Ingresos por\nmétodo de pago', 'lx': 3.5, 'ly': 5.0},
    # Costos -> Tesorería
    {'from': (6, 6.5 - box_h/2), 'to': (6, 4 + box_h/2),
     'label': 'Costo MP\nconsumida', 'lx': 6.8, 'ly': 5.25},
    # Costos -> Reportes
    {'from': (6 + box_w/2, 6.5), 'to': (10 - box_w/2, 5.25 + box_h/4),
     'label': 'Costo unitario\npor producto', 'lx': 8.5, 'ly': 6.3},
    # Tesorería -> Reportes
    {'from': (6 + box_w/2, 4), 'to': (10 - box_w/2, 5.25 - box_h/4),
     'label': 'Flujo de caja\ny saldos', 'lx': 8.5, 'ly': 4.2},
    # Nómina -> Tesorería
    {'from': (2 + box_w/2, 4), 'to': (6 - box_w/2, 4),
     'label': 'Gasto de nómina\nquincenal', 'lx': 4, 'ly': 3.5},
    # Nómina -> Reportes
    {'from': (2 + box_w/2, 4 - box_h/4), 'to': (10 - box_w/2, 5.25 - box_h/2),
     'label': 'Costo laboral\npor periodo', 'lx': 6, 'ly': 2.8},
    # POS -> Reportes
    {'from': (2 + box_w/2, 6.5 + box_h/4), 'to': (10 - box_w/2, 5.25 + box_h/2),
     'label': 'Volumen de ventas\ny ticket promedio', 'lx': 6, 'ly': 7.6},
    # Tesorería -> Reportes (egresos)
    {'from': (6 + box_w/2, 4 - box_h/4), 'to': (10 - box_w/2, 5.25 - box_h/2 + 0.2),
     'label': 'Egresos\ncategorizados', 'lx': 9, 'ly': 3.5},
]

for a in arrows:
    ax.annotate('', xy=a['to'], xytext=a['from'],
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5,
                                connectionstyle='arc3,rad=0.05'))
    ax.text(a['lx'], a['ly'], a['label'], fontsize=6.5, ha='center', va='center',
            color='#444444', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#f8f9fa',
                      edgecolor='#dddddd', alpha=0.9))

# Legend
ax.text(1, 1.5, 'Principios de diseño:', fontsize=10, fontweight='bold', color='#1b4332')
principles = [
    'Modularidad: cada módulo se implementa de forma independiente',
    'Flujo unidireccional: datos desde POS hacia los demás módulos',
    'Simplicidad: operable sin formación contable especializada',
    'Escalabilidad: permite agregar funcionalidades conforme crezca el negocio'
]
for i, p in enumerate(principles):
    ax.text(1.3, 1.1 - i * 0.3, f'• {p}', fontsize=8, color='#555555')

plt.tight_layout()
plt.savefig('/mnt/c/Users/HG_Co/OneDrive/Documents/Github/rustico/capitulo_7/diagramas/fig1_arquitectura_sistema.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fig1 generated successfully")
