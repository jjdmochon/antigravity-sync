import os
import io
import sys
import olefile

def fix_cdx_files_in_dir(target_dir):
    """
    Recursively scans target_dir for .cdx files.
    If a file is actually an OLE Compound Document containing a 'CONTENTS'
    stream with ChemDraw binary magic ('VjCD0100'), it extracts the genuine
    CDX stream and replaces the OLE wrapper with the pure CDX file.
    """
    fixed = 0
    already_clean = 0
    skipped = 0

    for root, _, files in os.walk(target_dir):
        for f in files:
            if f.lower().endswith(".cdx"):
                p = os.path.join(root, f)
                try:
                    if olefile.isOleFile(p):
                        ole = olefile.OleFileIO(p)
                        if ole.exists("CONTENTS"):
                            cdx_data = ole.openstream("CONTENTS").read()
                            if cdx_data.startswith(b"VjCD0100"):
                                ole.close()
                                with open(p, "wb") as out_f:
                                    out_f.write(cdx_data)
                                fixed += 1
                                print(f"[FIXED] {p} ({len(cdx_data)} bytes)")
                            else:
                                ole.close()
                                skipped += 1
                                print(f"[SKIPPED: CONTENTS not CDX] {p}")
                        else:
                            ole.close()
                            skipped += 1
                            print(f"[SKIPPED: No CONTENTS stream] {p}")
                    else:
                        with open(p, "rb") as test_f:
                            hdr = test_f.read(8)
                        if hdr.startswith(b"VjCD0100"):
                            already_clean += 1
                        else:
                            skipped += 1
                except Exception as e:
                    print(f"[ERROR] {p}: {e}")
                    skipped += 1

    print(f"\n--- Summary ---")
    print(f"Fixed files: {fixed}")
    print(f"Already clean CDX files: {already_clean}")
    print(f"Skipped / non-CDX: {skipped}")

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    fix_cdx_files_in_dir(folder)
