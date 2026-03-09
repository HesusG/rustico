# Prompts para regenerar imagenes de evidencia — Gemini Imagen 3

**Modelo recomendado:** Gemini 2.0 Flash (con generacion de imagenes) o Imagen 3 via API.
**Idioma:** Todo el texto visible en las imagenes DEBE estar en espanol mexicano.
**Resolucion:** 1536x1024 o superior, aspect ratio 3:2 horizontal (excepto donde se indique).

---

## Instrucciones generales (system prompt / prefijo comun)

Usar este prefijo antes de cada prompt individual:

```
Genera una fotografia hiperrealista, estilo documental, tomada con un smartphone moderno
(iPhone 15 o Samsung Galaxy S24) con iluminacion natural. La imagen es una evidencia
fotografica para una investigacion academica sobre control interno en una pizzeria artesanal
en Morelia, Michoacan, Mexico. Octubre 2025.

REGLAS CRITICAS PARA EL TEXTO:
1. Todo texto visible DEBE estar en espanol mexicano. Nunca mezclar con ingles.
2. TEXTO MANUSCRITO — IMPERFECCION REALISTA (MUY IMPORTANTE):
   El texto escrito a mano NO debe verse perfecto ni generado por computadora.
   Debe simular la letra de una persona real escribiendo rapido en un negocio:
   - Variaciones de tamano entre letras (algunas mas grandes, otras mas chicas)
   - Inclinacion inconsistente (no todas las letras al mismo angulo)
   - Presion variable de la pluma (trazos mas gruesos y mas delgados)
   - Espaciado irregular entre palabras y letras
   - Algunas letras ligeramente conectadas, otras separadas
   - Los renglones NO deben ser perfectamente rectos (ligera ondulacion natural)
   - Las "a" a veces abiertas, a veces cerradas; las "e" a veces como un loop
   - Los numeros claros pero no tipograficos (el "4" abierto o cerrado, el "7" con
     o sin raya, el "1" simple o con patines, variando naturalmente)
   - Referencia: letra de alguien que no tiene mala letra pero escribe rapido,
     como un empleado llenando una nota entre clientes
   - NUNCA letra de caligrafia, NUNCA letra de fuente tipografica, NUNCA letra
     infantil o temblorosa. Es letra adulta informal de trabajo.
3. El texto impreso debe usar tipografias comunes mexicanas (Arial, Times, Courier).
4. Los numeros y signos de pesos ($) deben ser legibles aunque imperfectos.
5. La ortografia debe ser correcta en espanol (acentos incluidos donde aplique).
6. Los nombres de productos alimenticios deben ser los terminos usados en Mexico:
   "harina de trigo" (no "flour"), "queso Oaxaca" (no "Oaxaca cheese"),
   "bulto" (no "sack"), "carton" (no "carton de huevo" no "box").
```

---

## Imagen 01 — Libreta de gastos

**Archivo:** `01_libreta_gastos.jpg`
**Estado actual:** Texto manuscrito demasiado perfecto/uniforme. Precio de harina desactualizado.
**REGENERAR.** Hacer la letra mas irregular y natural. Actualizar precio harina a $790.

```
Fotografia cenital de una libreta de pasta dura abierta sobre una mesa de madera rustica
oscura con veta visible. La libreta tiene hojas de raya, amarillentas por el uso. Una pluma
BIC azul con tapa esta apoyada sobre la pagina derecha. En la pagina derecha hay una mancha
circular de cafe (marca de taza).

En la pagina izquierda, texto manuscrito con pluma azul, letra cursiva informal pero legible,
registrando gastos del negocio. El formato es: fecha — concepto — monto. Cada linea en un
renglon:

12/10  Gas LP — $380
14/10  Harina (2 bultos) — $790
15/10  Queso Oaxaca 5kg — $650
17/10  Servilletas y desechables — $145
19/10  Jitomate caja — $230
22/10  Aceite de oliva — $310
24/10  Huevo carton — $95  [esta linea tachada con una raya horizontal]
24/10  Huevo carton — $110
26/10  Verdura variada — $150  [esta linea tachada con una raya horizontal]
26/10  Verdura surtida — $165

Las lineas tachadas deben verse como correcciones naturales (una sola raya, se lee el texto
debajo). La letra debe tener personalidad: las "g" con cola larga, los numeros claros.

IMPERFECCIONES DE ESCRITURA A MANO (obligatorias):
- Algunas letras mas grandes que otras en la misma palabra
- El renglon sube o baja ligeramente respecto a la linea de la libreta
- La tinta varia en intensidad (mas oscura al inicio de cada linea, mas clara al final)
- Un par de letras con trazos incompletos o retocados
- Los signos "$" no todos identicos entre si
```

