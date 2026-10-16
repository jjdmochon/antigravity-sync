#!/usr/bin/env python3
r"""
calibrar_registros.py - Valida las instrucciones de voz por registro contra pares de contraste.

Para cada muestra de tests/registros_contraste.json hace UNA llamada a Jev con el Choice de
registro y el Noul de voz de todos los registros, y comprueba:

  - p_voz(ok)  bajo su propio registro   < --max-ok   (def. 0.35)
  - p_voz(mal) bajo su propio registro   > --min-mal  (def. 0.65)
  - separacion media mal - ok            >= --min-sep (def. 0.60; ideal ~0.8)
  - el Choice acierta el registro de las muestras 'ok' (bloqueante)
  - ninguna muestra 'mal' queda enmascarada en modo automatico: si el Choice la envia a
    otro registro, la voz de ese registro debe seguir rechazandola (p_voz >= --umbral).
    Un 'mal' mal enrutado pero rechazado se informa sin bloquear: el gate acierta igual.

Imprime tambien la matriz cruzada: muestras 'ok' de cada registro puntuadas con la voz de los
demas. Si un registro aprueba textos de otros (valores bajos fuera de la diagonal), su
instruccion no discrimina el formato.

Uso:
  py -3.13 calibrar_registros.py
  py -3.13 calibrar_registros.py --solo alumnos manuscrito --json
Sale con codigo 1 si algun registro no supera los umbrales.
"""

import argparse
import json
import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import jev_registros as reg  # noqa: E402
import jev_doc_gatekeeper as gk  # noqa: E402  (carga ~/.env)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

FIXTURES = AQUI.parent / "tests" / "registros_contraste.json"


def puntuar(cliente, Noul, Choice, texto, lang):
    preguntas = {"voz_" + k: Noul(instructions=reg.instr_voz(k, lang)) for k in reg.REGISTROS}
    preguntas["registro"] = Choice(instructions=reg.INSTR_CHOICE,
                                   criteria={k: v["choice"] for k, v in reg.REGISTROS.items()})
    a = cliente.system_one(state={"documento": texto}, questions=preguntas).answers
    return ({k: round(float(a["voz_" + k].noul), 3) for k in reg.REGISTROS},
            reg.normalizar(a["registro"].choice), round(float(a["registro"].confidence), 3))


def main():
    ap = argparse.ArgumentParser(description="Calibracion de registros de voz de Jev")
    ap.add_argument("--solo", nargs="*", help="Registros a calibrar (def. todos)")
    ap.add_argument("--max-ok", type=float, default=0.35)
    ap.add_argument("--min-mal", type=float, default=0.65)
    ap.add_argument("--min-sep", type=float, default=0.60)
    ap.add_argument("--umbral", type=float, default=0.50,
                    help="Umbral del gate para el control de enmascaramiento (def. 0.50)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    from typesafe_sdk import TypeSafeClient, Noul, Choice
    cliente = TypeSafeClient(api_key=os.getenv("TYPESAFE_API_KEY"))
    datos = json.loads(FIXTURES.read_text(encoding="utf-8"))
    registros = [r for r in reg.REGISTROS if not args.solo or r in args.solo]

    informe, matriz, fallos = {}, {}, []
    for r in registros:
        filas = {"ok": [], "mal": []}
        for tipo in ("ok", "mal"):
            for m in datos.get(r, {}).get(tipo, []):
                voces, elegido, conf = puntuar(cliente, Noul, Choice, m["texto"], m["lang"])
                filas[tipo].append({"lang": m["lang"], "p_voz": voces[r], "choice": elegido,
                                    "choice_conf": conf, "acierto_choice": elegido == r,
                                    "p_voz_auto": voces.get(elegido, voces[r])})
                if tipo == "ok":
                    matriz.setdefault(r, []).append(voces)
        ok = [f["p_voz"] for f in filas["ok"]]
        mal = [f["p_voz"] for f in filas["mal"]]
        sep = (sum(mal) / len(mal) - sum(ok) / len(ok)) if ok and mal else None
        problemas = []
        if ok and max(ok) >= args.max_ok:
            problemas.append("ok con p_voz %.2f >= %.2f" % (max(ok), args.max_ok))
        if mal and min(mal) <= args.min_mal:
            problemas.append("mal con p_voz %.2f <= %.2f" % (min(mal), args.min_mal))
        if sep is not None and sep < args.min_sep:
            problemas.append("separacion %.2f < %.2f" % (sep, args.min_sep))
        errores_ok = [f for f in filas["ok"] if not f["acierto_choice"]]
        if errores_ok:
            problemas.append("choice falla en %d muestra(s) ok: %s"
                             % (len(errores_ok), ", ".join(f["choice"] or "?" for f in errores_ok)))
        enmascaradas = [f for f in filas["mal"]
                        if not f["acierto_choice"] and f["p_voz_auto"] < args.umbral]
        if enmascaradas:
            problemas.append("%d muestra(s) mal enmascaradas: el choice las envia a %s y alli "
                             "pasarian el gate (p_voz %s)"
                             % (len(enmascaradas), ", ".join(f["choice"] or "?" for f in enmascaradas),
                                ", ".join("%.2f" % f["p_voz_auto"] for f in enmascaradas)))
        avisos = ["mal enrutada a %s pero rechazada igual (p_voz %.2f)" % (f["choice"], f["p_voz_auto"])
                  for f in filas["mal"] if not f["acierto_choice"] and f["p_voz_auto"] >= args.umbral]
        if problemas:
            fallos.append(r)
        informe[r] = {"muestras": filas, "separacion": round(sep, 3) if sep is not None else None,
                      "problemas": problemas, "avisos": avisos, "ok": not problemas}

    cruzada = {r: {k: round(sum(v[k] for v in vs) / len(vs), 3) for k in reg.REGISTROS}
               for r, vs in matriz.items()}

    if args.json:
        print(json.dumps({"registros": informe, "matriz_ok": cruzada, "fallos": fallos},
                         indent=2, ensure_ascii=False))
    else:
        print("\n=== CALIBRACION DE REGISTROS (Jev Noul de voz) ===")
        for r, d in informe.items():
            ok = ", ".join("%.2f" % f["p_voz"] for f in d["muestras"]["ok"]) or "-"
            mal = ", ".join("%.2f" % f["p_voz"] for f in d["muestras"]["mal"]) or "-"
            print("%-13s %s  ok=[%s]  mal=[%s]  sep=%s"
                  % (r, "OK   " if d["ok"] else "FALLA", ok, mal, d["separacion"]))
            for pr in d["problemas"]:
                print("              - " + pr)
            for av in d["avisos"]:
                print("              · aviso: " + av)
        print("\nMatriz cruzada (fila: muestras ok del registro; columna: voz aplicada)")
        print("%-13s " % "" + " ".join("%6s" % k[:6] for k in reg.REGISTROS))
        for r, fila in cruzada.items():
            print("%-13s " % r + " ".join("%6.2f" % fila[k] for k in reg.REGISTROS))
        print("\nDiagonal baja y resto alto = el registro discrimina. Ajusta la instruccion de "
              "jev_registros.py que falle y repite.\n")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
