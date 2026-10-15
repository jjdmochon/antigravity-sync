---
name: qfdos-exam-generator
description: Metodología oficial, pipeline de generación, calibración psicométrica y quimioinformática para la preparación de exámenes de Química Farmacéutica II (2627 QFDOS E · Grado en Farmacia, Universidad de Granada), impartida por el Dr. Juan José Díaz-Mochón. Cubre diseño por bloques temáticos (SAR, síntesis y retrosíntesis, farmacóforos, bioisostería, interacciones moleculares PDB), balanceo riguroso de claves (25% A/B/C/D), paridad de longitud anti-slop, estructuras químicas vectoriales RDKit y formatos duales (alumno/solucionario) en Markdown limpio y HTML5. Consolida cada pregunta contra los apuntes finales publicados de cada tema (fuente de verdad docente) e incluye mecanismo de auto-actualización progresiva desde '1. Temas 2627/Presentaciones Finales'.
license: MIT
metadata:
  author: Dr. Juan José Díaz-Mochón & Jev System-1
  institution: Universidad de Granada (UGR) · Dpto. Química Farmacéutica y Orgánica
  course: Química Farmacéutica II (2627 QFDOS E)
  repository_source: "1. Temas 2627/Presentaciones Finales"
---

# QFDOS Exam Generator · Química Farmacéutica II (UGR)

Esta skill codifica la metodología oficial, psicométrica y quimioinformática del **Dr. Juan José Díaz-Mochón** para diseñar, redactar, calibrar y maquetar los exámenes de **Química Farmacéutica II (2627 QFDOS E)** en el Grado en Farmacia de la Universidad de Granada.

Cualquier agente (Claude Projects, Claude Cowork, Claude Desktop, Antigravity) que prepare exámenes o bancos de autoevaluación para QFDOS debe seguir estrictamente este estándar.

---

## 0. Modos de Examen y Criterios Docentes de Juanjo

### Modalidades Disponibles
1. **Modalidad UGR / Oficial Mochón (Por Defecto):**
   - 4 opciones (**a**, **b**, **c**, **d**) o 5 opciones (**a**–**e**).
   - Baremo oficial: acierto **+1.0**, error **-0.25**, en blanco **0.0**.
   - Énfasis absoluto en: estructuras químicas en enunciados y opciones, mecanismos de síntesis paso a paso, desconexiones retrosintéticas con sintones/reactivos, residuos aminoacídicos del sitio de unión (PDB), conformaciones activas y diagramas SAR.
2. **Modalidad FIR (Simulacro Especialidad):**
   - 4 opciones numeradas (**1**, **2**, **3**, **4**).
   - Baremo: acierto **+3.0**, error **-1.0**, en blanco **0.0**.
   - Enfoque conceptual aplicado, discriminación de alternativas "FALSA", "INCORRECTA" o "EXCEPTO", sin desarrollo de síntesis multinivel.