**Nota:** Se actualizo el precio de harina de $520 (2 bultos x $275) a $790 (2 bultos x $395) para consistencia con el precio corregido.

---

## Imagen 02 — Corte de caja

**Archivo:** `02_corte_caja.jpg`
**Estado actual:** Texto manuscrito demasiado uniforme y limpio para ser real.
**REGENERAR.** La letra debe verse mas apresurada, con variaciones naturales de tamano y presion.

```
Fotografia en angulo de 30 grados de una hoja de papel cuadriculado (tamano carta) sobre un
mostrador de acero inoxidable. La hoja esta ligeramente arrugada y doblada en una esquina.
Una calculadora Casio negra basica esta parcialmente visible en la esquina superior derecha.

Texto manuscrito con pluma azul y roja. En la parte superior:

"Corte de Caja          Martes 14/Oct/2025"

Debajo, una tabla dibujada a mano con regla (lineas rectas pero no perfectas):

| Concepto          | Entrada  | Salida | Saldo   |
|-------------------|----------|--------|---------|
| Fondo inicial     |    —     |   —    | $2,000  |
| Ventas mostrador  | $4,850   |   —    |   —     |
| Pago repartidor   |    —     |  $350  |   —     |
| Compra refrescos  |    —     |  $480  |   —     |
| Ventas Rappi      | $1,200   |   —    |   —     |
| TOTAL             | $8,050   |  $830  | $7,220  |

La fila TOTAL esta escrita en rojo. El saldo final "$7,220" esta encerrado en un circulo
rojo con un signo "?" al lado. En el margen derecho, operaciones aritmeticas a mano:
$2,000 + $4,850 - $350 + $480 = $7,220 (con el + $480 que deberia ser - $480, mostrando
el error de calculo).

IMPERFECCIONES DE ESCRITURA A MANO (obligatorias):
- Las lineas de la tabla dibujadas con regla pero no perfectamente alineadas
- La letra en rojo ligeramente mas grande y descuidada que la azul
- Las comas de los miles no siempre en la misma posicion vertical
- El circulo rojo alrededor del $7,220 no es un circulo perfecto, es ovalado e irregular
- Las operaciones del margen derecho mas pequenas y apretadas, como anotacion rapida
```

---

## Imagen 03 — Notas de proveedor

**Archivo:** `03_notas_proveedor.jpg`
**Estado actual:** PROBLEMAS. La nota derecha dice "Bulck Floura" (ingles incorrecto). Debe decir "Bulto Harina".
**REGENERAR — PRIORITARIA.**

