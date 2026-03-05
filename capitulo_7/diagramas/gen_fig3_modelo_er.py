import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(8, 11.5, 'Modelo entidad-relación del sistema de gestión financiera',
        fontsize=16, fontweight='bold', ha='center', color='#1b4332')
ax.text(8, 11.1, 'Modelo conceptual simplificado — Rústico Pizza y Pan',
        fontsize=11, ha='center', color='#555555')

def draw_entity(ax, x, y, name, fields, color='#2d6a4f', w=3.2, field_h=0.25):
    h_header = 0.45
    h_total = h_header + len(fields) * field_h + 0.1
    # Header
    rect = FancyBboxPatch((x - w/2, y - h_header/2), w, h_header,
                           boxstyle='round,pad=0.08', facecolor=color,
                           edgecolor='#1b4332', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, name, fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    # Fields background
    fields_top = y - h_header/2
    fields_h = len(fields) * field_h + 0.15
    rect2 = FancyBboxPatch((x - w/2, fields_top - fields_h), w, fields_h,
                            boxstyle='round,pad=0.05', facecolor='#f8f9fa',
                            edgecolor='#cccccc', linewidth=1)
    ax.add_patch(rect2)
    for i, (fname, ftype, fkey) in enumerate(fields):
        fy = fields_top - 0.1 - i * field_h - field_h/2
        prefix = ''
        if fkey == 'PK':
            prefix = 'PK '
            ax.text(x - w/2 + 0.15, fy, prefix, fontsize=7, ha='left', va='center',
                    color='#e76f51', fontweight='bold')
        elif fkey == 'FK':
            prefix = 'FK '
            ax.text(x - w/2 + 0.15, fy, prefix, fontsize=7, ha='left', va='center',
                    color='#2a9d8f', fontweight='bold')
        ax.text(x - w/2 + 0.45, fy, fname, fontsize=7.5, ha='left', va='center', color='#333')
        ax.text(x + w/2 - 0.15, fy, ftype, fontsize=7, ha='right', va='center', color='#888')
    return fields_top - fields_h  # bottom y

# Entity definitions
entities = {
    'PRODUCTO': {
        'pos': (2.5, 10),
        'color': '#2d6a4f',
        'fields': [('productoId', 'int', 'PK'), ('nombre', 'string', ''), ('categoria', 'string', ''),
                   ('precioVenta', 'decimal', ''), ('costoUnitario', 'decimal', ''), ('activo', 'bool', '')]
    },
    'VENTA': {
        'pos': (8, 10),
        'color': '#264653',
        'fields': [('ventaId', 'int', 'PK'), ('fecha', 'date', ''), ('hora', 'time', ''),
                   ('metodoPago', 'string', ''), ('totalVenta', 'decimal', ''),
                   ('empleadoId', 'int', 'FK'), ('corteCajaId', 'int', 'FK')]
    },
    'DETALLE_VENTA': {
        'pos': (5.25, 7),
        'color': '#2a9d8f',
        'fields': [('detalleId', 'int', 'PK'), ('ventaId', 'int', 'FK'), ('productoId', 'int', 'FK'),
                   ('cantidad', 'int', ''), ('precioUnitario', 'decimal', ''), ('subtotal', 'decimal', '')]
    },
    'INSUMO': {
        'pos': (2.5, 4),
        'color': '#40916c',
        'fields': [('insumoId', 'int', 'PK'), ('nombre', 'string', ''), ('unidadMedida', 'string', ''),
                   ('costoUnitario', 'decimal', ''), ('existencia', 'decimal', ''),
                   ('stockMinimo', 'decimal', ''), ('proveedor', 'string', '')]
    },
    'RECETA': {
        'pos': (2.5, 7),
        'color': '#52b788',
        'fields': [('recetaId', 'int', 'PK'), ('productoId', 'int', 'FK'), ('insumoId', 'int', 'FK'),
                   ('cantidadRequerida', 'decimal', ''), ('unidadMedida', 'string', '')]
    },
    'GASTO': {
        'pos': (13.5, 4),
        'color': '#e9c46a',
        'fields': [('gastoId', 'int', 'PK'), ('fecha', 'date', ''), ('categoria', 'string', ''),
                   ('descripcion', 'string', ''), ('monto', 'decimal', ''),
                   ('metodoPago', 'string', ''), ('comprobante', 'string', '')]
    },
    'CORTE_CAJA': {
        'pos': (13.5, 10),
        'color': '#f4a261',
        'fields': [('corteCajaId', 'int', 'PK'), ('fecha', 'date', ''), ('ventasEfectivo', 'decimal', ''),
                   ('ventasTarjeta', 'decimal', ''), ('fondoInicial', 'decimal', ''),
                   ('efectivoContado', 'decimal', ''), ('diferencia', 'decimal', ''),
                   ('empleadoId', 'int', 'FK')]
    },
    'EMPLEADO': {
        'pos': (10.5, 7),
        'color': '#e76f51',
        'fields': [('empleadoId', 'int', 'PK'), ('nombre', 'string', ''), ('puesto', 'string', ''),
                   ('salarioQuincenal', 'decimal', ''), ('fechaIngreso', 'date', ''), ('activo', 'bool', '')]
    },
    'NOMINA': {
        'pos': (8, 4),
        'color': '#74c69d',
        'fields': [('nominaId', 'int', 'PK'), ('empleadoId', 'int', 'FK'), ('fechaInicio', 'date', ''),
                   ('fechaFin', 'date', ''), ('salarioBase', 'decimal', ''),
                   ('netoAPagar', 'decimal', ''), ('fechaPago', 'date', '')]
    },
}

# Draw entities
bottoms = {}
for name, info in entities.items():
    x, y = info['pos']
    bottom = draw_entity(ax, x, y, name, info['fields'], info['color'])
    bottoms[name] = bottom

# Draw relationships (simple lines with labels)
def rel_line(ax, x1, y1, x2, y2, label, lx, ly, color='#888'):
    ax.plot([x1, x2], [y1, y2], '-', color=color, lw=1.2, zorder=1)
    ax.text(lx, ly, label, fontsize=6.5, ha='center', va='center', color='#555',
            style='italic', bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                                       edgecolor='#ddd', alpha=0.9))