### Las Máximas Docentes de Juanjo ("No quiero Cervantes, quiero Fórmulas")
- **Química sobre retórica:** No describir con párrafos vagos lo que se explica con un centro estereogénico, un desplazamiento de electrones o una interacción electrostática calculable.
- **Rigor en reactivos e intermedios:** Exigir siempre reactivos concretos (ej. no decir "se añade una amina", especificar *trimetilamina en SN2* o *anhídrido acético con catálisis ácida*).
- **Mecanismos catalíticos y aminoácidos del sitio activo:** Formular preguntas rigurosas sobre los residuos involucrados en la acción catalítica y de fijación de las enzimas (ej. en AChE: enlace iónico con Asp en sitio aniónico, enlace H con Tyr en sitio esterásico, Ser como nucleófilo principal e His como catalizador ácido/base general).
- **Prohibición de Spoilers Visuales en Exámenes:** **NUNCA incluir imágenes de presentaciones o esquemas que contengan la respuesta a la pregunta** (por ejemplo, infografías con flechas de reacción rotuladas con los reactivos o esquemas con los aminoácidos etiquetados). En un examen, la imagen debe ser la estructura de partida o el reto, nunca la resolución.
- **Prohibición de Citas de Diapositivas:** **NUNCA mencionar "Diapositiva X", "impartido en clase" ni referencias a slides en el enunciado.** Es un modelo oficial de examen, por lo que la redacción debe ser formal, contextualizada y directa.
- **Ruta Prioritaria para Estructuras Químicas (`Estructuras QFDOS/Tema X`):** Antes de generar estructuras con RDKit desde cero o buscar externamente, el agente DEBE revisar obligatoriamente si las moléculas ya están curadas en el repositorio institucional:  
  `<unidad>:\Mi unidad\Classroom\2627 QFDOS E\1. Temas 2627\Estructuras QFDOS\Tema X\` (ficheros `QFDOS-0xx_<nombre>.png`). Si no existieran o se requiere vector SVG limpio, generarlas con RDKit y enriquecerlas vía PubChem.
- **Fidelidad a los apuntes finales:** Cada pregunta se consolida contra los apuntes finales publicados del tema (`QFDOS Tema X Apuntes.pdf`). Si no está en los apuntes, no se pregunta.
- **Justificación mecanística en solucionarios:** Detallar siempre el porqué químico (pKa, estados de transición tetraédricos, grupos salientes, constantes dieléctricas locales, impedimento estérico vs resonancia).

---

## 1. Protocolo de Auto-Actualización Progresiva del Temario

Esta skill está diseñada para sincronizarse dinámicamente conforme avance el curso 2026/2027.

### Rutas Maestras de Fuentes Docentes

Raíz del curso: `<unidad>:\Mi unidad\Classroom\2627 QFDOS E\` (Google Drive para escritorio; `K:` en destina-onp, la letra puede variar en otro equipo). Todas las rutas siguientes son relativas a `1. Temas 2627\`.

1. **Apuntes Finales Publicados del Tema (Fuente de Verdad para Consolidar Preguntas):**
   `Presentaciones Finales\Apuntes\Publicados\QFDOS Tema X Apuntes.pdf`
   Es el texto que estudia el alumno. Toda pregunta debe poder resolverse con lo que dicen estos apuntes (ver sección 8, LOOP 0).
   Si el PDF no permite extraer texto limpio (`pdftotext -layout` o PyMuPDF), usar la versión fuente en `Presentaciones Finales\Apuntes\raw\` (ej. `Tema 3. QFDOS Completa.md`), comprobando que coincide con el PDF publicado.
2. **Repositorio Oficial de Estructuras Químicas (Prioridad 1 para Imágenes de Moléculas):**
   `Estructuras QFDOS\Tema X\`
   Contiene los archivos curados en alta resolución (`QFDOS-001_acetilcolina.png`, `QFDOS-014_betanecol.png`, etc.) y el maestro `estructuras_qfdos.csv`.
3. **Presentación de Diapositivas (Para Extraer Contenidos y Síntesis, NO para pegar como respuesta en test):**
   `Presentaciones Finales\Tema X\Tema X QFDOS Final.md` (y su carpeta `chemdraw/`).
4. **Transcripciones de Clase:**
   `Transcripciones\` (y `Transcripciones\Apuntes limpios\`). Sirven para detectar énfasis, ejemplos y matices dichos en el aula, no como fuente de verdad.

### Jerarquía de Fuentes ante Discrepancias
**Apuntes finales publicados > Presentación final > Transcripciones > Fuentes externas (PubChem, ChEMBL, bibliografía).**
Si una transcripción o la presentación contradicen los apuntes publicados (nombre de un reactivo, condiciones de una ruta, residuo del sitio activo, selectividad), la pregunta se redacta según los apuntes y la discrepancia se anota en el solucionario docente para revisión. Si un dato externo indica un error en los apuntes, ese punto no se pregunta hasta que el docente actualice los apuntes, y se avisa en el informe de la generación.

### Estado de Publicación por Tema
- **`Tema 1/`**: Acetilcolina y Sistema Colinérgico (COMPLETO ✅). Apuntes: `QFDOS Tema 1 Apuntes.pdf`.
- **`Tema 2/`**: Apuntes publicados: `QFDOS Tema 2 Apuntes.pdf`.
- **`Tema 3/`**: Dopamina, Parkinson y Antipsicóticos. Apuntes publicados: `QFDOS Tema 3 Apuntes.pdf`.
- **`Tema 4/` en adelante**: Antes de generar un examen, el agente lista `Presentaciones Finales\Apuntes\Publicados\`. Si los apuntes del tema todavía no están publicados, lo indica al docente y genera el examen como **borrador provisional**, consolidado solo contra la presentación final y marcado así en la cabecera del solucionario.

---

## 2. Catálogo Maestro de Contenidos Consolidados: Tema 1 (Sistema Colinérgico)

### 2.1. Las 7 Etapas Presinápticas y su Modulación Farmacológica
1. **Biosíntesis:** Colina acetiltransferasa (ChAT); colina + Acetil-CoA → Acetilcolina.
2. **Almacenamiento:** Transportador vesicular (VAChT); inhibido por *vesamicol*.
3. **Despolarización:** Apertura de canales de Ca²⁺ dependientes de voltaje; bloqueada por *anestésicos locales*.
4. **Liberación (Exocitosis):** Complejo SNARE dependiente de Ca²⁺; inhibido irreversiblemente por *toxina botulínica*.
5. **Interacción con Receptores:** Receptores Muscarínicos (GPCR: M1, M3, M5 acoplados a Gq; M2, M4 acoplados a Gi) y Nicotínicos (canales iónicos pentaméricos α2βγδ o α7).
6. **Recaptación de Colina:** Transportador de alta afinidad (CHT1, simporte Na⁺/Cl⁻); inhibido por *hemicolinio-3*.
7. **Metabolismo:** Acetilcolinesterasa (AChE); degradación a colina y acetato en microsegundos; inhibida por *anticolinesterásicos*.

### 2.2. Agonistas Colinérgicos Directos (SAR de la Acetilcolina)
- **Regla de los Cinco Átomos de Ing:** La cadena hidrocarbonada entre el nitrógeno cuaternario y el átomo de hidrógeno terminal no debe exceder de 5 átomos para mantener actividad agonista óptima.
- **Cabeza Catiónica:** Requiere tres metilos (-N⁺(CH₃)₃). La sustitución por etilos (trietilo) o grupos mayores transforma la molécula en antagonista o anula la afinidad por alejamiento estérico del residuo aniónico (r > 7 Å) y aumento de la constante dieléctrica local por intrusión de agua.
- **Puente Etilénico (alfa vs beta):**
  - **α-Metilcolina:** Selectiva por receptores *nicotínicos*.
  - **β-Metilcolina (Metacolina):** Selectiva por receptores *muscarínicos*. La hidrólisis por AChE se reduce a la mitad.
  - **Estereoquímica y Eudismia:** El enantiómero **(S)-metacolina** es ~250 veces más potente que el distómero (R), mimetizando la disposición tridimensional de la (+)-(2S,4R,5S)-muscarina.
- **Grupo Aciloxi (Éster vs Carbamato):**
  - **Carbacol:** Sustitución de -CH₃ por -NH₂ (carbamato). La deslocalización del par libre del nitrógeno reduce el carácter electrófilo del carbono carbonílico (estabilidad electrónica por resonancia).
  - **Betanecol:** Combina el carbamato (estabilidad electrónica) con el metilo en beta (estabilidad estérica). Fármaco selectivo muscarínico de gran estabilidad metabólica, activo por vía oral para la atonía gastrointestinal y retención urinaria postoperatoria.
- **Alcaloides Naturales Agonistas:** *Pilocarpina* (anillo lactónico + imidazol, tratamiento del glaucoma), *(+)-Muscarina*, *Cevimelina* (quinuclidina rígida, síndrome de Sjögren).

### 2.3. Síntesis Orgánica Industrial de Fármacos Colinérgicos
- **Metacolina:**
  1. Apertura regioselectiva de óxido de propileno con trimetilamina o cuaternización de 1-bromo-2-propanol con trimetilamina (N(CH₃)₃) vía SN2 → intermedio aminoalcohol cuaternario (1-(trimetilamonio)propan-2-ol).
  2. Acetilación del alcohol secundario con anhídrido acético ((CH₃CO)₂O) rindiendo metacolina.
- **Carbacol:**
  1. Reacción de 2-cloroetanol con fosgeno (COCl₂) → cloroformiato de 2-cloroetilo.
  2. Tratamiento con amoniaco gas (sustitución nucleófila acílica con Cl⁻ como grupo saliente) → carbamato de 2-cloroetilo.
  3. Cuaternización SN2 con trimetilamina → carbacol.
- **Betanecol:**
  1. Cuaternización de 1-cloropropan-2-ol con trimetilamina → 1-(trimetilamonio)propan-2-ol.
  2. Reacción con fosgeno → cloroformiato cuaternario intermedio.
  3. Amonólisis con amoniaco gas en exceso → betanecol.

### 2.4. Antagonistas Muscarínicos (Anticolinérgicos)
- **Modelos Naturales:** *(±)-Atropina* (éster del tropanol con ácido trópico; cruza BHE) y *Escopolamina* (puente epóxido 6,7; potente acción central y antiemética).
- **Derivados Cuaternarios Antiasmáticos / Espasmolíticos:**
  - *Bromuro de Ipratropio* (N-isopropilo, cuaternario, no cruza BHE, broncodilatador inhalado).
  - *Bromuro de Tiotropio* (anillos de tiofeno, acción prolongada LAMA).
  - *Butilescopolamina* (sal cuaternaria periférica, antiespasmódico visceral).
- **Diseño Racional y Convergencia Farmacofórica (Ésteres de Aminoalcoholes):**
  - La sobrecarga estérica de la acetilcolina y la simplificación de la atropina convergen en el andamiaje común: **R₁R₂C(OH)-COO-(CH₂)n-N⁺R₃R₄R₅**.
  - *Benactizina*, *Adifenina*, *Propantelina*, *Ciclopentolato*, *Tropicamida*.
- **Bioisostería del Enlace Éster en Antagonistas:**
  - **Amidas:** *Isopropamida* (amida cuaternaria de gran estabilidad metabólica).
  - **Alcoholes Terciarios (sin éster):** *Trihexifenidilo*, *Biperideno*, *Prociclidina* (antiparkinsonianos centrales).
  - **Éteres:** *Benztropina* (éter difenílico con tropina).

### 2.5. Retrosíntesis y Desconexiones Críticas en Colinérgicos
1. **Benactizina:** Desconexión éster acilo-oxígeno → ácido bencílico + 2-(dietilamino)etanol. El ácido bencílico procede de la **transposición del ácido bencílico** (bencilo [1,2-dicetona] tratada con KOH/EtOH).
2. **Ciclopentolato:** Desconexión carbinólica → ciclopentanona + dianión del ácido fenilacético (**Reactivo de Ivanov**).
3. **Trihexifenidilo y Biperideno:** Desconexión carbinólica → adición de reactivo de Grignard/organolítico (ciclohexilo o norbornenilo) sobre una **base de Mannich** (formada por acetofenona + formaldehído + piperidina).
4. **Isopropamida:** Desconexión retro-SN2 de metilo cuaternario, FGI amida a nitrilo, y alquilación con 2,2-difenilacetonitrilo.

### 2.5. Antagonistas Nicotínicos y Bloqueantes Neuromusculares (Curarizantes)
- **Tubocurarina:** Alcaloide natural bis-nitrogenado prototipo de los bloqueantes neuromusculares no despolarizantes.
- **Distancia Nicotínica Canónica (Barlow e Ing):** Los dos centros catiónicos se encuentran separados por una distancia rígida de **1.4 nm (14 Å)**. Esta separación complementa con exactitud los dos bolsillos de unión o zonas de cisteínas de las dos subunidades α del receptor nicotínico pentamérico muscular (α2βγδ), bloqueando la apertura del poro iónico.
- **Atracurio:** Diseño híbrido entre tubocurarina y suxametonio con eliminación espontánea no enzimática de Hofmann.

### 2.6. Mecanismo Catalítico y Residuos Clave de la Acetilcolinesterasa (AChE)
- **Arquitectura del Centro Activo y Residuos Clave:**
  - **Sitio Aniónico:** Residuo de **Aspartato (Asp)** que establece un enlace iónico/electrostático esencial con el catión trimetilamonio de la acetilcolina. En la garganta aromática intervienen **Trp-84** (interacción catión-π) y **Phe-330**.
  - **Sitio Esterásico:**
    - **Tirosina (Tyr):** Establece un enlace de hidrógeno clave con el oxígeno del enlace éster, orientando el sustrato.
    - **Serina (Ser-203):** Actúa como el **nucleófilo principal**. Por sí sola es incapaz de hidrolizar un éster.
    - **Histidina (His-440):** Actúa indispensablemente como **catalizador ácido/base general** a lo largo de todo el ciclo catalítico.
    - **Glutamato (Glu-327):** Asiste a la histidina en la tríada catalítica.
- **Fases del Mecanismo Catalítico:**
  - **Fase 1 (Ataque Nucleófilo):** El -OH de la Serina ataca al carbonilo de la AcC, asistido por la transferencia de protones con la Histidina.
  - **Fase 2 (Acetilación):** Se forma un enlace covalente acetil-enzima y se expulsa la colina como grupo saliente.
  - **Fase 3 (Desacetilación):** Ataque nucleófilo rápido del agua sobre la serina acetilada asistido por la histidina para regenerar la enzima libre en microsegundos.
- **Inhibición Carbámica vs Acetilación:** La carbamoilación de la Serina genera un intermediario carbamil-enzima resistente que tarda horas en hidrolizarse (pseudoirreversible).
- **Inhibidores Irreversibles (Organofosforados) y Reactivadores:** Fosforilación covalente de la Serina; fenómeno de envejecimiento (*aging*) por pérdida hidrolítica de un grupo alcoxi generando un oxígeno aniónico terminal (-P-O⁻) que repele electrostáticamente a los reactivadores oxímicos (*pralidoxima / 2-PAM*).
- **Inhibidores Reversibles no Covalentes:** *Donepezilo* (fármaco clave en Alzheimer que bloquea el centro activo mediante interacciones puramente no covalentes [fuerzas de Coulomb, puentes H y apilamiento π], sin transferir restos covalentes a la serina, a diferencia de los carbamatos pseudoirreversibles y organofosforados irreversibles).

---

## 3. Los 5 Mandamientos Psicométricos y Calidad JEV System-1

Para garantizar exámenes científicamente justos, robustos e inmunes a sesgos de detección de respuestas:

### Mandamiento 1 · Entropía de Claves Equilibrada (25% por Letra)
- En un examen de 4 opciones (**a**, **b**, **c**, **d**), la respuesta correcta debe estar uniformemente repartida:
  - En exámenes de 8 preguntas: exactamente **2 A, 2 B, 2 C, 2 D**.
  - En exámenes de 15 preguntas: exactamente **4 A, 4 B, 4 C, 3 D** (o permutaciones homogéneas).
  - En exámenes de 20 preguntas: exactamente **5 A, 5 B, 5 C, 5 D**.
  - En exámenes de 50 preguntas: exactamente **12-13 por opción** (~25%).
- **Prohibido:** Concentraciones de respuestas en una misma letra superiores al 30%.

### Mandamiento 2 · Paridad de Longitud Anti-Slop (Cero Pistas de Extensión)
- **Principio:** La opción correcta **NUNCA debe ser perceptiblemente más larga** ni más rica en detalles que los distractores.
- La desviación de longitud entre opciones dentro de una misma pregunta debe ser **inferior al 10% (±15 caracteres)**.
- Todos los distractores deben estar redactados con idéntico rigor conceptual, terminología farmacológica precisa y longitud homogénea.

### Mandamiento 3 · Distractores Verosímiles y Didácticos
- Los distractores deben fundamentarse en:
  1. Inversión estereoquímica (confundir eutómero con distómero; ej. (R)-metacolina activa).
  2. Confusión de subtipos de receptor (agonismo muscarínico confundido con nicotínico).
  3. Desconexiones retrosintéticas inviables químicamente (ej. intentar un ataque SN2 sobre un carbono sp² aromático sin activación, en vez de usar haluro bencílico).
  4. Falsa atribución mecanística (atribuir estabilidad a impedimento estérico cuando se debe a efecto de resonancia mesómera electrónica).

### Mandamiento 4 · Cero LaTeX Crudo (Tipografía Científica Unicode Nativa)
- En ningún caso deben utilizarse delimitadores LaTeX (`$...$`, `\(...\)`, `\text{...}`) en los textos Markdown, HTML o exportables a Word/Google Docs.
- Usar siempre símbolos tipográficos y químicos Unicode limpios:
  - Cationes y aniones: N⁺, Cl⁻, Br⁻, I⁻, Zn²⁺, O⁻
  - Enlaces y centros: C–C, C–N, C–O, sp², sp³, Cα, Cβ, π-stacking
  - Fórmulas químicas: H₂SO₄, COCl₂, CH₃COCl, (CH₃CO)₂O, NH₂, OH
  - Termodinámica y magnitudes: ΔG°, Kd, Ki, IC₅₀, pKa, Å, °C, μM, nM
  - Letras griegas: α, β, γ, δ, ε, λ, ν

### Mandamiento 5 · Verificación Quimioinformática Estricta (RDKit)
- Toda estructura química citada o mostrada debe tener asignado un código SMILES canónico químicamente válido.
- Prohibidos carbonos pentavalentes, valencias hipervalentes no permitidas en heteroátomos o estereocapas erróneas.
- Cada pregunta ilustrada debe contar con su correspondiente renderizado SVG vectorial limpio (sin fondos oscuros, tamaño estándar 240×180 o 300×200 px).

---

## 4. Estructura Estándar de una Pregunta de Examen

Cada ítem del banco debe seguir esta plantilla rigurosa:

```markdown
### Pregunta X · [Tema o Bloque Temático] · [Concepto Específico]
[Enunciado riguroso, contextualizado clínica o químicamente, planteando un problema directo o comparativo]

