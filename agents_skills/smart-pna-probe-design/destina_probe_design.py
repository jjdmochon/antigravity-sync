#!/usr/bin/env python3
"""Design DestiNA DGL / SMART PNA probes against a target sequence.

Scans the target for every interrogable blank position, ranks probe designs,
picks a panel, computes construct and labelled-product masses for the real
monomer chemistry, and optionally builds a 3D PNA.DNA duplex model.

Examples
--------
  # scan a mature miRNA and write the full design set
  python destina_probe_design.py -t UGGAGUGUGACAAUGGUGUUUG -i miR-122-5p -o out

  # same, built as chiral DGL probes with a serine-like blank, plus 3D models
  python destina_probe_design.py -t UGGAGUGUGACAAUGGUGUUUG -i miR-122-5p -o out \\
      --blank L-Ser --gamma 7,12,15 --model

  # weigh / locate an existing probe written in DestiNA notation
  python destina_probe_design.py -t UGGAGUGUGACAAUGGUGUUUG \\
      --probe "x x C A C C A T Tglu G T *L-Ser* A Cglu A C Tglu C C A"

  # read targets from a FASTA and process every record
  python destina_probe_design.py -f targets.fa -o out

Requires pna_design.py, pna_chem.py, pna_struct.py and destina_monomers.json
in the same directory (plus rdkit, biopython, numpy, scipy).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pna_chem as pc          # noqa: E402
import pna_design as pd_       # noqa: E402

TAGGED = "SMART-C-REX-PEG12-biotin"


# --------------------------------------------------------------------------- io
def read_fasta(path):
    recs, name, seq = [], None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                if name is not None:
                    recs.append((name, "".join(seq)))
                name, seq = line[1:].split()[0] or "target", []
            elif line:
                seq.append(line)
    if name is not None:
        recs.append((name, "".join(seq)))
    return recs


def write_csv(path, rows, fields=None):
    if not rows:
        return None
    fields = fields or list(rows[0])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return path


def clean_target(seq: str) -> str:
    s = "".join(c for c in seq.upper() if not c.isspace())
    bad = sorted(set(s) - set("ACGTU"))
    if bad:
        raise SystemExit(f"target contains non-ACGTU characters: {bad}")
    if not s:
        raise SystemExit("empty target sequence")
    return s


def parse_gamma(arg, n, blank_pos=None):
    if arg in (None, "", "none"):
        return {}
    if arg == "auto":
        if blank_pos is None:
            return {}
        return pd_.propose_gamma(n, blank_pos)
    if arg == "all":
        return {i: "Glu" for i in range(1, n + 1)}
    out = {}
    for tok in arg.split(","):
        tok = tok.strip()
        if not tok:
            continue
        if ":" in tok:
            pos, side = tok.split(":", 1)
        else:
            pos, side = tok, "Glu"
        out[int(pos)] = side
    return out


# ----------------------------------------------------------------------- report
def masses_for(display, gamma, blank_type, nterm, cterm):
    probe = pc.build_pna(display, gamma=gamma, blank_type=blank_type,
                         nterm=nterm, cterm=cterm)
    m = pc.masses(probe)
    out = dict(formula=m["formula"], mono=m["monoisotopic"], avg=m["average"])
    for label, smi in (("tagged", pc.SMART_TAGGED[TAGGED]),):
        lp = pc.labelled_product(probe, smi)
        out[f"{label}_avg"] = lp["average"]
        out[f"{label}_mono"] = lp["monoisotopic"]
        out[f"{label}_delta_avg"] = lp["d_average"]
    return out


def design_rows(designs, gamma_arg, blank_type, nterm, cterm, limit):
    rows = []
    for rank, d in enumerate(designs[:limit], start=1):
        g = parse_gamma(gamma_arg, d.probe_len, d.blank_pos)
        r = dict(rank=rank, **pd_.asdict(d))
        try:
            r.update(masses_for(d.pna_display, g, blank_type, nterm, cterm))
        except Exception as exc:                      # chemistry is optional here
            r["formula"] = f"n/a ({exc})"
        rows.append(r)
    return rows


def markdown_report(target_id, target, scan, unreachable, panel_rows, probe_info,
                    blank_type, gamma_arg):
    L = []
    L.append(f"# DestiNA DGL probe design - {target_id}\n")
    L.append(f"Target `5'-{target}-3'` ({len(target)} nt)\n")
    L.append(f"Blank monomer: `*{blank_type}*`   gamma: `{gamma_arg or 'none'}`\n")
    if unreachable:
        L.append(f"**Not interrogable** (within the flank constraint of "
                 f"{pd_.MIN_ARM} matched bases each side): positions "
                 f"{', '.join(map(str, unreachable))}. Extend the target "
                 f"sequence if any of these must be read.\n")
    L.append("\n## Scan - what each target position can deliver\n")
    L.append("| pos | base | reagent | designs | best score | L | window | "
             "blank N/C | Tm | Tm range | probe N->C |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in scan:
        L.append("| {interrogated_pos} | {interrogated_base} | {smart_reagent} | "
                 "{n_designs} | {best_score} | {best_len} | {best_window} | "
                 "{best_blank_pos}/{best_blank_from_cterm} | {best_tm} | "
                 "{tm_min}-{tm_max} | `{best_pna}` |".format(**r))
    L.append("\n## Panel - one probe per SMART reagent\n")
    L.append("| probe | reads | reagent | L | window | blank N/C | Tm | seq score | "
             "rank | yield score | formula | avg mass | + tagged |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in panel_rows:
        L.append("| {name} | {interrogated_base}{interrogated_pos} | {smart_reagent} | "
                 "{probe_len} | {target_start}-{target_end} | "
                 "{blank_pos}/{blank_from_cterm} | {tm_pna} | {score} | {rank} | "
                 "{yield_score} | {formula} | {avg} | {tagged_avg} |".format(
                     rank=r.get("rank_of", "-"), **r))
    flagged = [r for r in panel_rows if r.get("yield_flags")]
    if flagged:
        L.append("\nPlacement flags:\n")
        for r in flagged:
            L.append(f"- **{r['name']}**: {r['yield_flags']}")
    L.append("\nSequences (N->C, `_` = abasic blank):\n")
    for r in panel_rows:
        L.append(f"- **{r['name']}** `{r['pna_display']}`")
    if probe_info:
        L.append("\n## Supplied probe\n")
        for k, v in probe_info.items():
            L.append(f"- **{k}**: {v}")
    L.append(textwrap.dedent("""
        ## Read this with the numbers

        - Tm is the Giesen PNA/DNA regression (+/- 5 K for >90% of sequences):
          **rank with it, do not quote it as a prediction**. An RNA target is
          folded to DNA for the calculation and PNA.RNA duplexes are more
          stable, so values are conservative for a miRNA.
        - gamma modification raises Tm; no magnitude is asserted here
          (`pna_design.GAMMA_TM_OFFSET` is 0.0 by default).
        - Mass windows must use the **tagged** reagent increment, not the bare
          nucleobase aldehyde.
        - Off-target cross-hybridisation is **not** screened - that needs the
          rest of the panel plus the background transcriptome.
        - **Two scores, never added.** `seq score` rates the SEQUENCE choice
          (blank position, reagent forced, Tm, flanks); `yield score` rates the
          MONOMER PLACEMENT (blank side chain, gamma positions) for labelling
          yield. Two of the yield terms are measured from a duplex model, the
          rest encode design rules; neither score is fitted to measured yield.
        - **The sequence score is a screening heuristic, not a yield model.** It ranks
          candidates on reagent precedent, blank centrality, Tm window, flank
          balance, pyrimidine fraction and aggregation risk - none of which
          measures labelling yield. A probe validated experimentally outranks
          anything this score says; pass it with `--probe` and it is pinned
          into the panel above for comparison. Note also that the pyrimidine
          term partly double-counts Tm, which already carries -26.13*f_pyr.
        """))
    return "\n".join(L)


# ------------------------------------------------------------------------- main
def run_target(target_id, target, args):
    target = clean_target(target)
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.join(outdir, target_id.replace("/", "_"))

    if args.len_range:
        lo, hi = (int(x) for x in args.len_range.split("-"))
        pd_.LEN_RANGE = (lo, hi)
    if args.min_arm:
        pd_.MIN_ARM = args.min_arm
    if args.gamma_tm_offset:
        pd_.GAMMA_TM_OFFSET = args.gamma_tm_offset

    scan, designs = pd_.scan_target(target, target_id)
    unreachable = pd_.uncovered_positions(target, scan)
    if not designs:
        raise SystemExit(
            f"no valid designs: target is {len(target)} nt but needs at least "
            f"{2 * pd_.MIN_ARM + 1} to place a blank with "
            f"{pd_.MIN_ARM} matched bases each side")

    nterm = tuple(["AEEA"] * args.spacers)
    cterm = ("Lys",) if args.cterm_lys else ()

    write_csv(stem + "_scan.csv", scan)
    rows = design_rows(designs, args.gamma, args.blank, nterm, cterm, args.top)
    write_csv(stem + "_designs.csv", rows)

    # panel: best design per reagent, preferring Tm >= --min-tm
    panel, used = [], set()
    for rg in ("CCHO", "GCHO", "ACHO", "TCHO"):
        sub = [d for d in designs if d.smart_reagent == rg]
        warm = [d for d in sub if d.tm_pna >= args.min_tm] or sub
        if warm:
            panel.append(warm[0])
    panel_rows = []
    for n, d in enumerate(panel, start=1):
        g = parse_gamma(args.gamma, d.probe_len, d.blank_pos)
        r = dict(name=f"{target_id}_P{n}", **pd_.asdict(d))
        r.update(masses_for(d.pna_display, g, args.blank, nterm, cterm))
        ys = pd_.yield_score(d.pna_display, g, args.blank)
        r["yield_score"] = ys["total"]
        r["yield_flags"] = "; ".join(ys["flags"])
        panel_rows.append(r)
        tm0, mm = pd_.flank_mismatch_scan(d, target)
        write_csv(f"{stem}_P{n}_mismatch.csv", mm)
    write_csv(stem + "_panel.csv", panel_rows)

    probe_info = {}
    if args.probe:
        p = pc.parse_probe(args.probe)
        # pin the supplied probe into the panel so a validated sequence is always
        # shown next to the candidates, whatever the heuristic score ranks first
        _hit = [d for d in designs if d.pna_display == p["display"]]
        if _hit:
            _d = _hit[0]
            _r = dict(name=args.probe_name, **pd_.asdict(_d))
            _r.update(masses_for(p["display"], p["gamma"], p["blank_type"],
                                 p["nterm"], p["cterm"]))
            _ys = pd_.yield_score(p["display"], p["gamma"], p["blank_type"])
            _r["yield_score"] = _ys["total"]
            _r["yield_flags"] = "; ".join(_ys["flags"])
            _r["rank_of"] = f"{designs.index(_d) + 1}/{len(designs)}"
            panel_rows.insert(0, _r)
        mol = pc.build_probe(args.probe)
        m = pc.masses(mol)
        lp = pc.labelled_product(mol, pc.SMART_TAGGED[TAGGED])
        hit = [d for d in designs if d.pna_display == p["display"]]
        probe_info = {
            "sequence (N->C)": f"`{p['display']}`",
            "length": f"{p['n_residues']}-mer",
            "gamma positions": sorted(p["gamma"]) or "none",
            "blank": f"*{p['blank_type']}* at {p['blank_pos']} from N / "
                     f"{p['blank_from_cterm']} from C",
            "formula": m["formula"],
            "monoisotopic / average": f"{m['monoisotopic']} / {m['average']}",
            f"labelled ({TAGGED})": f"{lp['average']} (+{lp['d_average']})",
        }
        if hit:
            d = hit[0]
            probe_info["found in scan"] = (
                f"reads {d.interrogated_base}{d.interrogated_pos} via "
                f"{d.smart_reagent}, Tm {d.tm_pna} C, rank "
                f"{designs.index(d) + 1}/{len(designs)}")
        else:
            probe_info["found in scan"] = ("no - this probe does not match any "
                                           "window of the given target")
        json.dump({k: str(v) for k, v in probe_info.items()},
                  open(stem + "_probe.json", "w"), indent=1)

    md = markdown_report(target_id, target, scan, unreachable, panel_rows,
                         probe_info, args.blank, args.gamma)
    with open(stem + "_report.md", "w", encoding="utf-8") as fh:
        fh.write(md)

    if args.model:
        import pna_struct as ps
        src = panel[0] if not args.probe else (
            hit[0] if args.probe and hit else panel[0])
        g = sorted(parse_gamma(args.gamma, src.probe_len, src.blank_pos))
        tpl_path = args.template or _fetch_template(args.pdb_id, outdir)
        tpl = ps.Template(tpl_path, args.pdb_id)
        window = target.replace("U", "T")[src.target_start - 1:src.target_end]
        for tag, blank in (("abasic", True), ("labelled", False)):
            d_, p_ = ps.build_duplex(tpl, window, src.pna_display, blank=blank,
                                     gamma_positions=g or None)
            if g and args.sidechains:
                bp = src.pna_display.index("_") + 1
                side = "Ser" if "Ser" in args.blank else (
                    "Glu" if args.blank == "GL" else None)
                ps.add_gamma_sidechains(d_, p_, g, blank_pos=bp if side else None,
                                        blank_side=side)
            ps.write_pdb(f"{stem}_{tag}.pdb", d_, p_,
                         f"{target_id} {tag} ({args.pdb_id} template)")

    print(f"[{target_id}] {len(designs)} designs over {len(scan)} interrogable "
          f"positions -> {stem}_report.md")
    return stem, (panel[0] if panel else None)


def _fetch_template(pdb_id, outdir):
    import urllib.request
    path = os.path.join(outdir, f"{pdb_id}.pdb")
    if not os.path.exists(path):
        urllib.request.urlretrieve(
            f"https://files.rcsb.org/download/{pdb_id}.pdb", path)
    return path


def build_parser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("-t", "--target", help="target sequence (DNA or RNA)")
    src.add_argument("-f", "--fasta", help="FASTA file of targets")
    p.add_argument("-i", "--id", default="target", help="target name")
    p.add_argument("-o", "--outdir", default="destina_out", help="output directory")
    p.add_argument("--blank", default="L-Ser",
                   choices=sorted(pc.BLANK_TYPES), help="abasic monomer")
    p.add_argument("--gamma", default=None,
                   help="'auto' (offsets -3/+2/+5 from each probe's own blank, "
                        "recommended), 'all', 'none', or explicit positions "
                        "e.g. 7,12,15 (optionally 7:Glu,10:Ser)")
    p.add_argument("--probe", help="existing probe in DestiNA notation, to weigh "
                                   "and locate on the target; it is also pinned "
                                   "into the panel table for comparison")
    p.add_argument("--probe-name", default="supplied",
                   help="label for --probe in the panel table")
    p.add_argument("--top", type=int, default=200, help="designs to write")
    p.add_argument("--min-tm", type=float, default=55.0,
                   help="preferred minimum Tm when picking the panel")
    p.add_argument("--len-range", help="probe lengths, e.g. 9-18")
    p.add_argument("--min-arm", type=int, help="matched bases each side of blank")
    p.add_argument("--gamma-tm-offset", type=float, default=None,
                   help="additive K for gamma modification (default 0, none asserted)")
    p.add_argument("--spacers", type=int, default=2,
                   help="N-terminal AEEA spacers (monomer code X)")
    p.add_argument("--no-cterm-lys", dest="cterm_lys", action="store_false",
                   help="omit the C-terminal lysine")
    p.add_argument("--model", action="store_true", help="build 3D duplex models")
    p.add_argument("--sidechains", action="store_true",
                   help="with --model, grow the real gamma side chains")
    p.add_argument("--pdb-id", default="3PA0", choices=["3PA0", "1NR8"],
                   help="structural template (3PA0 = gamma-modified)")
    p.add_argument("--template", help="local template PDB instead of downloading")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    pc.validate()
    targets = (read_fasta(args.fasta) if args.fasta
               else [(args.id, args.target)])
    if not targets:
        raise SystemExit("no sequences found")
    chosen = {}
    for name, seq in targets:
        chosen[name] = run_target(name, seq, args)
    # multiplex panel: check every probe against the other targets
    if len(targets) > 1:
        tmap = {n: clean_target(s) for n, s in targets}
        rows = []
        for name, (_stem, best) in chosen.items():
            if best is not None:
                rows += pd_.cross_check(best, name, tmap)
        path = os.path.join(args.outdir, "panel_cross_check.csv")
        write_csv(path, rows)
        hot = [r for r in rows if r["fires"] == "YES"]
        print(f"[panel] cross-check over {len(targets)} targets -> {path}"
              + (f"  ** {len(hot)} FLAGGED **" if hot else "  (no probe fires on a "
                 "non-cognate target)"))
        for r in hot:
            print(f"   ! {r['probe_target']} probe matches {r['off_target']} "
                  f"{r['matches']}/{r['of']} with {r['base_opposite_blank']} "
                  f"opposite the blank")


if __name__ == "__main__":
    main()