```
Fotografia cenital de tres notas de remision de papel (media carta) sobre una superficie
de acero inoxidable de cocina. Las notas estan ligeramente arrugadas, con bordes doblados,
una tiene una mancha de grasa translucida. Estan colocadas lado a lado, ligeramente
superpuestas.

NOTA IZQUIERDA — Cremeria Don Pancho:
Encabezado impreso: "Cremeria Don Pancho"
Subtitulo: "Morelia, Mich. Tel: (443) 315-0779"
Texto: "nota de remision"
Tabla manuscrita con pluma azul:
| Descripcion        | Precio   |
| Queso Oaxaca 1kg   | $1,480   |
| Crema              |   $140   |
| Queso Chihuahua    | $2,140   |
TOTAL: $1,480 MXN
Sello morado: "PAGADO" en rectangulo
Linea: "Proveedor: ___________"

NOTA CENTRAL — Abarrotes El Sol:
Encabezado impreso: "Abarrotes El Sol"
Subtitulo: "Morelia, Mich."
Texto: "nota de remision"
Tabla manuscrita:
| Descripcion  | Precio |
| Aceite       |  $620  |
| Sal          |  $460  |
| Azucar       |  $230  |
| Levadura     |  $320  |
TOTAL: $620 MXN

NOTA DERECHA — Distribuidora de Harinas del Bajio:
Encabezado impreso: "Distribuidora de Harinas del Bajio"
Subtitulo: "Morelia, Mich. Tel: (443) 312-9738"
Texto: "nota de remision"
Tabla manuscrita:
| Descripcion           | Precio   |
| Bulto Harina 1o       | $1,950   |
| Bulto Harina 2o       | $1,050   |
| Bulto Harina 3o       |   $850   |
| Bulto Harina 4o       |   $350   |
| Bulto Harina 5o       |   $350   |
TOTAL: $1,950 MXN
Sello morado circular: "P"

IMPORTANTE: Todos los textos en espanol. "Bulto Harina", NO "Bulk Flour" ni "Bulck Floura".
Las notas deben verse como formularios pre-impresos reales de papeleria mexicana generica
(papel bond blanco, texto impreso en azul oscuro, llenadas a mano con pluma).

IMPERFECCIONES DE ESCRITURA A MANO (obligatorias):
- Cada nota llenada por una persona diferente (3 letras distintas)
- Nota izquierda: letra cursiva apretada, rapida, apenas legible
- Nota central: letra de molde grande y clara pero irregular
- Nota derecha: letra intermedia, algunos numeros retocados/corregidos
- Tinta de pluma no uniforme (algunas lineas mas claras por pluma gastada)
- Texto no perfectamente centrado en las columnas del formulario
```

---

## Imagen 04 — App bancaria

**Archivo:** `04_app_bancaria.jpg`
**Estado actual:** BUENA. UI realista, texto digital limpio, todo en espanol.
**Regenerar solo si** se necesita mayor resolucion.

```
Fotografia de una mano masculina morena sosteniendo un smartphone negro (pantalla 6.5")
sobre una mesa de madera. Un vaso de cafe de carton desenfocado al fondo. La pantalla muestra
una aplicacion bancaria mexicana con interfaz moderna:

Barra superior azul oscuro:
"Rustico Pizza y Pan"
"Cuenta: 60-**-***-**78"

Seccion de saldo con fondo blanco:
"Saldo disponible"
"$45,230.17 MXN"  (tipografia grande, negra, bold)

Seccion "Movimientos" — "OCTUBRE 2025":

1. Transferencia recibida — Uber Eats        +$3,420.00  (verde)
2. Compra TPV — Distribuidora de Harinas      -$1,950.00  (rojo, resaltado amarillo)
3. Deposito efectivo — Sucursal Centro        +$8,500.00  (verde)
4. Pago de servicio — CFE Luz                 -$2,180.00  (negro)
5. Transferencia enviada — Luis A. Hernandez  -$3,500.00  (rojo)
6. Compra en linea — Amazon MX                  -$459.00  (negro)

Barra inferior de navegacion: Inicio | Transferir | Pagos | Tarjetas | Mas

Todo el texto de la UI en espanol. La interfaz debe parecer una app bancaria mexicana real
(estilo BBVA, Banorte o similar). Las transacciones resaltadas en amarillo indican gastos
mezclados personales/negocio.
```

---

## Imagen 05 — Inventario

**Archivo:** `05_inventario.jpg`
**Estado actual:** Texto manuscrito demasiado perfecto, parece fuente tipografica.
**REGENERAR.** La letra debe ser de alguien contando inventario rapido, no caligrafia.

