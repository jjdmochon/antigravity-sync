#!/usr/bin/env python3
"""
jev_router.py - Enrutador semántico System-1 híbrido (Jev nativo + Local Fallback)
Ejecuta decisiones tipadas en sub-100ms mediante Jev (TypeSafe AI).
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path

# Cargar variables de entorno desde ~/.env
try:
    import dotenv
    dotenv.load_dotenv(Path.home() / ".env")
except ImportError:
    pass

DOMAIN_DEFINITIONS = {
    "destina_biotech": {
        "description": "Química de PNA, Dynamic Chemical Labeling (DCL), sondas SMART, miR-122, toxicidad hepática DILI, BioNeMo NIMs, Drug2cell, espectrometría MALDI-TOF/LC-MS.",
        "keywords": ["pna", "dcl", "smart", "mir-122", "mir", "microrna", "biomarcador", "destina", "dili", "maldi", "lc-ms", "bionemo", "diffdock", "molmim", "boltz", "drug2cell"]
    },
    "ugr_teaching": {
        "description": "Docencia universitaria en Farmacia UGR (Química Farmacéutica I y II, QFUNO, QFDOS, TRANSMED), exámenes, evaluación continua, TFM/TFG, campus virtual.",
        "keywords": ["ugr", "qfuno", "qfdos", "qf1", "qf2", "quimica farmaceutica", "farmacia", "examen", "alumnos", "docencia", "evaluacion continua", "tfm", "tfg", "transmed", "diapositiva", "tema"]
    },
    "biophysics_pna": {
        "description": "Modelado biofísico de PNA, termodinámica de dúplex/tríplex, Geometric Deep Learning (PyG), diseño de análogos.",
        "keywords": ["termodinamica", "duplex", "triplex", "pyg", "geometric deep learning", "gdl", "analogos", "entalpia", "melting", "tm"]
    },
    "keratin_krt10": {
        "description": "Genómica y variantes de queratina KRT10, ictiosis epidermolítica, mecánica de filamentos intermedios, mutaciones patogénicas.",
        "keywords": ["krt10", "queratina", "keratin", "ictiosis", "ichthyosis", "epidermolitica", "filamentos intermedios"]
    },
    "compliance_iso": {
        "description": "Gestión de calidad, auditorías ISO 9001 e ISO 13485, dashboards de métricas, listas de chequeo regulatorio.",
        "keywords": ["iso", "9001", "13485", "auditoria", "checklist", "calidad", "regulacion", "no conformidad", "dashboard", "metricas"]
    },
    "review_provenance": {
        "description": "Pipeline de revisión documental: marcas de agua de IA, watermarks-remover, no-ai-slop, humanizer-juanjo, estilo ejecutivo.",
        "keywords": ["revisar", "manuscrito", "slop", "no-ai-slop", "humanizer", "watermark", "marcas de agua", "procedencia", "c2pa", "estilo"]
    },
    "scientific_tools": {
        "description": "Búsqueda en bases de datos científicas (ChEMBL, PubChem, PDB, UniProt, ClinVar, EuropePMC) y ToolUniverse.",
        "keywords": ["chembl", "pubchem", "uniprot", "pdb", "clinvar", "blast", "foldseek", "tooluniverse", "secuencia", "estructura", "smiles"]
    },
    "general_dev": {
        "description": "Scripts generales de Python, PowerShell, automatización de archivos, administración de sistema.",
        "keywords": ["script", "python", "powershell", "terminal", "bash", "git", "archivo", "carpeta", "convertir", "bulk", "instalar", "error"]
    }
}

SUBAGENT_TRIGGERS = [
    "en paralelo", "subagente", "subagentes", "analiza en profundidad", 
    "revisa los dos", "pipeline", "bulk", "lote", "exhaustivo", "dossier"
]

CODE_TRIGGERS = [
    "ejecuta", "script", "codigo", "terminal", "powershell", "python", 
    "convierte", "extrae", "guarda", "instala", "corre", "descarga", "crea"
]

def run_local_system_one(text: str):
    text_lower = text.lower()
    scores = {}
    for domain, data in DOMAIN_DEFINITIONS.items():
        score = 0
        for kw in data["keywords"]:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                score += 2
            elif kw in text_lower:
                score += 1
        scores[domain] = score
    
    best_domain = max(scores, key=scores.get)
    best_score = scores[best_domain]
    confidence = min(0.99, max(0.55, best_score / 4.0)) if best_score > 0 else 0.50
    if best_score == 0:
        best_domain = "general_dev"

    requires_subagent = any(t in text_lower for t in SUBAGENT_TRIGGERS) or len(text.split()) > 40
    requires_code = any(t in text_lower for t in CODE_TRIGGERS)

    word_count = len(text.split())
    if word_count < 10 and not requires_subagent:
        complexity = 0.2
    elif word_count < 35 and not requires_subagent:
        complexity = 1.0
    else:
        complexity = 2.0

    return {
        "domain": best_domain,
        "domain_confidence": round(confidence, 2),
        "requires_subagent": 0.85 if requires_subagent else 0.15,
        "requires_code_execution": 0.90 if requires_code else 0.10,
        "complexity_level": complexity,
        "engine": "local-fallback (fast-rule)",
        "status": "success"
    }

def run_jev_native(text: str, api_key: str):
    from typesafe_sdk import TypeSafeClient, Choice, Noul, Score
    client = TypeSafeClient(api_key=api_key)
    criteria = {k: v["description"] for k, v in DOMAIN_DEFINITIONS.items()}
    
    resp = client.system_one(
        state={"prompt": text},
        questions={
            "domain": Choice(instructions="Clasifica el dominio técnico principal.", criteria=criteria),
            "requires_subagent": Noul(instructions="¿Requiere subagente dedicado o delegación paralela?"),
            "requires_code_execution": Noul(instructions="¿Requiere ejecutar código o scripts?"),
            "task_complexity": Score(instructions="Complejidad de la tarea", criteria=["Simple", "Media", "Compleja"])
        }
    )
    ans = resp.answers
    return {
        "domain": ans["domain"].choice,
        "domain_confidence": getattr(ans["domain"], "confidence", 1.0),
        "requires_subagent": ans["requires_subagent"].noul,
        "requires_code_execution": ans["requires_code_execution"].noul,
        "complexity_level": ans["task_complexity"].score,
        "engine": "jev-native (typesafe-ai)",
        "status": "success"
    }

def route_task(text_or_prompt: str):
    api_key = os.getenv("TYPESAFE_API_KEY")
    if api_key:
        try:
            return run_jev_native(text_or_prompt, api_key)
        except Exception as e:
            fallback = run_local_system_one(text_or_prompt)
            fallback["warning"] = f"Fallo en Jev API ({e}), usando fallback."
            return fallback
    else:
        return run_local_system_one(text_or_prompt)

def main():
    parser = argparse.ArgumentParser(description="Jev System-1 Hybrid Router")
    parser.add_argument("query", help="Texto o instrucción a clasificar")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON estructurado")
    args = parser.parse_args()

    res = route_task(args.query)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        sub_bool = "SÍ" if float(res['requires_subagent']) >= 0.5 else "NO"
        cod_bool = "SÍ" if float(res['requires_code_execution']) >= 0.5 else "NO"
        print(f"[DOMINIO]             {res['domain']} (confianza: {res['domain_confidence']})")
        print(f"[SUBAGENTE]           {sub_bool} (probabilidad: {res['requires_subagent']})")
        print(f"[CODIGO]              {cod_bool} (probabilidad: {res['requires_code_execution']})")
        print(f"[COMPLEJIDAD]         {res['complexity_level']}")
        print(f"[MOTOR]               {res['engine']}")

if __name__ == "__main__":
    main()
