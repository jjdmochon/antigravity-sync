#!/usr/bin/env python3
r"""
jev_registros.py - Registros de voz para el gatekeeper Jev.

Una sola voz "CEO ejecutivo" suspendia manuscritos (penaliza el hedging y la prosa
academica), diapositivas (penaliza fragmentos y vinetas) y avisos a alumnos (penaliza la
segunda persona y las frases cortas). Cada registro lleva aqui su propia instruccion Noul
de voz, en espanol y en ingles, y una clausula de tolerancia para la instruccion de slop.

Reglas de redaccion (ver memoria jev-gatekeeper-pipeline-documental):
  - Cada instruccion enumera rasgos concretos. Una pregunta vaga deja el Noul en ~0.6 y
    la compuerta deja de discriminar sin dar error.
  - Semantica del Noul de voz: VERDADERO = el texto se DESVIA del registro.
  - Toda instruccion nueva o editada se valida con calibrar_registros.py antes de usarla.

Orden de resolucion del registro (jev_doc_gatekeeper.resolver_registro):
  1. --registro / parametro registro de la herramienta MCP
  2. marcador en el propio fichero:  <!-- registro: alumnos -->  o  'registro: alumnos'
     en el frontmatter YAML (primeras 40 lineas)
  3. fichero .jev-registro en la carpeta del documento o en una superior (una palabra)
  4. Choice de Jev sobre el texto (misma llamada que el resto de preguntas)
  5. heuristica local (extension, vocabulario, densidad de vinetas)
  6. 'ceo' por defecto, que reproduce el comportamiento anterior
"""

import re

POR_DEFECTO = "ceo"

# --------------------------------------------------------------------------
# Definicion de registros
# --------------------------------------------------------------------------