```
Fotografia frontal de una tabla con clip (clipboard) de madera colgada en una pared de acero
inoxidable de cocina industrial. La hoja es papel bond blanco tamano carta.

Titulo centrado, manuscrito con marcador negro grueso:
"Inventario — 15 Oct"

Tabla manuscrita con pluma negra:

| Producto         | Cantidad | Unidad        |
|------------------|----------|---------------|
| Harina de trigo  |  8 ?     | bultos 44kg   |
| Queso Oaxaca     |  3.5     | kg            |
| Queso Chihuahua  |  2 ?     | kg            |
| Salsa de tomate  | 12       | latas         |
| Pepperoni        |  1.5     | kg            |
| Champinones      |  0.8 *   | kg            |   * pedir el jueves
| Aceite de oliva  |  4       | L             |
| Azucar           |  3 ?     | kg            |
| Mantequilla      |  2.5     | kg            |
| Huevo            |  2       | cartones (30) |
| Levadura         |  6       | sobres        |

Los signos "?" junto a las cantidades indican duda/estimacion. El asterisco en champinones
tiene una nota al margen: "* pedir el jueves". Hay una mancha de harina/polvo blanco
en la parte inferior de la hoja.

IMPERFECCIONES DE ESCRITURA A MANO (obligatorias):
- Letra de marcador grueso para el titulo (trazos desiguales, no caligrafia)
- El cuerpo en pluma negra con letra mas pequena e irregular
- Las lineas de la tabla NO son rectas (dibujadas a mano sin regla)
- Algunos numeros escritos encima de otros (correciones: el "8?" sobre un "6" tachado)
- La columna "Unidad" con letra mas apretada porque se quedo sin espacio
- "bultos 44kg" escrito mas chico al quedarse sin renglon
```

---

## Imagen 06 — Recibo de nomina

**Archivo:** `06_recibo_nomina.jpg`
**Estado actual:** Texto manuscrito (nombre, datos llenados) demasiado uniforme.
**REGENERAR.** Los campos llenados a mano deben verse como escritura rapida real.

```
Fotografia en angulo de una hoja tamano media carta sobre una mesa de madera oscura. Una
pluma BIC azul al lado. La hoja tiene dobleces (fue doblada en tres). Iluminacion calida
de interior.

Encabezado centrado, texto impreso:
"Rustico Pizza y Pan"
[Icono pequeno de rebanada de pizza con espiga de trigo]

Sello de goma rectangular en la esquina superior derecha:
"Rustico Pizza y Pan — Morelia, Mich."

Texto impreso en negrita:
"RECIBO DE PAGO"

Contenido impreso con datos llenados a mano (pluma azul):
Nombre: Luis Angel Hernandez Martinez
Periodo: 1 al 15 de Octubre 2025
Concepto: Sueldo quincenal
Cantidad: $3,500.00 (Tres mil quinientos pesos 00/100 M.N.)

Dos lineas de firma en la parte inferior:
Izquierda: firma ilegible cursiva — debajo "Recibe"
Derecha: firma ilegible cursiva — debajo "Entrega"

Las firmas deben verse como garabatos rapidos reales, no texto legible.

IMPERFECCIONES DE ESCRITURA A MANO (obligatorias):
- Los datos llenados a mano (nombre, periodo, concepto) en letra distinta al texto impreso
- La letra manuscrita tiene inclinacion hacia la derecha, un poco apresurada
- "Hernandez" escrito ligeramente mas apretado porque el espacio se acaba
- El monto "$3,500.00" escrito con mas cuidado que el resto (mas lento, mas legible)
- Las firmas son garabatos asimetricos, diferentes entre si
```

---

## Imagen 07 — Local exterior

**Archivo:** `07_local_exterior.jpg`
**Estado actual:** Texto de pizarra demasiado limpio para gis real.
**REGENERAR.** El gis debe verse irregular, con polvo, trazos gruesos imperfectos.