- **a)** [Opción A - longitud calibrada ~120-150 car.]
- **b)** [Opción B - longitud calibrada ~120-150 car.]
- **c)** [Opción C - longitud calibrada ~120-150 car.]
- **d)** [Opción D - longitud calibrada ~120-150 car.] **[CORRECTA]**

*Justificación Química y Mecanística:* 
[Explicación detallada de por qué la opción seleccionada es la químicamente verídica (mecanismo, centros reactivos, pKa, distancias, interacciones PDB)].

*Análisis de Distractores:*
- **a)** [Por qué es falsa: qué error conceptual representa].
- **b)** [Por qué es falsa: qué mecanismo o reactivo equivocado asume].
- **c)** [Por qué es falsa: qué regla de SAR o estereoquímica vulnera].
```

---

## 5. Formatos de Salida Dual Obligatorios

Cuando se solicite un examen, se deben generar simultáneamente dos archivos maestros:

1. **Cuadernillo del Alumno (`..._ALUMNO.md` / `.html`):**
   - Encabezado oficial UGR (Grado en Farmacia, Asignatura, Convocatoria).
   - Tabla de instrucciones y puntuación (+1 acierto, -0.25 error, 0 en blanco).
   - Enunciados y opciones limpias con sus gráficos moleculares.
   - Sin marcas de respuestas correctas ni justificaciones.
   - Plantilla de respuestas integrada al final para corrección rápida.

2. **Solucionario Docente (`..._SOLUCIONARIO.md` / `.html`):**
   - Tabla con la Clave de Corrección Rápida en la cabecera (distribución 25% por letra).
   - En cada pregunta: indicación explícita de `[CORRECTA]`.
   - Justificación química pormenorizada con mecanismos, flechas sintéticas o residuos aminoacídicos involucrados.
   - Desglose pedagógico de los 3 distractores para retroalimentación en clase de dudas o seminario.
   - Referencia a la sección de los apuntes finales del tema que respalda cada respuesta, y lista de discrepancias detectadas entre apuntes, presentación y transcripciones.

---

## 6. Script Helper Quimioinformático (RDKit SVG Pipeline)

Para generar las imágenes vectoriales SVG con RDKit para las opciones y enunciados:

```python
from rdkit import Chem
from rdkit.Chem import rdMolDraw2D

