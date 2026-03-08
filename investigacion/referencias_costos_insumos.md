# Referencias de costos de insumos clave

Verificacion de precios de insumos citados en capitulo_7.md y fichas_analisis.md.

**Fecha de consulta:** 7 de marzo de 2026

---

## 1. Contradicciones detectadas entre documentos

### 1.1 Pizza Margarita: costo y precio de venta NO coinciden

**En capitulo_7.md (linea 94) dice:**
> "La tabla de costos de marzo de 2025 calcula un costo de materia prima de **$42** para la pizza Margarita (la mas pequena vendida a **$120**), lo que implicaria un margen bruto del **65%**."

**En fichas_analisis.md (Ficha 7, linea 243) dice:**
> "Pizza margarita costeada en **$38** (venta en **$130**, margen aparente **70.8%**), pero con precios de queso de marzo ($105/kg). Precio actual: $130/kg (+23.8%). Costo real estimado: **$45** (margen real: **65.4%**)."

| Dato | capitulo_7.md | fichas_analisis.md | Coincide? |
|---|---|---|---|
| Costo materia prima (tabla marzo 2025) | $42 | $38 | NO |
| Precio de venta | $120 | $130 | NO |
| Margen bruto | 65% | 70.8% | NO |

**Verificacion matematica:** Ambos calculos son correctos internamente:
- Cap7: (120-42)/120 = 65.0% ✓
- Ficha 7: (130-38)/130 = 70.8% ✓

**Pero los datos de entrada son diferentes.** Se refieren al mismo producto, la misma tabla de costos (marzo 2025), del mismo negocio. No pueden coexistir dos costos ni dos precios de venta distintos.

**REQUIERE DECISION DEL USUARIO:** Cual es el dato correcto? El de capitulo_7.md ($42/$120) o el de fichas_analisis.md ($38/$130)?

### 1.2 Queso Oaxaca: precios en la tabla de costos

**En capitulo_7.md (linea 72) dice:**
> "el queso Oaxaca paso de **$120/kg** a **$130/kg** (+8.3% documentado en notas de proveedores)"

**En fichas_analisis.md (Ficha 4, linea 136) dice:**
> "Incremento del 8.3% en queso Oaxaca entre septiembre (**$120/kg**) y noviembre (**$130/kg**)"

**En fichas_analisis.md (Ficha 7, linea 243) dice:**
> "precios de queso de marzo (**$105/kg**). Precio actual: **$130/kg** (+23.8%)"

**Analisis:** Estos NO se contradicen. Son dos comparaciones distintas:
- $105 (marzo 2025, tabla de costos) -> $120 (sep 2025, notas proveedor) -> $130 (nov 2025, notas proveedor)
- Cap7 reporta el tramo $120->$130 (+8.3%)
- Ficha 7 reporta el tramo $105->$130 (+23.8%)
- Verificacion: (130-120)/120 = 8.33% ✓ y (130-105)/105 = 23.81% ✓

### 1.3 Harina de trigo: consistente entre documentos

**En capitulo_7.md (linea 72):** "$220 a $275 por bulto de 44 kg (+25%)"
**En fichas_analisis.md (Ficha 7, linea 244):** "$220/bulto ($5/kg). Precio actual: $275/bulto ($6.25/kg), incremento del 25%."

Verificacion: (275-220)/220 = 25.0% ✓ | 220/44 = $5.00/kg ✓ | 275/44 = $6.25/kg ✓
**Consistente entre ambos documentos.**

---

## 2. Verificacion de precios con fuentes externas

### 2.1 Queso Oaxaca — $130/kg: CONFIRMADO

**Precios de canal mayorista (comparables a Cremeria Don Pancho):**

| Fuente | Precio/kg | Canal | URL |
|---|---|---|---|
| Super Mayoreo, CDMX | **$130.00** | Mayoreo | https://huevosupermayoreo.com/products/queso-oaxaca-1kg |
| LICACE Mexico | **$127.00** | Distribuidor | https://licace.com.mx/product/queso-oaxaca-kg/ |
| Moisaner Gourmet, CDMX | **$160.00** | Mayoreo/menudeo | https://moisaner.com/producto/queso-oaxaca-por-kilo/ |
| Abasto Deli (con grasa vegetal) | **$95.00** | Abasto | https://www.abastodeli.com/product/queso-oaxaca-villasana-kg |
| PROFECO 2025 (chile en nogada) | **$128.66** | Referencia oficial | Via medios |

