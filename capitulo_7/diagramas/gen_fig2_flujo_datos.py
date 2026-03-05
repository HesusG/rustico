import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(10, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(5, 11.6, 'Flujo de datos del sistema de gestión financiera',
        fontsize=14, fontweight='bold', ha='center', color='#1b4332')

def box(ax, x, y, text, color='#f8f9fa', edge='#333', tc='#333', w=3.2, h=0.7, fs=8.5):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle='round,pad=0.1', facecolor=color,
                           edgecolor=edge, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y, text, fontsize=fs, ha='center', va='center',
            color=tc, fontweight='bold')

def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))

def label(ax, x, y, text, fs=7):
    ax.text(x, y, text, fontsize=fs, ha='center', va='center',
            color='#666', style='italic')

# Step 1: Client order
box(ax, 5, 11, 'Cliente realiza un pedido', '#264653', '#1d3557', 'white')

arrow(ax, 5, 10.65, 5, 10.15)

# Step 2: POS register
box(ax, 5, 9.8, 'Sofía registra en POS', '#2a9d8f', '#264653', 'white')

# Split into 3 branches
arrow(ax, 3.4, 9.45, 2.5, 8.85)  # left: cash/card
arrow(ax, 5, 9.45, 5, 8.85)      # center: inventory
arrow(ax, 6.6, 9.45, 7.5, 8.85)  # right: cost

# LEFT BRANCH: Payment
label(ax, 2.8, 9.2, 'Pago')
box(ax, 2.5, 8.5, 'Registrar cobro\n(efectivo / tarjeta)', '#d8f3dc', '#2d6a4f', '#1b4332', w=3)

arrow(ax, 2.5, 8.15, 2.5, 7.55)
box(ax, 2.5, 7.2, 'Corte de caja\nal cierre', '#e9c46a', '#f4a261', '#264653', w=3)

arrow(ax, 2.5, 6.85, 2.5, 6.25)
box(ax, 2.5, 5.9, 'Conciliación:\nventas vs. depósitos', '#f4a261', '#e76f51', '#264653', w=3)

# CENTER BRANCH: Inventory
label(ax, 5, 9.2, 'Inventario')
box(ax, 5, 8.5, 'Descontar insumos\nsegún receta (BOM)', '#b7e4c7', '#2d6a4f', '#1b4332', w=3)

arrow(ax, 5, 8.15, 5, 7.55)
box(ax, 5, 7.2, 'Actualizar existencias\n(alerta si bajo mínimo)', '#b7e4c7', '#2d6a4f', '#1b4332', w=3)

# RIGHT BRANCH: Cost
label(ax, 7.2, 9.2, 'Costos')
box(ax, 7.5, 8.5, 'Calcular costo de\nmateria prima', '#b7e4c7', '#2d6a4f', '#1b4332', w=3)

arrow(ax, 7.5, 8.15, 7.5, 7.55)
box(ax, 7.5, 7.2, 'Actualizar costo\nde ventas del día', '#b7e4c7', '#2d6a4f', '#1b4332', w=3)

# All three converge to cash flow
arrow(ax, 2.5, 5.55, 4, 4.95)
arrow(ax, 5, 6.85, 5, 4.95)
arrow(ax, 7.5, 6.85, 6, 4.95)

box(ax, 5, 4.6, 'Registrar en flujo de caja', '#52b788', '#40916c', '#1b4332', w=4)

# -> Reports
arrow(ax, 5, 4.25, 5, 3.65)
box(ax, 5, 3.3, 'Consolidar en\nReportes y Dashboard', '#e76f51', '#264653', 'white', w=4, h=0.7)

# -> KPIs
arrow(ax, 3, 2.95, 2.5, 2.35)
box(ax, 2.5, 2, 'KPIs: margen bruto,\nticket promedio,\ncosto MP (%)', '#95d5b2', '#74c69d', '#1b4332', w=3.2, h=0.7)

arrow(ax, 7, 2.95, 7.5, 2.35)
box(ax, 7.5, 2, 'Reporte diario/semanal\npara Martín', '#95d5b2', '#74c69d', '#1b4332', w=3.2, h=0.7)

plt.tight_layout()
plt.savefig('/mnt/c/Users/HG_Co/OneDrive/Documents/Github/rustico/capitulo_7/diagramas/fig2_flujo_datos.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fig2 generated successfully")