```
Fotografia exterior de una fachada colonial en calle empedrada de Morelia, Michoacan.
Hora dorada (atardecer). Edificio de cantera rosa-terracota con puerta de madera antigua
abierta. Sobre la puerta, letrero de madera tallado:

"Rustico"  (con acento: Rustico, tipografia serif rustica con espiga de trigo grabada)

A la izquierda de la puerta, pizarra tipo A-frame (caballete negro) con texto en gis de
colores:

"Especiales de Hoy:
Pizza Margarita — $120
Pan de Masa Madre — $50"

(el texto de la pizarra en gis blanco y amarillo, letra informal de pizarron)

IMPERFECCIONES DEL GIS (obligatorias):
- El gis deja trazos irregulares con bordes porosos (no lineas limpias)
- Polvo de gis acumulado en la base de la pizarra
- Las letras tienen grosor variable (el gis se gasta y cambia de angulo)
- Alguna letra borrada y reescrita (residuo de gis anterior visible)
- "$120" y "$50" escritos mas grandes para ser visibles desde la calle

Dos macetas de barro con plantas: una con flores bugambilia rosa, otra con hierbas.
La calle muestra fachadas coloniales de colores (amarillo, terracota) a los lados.
Ventana con reja de herreria negra.
```

---

## Imagen 08 — Cocina y horno

**Archivo:** `08_cocina_horno.jpg`
**Estado actual:** Etiquetas en masking tape demasiado limpias. Letra muy uniforme.
**REGENERAR.** Las etiquetas deben verse escritas con marcador grueso de forma rapida e informal.

```
Fotografia de interior de cocina de pizzeria artesanal. Horno industrial de acero inoxidable
empotrado en pared revestida con azulejo de talavera poblana (patron floral azul, amarillo,
naranja). El horno esta encendido (brillo anaranjado visible por la ventanilla).

Mesa de trabajo de acero inoxidable con harina espolvoreada y 6-8 bolas de masa en
diferentes etapas de formado. Un brazo masculino (piel morena) amasando una bola a la
derecha.

Estanteria metalica al fondo con contenedores de plastico translucido con tapas rojas.
Etiquetas manuscritas en cinta masking tape amarilla pegadas al frente:
"Harina"   "Azucar"   "Sal"
(escritas con marcador negro grueso tipo Sharpie, letra de molde grande e irregular,
trazos rapidos, la cinta cortada a mano con bordes desiguales, ligeramente torcidas)

Pala de pizza de madera apoyada contra la pared. Botellas de squeeze con salsas.
Refrigerador industrial de acero al fondo. Iluminacion fluorescente de techo.
```

---

## Imagen 09 — Mostrador y caja

**Archivo:** `09_mostrador_caja.jpg`
**Estado actual:** PROBLEMAS. La pizarra tiene textos en ingles ("Cinnamon rolla") y sin sentido ("Pizza ya morando"). El cuaderno dice "Sofia's sales log" (ingles).
**REGENERAR — PRIORITARIA.**

