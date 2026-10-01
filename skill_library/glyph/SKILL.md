---
name: glyph
description: Chemical structures, Unicode scientific typography, and visual glyph generator. Use for rendering SMILES to SVG/PNG (RDKit), converting formulas to clean Unicode glyphs (zero raw LaTeX), and generating QFDOS visual badges and pharmacophore callouts.
---

# glyph — Generador de Glifos Científicos y Estructuras Químicas

**Trigger**: Usar cuando el usuario pida renderizar estructuras químicas desde SMILES, convertir notación científica/química a glifos Unicode nativos, generar diagramas 2D/3D moleculares o crear insignias visuales (badges/iconos) acordes al sistema de diseño QFDOS.

---

## Capacidades Principales

1. **Renderizado de Estructuras Moleculares (2D/3D)**:
   - Conversión de SMILES / nombres de fármacos a imágenes vectoriales SVG o mapas de bits PNG de alta resolución mediante RDKit.
   - Resaltado de farmacóforos, subestructuras y grupos funcionales clave.
   - Generación de conformeros 3D y compatibilidad con Rowan Scientific API.

2. **Tipografía y Glifos Científicos Unicode (Zero Raw LaTeX)**:
   - Conversión automática de fórmulas y expresiones LaTeX (`$...$`, `\Delta`, `\pm`) a caracteres Unicode limpios para diapositivas, apuntes y web.
   - Notación estandarizada: RMN (¹H, ¹³C), constantes (KD, Ka, ΔG°, ΔH, Ea), iones ([M+H]⁺, Zn²⁺) y unidades (µM, nM, Å, °C).

3. **Insignias y Glifos Visuales QFDOS (Genyo Fusion)**:
   - Creación de componentes SVG / HTML de insignias visuales con la paleta de identidad QFDOS: Azul Marino (`#1e3a8a`), Teal (`#0d9488`), Menta (`#2dd4bf`).

---

## 1. Pipeline de Renderizado Químico (RDKit)

Para generar una imagen molecular limpia y estilizada:

```python
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D

def render_smiles_to_svg(smiles: str, output_path: str, width: int = 400, height: int = 300):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        raise ValueError(f"SMILES inválido: {smiles}")
    
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    opts = drawer.drawOptions()
    opts.clearBackground = True
    opts.bondLineWidth = 2.0
    opts.padding = 0.05
    
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
    drawer.FinishDrawing()
    
    svg = drawer.GetDrawingText()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return output_path
```

---

## 2. Tabla de Normalización de Glifos Unicode

| Expresión Cruda / LaTeX | Glifo Unicode Estándar | Ámbito |
| :--- | :--- | :--- |
| `^1H NMR`, `1H-RMN` | **¹H RMN** | Resonancia Magnética Nuclear |
| `^13C NMR` | **¹³C RMN** | Resonancia Magnética Nuclear |
| `[M+H]^+` | **[M+H]⁺** | Espectrometría de Masas |
| `[M-H]^-` | **[M-H]⁻** | Espectrometría de Masas |
| `\Delta G^\circ` | **ΔG°** | Termodinámica química |
| `\Delta H`, `\Delta S` | **ΔH, ΔS** | Entalpía / Entropía |
| `K_D`, `K_a`, `K_b` | **KD, Ka, Kb** | Constantes de afinidad / equilibrio |
| `+/-` o `\pm` | **±** | Incertidumbre / Estadísticos |
| `\approx`, `\sim` | **≈** | Aproximación |
| `\mu M`, `uM` | **µM** | Concentración |
| `Angstrom`, `\AA` | **Å** | Distancia interatómica |
| `delta = 7.5 ppm` | **δ = 7,5 ppm** | Desplazamiento químico |
| `J = 8.2 Hz` | **J = 8,2 Hz** | Constante de acoplamiento |

---

## 3. Insignias y Glifos Visuales (HTML/SVG)

Para insertar insignias de farmacóforo o propiedades ADMET en materiales didácticos:

```html
<!-- Badge Farmacóforo QFDOS -->
<span style="display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:9999px; background:#1e3a8a; color:#ffffff; font-family:'Montserrat',sans-serif; font-size:12px; font-weight:600;">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"></circle>
    <path d="m10 15 5-3-5-3v6Z"></path>
  </svg>
  FARMACOFORO
</span>
```

---

## 4. Script de Soporte Local

Puedes invocar directamente el script auxiliar ubicado en:
`scripts/render_glyph.py`, dentro de la carpeta de esta skill (en este equipo: `~/.agents/skill-library/glyph/scripts/render_glyph.py`; usa `py -3.13`, que tiene RDKit).

Sintaxis CLI:
```bash
py -3.13 "$HOME/.agents/skill-library/glyph/scripts/render_glyph.py" --smiles "CC(=O)Oc1ccccc1C(=O)O" --out "Imagenes/aspirina.svg" --name "Aspirina"
```
