---
name: jev-system-one
description: Ultrarrápido motor de decisiones "System 1" no autoregresivo (TypeSafe AI Jev) para enrutamiento de subagentes (<100ms), circuit breakers, filtrado de slop de IA y triaje de tareas docentes y biotecnológicas con primitivas Choice, Noul y Score.
---

# Jev System-1 Fast Decision Engine

Motor de decisiones estructuradas de ultrabaja latencia impulsado por **Jev (TypeSafe AI)**.

## Capacidades principales

1. **Subagent & Domain Routing**
   - Clasifica cualquier instrucción hacia los dominios de Juanjo (`destina_biotech`,
     `ugr_teaching`, `biophysics_pna`, `keratin_krt10`, `compliance_iso`,
     `review_provenance`, `scientific_tools`, `general_dev`).
   - Decide de forma no autoregresiva si delegar en subagente paralelo (`requires_subagent`)
     o ejecutar directamente.

2. **Quality Gate documental (`Noul`)**
   - Decide qué etapas del pipeline de revisión necesita realmente un documento, y
     certifica el entregable antes de la firma.

3. **Primitivas disponibles**
   - `Choice`: clasificación discreta tipada. Devuelve `.choice`, `.confidence`, `.probabilities`.
   - `Noul`: decisión booleana calibrada. Devuelve `.noul` como probabilidad flotante.
   - `Score`: nivel ordinal o rúbrica. Devuelve `.score`, `.confidence`, `.probabilities`.

## Enrutamiento de tareas

```bash
# Salida estándar en texto:
python "$HOME/.agents/skills/jev-system-one/scripts/jev_router.py" "¿Cómo diseñar sondas SMART para detectar miR-122?"

# Salida en JSON para consumo directo por otros agentes:
python "$HOME/.agents/skills/jev-system-one/scripts/jev_router.py" "Prepara el examen de QFDOS tema 4" --json
```

## Gatekeeper del pipeline documental

Etapas 0 y 4 de la sección 3 de CLAUDE.md: triaje previo y certificación final.

```bash
# Triaje: qué etapas necesita realmente el documento
python "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" "ruta/documento.md"

# JSON para subagentes (así lo consume document-reviewer):
python "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" "informe.docx" --json

# Texto por stdin:
echo "texto a auditar" | python "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" -
```

Acepta `.md`, `.txt`, `.docx`, `.pdf` y `-` (stdin). Pasa **siempre la ruta del fichero**,
no el texto pegado: extrae `.docx` con python-docx y `.pdf` con PyMuPDF, y sobre
documentos largos muestrea cabeza, centro y cola para no perder slop enterrado a mitad.

`--lang es|en` fuerza el idioma; por defecto lo detecta Jev y resuelve el humanizador.

### Claves de salida

| Clave | Significado |
|---|---|
| `etapas_a_ejecutar` | Lista de etapas que sí hacen falta. Ejecuta solo esas. |
| `quality_gate_passed` | Certificación. `true` únicamente con veredicto real de Jev. |
| `humanizer_skill` | `humanizer-juanjo-es` o `humanizer-juanjo`, ya resuelto por idioma. |
| `slop_probability` | Noul de slop, umbral 0.50. |
| `has_latex_violations` | Regex literal OR Noul. |
| `engine` | `jev-native (typesafe-ai)` o `fallo-abierto (sin Jev)`. |

### Reparto de responsabilidades

Los invisibles (ZWSP, BOM, soft hyphen, TAG chars U+E0000), los homoglifos cirílicos y
griegos, y los formatos portadores de metadatos se detectan **localmente y sin API**: son
preguntas mecánicas con respuesta exacta y no procede delegarlas en un modelo
probabilístico. Solo el slop, la voz y el LaTeX van a Jev, que es donde hay juicio.

### Dos propiedades que conviene no romper

**Las instrucciones de `Noul` van especificadas al detalle a propósito.** Medido sobre el
mismo texto de slop evidente: con la instrucción vaga "¿contiene clichés de IA?" el Noul
devuelve 0.63 y no separa nada; con la instrucción enumerada que lleva el script, 0.97
frente a 0.03 en un texto limpio. Si alguien acorta esas constantes, la compuerta deja de
discriminar sin dar ningún error.

**Falla en abierto.** Si la API no responde, el gatekeeper ejecuta las cuatro etapas y
**deniega** la certificación. Una caída de red nunca debe aprobar un entregable.

## Configuración de entorno

La clave se lee de `~/.env` o de la variable de entorno:

```powershell
$env:TYPESAFE_API_KEY = "tu-api-key-de-typesafe"
```

Dependencias: `typesafe_sdk`, `python-dotenv`, `python-docx`, `pymupdf`.