# PRODUCTO -> DETALLE_VENTA
rel_line(ax, 2.5, 8.3, 5.25, 7.45, '1:N\nse vende en', 3.5, 7.9)
# VENTA -> DETALLE_VENTA
rel_line(ax, 8, 8.2, 5.25, 7.45, '1:N\ncontiene', 6.8, 7.9)
# PRODUCTO -> RECETA
rel_line(ax, 2.5, 8.3, 2.5, 7.45, '1:N\nse compone de', 1.2, 7.9)
# INSUMO -> RECETA
rel_line(ax, 2.5, 5.3, 2.5, 5.75, '1:N\nse usa en', 1.2, 5.5)
# VENTA -> CORTE_CAJA
rel_line(ax, 9.6, 10, 11.9, 10, 'N:1\npertenece a', 10.75, 10.3)
# VENTA -> EMPLEADO
rel_line(ax, 8, 8.2, 10.5, 7.45, 'N:1\nregistrada por', 9.5, 8.0)
# EMPLEADO -> NOMINA
rel_line(ax, 10.5, 5.3, 8, 4.45, '1:N\nrecibe', 9.5, 4.9)
# EMPLEADO -> CORTE_CAJA
rel_line(ax, 12, 7, 13.5, 8.2, '1:N\nrealiza', 13, 7.7)

# Legend
ax.text(0.5, 1.2, 'Leyenda:', fontsize=9, fontweight='bold', color='#333')
ax.text(0.5, 0.9, 'PK = Clave primaria    FK = Clave foránea    1:N = Relación uno a muchos',
        fontsize=8, color='#555')

plt.tight_layout()
plt.savefig('/mnt/c/Users/HG_Co/OneDrive/Documents/Github/rustico/capitulo_7/diagramas/fig3_modelo_er.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fig3 generated successfully")