def generate_svg(smiles: str, output_path: str, width: int = 280, height: int = 180):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"SMILES no válido: {smiles}")
    Chem.Kekulize(mol)
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    drawer.drawOptions().clearBackground = True
    drawer.drawOptions().bondLineWidth = 2
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(drawer.GetDrawingText())
```

---

## 7. Bloque SAR y Calibración Cuantitativa con ChEMBL

Para preguntas de Relación Estructura-Actividad (SAR), selectividad de subtipo y relaciones eudísmicas, el agente debe basarse en datos experimentales reales contrastados en **ChEMBL** (`scripts/chembl_qfdos.py` y `scripts/generar_preguntas_sar.py`):

1. **Selectividad de Subtipo Receptor/Enzima**:
   - Contrastar valores de afinidad Ki o IC50 medidos en subtipos humanos (ej. M1 vs M2/M3 para pirenzepina, beta1 vs beta2 para atenolol/propranolol, COX-1 vs COX-2 para celecoxib).
   - Justificar las diferencias de afinidad en función de los bolsillos aminoacídicos del receptor (residuos PDB).
2. **Relación Eudísmica y Estereoquímica Cuantitativa**:
   - Cuantificar la relación eudísmica real (potencia del eutómero frente al distómero) y vincularla a la regla de Pfeiffer y a la interacción multipuntual de Easson-Stedman.
3. **Modificaciones Bioisostéricas**:
   - Evaluar cuantitativamente la variación del pChEMBL y la estabilidad metabólica (ej. éster vs carbamato en colinérgicos).
4. **Comando de Generación Automatizada**:
   ```powershell
   .\.venv\Scripts\python.exe scripts\generar_preguntas_sar.py --tema 1 --modalidad ugr -o "Pregunta tipo tests (examenes)\Tema 1\examen_sar_chembl.md"
   ```

---

## 8. Grafo de Orquestación Multiagente (Plantilla Común a Todos los Temas)

Todo examen de QFDOS se genera con el mismo grafo. La topología es fija; lo único que cambia de un tema a otro es la entrada (rango del catálogo `QFDOS-xxx`, apuntes finales publicados y transcripciones del tema) y la asignación de fármacos a cada subagente.

### 8.1. Topología (instancia de referencia: Tema 3 · Dopamina, Parkinson y Antipsicóticos)

```text
[Input: Catálogo Maestro QFDOS-127 a QFDOS-169 + QFDOS Tema 3 Apuntes.pdf + Transcripciones Aula 7]
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│  ORQUESTADOR CENTRAL (QFDOS Exam Generator · Grupo E · Modelo B)  │
└───────┬─────────────────┬────────────────────┬────────────────────┘
        │                 │                    │
        ▼                 ▼                    ▼
 [Subagente SAR]   [Subagente Síntesis]  [Subagente Bio/Metab]
  · Prometazina     · Carfenazina         · Selegilina (R vs S)
  · Levomepromazina · Amantadina (Ritter) · Rasagilina (Indano)
  · Ortopramidas    · Haloperidol (Prins) · Tolcapona (pKa/COMT)
  · Droperidol      · Tionación / Ullmann · MPTP → MPP+ (MAO-B)
        │                 │                    │
        └─────────────────┼────────────────────┘
                          ▼
        🔄 LOOP 0: Consolidación contra Apuntes Finales del Tema
        (Cada ítem trazado a una sección de los apuntes · Apuntes > Presentación > Transcripción)
                          │
                          ▼
        🔄 LOOP 1: Renderizado de Estructuras Químicas
        (Diagramas estructurales ASCII/Unicode + SMILES validados)
                          │
                          ▼
        🔄 LOOP 2: Auditoría Psicométrica JEV System-1
        (Entropía 25%: 4A, 4B, 4C, 3D · Paridad de longitud ±15 car. · Cero LaTeX)
                          │
                          ▼
        [Entregable Dual: Cuadernillo del Alumno + Solucionario Docente]
