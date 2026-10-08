"""Kernel sidecar for smart-pna-probe-design.

Loads the three bundled modules (pna_design, pna_chem, pna_struct) into the
live kernel and provides the two entry points used by SKILL.md.
"""
import os
import sys


def pna_skill_dir():
    """Absolute path of this skill's directory on disk."""
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    if not here:
        raise RuntimeError("skill dir unavailable in this runtime")
    return here


def pna_modules():
    """Import and return (pna_design, pna_chem, pna_struct)."""
    d = pna_skill_dir()
    if d not in sys.path:
        sys.path.insert(0, d)
    import pna_design
    import pna_chem
    import pna_struct
    return pna_design, pna_chem, pna_struct


def pna_template(path=None, pdb_id="3PA0"):
    """Return a local path to a PNA.DNA template PDB, downloading if absent.

    pdb_id="3PA0" (default) is the 1.6 A GAMMA-modified PNA.DNA duplex - the
    structurally matched template for DestiNA gamma-Glu / gamma-Ser DGL probes.
    pdb_id="1NR8" is the 1.66 A ALPHA-modified (D-Lys) chiral PNA.DNA duplex,
    mostly plain aeg monomers; use it for achiral aeg probes.
    """
    import urllib.request
    if path is None:
        path = os.path.join("struct", pdb_id + ".pdb")
    if not os.path.exists(path):
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        urllib.request.urlretrieve(
            "https://files.rcsb.org/download/" + pdb_id + ".pdb", path)
    return path


def pna_design_panel(target, target_id="target", one_per_reagent=True,
                     min_tm=55.0, top_n=None):
    """Enumerate probe designs for one target and pick a panel.

    Returns {"designs": [...all, ranked...], "panel": [...selected...]} as
    dataclass instances. With one_per_reagent, picks the best design for each
    SMART reagent class (so all four bases of the target become readable),
    preferring designs at or above min_tm; otherwise returns the top_n overall.
    """
    pd_, _pc, _ps = pna_modules()
    designs = pd_.enumerate_designs(target, target_id)
    if not one_per_reagent:
        return {"designs": designs, "panel": designs[:(top_n or 4)]}
    panel = []
    for rg in ("CCHO", "GCHO", "ACHO", "TCHO"):
        sub = [d for d in designs if d.smart_reagent == rg]
        warm = [d for d in sub if d.tm_pna >= min_tm]
        if warm:
            panel.append(warm[0])
        elif sub:
            panel.append(sub[0])
    return {"designs": designs, "panel": panel}


def pna_scan(target, target_id="target"):
    """Scan every interrogable position along the target (step 1 of the DGL
    workflow). Returns {"scan": rows 5'->3', "designs": ranked, "unreachable":
    positions no probe can read under the flank constraint}."""
    pd_, _pc, _ps = pna_modules()
    rows, designs = pd_.scan_target(target, target_id)
    return {"scan": rows, "designs": designs,
            "unreachable": pd_.uncovered_positions(target, rows)}


def pna_model_duplex(design, target, out_prefix="probe", template=None,
                     labelled=True, pdb_id="3PA0", gamma_positions=None):
    """Build and write PNA.DNA duplex models for one Design.

    Writes <out_prefix>_abasic.pdb and, when labelled, <out_prefix>_labelled.pdb.
    Returns a dict of file paths plus the geometry QC that should be reported
    with any model: junction bond lengths, Watson-Crick H-bond distances, and
    the abasic cavity dimensions.
    """
    import numpy
    pd_, _pc, ps = pna_modules()
    tpl = ps.Template(pna_template(template, pdb_id), pdb_id)
    window = target.upper().replace("U", "T")[
        design.target_start - 1:design.target_end]
    out = {"template": tpl.name, "modification": tpl.modification,
           "template_best_step_rmsd": tpl.best_step_rmsd,
           "helix": dict(tpl.step_stats)}
    for tag, is_blank in (("abasic", True), ("labelled", False)):
        if tag == "labelled" and not labelled:
            continue
        d_, p_ = ps.build_duplex(tpl, window, design.pna_display, blank=is_blank,
                                 gamma_positions=gamma_positions)
        path = out_prefix + "_" + tag + ".pdb"
        ps.write_pdb(path, d_, p_, out_prefix + " " + tag)
        db, pb = ps.backbone_continuity(d_, p_)
        wc = [r["d"] for r in ps.wc_distances(d_, p_, window)]
        out[tag] = {
            "path": path,
            "o3p_bond": (round(min(db), 3), round(max(db), 3)),
            "amide_bond": (round(min(pb), 3), round(max(pb), 3)),
            "wc_n": len(wc),
            "wc_range": (round(min(wc), 2), round(max(wc), 2)),
        }
        if is_blank:
            blk = p_[design.blank_pos][1]
            tgt = d_[design.interrogated_pos][1]
            face = ps.BASE_ATOMS[design.interrogated_base]
            ds = [float(numpy.linalg.norm(blk["N4'"] - tgt[a]))
                  for a in ("N1", "N2", "O6", "N4", "O2", "N3", "O4", "N6")
                  if a in tgt and a in face]
            out[tag]["cavity_range"] = (round(min(ds), 2), round(max(ds), 2))
    return out

def pna_reference_probe(name=None, target="UGGAGUGUGACAAUGGUGUUUG"):
    """Parse a DestiNA production probe, weigh it, and locate it on the target.

    Defaults to the current default probe DGL-122_4.6 against mature
    miR-122-5p. Returns the parsed spec, construct masses (free and labelled
    with the tagged SMART reagent), and the matching Design from a scan of the
    target - ready to pass to pna_model_duplex().
    """
    pd_, pc, _ps = pna_modules()
    if name is None:
        name = pc.REFERENCE_PROBE_DEFAULT
    spec = pc.REFERENCE_PROBES[name]
    parsed = pc.parse_probe(spec)
    probe = pc.build_probe(spec)
    tagged = pc.SMART_TAGGED["SMART-C-REX-PEG12-biotin"]
    _rows, designs = pd_.scan_target(target, name)
    match = [d for d in designs if d.pna_display == parsed["display"]]
    return {"name": name, "spec": spec, "parsed": parsed,
            "masses": pc.masses(probe),
            "labelled": pc.labelled_product(probe, tagged),
            "design": match[0] if match else None,
            "gamma_positions": sorted(parsed["gamma"])}
