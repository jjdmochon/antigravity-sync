import os
import sys
import anydoc

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_anydoc.py <file_path> [output_md] [--no-assets]")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    output_md = None
    extract_assets = True

    for arg in sys.argv[2:]:
        if arg == "--no-assets":
            extract_assets = False
        elif not arg.startswith("--"):
            output_md = arg

    if not output_md:
        output_md = os.path.splitext(file_path)[0] + ".md"

    with open(file_path, "rb") as f:
        data = f.read()

    doc = None
    try:
        doc = anydoc.to_document(data)
    except Exception:
        doc = None

    try:
        markdown_text = anydoc.to_markdown_bytes(data)
    except Exception:
        markdown_text = ""

    assets_count = 0
    assets_dir = ""
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.dirname(os.path.abspath(output_md))
    if extract_assets:
        assets_dir = os.path.join(output_dir, f"{base_name}_assets")

    if extract_assets and doc and getattr(doc, "assets", None):
        os.makedirs(assets_dir, exist_ok=True)
        ext_map = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif",
            "image/svg+xml": ".svg",
            "image/webp": ".webp",
            "image/wmf": ".wmf",
            "image/emf": ".emf",
            "application/vnd.ms-ole-object": ".cdx"
        }

        for i, asset in enumerate(doc.assets):
            ext = ext_map.get(asset.media_type, ".bin")
            data_to_write = asset.data

            # Check if this is an OLE container (e.g. embedded ChemDraw drawing or office object)
            if asset.media_type == "application/vnd.ms-ole-object" or data_to_write.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
                try:
                    import olefile
                    import io
                    ole = olefile.OleFileIO(io.BytesIO(data_to_write))
                    # ChemDraw embedded drawings store native CDX in CONTENTS stream
                    if ole.exists("CONTENTS"):
                        cdx_stream = ole.openstream("CONTENTS").read()
                        if cdx_stream.startswith(b"VjCD0100"):
                            data_to_write = cdx_stream
                            ext = ".cdx"
                    ole.close()
                except Exception:
                    pass

            fname = f"asset_{i+1}{ext}"
            apath = os.path.join(assets_dir, fname)
            with open(apath, "wb") as af:
                af.write(data_to_write)
            assets_count += 1

    # If PDF and assets requested, extract via PyMuPDF if doc.assets was not populated
    if extract_assets and file_path.lower().endswith(".pdf"):
        try:
            import fitz
            pdf_doc = fitz.open(file_path)
            os.makedirs(assets_dir, exist_ok=True)
            seen_xrefs = set()
            for pno, page in enumerate(pdf_doc):
                for img_info in page.get_images():
                    xref = img_info[0]
                    if xref in seen_xrefs:
                        continue
                    seen_xrefs.add(xref)
                    base_image = pdf_doc.extract_image(xref)
                    ext = "." + base_image.get("ext", "png")
                    fname = f"page_{pno+1:02d}_img_{xref}{ext}"
                    apath = os.path.join(assets_dir, fname)
                    with open(apath, "wb") as af:
                        af.write(base_image["image"])
                    assets_count += 1
        except Exception as e:
            print(f"Notice: PyMuPDF asset extraction skipped or failed: {e}")

    with open(output_md, "w", encoding="utf-8") as mf:
        mf.write(markdown_text)

    print(f"Successfully converted '{file_path}' to '{output_md}'")
    if extract_assets and assets_count > 0:
        print(f"Extracted {assets_count} assets to '{assets_dir}'")

if __name__ == "__main__":
    main()
