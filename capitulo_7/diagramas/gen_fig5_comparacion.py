import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 8))
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(0.5, 0.97, 'Comparación de alternativas tecnológicas para Rústico Pizza y Pan',
        fontsize=16, fontweight='bold', ha='center', va='top', transform=ax.transAxes,
        color='#1b4332')

headers = ['Criterio', 'Sistema modular\na la medida', 'POS comercial\ngenérico', 'ERP completo\n(ej. Odoo)']

rows = [
    ['Costo estimado', '$5,000 – $15,000 MXN\n(desarrollo único)', '$500 – $2,000 MXN/mes\n(suscripción)', '$15,000 – $80,000 MXN\n(implementación + consultor)'],
    ['Módulos incluidos', '5 módulos diseñados\npara el diagnóstico\n(POS, costos, tesorería,\nnómina, reportes)', 'Solo POS y pagos\n(resuelve H1 pero\nno H2–H7)', '30+ módulos\n(contabilidad, CRM,\ninventario, RRHH, etc.)'],
    ['Curva de aprendizaje', 'Baja: diseñado para\nusuarios sin formación\ncontable', 'Baja–Media:\ninterfaz estándar', 'Alta: requiere\ncapacitación formal\ny consultor'],
    ['Adaptación al\nnegocio', 'Total: construido\na partir del\ndiagnóstico', 'Parcial: configuración\nlimitada a opciones\npredefinidas', 'Alta (con consultor):\npero sobredimensionado\npara 4 empleados'],
    ['Infraestructura\nrequerida', 'PC o tablet +\nhojas de cálculo\no app web', 'Tablet o smartphone\n+ conexión a internet\npermanente', 'Servidor (local o nube)\n+ soporte técnico\ncontinuo'],
    ['Cobertura del\ndiagnóstico', 'H1–H7: aborda todas\nlas deficiencias\nidentificadas', 'H1 parcialmente:\nsolo registro de\nventas', 'H1–H7 teóricamente,\npero con complejidad\ninnecesaria'],
    ['Tiempo de\nimplementación', '14 semanas\n(4 fases graduales)', '1–2 semanas\n(configuración básica)', '3–6 meses\n(con consultor)'],
    ['Mantenimiento', 'Bajo: el propio\nnegocio lo opera', 'Medio: depende\ndel proveedor', 'Alto: requiere\nsoporte técnico\nespecializado'],
]

n_rows = len(rows) + 1
n_cols = 4
cell_height = 0.095
cell_widths = [0.18, 0.27, 0.27, 0.27]
start_x = 0.005
start_y = 0.88

header_colors = ['#1b4332', '#2d6a4f', '#e9c46a', '#e76f51']
header_text_colors = ['white', 'white', '#1b4332', 'white']

for j, (header, color, tcolor) in enumerate(zip(headers, header_colors, header_text_colors)):
    x = start_x + sum(cell_widths[:j])
    rect = mpatches.FancyBboxPatch((x, start_y - cell_height), cell_widths[j] - 0.005,
                                     cell_height - 0.005, boxstyle='round,pad=0.005',
                                     facecolor=color, edgecolor='#333333', linewidth=1.5,
                                     transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x + cell_widths[j]/2 - 0.0025, start_y - cell_height/2 - 0.0025,
            header, fontsize=9, fontweight='bold', ha='center', va='center',
            color=tcolor, transform=ax.transAxes)

row_colors_bg = ['#f8f9fa', '#ffffff']

for i, row in enumerate(rows):
    y = start_y - (i + 1) * cell_height
    bg = row_colors_bg[i % 2]
    for j, cell in enumerate(row):
        x = start_x + sum(cell_widths[:j])
        if j == 1:
            cell_bg = '#d8f3dc'
        elif j == 0:
            cell_bg = '#e8e8e8'
        else:
            cell_bg = bg
        rect = mpatches.FancyBboxPatch((x, y - cell_height + 0.005), cell_widths[j] - 0.005,
                                         cell_height - 0.005, boxstyle='round,pad=0.003',
                                         facecolor=cell_bg, edgecolor='#cccccc', linewidth=0.8,
                                         transform=ax.transAxes)
        ax.add_patch(rect)
        fontw = 'bold' if j == 0 else 'normal'
        fontsz = 7.5 if j == 0 else 7
        ax.text(x + cell_widths[j]/2 - 0.0025, y - cell_height/2 + 0.005,
                cell, fontsize=fontsz, fontweight=fontw, ha='center', va='center',
                color='#333333', transform=ax.transAxes)

note_y = start_y - (len(rows) + 1) * cell_height - 0.01
rect = mpatches.FancyBboxPatch((start_x, note_y), 0.985, 0.04,
                                 boxstyle='round,pad=0.008', facecolor='#d8f3dc',
                                 edgecolor='#2d6a4f', linewidth=2,
                                 transform=ax.transAxes)
ax.add_patch(rect)
ax.text(0.5, note_y + 0.02,
        'Recomendación: El sistema modular a la medida es la alternativa que mejor responde al diagnóstico, '
        'con el menor costo, la menor complejidad y la mayor cobertura de las deficiencias identificadas.',
        fontsize=8, fontweight='bold', ha='center', va='center', color='#1b4332',
        transform=ax.transAxes, style='italic')

plt.tight_layout()
plt.savefig('/mnt/c/Users/HG_Co/OneDrive/Documents/Github/rustico/capitulo_7/diagramas/fig5_comparacion_soluciones.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fig5 generated successfully")