REGISTROS = {
    "ceo": {
        "nombre": "Emails de CEO y corporativos",
        "choice": (
            "Correspondencia de direccion de una empresa biotecnologica: emails o cartas a "
            "inversores, consejo, socios, clientes farmaceuticos o colaboradores industriales; "
            "actualizaciones de estado de proyectos, hitos comerciales, patentes, financiacion. "
            "Marcas formales: destinatario concreto (saludo 'Hola Paul', 'Dear board', 'Hope "
            "you are well'), firma, referencias a reuniones, inversores, consejo, ronda o hitos "
            "de la empresa."
        ),
        # Texto identico al INSTR_VOZ_ES / INSTR_VOZ_EN calibrados antes de los registros.
        "voz_es": (
            "El texto se DESVIA de la voz ejecutiva de Juanjo. Esa voz es: compuesta y "
            "tecnicamente precisa, con cifras y unidades concretas, plural natural en espanol "
            "('hemos cerrado', 'proponemos'), encabezados topicos ('En cuanto a...', "
            "'Respecto a...'), afirmaciones verificables y orientadas a la accion, calida pero "
            "controlada. Responde verdadero si el texto suena promocional, grandilocuente, "
            "impersonal, academicamente farragoso, o carece de concrecion tecnica; responde "
            "falso si ya cumple esa voz."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's executive voice. That voice is: composed, "
            "quietly confident and technically specific, as written by a scientist-CEO; "
            "medium-to-long deliberate sentences rather than punchy fragments; 'we' as the "
            "default subject for team and company work and 'I' for personal ownership; explicit "
            "topic-led transitions ('Regarding...', 'On the ... front...', 'For the ...'); "
            "practitioner technical terms woven into prose (assays, platforms, patents, ISO 13485, "
            "IVDR) with concrete names, dates and figures; plain assertive statements ('the data "
            "clearly shows', 'I am confident'); action-oriented closings; warm but restrained. "
            "Slide fragments, short labels and table cells are acceptable in a presentation. "
            "Answer true if the text sounds promotional, grandiloquent, impersonal, generic, "
            "motivational, hedging, academically convoluted, or lacks technical concreteness; "
            "answer false if it already matches that voice."
        ),
        # Vacia a proposito: con registro 'ceo' la instruccion de slop queda identica a la
        # calibrada antes de los registros (0.97 frente a 0.03).
        "tolerancia_slop": "",
    },

    "alumnos": {
        "nombre": "Comunicación con alumnos",
        "choice": (
            "Mensajes de un profesor universitario a sus estudiantes: avisos del campus virtual "
            "(PRADO), emails a alumnos, convocatorias de examen o tutoria, instrucciones de "
            "practicas, normas de evaluacion continua, feedback a un TFG o TFM. Se dirige al "
            "lector en segunda persona (tu, vosotros, you). Marcas formales: asignatura, "
            "examen, fecha de entrega, aula, PRADO, nota, alumno o alumna nombrado."
        ),
        "voz_es": (
            "El texto se DESVIA de la voz de Juanjo como profesor que escribe a sus alumnos. Esa "
            "voz es: cercana pero con autoridad docente; segunda persona directa ('tenéis', "
            "'os pido', 'revisa'); frases claras de longitud media, una instruccion por frase; "
            "datos operativos exactos (fecha, hora, aula, plataforma, porcentaje de la nota, "
            "criterio de evaluacion); explica el porque de una norma en una frase cuando hace "
            "falta; firme con plazos y criterios, sin dureza; feedback especifico que senala que "
            "esta bien, que falla y como corregirlo; listas numeradas solo para pasos o fechas. "
            "Responde verdadero si el texto suena corporativo o de CEO (hitos, inversores, "
            "estrategia), burocratico o administrativo frio, condescendiente o infantil, "
            "excesivamente entusiasta (exclamaciones, emojis, animos genericos), ambiguo en "
            "plazos o criterios, o si da feedback vago ('buen trabajo', 'mejorable'); responde "
            "falso si ya cumple esa voz."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's voice as a university lecturer writing to "
            "his students. That voice is: approachable but with clear teaching authority; direct "
            "second person ('you need to', 'please submit', 'check'); clear medium-length "
            "sentences, one instruction per sentence; exact operational details (date, time, "
            "room, platform, weight in the final grade, assessment criterion); one sentence of "
            "rationale for a rule when needed; firm on deadlines and criteria without harshness; "
            "specific feedback that names what works, what fails and how to fix it; numbered "
            "lists only for steps or dates. Answer true if the text sounds corporate or CEO-like "
            "(milestones, investors, strategy), cold bureaucratic, condescending or childish, "
            "over-enthusiastic (exclamation marks, emojis, generic encouragement), vague about "
            "deadlines or criteria, or gives vague feedback ('good job', 'could be improved'); "
            "answer false if it already matches that voice."
        ),
        "tolerancia_slop": (
            "Listas numeradas de pasos, fechas o criterios de evaluacion son formato legitimo "
            "en un aviso a alumnos y no cuentan como cadencia artificial."
        ),
    },

    "manuscrito": {
        "nombre": "Manuscritos científicos",
        "choice": (
            "Texto cientifico academico: articulo de investigacion, revision, tesis doctoral, "
            "TFG o TFM redactado por el autor, abstract, carta de respuesta a revisores. "
            "Secciones tipo Introduccion, Metodos, Resultados, Discusion; citas bibliograficas, "
            "estadistica, condiciones experimentales. Marcas formales: encabezado de seccion de "
            "articulo, referencias a figuras o tablas (Fig. 2, Tabla 1), citas [12] o (Autor, "
            "ano), n, p, desviacion estandar. Un texto con estas marcas es 'manuscrito' aunque "
            "su tono sea promocional o de email."
        ),
        "voz_es": (
            "El texto se DESVIA del registro de manuscrito cientifico de Juanjo. Ese registro es: "
            "preciso y sobrio; cada afirmacion apoyada en un dato, una cita o un resultado "
            "propio; cifras con unidades y estadistica (n, media ± DE, IC 95 %, valor p, KD, Tm, "
            "LOD); tiempos verbales convencionales (pasado en metodos y resultados, presente para "
            "conocimiento establecido); primera persona del plural academica ('hemos disenado', "
            "'observamos') o impersonal; cautela proporcional a la evidencia ('sugiere', 'es "
            "compatible con') solo donde el dato es indirecto; terminologia exacta de quimica, "
            "biologia molecular y diagnostico; parrafos con una idea central y transiciones "
            "logicas, no de carta. Responde verdadero si el texto suena promocional o de "
            "comunicado ('revolucionario', 'sin precedentes', 'cambia las reglas'), si usa tono de "
            "CEO o de email ('En cuanto a...', 'estamos empujando fuerte', hitos comerciales), si "
            "sobreafirma sin dato, si es coloquial, si es vago en metodos o cifras, o si encadena "
            "cautelas vacias ('podria potencialmente sugerir'); responde falso si ya cumple ese "
            "registro."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's scientific manuscript register. That "
            "register is: precise and sober; every claim backed by data, a citation or an own "
            "result; figures with units and statistics (n, mean ± SD, 95 % CI, p value, KD, Tm, "
            "LOD); conventional tenses (past for methods and results, present for established "
            "knowledge); academic 'we' ('we designed', 'we observed') or impersonal voice; "
            "hedging proportional to the evidence ('suggests', 'is consistent with') only where "
            "the data is indirect; exact chemistry, molecular biology and diagnostics terminology; "
            "paragraphs built around one central point with logical, not letter-style, "
            "transitions. Answer true if the text sounds promotional or press-release-like "
            "('groundbreaking', 'unprecedented', 'game-changing', overuse of 'novel'), uses a CEO "
            "or email tone ('Regarding...', 'we are pushing hard', commercial milestones), "
            "overclaims without data, is colloquial, is vague about methods or numbers, or stacks "
            "empty hedges ('could potentially suggest'); answer false if it already matches that "
            "register."
        ),
        "tolerancia_slop": (
            "Terminos tecnicos estandar no son muletillas: 'robust' o 'robusto' en sentido "
            "estadistico, 'mutational landscape', 'pivotal trial', 'key residue'. La cautela "
            "proporcional al dato ('suggests', 'sugiere') tampoco cuenta como relleno."
        ),
    },

    "diapositivas": {
        "nombre": "Textos para diapositivas",
        "choice": (
            "Texto de una presentacion: titulos de diapositiva, vinetas cortas, etiquetas, "
            "llamadas a figuras, notas breves del ponente. Clases, congresos, pitch a inversores. "
            "Lineas cortas, fragmentos sin verbo, muchas vinetas. Marcas formales: un titulo "
            "corto en la primera linea seguido de vinetas, numero o titulo de diapositiva, "
            "'Diapositiva 4', notas del ponente. Una linea de titulo seguida de vinetas es "
            "'diapositivas' aunque las vinetas sean largas o esten en prosa."
        ),
        "voz_es": (
            "El texto se DESVIA del registro de diapositiva de Juanjo. Ese registro es: titulos "
            "que afirman la conclusion de la diapositiva ('miR-122 sube 40 veces en DILI "
            "temprana') en lugar de etiquetas genericas; vinetas cortas, idealmente de menos de "
            "12 palabras, gramaticalmente paralelas; fragmentos sin verbo aceptables; una idea "
            "por diapositiva; la cifra clave visible con su unidad; terminologia exacta sin "
            "explicaciones de manual. Responde verdadero si hay parrafos de prosa completa, "
            "vinetas de mas de 20 palabras, titulos vacios ('Introduccion', 'Resultados', "
            "'Conclusiones' sin mensaje), frases de relleno ('Como podemos ver', 'Es importante "
            "destacar'), adjetivos promocionales o tono de email; responde falso si ya cumple "
            "ese registro."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's slide register. That register is: titles "
            "that state the slide's conclusion ('miR-122 rises 40-fold in early DILI') rather "
            "than generic labels; short bullets, ideally under 12 words, grammatically parallel; "
            "verbless fragments are acceptable; one idea per slide; the key figure visible with "
            "its unit; exact terminology without textbook explanations. Answer true if there are "
            "full prose paragraphs, bullets longer than 20 words, empty titles ('Introduction', "
            "'Results', 'Conclusions' with no message), filler phrases ('As we can see', 'It is "
            "important to note'), promotional adjectives or an email tone; answer false if it "
            "already matches that register."
        ),
        "tolerancia_slop": (
            "En diapositivas las vinetas paralelas, los fragmentos sin verbo y las enumeraciones "
            "de tres elementos son formato legitimo: solo cuenta el slop lexico y el relleno."
        ),
    },

    "propuesta": {
        "nombre": "Propuestas de financiación",
        "choice": (
            "Solicitud de financiacion o memoria cientifico-tecnica: ISCIII, AEI, Horizon "
            "Europe, FIBAO, EQC, CDTI. Objetivos, hipotesis, plan de trabajo, cronograma, "
            "paquetes de trabajo, entregables, impacto, presupuesto, capacidad del equipo."
        ),
        "voz_es": (
            "El texto se DESVIA del registro de propuesta de financiacion de Juanjo. Ese registro "
            "es: hipotesis explicita y contrastable; objetivos medibles con indicador y plazo; "
            "plan de trabajo con paquetes, hitos y entregables fechados; resultados previos del "
            "grupo citados con cifras como prueba de viabilidad; impacto concreto (pacientes, "
            "coste, tiempo de diagnostico, transferencia, patente) en vez de generico; riesgos "
            "con plan de contingencia; persuasivo pero verificable, en plural de equipo "
            "('proponemos', 'nuestro grupo ha demostrado'). Responde verdadero si el texto usa "
            "superlativos sin respaldo, impacto vago ('cambiara la medicina', 'gran impacto "
            "social'), objetivos no medibles, ausencia de cifras o fechas, tono de email o de "
            "articulo sin orientacion al evaluador; responde falso si ya cumple ese registro."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's grant proposal register. That register is: "
            "an explicit, testable hypothesis; measurable objectives with indicator and timeline; "
            "a work plan with work packages, milestones and dated deliverables; the group's prior "
            "results quoted with figures as proof of feasibility; concrete impact (patients, "
            "cost, time to diagnosis, technology transfer, patents) rather than generic claims; "
            "risks with contingency plans; persuasive but verifiable, in team plural ('we "
            "propose', 'our group has shown'). Answer true if the text relies on unsupported "
            "superlatives, vague impact ('will transform medicine', 'huge societal impact'), "
            "non-measurable objectives, missing figures or dates, or an email or paper tone with "
            "no orientation to the evaluator; answer false if it already matches that register."
        ),
        "tolerancia_slop": (
            "'Impacto', 'transferencia', 'escalabilidad' e 'innovacion' son terminos de las "
            "bases de la convocatoria; solo cuentan como relleno si no llevan dato concreto."
        ),
    },

    "informe": {
        "nombre": "Informes técnicos y de calidad",
        "choice": (
            "Documento tecnico o de calidad: informe de validacion, informe ISO 9001 o "
            "ISO 13485, CAPA, no conformidad, SOP, acta de reunion, informe de resultados de "
            "laboratorio, documentacion regulatoria IVDR. Marcas formales: codigo de documento "
            "(VAL-012, CAPA-018, NC-031), lote, version, apartados numerados ('4. Resultados'), "
            "criterio de aceptacion, clausula de una norma. Un texto con estas marcas es "
            "'informe' aunque su tono sea de email o comercial."
        ),
        "voz_es": (
            "El texto se DESVIA del registro de informe tecnico y de calidad de Juanjo. Ese "
            "registro es: factual, impersonal o en plural institucional; trazable (codigo de "
            "documento, lote, version, fecha, responsable, referencia a la clausula de la "
            "norma); apartados numerados; resultados frente a criterio de aceptacion predefinido "
            "('CV = 4,2 %, criterio ≤ 10 %: conforme'); sin adjetivos valorativos; acciones con "
            "responsable y plazo. Responde verdadero si el texto opina o valora sin dato, usa "
            "narrativa de carta o de CEO, tono comercial, imprecision en cifras o lotes, o "
            "conclusiones sin criterio de aceptacion; responde falso si ya cumple ese registro."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's technical and quality report register. "
            "That register is: factual, impersonal or institutional plural; traceable (document "
            "code, lot, version, date, owner, reference to the standard clause); numbered "
            "sections; results against a predefined acceptance criterion ('CV = 4.2 %, "
            "criterion ≤ 10 %: pass'); no evaluative adjectives; actions with owner and due "
            "date. Answer true if the text gives opinions without data, uses a letter or CEO "
            "narrative, a commercial tone, imprecise figures or lots, or conclusions without an "
            "acceptance criterion; answer false if it already matches that register."
        ),
        "tolerancia_slop": (
            "Estructura repetitiva por apartados numerados y formulas normativas ('conforme', "
            "'no conforme', 'segun la clausula 7.5') son formato legitimo de informe."
        ),
    },

    "divulgacion": {
        "nombre": "Divulgación y web",
        "choice": (
            "Texto para publico general o no especialista: post de LinkedIn, nota de prensa, "
            "texto de pagina web, guion de podcast, articulo divulgativo, presentacion de "
            "empresa o de grupo de investigacion para la sociedad. Marcas formales: sin "
            "destinatario concreto, hashtags, menciones, titular de prensa, lenguaje para no "
            "especialistas. Un email con saludo a una persona concreta no es divulgacion."
        ),
        "voz_es": (
            "El texto se DESVIA del registro divulgativo de Juanjo. Ese registro es: claro para "
            "un no especialista sin perder rigor; un concepto tecnico explicado con una imagen "
            "concreta o una cifra comprensible; frases medias, activas; el problema real antes "
            "que la tecnologia (el paciente, el diagnostico tardio, el coste); entusiasmo "
            "contenido, apoyado en hechos; sin jerga sin explicar. Responde verdadero si el "
            "texto usa hype ('revolucionario', 'el futuro ya esta aqui'), cliches de LinkedIn "
            "('orgulloso de anunciar', 'emocionado de compartir'), emojis o exclamaciones en "
            "serie, jerga no explicada, tono de manuscrito o de informe, o promesas clinicas no "
            "respaldadas; responde falso si ya cumple ese registro."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's outreach register. That register is: clear "
            "to a non-specialist without losing rigour; each technical concept explained through "
            "a concrete image or an understandable figure; medium, active sentences; the real "
            "problem before the technology (the patient, the late diagnosis, the cost); "
            "restrained enthusiasm grounded in facts; no unexplained jargon. Answer true if the "
            "text uses hype ('revolutionary', 'the future is here'), LinkedIn cliches ('thrilled "
            "to announce', 'excited to share'), strings of emojis or exclamation marks, "
            "unexplained jargon, a manuscript or report tone, or unsupported clinical promises; "
            "answer false if it already matches that register."
        ),
        "tolerancia_slop": (
            "Una analogia o imagen concreta para explicar un concepto es recurso legitimo de "
            "divulgacion, no relleno."
        ),
    },

    "recomendacion": {
        "nombre": "Cartas de recomendación",
        "choice": (
            "Carta de recomendacion o de referencia firmada por Juanjo sobre una persona "
            "concreta: alumno, doctorando, postdoc o colega que solicita un master, doctorado, "
            "beca, contrato, plaza, promocion o premio. Habla de la relacion con el candidato, "
            "sus logros y su idoneidad para el puesto."
        ),
        "voz_es": (
            "El texto se DESVIA del registro de carta de recomendacion de Juanjo. Ese registro "
            "es: primera persona del singular ('le dirijo el TFM', 'he supervisado'); relacion "
            "con el candidato explicita al principio (en que calidad, desde cuando, durante "
            "cuanto tiempo); cada cualidad respaldada por un hecho observado y concreto "
            "(proyecto, tecnica dominada, resultado, publicacion, problema que resolvio sola o "
            "solo); comparacion calibrada con un grupo de referencia ('entre los tres mejores "
            "alumnos que he dirigido en quince anos'); idoneidad para el puesto o programa "
            "concreto al que aspira; elogio firme pero creible; cierre con una recomendacion "
            "clara y disponibilidad para ampliar informacion. Responde verdadero si el texto "
            "acumula adjetivos sin hechos ('brillante, apasionada, dedicada'), es generico y "
            "serviria para cualquier candidato, no dice como ni desde cuando se conoce al "
            "candidato, usa superlativos absolutos sin referencia ('el mejor alumno de la "
            "historia'), introduce reservas que siembran duda ('aunque a veces', 'pese a') sin "
            "necesidad, valora solo el esfuerzo y no la capacidad, o suena a email de CEO, a "
            "informe o a nota de prensa; responde falso si ya cumple ese registro."
        ),
        "voz_en": (
            "The English text DEVIATES from Juanjo's recommendation letter register. That "
            "register is: first person singular ('I supervised her MSc thesis', 'I have "
            "worked with him'); the relationship stated up front (in what capacity, since when, "
            "for how long); every quality backed by a concrete observed fact (a project, a "
            "technique mastered, a result, a publication, a problem solved independently); a "
            "calibrated comparison with a reference group ('among the top three students I have "
            "supervised in fifteen years'); fit for the specific position or programme applied "
            "to; firm but credible praise; a clear recommendation in the closing and an offer "
            "to provide further information. Answer true if the text stacks adjectives without "
            "facts ('brilliant, passionate, dedicated'), is generic enough to fit any "
            "candidate, does not say how or since when the candidate is known, uses absolute "
            "superlatives with no reference group ('the best student ever'), adds unnecessary "
            "doubt raisers ('although at times', 'despite'), praises only effort and not "
            "ability, or sounds like a CEO email, a report or a press release; answer false if "
            "it already matches that register."
        ),
        "tolerancia_slop": (
            "Las formulas convencionales del genero ('es un placer recomendar', 'I recommend "
            "her without reservation', 'top 5 %') no cuentan como slop si aparecen una vez y "
            "van acompanadas de hechos concretos."
        ),
    },
}

