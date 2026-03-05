import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(14, 16))
ax.set_xlim(0, 14)
ax.set_ylim(0, 16)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(7, 15.5, 'Flujo de datos del sistema de gestión financiera',
        fontsize=16, fontweight='bold', ha='center', color='#1b4332')
ax.text(7, 15.1, 'Desde el pedido del cliente hasta los reportes gerenciales',
        fontsize=11, ha='center', color='#555555')

def draw_box(ax, x, y, text, color='#ffffff', edge='#333333', tc='#333333', w=3, h=0.8, fs=8):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle='round,pad=0.12', facecolor=color,
                           edgecolor=edge, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y, text, fontsize=fs, ha='center', va='center', color=tc, fontweight='bold')

def draw_diamond(ax, x, y, text, color='#fff3cd', edge='#ffc107', w=2.5, h=1):
    diamond = plt.Polygon([(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)],
                           facecolor=color, edgecolor=edge, linewidth=1.5)
    ax.add_patch(diamond)
    ax.text(x, y, text, fontsize=7, ha='center', va='center', color='#333333', fontweight='bold')

def arrow(ax, x1, y1, x2, y2, label=None, lx=None, ly=None):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5))
    if label and lx and ly:
        ax.text(lx, ly, label, fontsize=7, ha='center', va='center', color='#666666',
                style='italic')

# Row 1: Client
draw_box(ax, 7, 14.5, 'Cliente realiza\nun pedido', '#264653', '#1d3557', 'white', w=3, h=0.7)

# Row 2: POS registration
arrow(ax, 7, 14.15, 7, 13.65)
draw_box(ax, 7, 13.3, 'Sofía registra el\npedido en POS', '#2a9d8f', '#264653', 'white', w=3, h=0.7)

# Split: payment method
arrow(ax, 7, 12.95, 7, 12.3)
draw_diamond(ax, 7, 11.9, '¿Método\nde pago?', w=2.2, h=0.8)

# Left: cash
arrow(ax, 5.9, 11.9, 4.5, 11.9)
ax.text(5.2, 12.1, 'Efectivo', fontsize=7, ha='center', color='#666')
draw_box(ax, 3.5, 11.9, 'Registrar cobro\nen efectivo', '#d8f3dc', '#2d6a4f', '#1b4332', w=2.8, h=0.6)

# Right: card
arrow(ax, 8.1, 11.9, 9.5, 11.9)
ax.text(8.8, 12.1, 'Tarjeta', fontsize=7, ha='center', color='#666')
draw_box(ax, 10.5, 11.9, 'Registrar cobro\ncon terminal', '#d8f3dc', '#2d6a4f', '#1b4332', w=2.8, h=0.6)

# Cash -> fund
arrow(ax, 3.5, 11.6, 3.5, 11.0)
draw_box(ax, 3.5, 10.6, 'Acumular en\nfondo de caja', '#d8f3dc', '#2d6a4f', '#1b4332', w=2.8, h=0.6)

# Card -> bank ref
arrow(ax, 10.5, 11.6, 10.5, 11.0)
draw_box(ax, 10.5, 10.6, 'Registrar referencia\ntransacción bancaria', '#d8f3dc', '#2d6a4f', '#1b4332', w=2.8, h=0.6)

# Both -> Cash cut
arrow(ax, 3.5, 10.3, 7, 9.8)
arrow(ax, 10.5, 10.3, 7, 9.8)
draw_box(ax, 7, 9.5, 'Corte de caja al\ncierre del turno', '#e9c46a', '#f4a261', '#264653', w=3.5, h=0.6)

# Cash cut -> Reconciliation
arrow(ax, 7, 9.2, 7, 8.6)
draw_box(ax, 7, 8.3, 'Conciliación: ventas vs.\nefectivo vs. depósitos', '#f4a261', '#e76f51', '#264653', w=3.5, h=0.6)

# INVENTORY BRANCH (from POS)
arrow(ax, 7, 12.95, 12, 12.95)
ax.text(9.5, 13.15, 'Simultáneamente', fontsize=7, ha='center', color='#666', style='italic')

# Inventory flow on the right side
draw_box(ax, 12, 12.6, 'Descontar insumos\ndel inventario\nsegún receta (BOM)', '#b7e4c7', '#2d6a4f', '#1b4332', w=2.8, h=0.8)

arrow(ax, 12, 12.2, 12, 11.5)
draw_diamond(ax, 12, 11.1, '¿Insumo bajo\nel mínimo?', w=2.2, h=0.8)

# Alert
arrow(ax, 12, 10.7, 12, 10.1)
ax.text(12.2, 10.4, 'Sí', fontsize=7, ha='left', color='#e76f51')
draw_box(ax, 12, 9.8, 'Generar alerta\nde reorden', '#ffccd5', '#e76f51', '#333', w=2.5, h=0.5)

# No -> update
ax.text(13.2, 11.1, 'No', fontsize=7, ha='left', color='#2d6a4f')

# Calculate cost
arrow(ax, 12, 9.55, 12, 8.9)
draw_box(ax, 12, 8.6, 'Calcular costo de\nmateria prima\nconsumida', '#b7e4c7', '#2d6a4f', '#1b4332', w=2.8, h=0.7)

arrow(ax, 12, 8.25, 12, 7.6)
draw_box(ax, 12, 7.3, 'Actualizar costo\nde ventas del día', '#b7e4c7', '#2d6a4f', '#1b4332', w=2.8, h=0.6)

# Conciliation -> Cash flow
arrow(ax, 7, 8.0, 7, 7.1)
draw_box(ax, 7, 6.8, 'Registrar ingresos\nen flujo de caja', '#52b788', '#40916c', '#1b4332', w=3.5, h=0.6)

# Cost -> Cash flow
arrow(ax, 12, 7.0, 8.75, 6.8)

# Cash flow -> Reports
arrow(ax, 7, 6.5, 7, 5.9)
draw_box(ax, 7, 5.5, 'Consolidar en\nReportes y Dashboard', '#e76f51', '#264653', 'white', w=4, h=0.8)

# Reports -> KPIs and report
arrow(ax, 5, 5.5, 3.5, 4.7)
draw_box(ax, 3.5, 4.3, 'Calcular KPIs:\nmargen bruto, ticket\npromedio, costo MP (%)', '#95d5b2', '#74c69d', '#1b4332', w=3.5, h=0.8)

arrow(ax, 9, 5.5, 10.5, 4.7)
draw_box(ax, 10.5, 4.3, 'Generar reporte\ndiario / semanal\npara Martín', '#95d5b2', '#74c69d', '#1b4332', w=3.5, h=0.8)

plt.tight_layout()
plt.savefig('/mnt/c/Users/HG_Co/OneDrive/Documents/Github/rustico/capitulo_7/diagramas/fig2_flujo_datos.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fig2 generated successfully")
