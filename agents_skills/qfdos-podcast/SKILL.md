---
name: qfdos-podcast
description: Redactar guiones de podcast docente a dos voces para Química Farmacéutica II (QFDOS, UGR) a partir de apuntes finales y transcripciones de clase, listos para locutar con Gemini TTS o importar en QFDOS Podcast Studio. Usar siempre que se pida un podcast, episodio, guion de audio, diálogo de repaso, simulacro oral de examen o «convertir los apuntes/la clase en audio» sobre contenido de QF2/QFDOS, aunque no se diga «podcast»; también para revisar o acortar un guion existente y para preparar perfiles de voz en JSON.
---

# Guiones de podcast QFDOS

Convierte apuntes finales y transcripciones de clase de Química Farmacéutica II en un diálogo natural entre dos voces, pensado para leerse en voz alta por un motor de voz.

## Jerarquía de fuentes

1. **Apuntes finales**: fuente de verdad. Ningún dato, estructura, mecanismo, síntesis o cifra puede contradecirlos.
2. **Transcripción de clase**: aporta tono, ejemplos y avisos del profesor («esto cae», «ojo con…»). Si contradice los apuntes, prevalecen los apuntes.
3. **Complementario**: contexto; nunca introduce datos que no estén en 1 o 2.

No inventar fármacos, reacciones ni datos. Si falta información, no se rellena: se omite el punto.

## Formatos de episodio

| Formato | Dinámica |
| :--- | :--- |
| Repaso activo (por defecto) | Dos estudiantes se lanzan preguntas; una responde, la otra corrige o matiza con el grupo funcional, el mecanismo o la SAR. Nada de lectura pasiva. |
| Simulacro de test | Enunciados con opciones trampa verosímiles, razonados en voz alta; se justifica por qué cada distractor es falso. Cierre con las trampas más probables. |
| Divulgativo | Un anfitrión guía, el otro aporta el detalle técnico; de lo general a lo particular, con analogías precisas. |

Duración: unas 150 palabras por minuto. Abre la voz A; cierre con tres o cuatro ideas clave dichas por ambos, sin despedida larga.

Anfitriones por defecto: **Lucía** (A, guía la sesión y explica con precisión) y **Álvaro** (B, pregunta, duda y cae en las trampas típicas para corregirlas). Respetar otros nombres si se indican.

## Reglas de oralidad

El texto irá a un motor de voz:

- Sin tablas, viñetas, markdown, emojis, URLs ni acotaciones entre corchetes.
- Química escrita como se pronuncia: «pe ka de cuatro coma dos», «beta dos», «grupo O-H», «carbono alfa», «ene metilo». Sin LaTeX ni subíndices.
- Frases cortas; turnos variados (de una línea a cuatro o cinco frases); interrupciones y confirmaciones breves («Exacto», «Espera, ¿y eso por qué?»).
- Cada turno, un único hablante. Sin muletillas de IA ni frases hechas vacías.
- Siglas que deben deletrearse, con guiones: C-O-M-T, M-A-O, S-A-R, S-N-C, A-D-N, A-R-N.

## Formato de salida

Siempre este formato, compatible con la importación de QFDOS Podcast Studio (paso 2 → Importar guion):

```
# Título nominal del episodio

Lucía: Primera intervención.

Álvaro: Respuesta.
```

Entregar como archivo `.md` cuando el guion supere unas pocas líneas. Indicar al final el recuento aproximado de palabras y minutos.

## Revisión de un guion existente

Mantener hablantes, formato y reglas de oralidad; aplicar solo la instrucción pedida (acortar, más trampas, más SAR, más ritmo) y devolver el guion completo.

## Voces

Para preparar o editar perfiles de voz, usar el esquema de `references/voces.json` (compatible con la app): `name`, `alias`, `timbreDescription`, `geminiBaseVoice` (una de las 30 voces precompiladas de Gemini) y `geminiStylePrompt` (acento, ritmo y carácter en una frase). Evitar que ambos anfitriones compartan voz base.