# Tolerancia usada cuando el registro aun no se conoce (deteccion automatica en la misma
# llamada): union prudente de las tolerancias de formato.
TOLERANCIA_GENERICA = (
    "Segun el tipo de texto, no cuentan como slop: vinetas y fragmentos sin verbo en "
    "diapositivas, listas numeradas de pasos o fechas en avisos e informes, terminos "
    "tecnicos estandar ('robust' estadistico, 'mutational landscape', 'pivotal trial') y la "
    "cautela proporcional al dato en textos cientificos."
)

INSTR_CHOICE = (
    "Clasifica el TIPO de texto por su destinatario y sus marcas formales, NO por su tono, su "
    "calidad ni su tema. Un texto mal escrito, promocional o con el tono de otro tipo sigue "
    "perteneciendo a su tipo: un manuscrito redactado como un email sigue siendo 'manuscrito'. "
    "Criterios, en este orden: "
    "1) codigo de documento, lote, apartados numerados, criterio de aceptacion o clausula de "
    "norma -> 'informe'; "
    "2) linea de titulo corta seguida de vinetas, o numero de diapositiva -> 'diapositivas'; "
    "3) secciones de articulo, figuras o tablas citadas, referencias bibliograficas o "
    "estadistica -> 'manuscrito'; "
    "4) hipotesis, objetivos, paquetes de trabajo, entregables o convocatoria -> 'propuesta'; "
    "5) carta que avala a una persona concreta para una plaza, beca o programa -> "
    "'recomendacion'; "
    "6) mensaje en segunda persona a estudiantes sobre asignatura, examen, practica o "
    "TFG/TFM -> 'alumnos'; "
    "7) email o carta con destinatario concreto del mundo empresarial (inversor, consejo, "
    "socio, cliente) -> 'ceo'; "
    "8) texto sin destinatario concreto para publico general, redes o prensa -> "
    "'divulgacion'. "
    "El tema no decide: un email a inversores sobre miR-122 es 'ceo' y un articulo sobre "
    "miR-122 es 'manuscrito'."
)

