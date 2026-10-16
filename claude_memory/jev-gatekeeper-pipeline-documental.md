---
name: jev-gatekeeper-pipeline-documental
description: El Noul de Jev necesita instrucciones enumeradas al detalle; con instrucciones vagas devuelve 0.63 sobre slop evidente y no discrimina
metadata: 
  node_type: memory
  type: project
  originSessionId: d2c2721d-e51d-4088-adc4-3f2b2d193ed5
  modified: 2026-09-21T14:02:55.696Z
---

Las primitivas `Noul` de Jev (TypeSafe AI) son muy sensibles a cómo se redacta
`instructions`. Medido el 2026-09-21 sobre el mismo texto de slop evidente:

- Instrucción vaga ("¿Contiene muletillas típicas de IA?") → `noul = 0.63`. Inservible:
  no separa un texto sucio de uno limpio.
- Instrucción enumerando muletillas concretas, construcciones y patrones, y cerrando con
  "responde verdadero solo si están presentes de forma marcada" → `0.97` sobre el sucio y
  `0.03` sobre uno limpio.

El fallo es silencioso: una instrucción floja no da error, solo devuelve probabilidades
centradas que hacen que la compuerta apruebe cualquier cosa.

**Why:** es un modelo no autoregresivo de clasificación, no un chat. No infiere el criterio
a partir de una pregunta corta; hay que dárselo explícito.

**How to apply:** al escribir o revisar cualquier `Noul` o `Choice` de Jev, enumerar los
criterios concretos y validar siempre con un par de contraste (un caso claramente positivo
y uno claramente negativo) antes de confiar en la salida. Si la separación entre ambos no
supera ~0.8, la instrucción está mal redactada, no el motor.

Las constantes ya calibradas viven en `jev_doc_gatekeeper.py` (`INSTR_SLOP`, `INSTR_VOZ`,
`INSTR_LATEX`). Acortarlas rompe la compuerta sin avisar.

**Registros de voz (2026-10-16).** La voz única de CEO daba falsos positivos sobre
manuscritos, diapositivas y avisos a alumnos. Desde esta fecha `jev_registros.py` define
siete registros (ceo, alumnos, manuscrito, diapositivas, propuesta, informe, divulgacion),
ampliados a ocho con `recomendacion` (cartas de recomendación) ese mismo día,
cada uno con su Noul de voz en español e inglés. El registro `ceo` conserva carácter a
carácter las instrucciones calibradas. Los otros siete están escritos con la misma regla
(criterios enumerados) pero **no se han medido todavía contra la API**: hay que ejecutar
`calibrar_registros.py` en un equipo con `TYPESAFE_API_KEY` y ajustar el que no separe.

Primera calibración real (2026-10-16): el Noul de voz separa en los 8 registros (ok 0.04–0.18,
mal 0.95–0.98). Falló solo el `Choice` en ceo, manuscrito, diapositivas e informe: las 7
muestras mal enrutadas eran exactamente las 'mal', que no llevaban marcas formales de su tipo,
así que Jev las clasificó por el tono. Corregido con `INSTR_CHOICE` enumerado por marcas
formales, muestras 'mal' con esas marcas, y una calibración que exige acierto del Choice solo
en las 'ok' y bloquea las 'mal' enmascaradas (mal enrutadas y aprobadas).

Segunda calibración (2026-10-16): los 8 registros en OK. p_voz ok 0.05–0.19, mal 0.95–0.98,
separación 0.77 (propuesta) a 0.93 (informe). En la matriz cruzada, los valores bajos fuera de
la diagonal están entre registros técnicos afines: informe y propuesta bajo la voz de
manuscrito (0.25 y 0.29), diapositivas bajo manuscrito (0.45), alumnos bajo ceo (0.34). Un
texto bueno enrutado a uno de esos vecinos también pasa, así que no hay daño; lo que importa
es que ninguna muestra mala quede enmascarada, y ninguna lo queda. `propuesta` es el registro
con menos margen: es el primero que hay que revisar si aparecen falsos negativos.

Relacionado: [[skills-duplicados-claude-y-agents]]