```

### 8.2. Plantilla genérica para cualquier Tema X

```text
[Input: Catálogo Maestro QFDOS-<inicio> a QFDOS-<fin> (Estructuras QFDOS\Tema X) + QFDOS Tema X Apuntes.pdf + Transcripciones del Tema X]
        │
        ▼
  ORQUESTADOR CENTRAL (QFDOS Exam Generator · Grupo E · Modelo <A/B/…>)
        │
        ├──► [Subagente SAR]          fármacos con preguntas de estructura-actividad, selectividad, eudismia
        ├──► [Subagente Síntesis]     fármacos con ruta sintética o retrosíntesis impartida (reacciones con nombre)
        └──► [Subagente Bio/Metab]    enzimas, metabolismo, profármacos, estereoquímica de unión, pKa
        │
        ▼
  LOOP 0 · Consolidación contra los apuntes finales publicados del Tema X
        │
        ▼
  LOOP 1 · Renderizado de estructuras (SMILES validados con RDKit, PNG oficiales QFDOS-xxx si existen)
        │
        ▼
  LOOP 2 · Auditoría psicométrica JEV System-1 (entropía de claves, paridad de longitud, cero LaTeX)
        │
        ▼
  Entregable dual: Cuadernillo del Alumno + Solucionario Docente