# --------------------------------------------------------------------------
# Alias y resolucion local
# --------------------------------------------------------------------------

ALIAS = {
    "ceo": "ceo", "corporativo": "ceo", "corporate": "ceo", "email": "ceo",
    "ejecutivo": "ceo", "executive": "ceo", "inversores": "ceo", "investors": "ceo",
    "alumnos": "alumnos", "estudiantes": "alumnos", "students": "alumnos",
    "docencia": "alumnos", "teaching": "alumnos", "prado": "alumnos",
    "manuscrito": "manuscrito", "manuscript": "manuscrito", "paper": "manuscrito",
    "articulo": "manuscrito", "artículo": "manuscrito", "tesis": "manuscrito",
    "thesis": "manuscrito", "cientifico": "manuscrito", "scientific": "manuscrito",
    "diapositivas": "diapositivas", "slides": "diapositivas", "slide": "diapositivas",
    "presentacion": "diapositivas", "presentación": "diapositivas", "deck": "diapositivas",
    "propuesta": "propuesta", "grant": "propuesta", "proposal": "propuesta",
    "convocatoria": "propuesta", "solicitud": "propuesta",
    "informe": "informe", "report": "informe", "calidad": "informe", "quality": "informe",
    "iso": "informe", "sop": "informe", "tecnico": "informe", "técnico": "informe",
    "divulgacion": "divulgacion", "divulgación": "divulgacion", "outreach": "divulgacion",
    "web": "divulgacion", "linkedin": "divulgacion", "prensa": "divulgacion",
    "press": "divulgacion",
    "recomendacion": "recomendacion", "recomendación": "recomendacion",
    "recommendation": "recomendacion", "referencia": "recomendacion",
    "reference": "recomendacion", "carta": "recomendacion", "aval": "recomendacion",
}