```
Fotografia de interior del mostrador/caja de una pizzeria artesanal mexicana. Iluminacion
natural de ventanal lateral. Mostrador de madera rustica gastada.

PIZARRA DE MENU (pared izquierda, marco de madera, fondo negro):
Texto en gis blanco, letra informal:

Pizza Margarita    $120
Pizza Pepperoni    $150
Pizza Hawaiana     $140
Pizza Especial     $150
Pizza 4 Quesos     $145
Pan de masa madre   $50
Concha              $15
Rol de canela       $25
Agua fresca         $25

CUADERNO ABIERTO (espiral, sobre el mostrador, primer plano):
Texto manuscrito con pluma azul, titulo subrayado:

"Registro de ventas — Sofia"

Pizza pepperoni     $150
Pan concha x3        $45
Agua fresca          $25

OTROS ELEMENTOS:
- Caja registradora metalica abierta con billetes mexicanos (de $20, $50, $100, $200)
  y monedas en compartimentos
- Terminal de pago (datáfono) pequena junto a la caja
- Vitrina de vidrio con pan artesanal (conchas, cuernos, roles de canela)
- Carpeta azul con pluma sobre el mostrador (libreta de gastos)
- Monitor antiguo de computadora al fondo mostrando una hoja de calculo borrosa

IMPORTANTE: Todo texto en espanol. "Rol de canela" (NO "Cinnamon roll"). "Registro de
ventas" (NO "Sales log"). "Pizza Hawaiana" (NO "Pizza ya morando").

IMPERFECCIONES DE ESCRITURA (obligatorias):
- PIZARRA: gis con trazos gruesos e irregulares, polvo de gis en la base, letras de
  diferente tamano, precios mas grandes que los nombres, alguna linea ligeramente chueca
- CUADERNO: pluma azul, letra rapida de adolescente/joven (Sofia es la empleada joven),
  letra de molde informal, algunos numeros redondeados, titulo subrayado con linea
  ondulada no recta
- La pizarra y el cuaderno deben tener letras CLARAMENTE DIFERENTES (personas distintas)
```

---

## Imagen 10 — Bolsa de notas de remision

**Archivo:** `10_bolsa_notas.jpg`
**Estado actual:** Aceptable (texto pequeno e ilegible es realista para esta toma general).
**REGENERAR** para consistencia con el resto de imagenes y mejor resolucion.

```
Fotografia cenital de un escritorio de madera oscura con aproximadamente 20-25 notas de
remision esparcidas desordenadamente. Una bolsa de plastico negra arrugada en la esquina
superior izquierda (donde se guardaban las notas).

Las notas son formularios pre-impresos de papeleria mexicana, tamano media carta, papel bond
blanco. Encabezado impreso en cada una: "NOTA DE REMISION" (tipografia serif azul oscuro).

Variaciones entre las notas:
- Algunas llenadas con pluma azul, otras con pluma negra
- 3-4 notas con sello morado "PAGADO" (rectangular o circular)
- 2-3 notas con manchas de grasa translucidas
- Algunas dobladas, otras arrugadas, bordes desgastados
- Letras manuscritas parcialmente legibles (la intencion es mostrar el volumen y desorden,
  no leer cada nota individual)

La imagen debe transmitir desorden documental: evidencia de que las notas de proveedores
se guardan en una bolsa de plastico sin organizacion. Algunas notas se superponen.
```

---

## Resumen de prioridades

**TODAS las imagenes con texto deben regenerarse.** El texto manuscrito actual es demasiado perfecto y uniforme, parece generado por computadora. El objetivo es que parezca escrito por personas reales en un negocio real.

| Prioridad | Imagen | Razon principal |
|-----------|--------|-----------------|
| CRITICA | 03 — Notas proveedor | Texto en ingles ("Bulck Floura") + letra perfecta |
| CRITICA | 09 — Mostrador/caja | Texto en ingles ("Sofia's sales log", "Cinnamon rolla", "Pizza ya morando") + letra perfecta |
| ALTA | 01 — Libreta gastos | Letra demasiado uniforme + precio harina desactualizado ($520 -> $790) |
| ALTA | 02 — Corte de caja | Letra demasiado limpia y uniforme para nota a mano |
| ALTA | 05 — Inventario | Letra parece fuente tipografica, no escritura real |
| ALTA | 06 — Recibo nomina | Campos llenados a mano demasiado perfectos |
| MEDIA | 07 — Local exterior | Gis de pizarra demasiado limpio |
| MEDIA | 08 — Cocina/horno | Etiquetas de masking tape demasiado limpias |
| MEDIA | 10 — Bolsa notas | Regenerar por consistencia y resolucion |
| BAJA | 04 — App bancaria | Es texto digital (UI), no manuscrito. Solo regenerar por consistencia |
