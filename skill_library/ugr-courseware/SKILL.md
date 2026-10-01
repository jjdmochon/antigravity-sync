---
name: ugr-courseware
description: Create or enhance teaching materials for UGR courses (QF1/QF2/Quimica Farmaceutica), including class notes, HTML5 simulators (Genyo Fusion), quizzes, and exam problems.
---

# ugr-courseware

**Activación**: Crear o mejorar material docente para asignaturas UGR, especialmente Química Física I (QF1) y II (QF2) / Química Farmacéutica. Incluye: apuntes, simuladores web, cuestionarios de evaluación, webs de asignatura (Google Sites), presentaciones de clase, problemas tipo examen.

---

## Contexto de la Asignatura

**Departamento**: Química Física — Universidad de Granada  
**Asignaturas principales**: QF1 (Termodinámica química y equilibrio), QF2 (Cinética química y electroquímica)  
**Sistema de evaluación**: Evaluación continua via Google Sites + Genyo  
**Entorno técnico**: Google Sites (hubs de evaluación), HTML5/CSS3 para simuladores, Genyo Fusion design system

---

## Tipos de Entregable y Protocolo

### 1. Apuntes / Notas de Clase

**Estructura para cada tema**:
1. **Motivación** (½ página): un problema real que el concepto resuelve (ej. "¿Por qué el diamante no se convierte en grafito a temperatura ambiente?")
2. **Marco conceptual**: definiciones formales con notación Unicode (ver abajo)
3. **Desarrollo matemático**: paso a paso, con cada paso justificado en texto
4. **Ejemplos resueltos**: mínimo 2, con valores numéricos y unidades completas
5. **Aplicaciones**: conexión explícita con química farmacéutica / bioquímica / DestiNA cuando sea relevante
6. **Problemas propuestos**: 3-5 problemas graduados (básico → intermedio → avanzado)

**Notación estándar** (nunca LaTeX en Markdown):
- Energía de Gibbs: ΔG, ΔG°, ΔfG°
- Entalpía: ΔH, ΔHr°, ΔHf°, ΔHcomb
- Entropía: ΔS, S°
- Equilibrio: Kp, Kc, Ka, Kb, Kw, Ksp
- Cinética: k (constante de velocidad), Ea (energía de activación), A (factor preexponencial)
- Electroquímica: E°cell, E°(cátodo), E°(ánodo), ΔG = -nFE
- Termodinámica: Cp, Cv, γ = Cp/Cv
- Concentración: [A], mol L⁻¹, M, mM, µM
- Temperatura: T (K), θ (°C)
- Presión: p (Pa), p° = 100 kPa

### 2. Simuladores Web HTML5 (Genyo Fusion)

Cuando el usuario pide un "simulador" o "herramienta interactiva":

**Diseño visual** (Genyo Fusion design system):
```css
/* Paleta principal */
--color-primary: #003B7E;      /* Azul UGR */
--color-secondary: #C8102E;    /* Rojo UGR */
--color-accent: #F5A623;       /* Naranja acento */
--color-bg: #F8F9FA;
--font-main: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

**Estructura estándar de simulador**:
```html
<!-- Cabecera con logo UGR + nombre asignatura -->
<!-- Panel de parámetros (sliders + inputs numéricos) -->
<!-- Visualización en tiempo real (Canvas o SVG) -->
<!-- Panel de resultados numéricos -->
<!-- Sección "¿Qué observas?" con preguntas guía -->
<!-- Botón "Exportar PNG" para entrega -->
```

**Funcionalidades mínimas**:
- Sliders con actualización en tiempo real (sin botón "calcular")
- Display de ecuación/fórmula relevante actualizada
- Tooltip explicativo en cada parámetro
- Modo oscuro / claro automático
- Responsive (funciona en tablet del estudiante)
- Sin dependencias externas (standalone HTML)

**Temas más frecuentes** (simuladores típicos QF):
- Diagrama de Gibbs vs temperatura / concentración
- Perfil de energía de reacción (RC diagram)
- Cinética: integración de leyes de velocidad (orden 0, 1, 2)
- Arrhenius: ln(k) vs 1/T interactivo
- Tampones Henderson-Hasselbalch
- Diagramas de fases (P-T)
- Distribución de Maxwell-Boltzmann
- Polarografía y curvas i-E

### 3. Cuestionarios de Evaluación Continua

**Formato Genyo**:
- 10 preguntas por cuestionario
- Dificultad distribuida: 4 básicas, 4 intermedias, 2 avanzadas
- Cada pregunta con 4 opciones, exactamente 1 correcta
- Distractores plausibles basados en errores conceptuales frecuentes
- Explicación de la respuesta correcta (mostrada tras responder)

**Formato HTML interactivo** (cuando se pide quiz standalone):
```
Pregunta → 4 opciones → Selección → Feedback inmediato (✓/✗ + explicación) → Siguiente
```
Score final con desglose por concepto.

### 4. Problemas Tipo Examen

**Estructura**:
1. Enunciado claro con todos los datos necesarios
2. Datos adicionales que el alumno debe reconocer como irrelevantes (cuando aplique)
3. Apartados progresivos (a → b → c)
4. **Solución completa** con:
   - Ecuaciones nombradas antes de usarse
   - Sustitución numérica explícita con unidades
   - Resultado final con unidades y cifras significativas correctas
   - Comentario físico-químico del resultado

### 5. Presentaciones de Clase

Usar skill `pptx` para generar PowerPoint. Estructura por diapositiva:
- **Portada**: título del tema, número, asignatura, fecha
- **Agenda** (1 slide): 3-5 puntos clave del tema
- **Motivación** (1-2 slides): imagen + pregunta provocadora
- **Desarrollo** (8-12 slides): uno por concepto, max 5 líneas de texto por slide
- **Ejemplos** (2-4 slides): resueltos paso a paso
- **Resumen** (1 slide): mapa conceptual o tabla
- **Problemas propuestos** (1 slide): 2-3 para trabajo personal

---

## Pipeline de Calidad

Antes de entregar cualquier material docente:
1. **Verificación científica**: todas las ecuaciones y valores numéricos correctos
2. **Notación**: Unicode, sin LaTeX crudo, con unidades en toda expresión numérica
3. **Voz**: aplicar `humanizer-juanjo-es` (documentos en español)
4. **Accesibilidad**: contraste de colores, fuente ≥ 14pt en presentaciones, alt text en imágenes
5. **Formato de entrega**: PDF para imprimir, HTML para simuladores, PPTX para presentaciones