def normalizar(valor):
    """Alias -> clave canonica. Devuelve None si no es un registro reconocido."""
    if not valor:
        return None
    return ALIAS.get(str(valor).strip().lower())


RX_MARCADOR = re.compile(
    r"^\s*(?:<!--\s*|#\s*|%\s*)?(?:jev[-_ ])?(?:registro|register)\s*[:=]\s*([\w\-áéíóú]+)",
    re.I | re.M)


def registro_marcado(texto):
    """Marcador explicito en las primeras 40 lineas del documento."""
    cabeza = "\n".join(texto.splitlines()[:40])
    m = RX_MARCADOR.search(cabeza)
    return normalizar(m.group(1)) if m else None


def registro_carpeta(ruta, niveles=8):
    """Fichero .jev-registro en la carpeta del documento o en una superior."""
    if ruta is None:
        return None, None
    d = ruta.resolve().parent
    for _ in range(niveles):
        f = d / ".jev-registro"
        if f.is_file():
            try:
                valor = f.read_text(encoding="utf-8", errors="replace").split()[0]
            except (OSError, IndexError):
                return None, None
            return normalizar(valor), str(f)
        if d.parent == d:
            break
        d = d.parent
    return None, None


PISTAS = {
    "alumnos": [r"\balumn[oa]s?\b", r"\bestudiantes\b", r"\bprado\b", r"\btutor[ií]a\b",
                r"\bconvocatoria (?:ordinaria|extraordinaria)\b", r"\bevaluaci[oó]n continua\b",
                r"\bteneis\b|\btenéis\b", r"\bos (?:recuerdo|pido|informo)\b", r"\bstudents\b",
                r"\bsubmit your\b", r"\bTF[GM]\b"],
    "manuscrito": [r"\bet al\.", r"\bp\s*[<=>]\s*0[.,]\d", r"\b(?:Abstract|Resumen|Methods|"
                   r"M[eé]todos|Results|Resultados|Discussion|Discusi[oó]n)\b", r"\[\d+(?:[,–-]\d+)*\]",
                   r"\bn\s*=\s*\d+", r"\bIC\s*95|\b95\s*% CI\b", r"\bdoi\b"],
    "propuesta": [r"\bpaquete de trabajo\b|\bwork package\b|\bWP\d\b", r"\bentregable|\bdeliverable",
                  r"\bhip[oó]tesis\b|\bhypothesis\b", r"\bISCIII\b|\bAEI\b|\bHorizon\b|\bFIBAO\b|\bCDTI\b",
                  r"\bcronograma\b|\bGantt\b", r"\bpresupuesto\b|\bbudget\b"],
    "informe": [r"\bISO\s*(?:9001|13485)\b", r"\bCAPA\b", r"\bno conformidad\b|\bnonconformit",
                r"\bSOP\b|\bPNT\b", r"\bcriterio de aceptaci[oó]n\b|\bacceptance criteri",
                r"\blote\b|\blot\b", r"\bcl[aá]usula\b|\bclause\b"],
    "divulgacion": [r"#\w+", r"\bLinkedIn\b", r"\bnota de prensa\b|\bpress release\b",
                    r"\bpodcast\b", r"\borgullos[oa] de\b|\bthrilled\b|\bexcited to\b"],
    "recomendacion": [r"\brecomiendo\b|\brecommend (?:him|her|them)\b",
                      r"\bcarta de (?:recomendaci[oó]n|referencia)\b|\bletter of (?:recommendation|reference)\b",
                      r"\bTo whom it may concern\b|\bA quien corresponda\b",
                      r"\bwithout reservation\b|\bsin reservas\b",
                      r"\bcandidat[oa]\b|\bcandidate\b", r"\bI have known\b|\bconozco a\b"],
    "ceo": [r"\binversor|\binvestor", r"\bhito|\bmilestone", r"\bEn cuanto a\b|\bRegarding\b",
            r"\bHope you are well\b|\bEspero que est[eé]s bien\b", r"\bboard\b|\bconsejo\b",
            r"\bDestina\b", r"\bRUO\b|\bIVD\b"],
}


