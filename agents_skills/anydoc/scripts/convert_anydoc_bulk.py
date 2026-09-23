#!/usr/bin/env python3
"""
convert_anydoc_bulk.py - Conversión por lotes (bulk) de documentos a Markdown
Extracción automática de imágenes y detección de objetos ChemDraw (.cdx) en carpetas de assets.
"""

import os
import sys
import argparse
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import anydoc

EXT_MAP = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
    "image/webp": ".webp",
    "image/wmf": ".wmf",
    "image/emf": ".emf",
    "application/vnd.ms-ole-object": ".cdx",
}

CDX_MAGIC = b"VjCD0100"

SUPPORTED_EXTENSIONS = {
    ".docx", ".doc", ".pptx", ".ppt", ".pdf", 
    ".xlsx", ".xls", ".odt", ".odp", ".ods", ".rtf"
}

def detect_asset_extension(asset):
    if asset.data and len(asset.data) >= 8 and asset.data[:8] == CDX_MAGIC:
        return ".cdx"
    media_type = getattr(asset, "media_type", "") or ""
    if media_type in EXT_MAP:
        return EXT_MAP[media_type]
    if "ole" in media_type.lower() or "chemdraw" in media_type.lower():
        return ".cdx"
    return ".bin"

def convert_single_file(file_path: str, output_base_dir: str = None, extract_assets: bool = True, skip_existing: bool = False):
    try:
        f_path = Path(file_path)
        if output_base_dir:
            out_base = Path(output_base_dir)
            target_md = out_base / (f_path.stem + ".md")
            assets_dir = out_base / f"{f_path.stem}_assets"
        else:
            target_md = f_path.with_suffix(".md")
            assets_dir = f_path.parent / f"{f_path.stem}_assets"

        if skip_existing and target_md.exists():
            return {
                "file": str(f_path),
                "status": "skipped",
                "md_path": str(target_md),
                "assets_count": 0,
                "cdx_count": 0,
                "error": None
            }

        with open(f_path, "rb") as f:
            data = f.read()

        markdown_text = anydoc.to_markdown_bytes(data)
        doc = anydoc.to_document(data)

        assets_count = 0
        cdx_count = 0

        if extract_assets and doc.assets:
            assets_dir.mkdir(parents=True, exist_ok=True)
            for i, asset in enumerate(doc.assets):
                ext = detect_asset_extension(asset)
                if ext == ".cdx":
                    cdx_count += 1
                fname = f"asset_{i+1}{ext}"
                apath = assets_dir / fname
                with open(apath, "wb") as af:
                    af.write(asset.data)
                assets_count += 1

        target_md.parent.mkdir(parents=True, exist_ok=True)
        with open(target_md, "w", encoding="utf-8") as mf:
            mf.write(markdown_text)

        return {
            "file": str(f_path),
            "status": "success",
            "md_path": str(target_md),
            "assets_count": assets_count,
            "cdx_count": cdx_count,
            "error": None
        }
    except Exception as e:
        return {
            "file": str(file_path),
            "status": "error",
            "md_path": None,
            "assets_count": 0,
            "cdx_count": 0,
            "error": str(e)
        }

def find_candidate_files(source_path: Path, recursive: bool = True, extensions: set = None):
    if extensions is None:
        extensions = SUPPORTED_EXTENSIONS
    extensions = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in extensions}

    if source_path.is_file():
        if source_path.suffix.lower() in extensions:
            return [source_path]
        return []

    pattern = "**/*" if recursive else "*"
    files = []
    for p in source_path.glob(pattern):
        if p.is_file() and p.suffix.lower() in extensions:
            if not p.name.startswith("~$"):
                files.append(p)
    return sorted(files)

def main():
    parser = argparse.ArgumentParser(description="Conversión bulk de documentos a Markdown con extracción de assets y ChemDraw (.cdx)")
    parser.add_argument("input_path", help="Ruta de archivo o carpeta a procesar")
    parser.add_argument("-o", "--output-dir", help="Directorio de salida (opcional)")
    parser.add_argument("-r", "--recursive", action="store_true", default=True, help="Escanear subdirectorios recursivamente")
    parser.add_argument("--no-recursive", dest="recursive", action="store_false", help="Solo escanear directorio raíz")
    parser.add_argument("--exts", help="Lista de extensiones (ej: pptx,docx,pdf)")
    parser.add_argument("--no-assets", action="store_true", help="No extraer assets ni .cdx")
    parser.add_argument("--skip-existing", action="store_true", help="Saltar archivos cuyo .md ya exista")
    parser.add_argument("-w", "--workers", type=int, default=min(6, os.cpu_count() or 1), help="Workers paralelos")

    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    if not input_path.exists():
        print(f"[ERROR] No existe la ruta: {input_path}")
        sys.exit(1)

    out_dir = Path(args.output_dir).resolve() if args.output_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    if args.exts:
        custom_exts = {e.strip() for e in args.exts.split(",") if e.strip()}
    else:
        custom_exts = SUPPORTED_EXTENSIONS

    print("=" * 70)
    print("ANYDOC BULK CONVERTER (Markdown + Assets + ChemDraw .cdx)")
    print("=" * 70)
    print(f"Entrada:        {input_path}")
    print(f"Salida:         {out_dir if out_dir else 'Junto a cada archivo original'}")
    print(f"Recursivo:      {args.recursive}")
    print(f"Extraer assets: {not args.no_assets}")
    print(f"Paralelismo:    {args.workers} workers")
    print("-" * 70)

    start_time = time.time()
    files = find_candidate_files(input_path, recursive=args.recursive, extensions=custom_exts)

    if not files:
        print("[AVISO] No se han encontrado archivos compatibles para procesar.")
        sys.exit(0)

    print(f"Encontrados {len(files)} archivos para procesar.\n")

    total_converted = 0
    total_skipped = 0
    total_errors = 0
    total_assets = 0
    total_cdx = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                convert_single_file, 
                str(f), 
                str(out_dir) if out_dir else None, 
                not args.no_assets, 
                args.skip_existing
            ): f for f in files
        }

        for i, future in enumerate(as_completed(futures), 1):
            res = future.result()
            fname = Path(res["file"]).name
            if res["status"] == "success":
                total_converted += 1
                total_assets += res["assets_count"]
                total_cdx += res["cdx_count"]
                cdx_str = f" [{res['cdx_count']} .cdx]" if res["cdx_count"] > 0 else ""
                print(f"[{i}/{len(files)}] [OK] {fname} -> {res['assets_count']} assets{cdx_str}")
            elif res["status"] == "skipped":
                total_skipped += 1
                print(f"[{i}/{len(files)}] [OMITIDO] {fname} (Ya existía)")
            else:
                total_errors += 1
                print(f"[{i}/{len(files)}] [ERROR] {fname}: {res['error']}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print("RESUMEN FINAL DE LA CONVERSIÓN BULK")
    print("=" * 70)
    print(f"Tiempo total:            {elapsed:.2f} s")
    print(f"Archivos procesados:     {len(files)}")
    print(f"Convertidos con éxito:   {total_converted}")
    print(f"Omitidos (ya existían):  {total_skipped}")
    print(f"Errores:                 {total_errors}")
    print(f"Total assets extraídos:  {total_assets}")
    print(f"Total objetos CDX:       {total_cdx}")
    print("=" * 70)

if __name__ == "__main__":
    main()
