# Registros de voz de Juanjo

Guía de reescritura por registro. El humanizador del idioma (`humanizer-juanjo-es` o
`humanizer-juanjo`) identifica el registro del texto y aplica la sección correspondiente.

Qué se mantiene en todos los registros: cero slop, cero LaTeX crudo, precisión técnica,
cifras con unidades, terminología de practicante y ningún rasgo inventado.

Qué solo vale para `ceo`: la nota personal de apertura, los apóstrofes caídos del inglés
("Ive", "Im"), las transiciones de carta ("En cuanto a...", "Regarding...") y el
vocabulario de hitos y estrategia. Fuera de `ceo` esos rasgos son un error de registro.

Las cifras de los ejemplos antes/después son ilustrativas. Nunca se trasladan a un texto
real: el humanizador conserva las cifras del original y no añade ninguna.

---

<a id="ceo"></a>
## ceo: emails de CEO y corporativos

Inversores, consejo, socios, clientes farmacéuticos, colaboradores industriales.

Es el perfil completo de `humanizer-juanjo` / `humanizer-juanjo-es` tal como está escrito
en esas skills. No hay ajustes adicionales.

---

<a id="alumnos"></a>
## alumnos: comunicación con alumnos

Avisos de PRADO, emails a estudiantes, convocatorias, instrucciones de prácticas, normas
de evaluación continua, feedback de TFG y TFM.

Rasgos:
- Segunda persona directa: "tenéis", "os pido", "revisa"; en inglés "you need to", "please submit".
- Una instrucción por frase. Frases de longitud media, más cortas que en `ceo`.
- Datos operativos exactos y completos: fecha, hora, aula o enlace, plataforma, peso en
  la nota, criterio de evaluación, a quién escribir si hay un problema.
- Cuando una norma puede parecer arbitraria, una frase con el porqué.
- Firmeza en plazos y criterios, sin dureza ni amenaza.
- En feedback: qué está bien, qué falla y cómo corregirlo, con referencia a la página,
  la figura o el apartado.
- Listas numeradas permitidas solo para pasos o fechas.
- Saludo y despedida breves ("Hola a todos", "Un saludo"), sin fórmulas administrativas.