def densidad_vinetas(texto):
    lineas = [l for l in texto.splitlines() if l.strip()]
    if not lineas:
        return 0.0, 0.0
    vinetas = sum(1 for l in lineas if re.match(r"^\s*(?:[-*•▪◦–]|\d+[.)])\s+", l))
    cortas = sum(1 for l in lineas if len(l.split()) <= 12)
    return vinetas / len(lineas), cortas / len(lineas)


def registro_heuristico(texto, ruta=None):
    """Fallback local sin API. Devuelve (registro, confianza aproximada)."""
    if ruta is not None and ruta.suffix.lower() in (".pptx", ".ppt", ".key"):
        return "diapositivas", 0.9
    p_vin, p_cortas = densidad_vinetas(texto)
    if p_vin > 0.5 and p_cortas > 0.7:
        return "diapositivas", 0.7
    lineas = [l for l in texto.splitlines() if l.strip()]
    # Titulo corto + mayoria de vinetas: diapositiva aunque las vinetas esten en prosa.
    if (2 <= len(lineas) <= 15 and len(lineas[0].split()) <= 10 and p_vin >= 0.5):
        return "diapositivas", 0.65
    puntos = {r: sum(len(re.findall(p, texto, re.I)) for p in ps) for r, ps in PISTAS.items()}
    mejor = max(puntos, key=puntos.get)
    if puntos[mejor] == 0:
        return POR_DEFECTO, 0.3
    total = sum(puntos.values())
    return mejor, round(min(0.85, 0.4 + 0.45 * puntos[mejor] / total), 2)


def instr_voz(registro, idioma):
    r = REGISTROS[registro]
    return r["voz_en"] if idioma == "en" else r["voz_es"]


def listar():
    return [{"registro": k, "nombre": v["nombre"], "descripcion": v["choice"]}
            for k, v in REGISTROS.items()]
