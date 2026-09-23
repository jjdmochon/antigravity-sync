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

    markdown_text = anydoc.to_markdown_bytes(data)
    doc = anydoc.to_document(data)

    assets_count = 0
    assets_dir = ""
    if extract_assets and doc.assets:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = os.path.dirname(os.path.abspath(output_md))
        assets_dir = os.path.join(output_dir, f"{base_name}_assets")
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
            fname = f"asset_{i+1}{ext}"
            apath = os.path.join(assets_dir, fname)
            with open(apath, "wb") as af:
                af.write(asset.data)
            assets_count += 1

    with open(output_md, "w", encoding="utf-8") as mf:
        mf.write(markdown_text)

    print(f"Successfully converted '{file_path}' to '{output_md}'")
    if extract_assets and assets_count > 0:
        print(f"Extracted {assets_count} assets to '{assets_dir}'")

if __name__ == "__main__":
    main()