Evitar: vocabulario de empresa (hitos, estrategia, ventaja competitiva), tono de
resolución administrativa ("se comunica a los interesados"), condescendencia,
exclamaciones o emojis, ánimos genéricos ("¡mucho ánimo!"), feedback vago ("buen
trabajo", "mejorable").

Antes: "Se informa al alumnado de que la prueba parcial tendrá lugar próximamente. Es
crucial prepararse adecuadamente. ¡Mucho ánimo!"

Después: "El parcial de QFDOS (temas 1 a 4) es el martes 14 de enero a las 9:00 en el
aula B2 y cuenta un 30 % de la nota final. Traed el DNI; sin él no podréis entrar. Si
tenéis un solapamiento con otro examen, escribidme antes del 10 de enero."

---

<a id="manuscrito"></a>
## manuscrito: manuscritos científicos

Artículos, revisiones, tesis, abstracts, TFG o TFM, cartas de respuesta a revisores.

Rasgos:
- Cada afirmación apoyada en un dato propio, una cita o un resultado.
- Cifras con unidades y estadística completa: n, media ± DE, IC 95 %, valor p, KD, Tm, LOD.
- Pasado en Métodos y Resultados; presente para el conocimiento establecido y para lo
  que muestran las figuras ("La Figura 2 muestra...").
- "Hemos diseñado", "observamos" o impersonal; en inglés, "we" académico.
- Cautela proporcional a la evidencia: "sugiere", "es compatible con" donde el dato es
  indirecto; afirmación directa donde el dato es directo.
- Párrafo con una idea central y transición lógica ("Sin embargo", "Para descartarlo"),
  no de carta.
- Terminología exacta: nombres de sondas, secuencias, condiciones, instrumentos.

Evitar: adjetivos de comunicado ("revolucionario", "sin precedentes", abuso de "novel"),
cualquier rasgo de `ceo` ("En cuanto a...", "estamos empujando fuerte", hitos
comerciales), sobreafirmar sin dato, cautelas apiladas ("podría potencialmente
sugerir"), coloquialismos, vaguedad en métodos.

Antes: "Our groundbreaking DCL platform revolutionizes miRNA detection, showing
unprecedented sensitivity."

Después: "The DCL assay detected miR-122 at 10 fM in serum without amplification
(LOD = 8.4 fM, n = 3), a 12-fold improvement over the RT-qPCR reference run on the same
samples."

---

<a id="diapositivas"></a>
## diapositivas: textos para diapositivas

Clases, congresos, pitch a inversores, defensa de tesis.

Rasgos:
- Título que afirma la conclusión: "miR-122 sube 40 veces en DILI temprana", no "Resultados".
- Viñetas de menos de 12 palabras, paralelas entre sí (todas empiezan igual: sustantivo o verbo).
- Fragmentos sin verbo permitidos.
- Una idea por diapositiva; la cifra clave visible con su unidad.
- Terminología exacta sin explicación de manual; la explicación va a las notas del ponente.
- Notas del ponente, si las hay: prosa breve en el registro de destino (clase → `alumnos`,
  congreso → `manuscrito`, inversores → `ceo`).

Evitar: párrafos completos en la diapositiva, viñetas de más de 20 palabras, títulos
vacíos ("Introducción", "Conclusiones" sin mensaje), "Como podemos ver", "Es importante
destacar", adjetivos promocionales.

Antes: "Resultados — Es importante destacar que los resultados obtenidos muestran un
incremento significativo de los niveles de miR-122 en los pacientes."

Después:
"miR-122 sube 40 veces en DILI temprana
- 24 pacientes, 18 controles
- Detección 48 h antes que ALT
- p < 0,001 (Mann-Whitney)"

---

<a id="propuesta"></a>
## propuesta: propuestas de financiación

ISCIII, AEI, Horizon Europe, FIBAO, EQC, CDTI.

Rasgos:
- Hipótesis explícita y contrastable en una frase.
- Objetivos medibles con indicador y plazo ("validar el panel en 200 muestras en el mes 18").
- Paquetes de trabajo, hitos y entregables fechados.
- Resultados previos del grupo, con cifras y referencia, como prueba de viabilidad.
- Impacto concreto: pacientes, coste, tiempo de diagnóstico, transferencia, patente.
- Riesgos con plan de contingencia.
- Plural de equipo: "proponemos", "nuestro grupo ha demostrado".
- Vocabulario de la convocatoria (impacto, transferencia, escalabilidad) siempre con dato.

Evitar: superlativos sin respaldo, impacto genérico ("cambiará la medicina"), objetivos
sin indicador, ausencia de fechas, tono de email o de artículo que no orienta al evaluador.

---

<a id="informe"></a>
## informe: informes técnicos y de calidad

Validaciones, ISO 9001 e ISO 13485, CAPA, no conformidades, SOP o PNT, actas, IVDR.

Rasgos:
- Factual, impersonal o plural institucional.
- Trazable: código de documento, versión, lote, fecha, responsable, cláusula de la norma.
- Apartados numerados.
- Resultado frente a criterio de aceptación predefinido: "CV = 4,2 %, criterio ≤ 10 %: conforme".
- Acciones con responsable y fecha límite.

Evitar: valoraciones sin dato ("excelente resultado"), narrativa de carta, tono
comercial, cifras o lotes imprecisos, conclusiones sin criterio de aceptación.

---

<a id="divulgacion"></a>
## divulgacion: divulgación y web

LinkedIn, notas de prensa, web de Destina o del grupo, guiones de podcast, artículos
divulgativos.

Rasgos:
- El problema real antes que la tecnología: el paciente, el diagnóstico tardío, el coste.
- Cada concepto técnico con una imagen concreta o una cifra comprensible.
- Frases medias y activas; rigor intacto.
- Entusiasmo contenido, apoyado en hechos.

Evitar: hype ("revolucionario", "el futuro ya está aquí"), clichés de LinkedIn
("orgulloso de anunciar", "thrilled to share"), emojis o exclamaciones en serie, jerga
sin explicar, promesas clínicas que los datos no respaldan.

---

<a id="recomendacion"></a>
## recomendacion: cartas de recomendación

Cartas para máster, doctorado, becas (FPU, FPI, Marie Skłodowska-Curie), contratos, plazas,
promociones y premios, sobre alumnos, doctorandos, postdocs o colegas.

Rasgos:
- Primera persona del singular: es Juanjo quien avala, no el equipo. "He dirigido",
  "he supervisado"; en inglés "I supervised", "I have worked with".
- Primer párrafo: relación con el candidato, en qué calidad, desde cuándo y durante cuánto
  tiempo, y para qué plaza o programa escribe.
- Cada cualidad con un hecho observado: el proyecto, la técnica que dominó, el problema que
  resolvió sin ayuda, el resultado, la publicación, la nota.
- Comparación calibrada con un grupo de referencia: "entre los tres mejores alumnos de
  máster que he dirigido en quince años", "top 5 % for experimental design".
- Idoneidad para el puesto concreto: qué capacidad del candidato encaja con qué exigencia
  del programa.
- Elogio firme y creíble; capacidad, no solo esfuerzo.
- Cierre: recomendación explícita ("la recomiendo sin reservas") y disponibilidad para
  ampliar información. Las fórmulas del género se usan una vez.
- Las cifras, notas, fechas y logros salen del CV o de los datos que dé Juanjo. Si faltan,
  se dejan marcados como [pendiente] y se piden; nunca se inventan.

Evitar: listas de adjetivos sin hechos ("brillante, apasionada, dedicada"), cartas que
servirían para cualquier candidato, superlativos absolutos sin referencia ("la mejor alumna
de la historia"), reservas que siembran duda ("aunque a veces le cuesta"), elogiar solo el
esfuerzo ("muy trabajadora") cuando hay capacidad que destacar, adjetivos distintos según
el género del candidato, tono de email de CEO o de informe.

Antes: "Es un auténtico placer recomendar a Ana, una alumna brillante, apasionada y
dedicada. Aunque a veces le cuesta organizarse, será una gran incorporación."

Después: "Conozco a Ana Martínez desde 2022, cuando realizó en mi grupo el TFM del Máster
TRANSMED, que dirigí. En doce meses diseñó seis sondas PNA y puso a punto por su cuenta el
ensayo de desplazamiento de banda que hoy usa todo el laboratorio. Entre los alumnos de
máster que he dirigido en quince años, la sitúo entre los tres mejores, y la recomiendo sin
reservas para el programa de doctorado en química biológica."
