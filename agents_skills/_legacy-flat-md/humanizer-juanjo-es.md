# humanizer-juanjo-es

**Activación**: Reescribir en la voz ejecutiva española de Juanjo. Usar cuando el usuario pide humanizar, reescribir, pulir o calibrar el tono de cualquier texto en español: manuscritos científicos, material docente UGR, informes técnicos, comunicaciones DestiNA, documentación ISO.

---

## Perfil de Voz: Juanjo — Ejecutivo Técnico en Español

**Carácter**: Directo, plural natural ("analizamos", "implementamos"), headers temáticos claros, alta precisión de dominio. Ni formal-rígido ni informal-coloquial: el registro de un investigador que escribe para colegas exigentes.

**Registros cubiertos**: Artículos científicos, memorias de proyecto, material didáctico UGR (QF1/QF2), informes de calidad ISO, webs de asignatura, comunicaciones internas DestiNA.

---

## Protocolo de Reescritura Paso a Paso

### Paso 1 — Diagnóstico estructural
Lee el texto completo antes de modificar nada. Identifica:
- La tesis o entregable central de cada párrafo
- Párrafos que existen solo para suavizar, calificar o rellenar
- Anglicismos evitables y calcos sintácticos del inglés

### Paso 2 — Eliminar sin sustituir

**Rellenos de apertura** (borrar directamente):
- "Es importante destacar que", "Cabe mencionar que", "Resulta evidente que"
- "En el mundo actual", "En la era digital", "Hoy en día es fundamental"
- "Por supuesto", "Sin duda", "Evidentemente", "Como es de esperar"

**Cierres formulaicos** (borrar o reformular):
- "En conclusión", "En resumen", "Para finalizar", "En definitiva"
- "Queda claro que", "Se puede observar que", "Todo ello nos lleva a"

**Transiciones vacías**:
- "Además", "Asimismo", "Por otro lado", "No obstante" — usar solo cuando la relación lógica no es obvia
- "Cabe señalar", "Es menester", "Procede indicar"

**Intensificadores huecos**: "muy", "bastante", "enormemente", "sumamente", "realmente" — eliminar o cuantificar

### Paso 3 — Voz activa en plural natural
El sujeto del texto es el investigador/equipo hablando directamente.

| Antes | Después |
|---|---|
| "Se realizó la validación mediante..." | "Validamos el método mediante..." |
| "Los resultados obtenidos sugieren..." | "Los resultados sugieren..." |
| "Fue posible demostrar que la sonda..." | "La sonda demuestra..." |
| "Puede afirmarse que el método..." | "El método..." |

### Paso 4 — Cuantificar afirmaciones vagas
Donde existen datos, usar números. Sin datos, eliminar la afirmación.

| Antes | Después |
|---|---|
| "mejoró significativamente" | "mejoró un 40% (p < 0,01)" |
| "un gran número de muestras" | "1.847 muestras" |
| "varios estudios demuestran" | "Tres cohortes independientes (refs.) muestran" |

### Paso 5 — Terminología de dominio correcta
- Genes/proteínas: cursiva para genes (*KRT10*, *EGFR*), regular para proteínas (KRT10, EGFR)
- Química: Unicode directo — ¹H RMN, ¹³C RMN, [M+H]⁺, KD, δ, ν, Δ, ×, °C, µM, nM
- **Nunca** delimitadores LaTeX en prosa: prohibido `$...$`, `\(...\)`, `\text{...}`
- Datos de ensayo: siempre incluir n, unidades y prueba estadística
- Abreviaturas en español: RMN (no NMR), EM (no MS), LC-EM/EM, PCR

### Paso 6 — Estructura de párrafo
Cada párrafo: una afirmación → una o dos evidencias → una implicación. Máximo 5 oraciones. Si hay dos afirmaciones, crear dos párrafos.

### Paso 7 — Headers temáticos, no genéricos

| Genérico (evitar) | Temático (usar) |
|---|---|
| "Introducción" | "Detección de miR-122 sin amplificación" |
| "Métodos" | "Protocolo DCL y análisis MALDI-TOF" |
| "Resultados" | "Discriminación alélica a 37°C con sonda SMART" |
| "Conclusión" | "Viabilidad del diagnóstico PCR-free en matriz clínica" |

### Paso 8 — Verificación final de voz
Lee en voz alta (mentalmente). Cualquier oración que suene a "traducido del inglés" o "escrito por un comité" → reescribir como si se explicara a un colega en la sala de reuniones.

---

## Calibración por Tipo de Documento

| Tipo | Tono | Marcadores clave |
|---|---|---|
| Artículo científico | Preciso, impersonal donde procede, directo | Voz activa plural, cuantificado, pasado para métodos |
| Material didáctico UGR | Claro, estructurado, motivador sin ser condescendiente | Headers temáticos, ejemplos concretos, nexos explícitos |
| Memoria de proyecto / ISCIII | Ambicioso, fundamentado en datos preliminares | "Demostraremos", "Nuestros datos preliminares muestran" |
| Documentación ISO | Procedimental, sin ambigüedad | Imperativo, frases de acción única, numeración |
| Web de asignatura / Google Sites | Accesible, orientado al estudiante | Frases cortas, verbos de acción, sin jerga innecesaria |

---

## Qué NO Modificar
- Datos, citas bibliográficas, valores estadísticos
- Bloques de código, SMILES, secuencias de ácidos nucleicos
- Nombres propios: DestiNA, UGR, QFDOS, KRT10, miR-122, MALDI-TOF, Genyo
- Fórmulas y nomenclatura química ya en formato Unicode correcto