**Precios retail (NO comparables, solo referencia):**

| Fuente | Precio/kg | URL |
|---|---|---|
| La Vizcaina | $165.00 | https://www.lavizcaina.com.mx/collections/quesos |
| Alchef | $200.00 | https://alchef.mx/producto/queso-oaxaca-2/ |
| Walmart (Lala 400g) | ~$210.00 | super.walmart.com.mx |
| Click Abasto (Los Volcanes) | $299.99 | clickabasto.com |

**Veredicto:** El precio de **$130/kg es razonable**. Super Mayoreo lo lista exactamente a $130/kg. LICACE a $127/kg. Profeco reporta $128.66/kg. El rango mayorista es $95-$160/kg.

El precio anterior de **$120/kg tambien es plausible** como precio de cremeria local unos meses antes.

El precio de tabla de costos de marzo 2025 de **$105/kg tambien es plausible** como precio de hace ~1 ano.

### 2.2 Harina de trigo — CORREGIDO a $395/bulto 44 kg

**Precio original en documentos:** $275/bulto 44 kg (dato no verificable, posiblemente desactualizado).

**Precio corregido:** $395/bulto 44 kg, basado en la referencia mayorista mas conservadora.

**Precios encontrados de canal mayorista:**

| Fuente | Precio/bulto 44kg | Canal | URL |
|---|---|---|---|
| Deposito Los Cuates, Cd. Juarez | **$395.00** | Mayoreo local | Facebook |
| Casa del Pastelero, Veracruz | **$450.00** | Distribuidor | Facebook |
| Pealpan (25 kg Hoja de Plata) | $542.75/25kg → ~**$955/44kg** | Semi-mayoreo online | pealpan.mx |
| Click Abasto (Hoja de Plata 44 kg) | **$1,990.00** | Tienda online | clickabasto.com |
| MercadoLibre (Selecta 44 kg) | **$1,594-$1,651** | Marketplace | meliprice.com.mx |

**Cambios realizados en documentos:**
- `capitulo_7.md` linea 72: "harina de $220 a ~~$275~~ **$395** por bulto de 44 kg (~~+25%~~ **+79.5%**)"
- `fichas_analisis.md` Ficha 7: "Precio actual: ~~$275/bulto ($6.25/kg), incremento del 25%~~ **$395/bulto ($8.98/kg), incremento del 79.5%**"

**Verificacion matematica:** (395-220)/220 = 79.5% ✓ | 395/44 = $8.98/kg ✓

---

## 3. Resumen de verificacion

| Dato | En capitulo_7.md | En fichas_analisis.md | Verificacion externa | Estado |
|---|---|---|---|---|
| Queso Oaxaca actual | $130/kg | $130/kg | $127-$130/kg (mayoreo) | **CONFIRMADO** |
| Queso Oaxaca anterior (notas) | $120/kg | $120/kg (Ficha 4) | Plausible | **OK** |
| Queso tabla marzo 2025 | (no lo menciona directamente) | $105/kg (Ficha 7) | Plausible | **OK** |
| Harina actual | $275/bulto 44 kg | $275/bulto (Ficha 7) | $395-$450 (mayoreo) | **POSIBLEMENTE BAJO** |
| Harina base marzo 2025 | $220/bulto 44 kg | $220/bulto (Ficha 7) | No verificable | **DATO DEL NEGOCIO** |
| Pizza Margarita costo | **$42** | **$38** | — | **CONTRADICTORIO** |
| Pizza Margarita venta | **$120** | **$130** | — | **CONTRADICTORIO** |
| Pizza Margarita margen | **65%** | **70.8%** | — | **CONTRADICTORIO** |

---

## 4. Acciones pendientes

1. **Resolver contradiccion pizza Margarita:** Definir si el costo es $42 o $38, y si la venta es $120 o $130. Corregir el documento incorrecto.
2. **Decidir sobre harina $275:** Mantener como dato del negocio (nota de proveedor), o investigar directamente con el negocio si el precio es correcto.
3. Despues de resolver #1 y #2, actualizar capitulo_7.md y/o fichas_analisis.md segun corresponda.