```

### 8.3. Responsabilidades de cada nodo

- **Orquestador central:**
  - Lee primero los apuntes finales publicados del tema y extrae su índice de secciones; con él define los bloques y el peso de cada uno en el examen (un bloque que no aparece en los apuntes no se pregunta).
  - Lee el rango del catálogo (`estructuras_qfdos.csv` filtrado por tema) y las transcripciones del tema.
  - Reparte los fármacos entre los tres subagentes sin solapamientos y fija el número de preguntas por bloque (por defecto, reparto equilibrado: 5/5/5 para un examen de 15 preguntas).
  - Fija el modelo de examen (A, B…) y el grupo (E); el orden de preguntas y la clave cambian entre modelos.
- **Subagente SAR:** redacta preguntas de relación estructura-actividad, selectividad de subtipo y bioisostería (sección 7, datos ChEMBL cuando existan).
- **Subagente Síntesis:** redacta preguntas de síntesis y retrosíntesis con reactivos concretos, intermedios y reacciones con nombre tal como se impartieron (ej. Ritter, Prins, Ullmann, tionación en Tema 3).
- **Subagente Bio/Metab:** redacta preguntas de mecanismo enzimático, metabolismo, profármacos, estereoquímica de unión y pKa (ej. MAO-B, COMT, MPTP → MPP⁺ en Tema 3).
- Cada subagente recibe el fragmento de los apuntes que corresponde a sus fármacos y entrega sus ítems en la plantilla de la sección 4, con SMILES por cada estructura citada, la referencia a la sección de los apuntes que respalda la respuesta y sin asignar todavía la letra correcta definitiva.

### 8.4. Bucles de control (se repiten hasta pasar)

- **LOOP 0 · Consolidación contra los apuntes finales del tema:**
  - Cada ítem debe poder resolverse con el contenido de `QFDOS Tema X Apuntes.pdf`. En el solucionario se anota la sección o epígrafe de los apuntes que respalda la opción correcta (solo en el solucionario, nunca en el cuadernillo del alumno).
  - Se contrastan con los apuntes: nombres de fármacos y reactivos, condiciones y orden de las etapas sintéticas, intermedios, residuos del sitio activo, selectividades, valores numéricos (pKa, Ki, distancias) y estereoquímica.
  - Los distractores deben poder descartarse con claridad a partir de los apuntes; un distractor que los apuntes no permiten descartar invalida el ítem.
  - Falla si: el ítem pregunta por contenido ausente de los apuntes, usa una nomenclatura o ruta distinta a la de los apuntes, o la respuesta correcta depende solo de algo dicho en una transcripción.
  - Ante un fallo, el ítem vuelve a su subagente con el fragmento de los apuntes que debe usar. Las discrepancias entre fuentes se resuelven con la jerarquía de la sección 1.
  - Cobertura: el orquestador comprueba que los bloques principales de los apuntes quedan representados y que ningún bloque acumula más preguntas de las que justifica su extensión en los apuntes.

- **LOOP 1 · Renderizado de estructuras químicas:**
  - Prioridad 1: PNG oficial `QFDOS-xxx_<nombre>.png` de `Estructuras QFDOS\Tema X\`.
  - Si no existe: SVG con RDKit (sección 6) desde SMILES canónico validado; diagramas ASCII/Unicode solo como apoyo en texto plano.
  - Falla si: SMILES no parsea, valencias imposibles, estereocentros sin asignar donde la pregunta depende de ellos, o la imagen contiene la respuesta (spoiler visual, sección 0).
  - Ante un fallo, el ítem vuelve a su subagente de origen.
- **LOOP 2 · Auditoría psicométrica JEV System-1:**
  - El orquestador asigna las letras correctas para cumplir la entropía de la sección 3 (15 preguntas → 4A, 4B, 4C, 3D; 20 → 5/5/5/5).
  - Comprueba paridad de longitud ±15 caracteres por pregunta, que la correcta no sea la más larga, ausencia de absolutos delatores ("nunca", "siempre") y cero delimitadores LaTeX.
  - Si `jev_gate_text` / `jev_gate_file` están disponibles, se usan como gate automático; el ítem que no pasa vuelve a su subagente con el motivo.
- **Salida:** solo cuando los tres bucles (0, 1 y 2) pasan se maquetan el Cuadernillo del Alumno y el Solucionario Docente (sección 5).

### 8.5. Cómo instanciar el grafo para un tema nuevo

1. Sustituir el rango `QFDOS-<inicio>` a `QFDOS-<fin>` por el del tema (consultar `estructuras_qfdos.csv`).
2. Sustituir los apuntes finales y las transcripciones de entrada por los del tema (comprobar que `QFDOS Tema X Apuntes.pdf` existe en `Apuntes\Publicados\`).
3. Reasignar los fármacos del tema a los tres subagentes según el tipo de pregunta que permiten.
4. Mantener sin cambios los tres bucles, los criterios de la sección 3 y el entregable dual.

---

## 9. Calibración y Calidad Final (Quality Gate)

Antes de dar por finalizado un set de examen de QFDOS, el agente debe validar:

- [ ] ¿Están representados equilibradamente los bloques temáticos de la materia impartida?
- [ ] ¿Cumple la clave de respuestas la entropía del 25% por cada letra (A, B, C, D)?
- [ ] ¿Se ha verificado que la opción correcta no es la más larga en ninguna pregunta?
- [ ] ¿La diferencia de caracteres entre distractores y correcta es menor de 15 caracteres?
- [ ] ¿Hay cero delimitadores LaTeX crudos (`$...$`), empleando 100% tipografía Unicode nativa?
- [ ] ¿Todos los nombres de fármacos, reactivos, enzimas y residuos (ej. Ser203, Trp84) están contrastados bibliográficamente?
- [ ] ¿Se entregan por separado el cuadernillo del alumno y el solucionario con desglose de distractores?
- [ ] ¿Cada pregunta se resuelve con los apuntes finales publicados del tema y el solucionario indica la sección que la respalda?
- [ ] ¿Se ha seguido el grafo de la sección 8 (tres subagentes; LOOP 0 de consolidación con apuntes, LOOP 1 de estructuras y LOOP 2 psicométrico superados por todos los ítems)?
