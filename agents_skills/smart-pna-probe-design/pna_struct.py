"""Template-based construction of an antiparallel aeg-PNA.DNA duplex carrying an
abasic (blank) monomer, and of the labelled product after dynamic chemical
labelling.

Template: PDB 1NR8, a 1.66 A crystal structure of a D-lysine-based chiral
PNA.DNA decamer duplex (DNA chain A 5'-AGTGATCTAC-3', PNA chain B
N-GTAGATCACT-C). PNA residues 5-7 (A66/T66/C66) carry the chiral lysine
substituent and use N1'/CA for the backbone atoms that the standard aeg monomers
(APN/GPN/CPN/TPN) call N4'/C5'; these are aliased on load.

Method: the duplex is a regular helix, so the rigid-body screw transformation
that carries base pair i onto base pair i+1 is extracted for every step,
averaged in screw coordinates, and then propagated to build an arbitrary-length
duplex. Each position is populated with a template base pair of the required
type, brought into a common frame by superposition of its backbone atoms only
(chemically identical across residue types), so the bases inherit experimentally
observed positions relative to their own backbone.

This is a fibre/homology model, not a refined structure: it is used for register
and cavity geometry, and its internal consistency is reported (backbone bond
lengths, Watson-Crick hydrogen-bond distances, rise/twist spread).

Arm connectivity verified from the template: N4'-C7'(=O7')-C8'-N9/N1.
  blank monomer  = natural monomer minus {base, C7', O7', C8'}  -> secondary amine
  labelled product = natural monomer minus {O7'}                -> N4'-CH2-CH2-N9
"""
from __future__ import annotations

import collections
import os

import numpy as np

# The chiral (D-Lys) monomers A66/T66/C66 name the same backbone positions
# differently, and the two nitrogens are SWAPPED relative to the aeg monomers:
# verified from PDB 1NR8 connectivity, their "N" is the tertiary amide nitrogen
# bonded to the arm carbonyl C7' (= N4' in aeg monomers) while "N1'" is the
# N-terminal amine bonded to C2' (= N in aeg monomers). The rename must be
# applied simultaneously, not sequentially.
PNA_ALIAS = {"N": "N4'", "N1'": "N", "CA": "C5'"}
PNA_BB = ["N", "C2'", "C3'", "N4'", "C5'", "C", "O"]
DNA_BB = ["P", "O5'", "C5'", "C4'", "O4'", "C3'", "O3'", "C2'", "C1'"]
PNA_RES = {"A": "APN", "G": "GPN", "C": "CPN", "T": "TPN"}
DNA_RES = {"A": "DA", "G": "DG", "C": "DC", "T": "DT"}
ARM = ["C7'", "O7'", "C8'"]
PURINE_RING = ["N9", "C8", "N7", "C5", "C6", "N1", "C2", "N3", "C4"]
PYRIM_RING = ["N1", "C2", "N3", "C4", "C5", "C6"]
BASE_ATOMS = {
    "A": PURINE_RING + ["N6"], "G": PURINE_RING + ["N2", "O6"],
    "C": PYRIM_RING + ["N4", "O2"], "T": PYRIM_RING + ["O2", "O4", "C5M"],
}
GLYCOSYL_N = {"A": "N9", "G": "N9", "C": "N1", "T": "N1"}
WC_PAIRS = {  # (purine atom, pyrimidine atom) hydrogen bonds
    ("G", "C"): [("N1", "N3"), ("N2", "O2"), ("O6", "N4")],
    ("A", "T"): [("N1", "N3"), ("N6", "O4")],
}


# Experimental PNA.DNA templates. Both are antiparallel with PNA N->C = reverse
# complement of the target 5'->3' (verified independently on each).
#
#   1NR8  1.66 A  ALPHA-modified chiral PNA (D-Lys side chain on the carbon
#                 bonded to the backbone CARBONYL) in residues A66/T66/C66;
#                 the other seven residues are plain aeg monomers.
#   3PA0  1.60 A  GAMMA-modified chiral PNA (methyl on the carbon bonded to the
#                 backbone AMINE - the same position DestiNA's gamma-Glu/gamma-Ser
#                 side chains occupy), every residue modified, C-terminal Lys.
#
# For a gamma-modified DGL probe 3PA0 is the structurally matched template. Its
# PNA chain is numbered C->N in the file (the Lys at residue 1 is the
# C-terminus, verified from C(i+1)-N(i) amide bonds of 1.29-1.49 A), so it is
# renumbered on load; its gamma carbon is named CA where aeg monomers use C2',
# and the thymine 5-methyl is C7 where 1NR8 uses C5M.
TEMPLATES = {
    "1NR8": dict(
        dna_chain="A", pna_chain="B", pna_reversed=False, cap_res="NH2",
        pna_res_match=("PN", "66"),
        # chiral monomers of 1NR8 swap the two backbone nitrogen names
        alias={"66": {"N": "N4'", "N1'": "N", "CA": "C5'"}},
        # dropped: only 3 of 10 residues carry it and it sits at ALPHA, so
        # keeping it would decorate an otherwise uniform aeg model unevenly
        sidechain=["CB", "CG", "CD", "CE", "NZ"], keep_sidechain=False,
        modification="alpha"),
    "3PA0": dict(
        dna_chain="B", pna_chain="D", pna_reversed=True, cap_res="LYS",
        pna_res_match=("40",),
        alias={"40": {"CA": "C2'", "C7": "C5M"}},
        # kept: every residue carries it and it marks the GAMMA substituent
        # vector. It is the crystal's methyl - a stub showing where a
        # glutamyl/serinyl side chain would project, not that side chain.
        sidechain=["C2M"], keep_sidechain=True, modification="gamma"),
}
DEFAULT_TEMPLATE = "1NR8"


def pna_base(resname: str) -> str:
    """Base letter of a PNA residue name (APN/T66/40G/BLK/FIL all handled)."""
    if resname in ("BLK", "FIL", "NH2", "LYS"):
        return ""
    for ch in resname:
        if ch in "ACGT":
            return ch
    return ""


def template_for(path: str, template: str | None = None) -> tuple[str, dict]:
    """Resolve a template name from an explicit argument or the file name."""
    if template is None:
        base = os.path.basename(path).upper()
        for name in TEMPLATES:
            if name in base:
                template = name
                break
        else:
            template = DEFAULT_TEMPLATE
    if template not in TEMPLATES:
        raise ValueError(f"unknown template {template!r}; known: {sorted(TEMPLATES)}")
    return template, TEMPLATES[template]


def parse_pdb(path: str, template: str | None = None) -> dict:
    name, cfg = template_for(path, template)
    res: dict = collections.OrderedDict()
    for ln in open(path):
        if ln.startswith("ENDMDL"):
            break
        if ln.startswith(("ATOM", "HETATM")):
            rn = ln[17:20].strip()
            if rn not in ("HOH", "MG", "ZN", "EDO", "NA", "CL", "GOL"):
                key = (ln[21], int(ln[22:26]), rn)
                res.setdefault(key, {})[ln[12:16].strip()] = np.array(
                    [float(ln[30:38]), float(ln[38:46]), float(ln[46:54])])
    # Per-residue-class atom renames onto aeg nomenclature, applied
    # SIMULTANEOUSLY (1NR8's two nitrogens are swapped, so a sequential rename
    # would collapse them onto one name).
    for key in list(res):
        for suffix, amap in cfg["alias"].items():
            if key[2].endswith(suffix) or key[2].startswith(suffix):
                res[key] = {amap.get(a, a): v for a, v in res[key].items()}
                break
    return res


def kabsch(P: np.ndarray, Q: np.ndarray):
    """Rotation+translation mapping P onto Q (both n x 3)."""
    cp, cq = P.mean(0), Q.mean(0)
    H = (P - cp).T @ (Q - cq)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return R, cq - R @ cp


def rmsd(P, Q):
    return float(np.sqrt(((P - Q) ** 2).sum(1).mean()))


def to_screw(R, t):
    """Rotation+translation -> (axis, angle, rise along axis, point on axis)."""
    ang = float(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
    w = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    n = w / np.linalg.norm(w)
    rise = float(n @ t)
    p = np.linalg.pinv(np.eye(3) - R) @ (t - rise * n)
    return n, ang, rise, p


def from_screw(n, ang, rise, p):
    n = n / np.linalg.norm(n)
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    R = np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)
    return R, (np.eye(3) - R) @ p + rise * n


class Template:
    """Experimental PNA.DNA base-pair units and the helical step transform.

    `template` selects the entry in TEMPLATES; when omitted it is inferred from
    the file name, defaulting to 1NR8. Use 3PA0 for gamma-modified probes.
    """

    step_rmsd_cut = 0.60   # A; keep only steps this well fitted by a rigid motion

    def __init__(self, path: str, template: str | None = None):
        self.name, self.cfg = template_for(path, template)
        self.modification = self.cfg["modification"]
        self.res = parse_pdb(path, self.name)
        dch, pch = self.cfg["dna_chain"], self.cfg["pna_chain"]
        cap_res = self.cfg["cap_res"]
        self.dna = {k[1]: (k, v) for k, v in self.res.items()
                    if k[0] == dch and k[2] in DNA_RES.values()}
        pna_items = [(k, v) for k, v in self.res.items()
                     if k[0] == pch and k[2] != cap_res
                     and any(k[2].startswith(p) or k[2].endswith(p)
                             for p in self.cfg["pna_res_match"])]
        self.cap = next((v for k, v in self.res.items()
                         if k[0] == pch and k[2] == cap_res), None)
        # Renumber both strands 1..n in their chemical direction: DNA 5'->3' and
        # PNA N->C, so unit k = (DNA k, PNA n+1-k) holds for every template.
        if self.cfg["pna_reversed"]:
            pna_items = pna_items[::-1]
        self.pna = {i: (k, v) for i, (k, v) in enumerate(pna_items, start=1)}
        dna_items = sorted(self.dna.items())
        self.dna = {i: kv for i, (_, kv) in enumerate(dna_items, start=1)}
        self.n = len(self.pna)
        assert len(self.dna) == self.n, (len(self.dna), self.n)
        # unit k = (DNA residue k, PNA residue n+1-k); both are WC partners
        self.units = {k: (self.dna[k], self.pna[self.n + 1 - k])
                      for k in sorted(self.dna)}
        self._check_pairing()
        self.steps = self._steps()
        self.T = self._average_step()
        # best-fitted step between two usable units, used to grow the model
        cand = [s for s in self.steps
                if self._plain(self.n + 1 - s["k"]) and self._plain(self.n - s["k"])
                and "P" in self.dna[s["k"]][1] and "P" in self.dna[s["k"] + 1][1]]
        assert cand, f"{self.name}: no usable consecutive units"
        best = min(cand, key=lambda s: s["rmsd"])
        self.best_step = (best["k"], best["k"] + 1)
        self.best_step_rmsd = round(best["rmsd"], 3)
        # Donor base PAIR for each DNA base: an intact template unit with that
        # DNA base, a usable PNA partner and a 5'-phosphate, taken as close to
        # the duplex interior as possible.
        self.donor_pair = {}
        self.grafted_phosphate = []
        for b in "ACGT":
            cand = [k for k, ((dk, dv), (pk, pv)) in self.units.items()
                    if dk[2] == DNA_RES[b] and self._plain(self.n + 1 - k)]
            assert cand, f"{self.name}: no donor pair for DNA {b}"
            withP = [k for k in cand if "P" in self.units[k][0][1]]
            pool = withP or cand
            if not withP:
                self.grafted_phosphate.append(b)
            self.donor_pair[b] = min(pool, key=lambda k: abs(k - (self.n + 1) / 2))

    def donor_unit(self, dna_base: str):
        """Donor (DNA atoms, PNA atoms) for `dna_base`, phosphate guaranteed.

        A 5'-terminal donor residue carries no phosphate (3PA0's only adenine is
        the 5' terminus). P/OP1/OP2 are then grafted from a phosphate-bearing
        residue by superposing its deoxyribose onto the donor's, which places
        them from experimental geometry rather than idealised internal
        coordinates; the build's regularisation closes the O3'-P bond exactly.
        """
        k = self.donor_pair[dna_base]
        (dk, dv), (pk, pv) = self.units[k]
        dv = dict(dv)
        if not self.cfg.get("keep_sidechain", False):
            pv = {a: v for a, v in pv.items() if a not in self.cfg["sidechain"]}
        if "P" not in dv:
            src = next((v for i, (kk, v) in sorted(self.dna.items())
                        if "P" in v and all(a in v for a in SUGAR)), None)
            assert src is not None, f"{self.name}: no phosphate donor residue"
            shared = [a for a in SUGAR if a in src and a in dv]
            R, t = kabsch(np.array([src[a] for a in shared]),
                          np.array([dv[a] for a in shared]))
            for a in ("P", "OP1", "OP2"):
                if a in src:
                    dv[a] = R @ src[a] + t
        return dv, pv

    def _plain(self, pna_idx: int) -> bool:
        """PNA residue usable as a geometry donor.

        For 1NR8 that means an unmodified aeg monomer (the alpha-chiral ones
        perturb local geometry); for 3PA0 every residue is gamma-modified and
        equivalent, so all are usable.
        """
        if pna_idx not in self.pna:
            return False
        rn = self.pna[pna_idx][0][2]
        return rn.endswith("PN") if self.name == "1NR8" else True

    def _check_pairing(self):
        """Require every unit to be a real Watson-Crick pair in the crystal."""
        bad = []
        for k, ((dk, dv), (pk, pv)) in self.units.items():
            db, pb = dk[2][-1], pna_base(pk[2])
            key = (db, pb) if (db, pb) in WC_PAIRS else (pb, db)
            if key not in WC_PAIRS:
                bad.append((k, dk[2], pk[2], "not complementary"))
                continue
            pur_dna = key[0] == db
            ds = []
            for a1, a2 in WC_PAIRS[key]:
                A, B = (dv, pv) if pur_dna else (pv, dv)
                if a1 in A and a2 in B:
                    ds.append(float(np.linalg.norm(A[a1] - B[a2])))
            if not ds or min(ds) > 3.4:
                bad.append((k, dk[2], pk[2], f"min H-bond {min(ds) if ds else None}"))
        assert not bad, f"{self.name}: unit pairing check failed: {bad}"

    def _bb(self, k, atoms_only=True):
        (dk, dv), (pk, pv) = self.units[k]
        names = [("A", a) for a in DNA_BB if a in dv] + [("B", a) for a in PNA_BB if a in pv]
        return names

    def _coords(self, k, names):
        (dk, dv), (pk, pv) = self.units[k]
        return np.array([(dv if c == "A" else pv)[a] for c, a in names])

    def _steps(self):
        out = []
        ks = sorted(self.units)
        for k in ks[:-1]:
            if k + 1 not in self.units:
                continue
            shared = [nm for nm in self._bb(k) if nm in self._bb(k + 1)]
            P, Q = self._coords(k, shared), self._coords(k + 1, shared)
            R, t = kabsch(P, Q)
            out.append(dict(k=k, R=R, t=t, rmsd=rmsd(R @ P.T + t[:, None], Q.T).__float__()
                            if False else rmsd((R @ P.T).T + t, Q),
                            screw=to_screw(R, t)))
        return out

    def _average_step(self):
        """Single helical operator fitted globally.

        Averaging per-step screw transformations accumulates error along the
        build (the crystal duplex is not perfectly regular, and the chiral
        residues perturb local geometry). Instead one rigid transformation is
        least-squares fitted to carry every usable unit onto its successor
        simultaneously, which is the operator that best regularises the duplex
        and keeps inter-residue bonds closed when propagated.
        """
        usable = [k for k, ((dk, dv), (pk, pv)) in self.units.items()
                  if self._plain(self.n + 1 - k) and "P" in dv]
        pairs = [(k, k + 1) for k in usable if k + 1 in usable]
        # Terminal steps of the crystal duplex are irregular (fraying, packing);
        # keep only steps that are individually well described by a rigid motion,
        # which selects the regular interior steps.
        fit = {s["k"]: s["rmsd"] for s in self.steps}
        good = [(a, b) for a, b in pairs if fit.get(a, 9e9) <= self.step_rmsd_cut]
        if len(good) < 2:
            good = sorted(pairs, key=lambda ab: fit.get(ab[0], 9e9))[:2]
        pairs = good
        assert pairs, "no usable consecutive unmodified units in template"
        common = set(self._bb(pairs[0][0]))
        for a, b in pairs:
            common &= set(self._bb(a)) & set(self._bb(b))
        names = [nm for nm in self._bb(pairs[0][0]) if nm in common]
        P = np.vstack([self._coords(a, names) for a, _ in pairs])
        Q = np.vstack([self._coords(b, names) for _, b in pairs])
        R, t = kabsch(P, Q)
        n, ang, rise, p = to_screw(R, t)
        if rise < 0:
            n, ang, rise = -n, ang, -rise
        per_step = [np.degrees(s["screw"][1]) for s in self.steps]
        self.step_stats = dict(
            twist_deg=round(float(np.degrees(ang)), 2), rise_A=round(float(rise), 3),
            bp_per_turn=round(float(360 / np.degrees(ang)), 2),
            global_fit_rmsd=round(rmsd((R @ P.T).T + t, Q), 3),
            n_step_pairs=len(pairs), n_atoms_per_unit=len(names),
            per_step_twist_sd=round(float(np.std(per_step)), 2))
        return R, t

    def ref_unit_for(self, dna_base: str):
        """Template unit with this DNA base, an unmodified PNA partner and a 5'-P."""
        best = None
        for k, ((dk, dv), (pk, pv)) in self.units.items():
            if dk[2] != DNA_RES[dna_base]:
                continue
            score = (pk[2].endswith("PN"), "P" in dv, k)
            if best is None or score > best[0]:
                best = (score, k)
        return best[1]


def _apply(R, t, atoms: dict) -> dict:
    return {a: R @ v + t for a, v in atoms.items()}


SUGAR = ["C1'", "C2'", "C3'", "C4'", "O4'"]
CHIRAL_SIDECHAIN = ["CB", "CG", "CD", "CE", "NZ"]


def _swap_base(acceptor: dict, donor: dict, fit_atoms, keep_atoms, take_atoms):
    """Replace a residue's base (and PNA arm) with a donor's, keeping the
    acceptor's own backbone so inter-residue bonds are untouched."""
    shared = [a for a in fit_atoms if a in acceptor and a in donor]
    R, t = kabsch(np.array([donor[a] for a in shared]),
                  np.array([acceptor[a] for a in shared]))
    out = {a: v for a, v in acceptor.items() if a in keep_atoms}
    for a in take_atoms:
        if a in donor:
            out[a] = R @ donor[a] + t
    return out


O3P_BOND, AMIDE_BOND = 1.60, 1.33


def _regularize(frames, L, w_ref: float = 0.08, w_bond: float = 1.0):
    """Close inter-residue bonds by rigid-body adjustment of each base pair.

    Each base pair keeps its internal geometry exactly (so Watson-Crick
    hydrogen bonding is untouched) and is allowed a small rigid-body
    displacement. Residuals drive the DNA O3'-P and PNA C-N junction distances
    to their bonded values, with a weak restraint holding every pair near its
    template-derived starting placement so the helix cannot drift.
    """
    from scipy.optimize import least_squares
    from scipy.spatial.transform import Rotation

    cents = [np.mean(np.array(list(fd.values()) + list(fp.values())), 0)
             for fd, fp in frames]

    def place(x):
        out = []
        for i, (fd, fp) in enumerate(frames):
            rv, tr = x[6 * i:6 * i + 3], x[6 * i + 3:6 * i + 6]
            R = Rotation.from_rotvec(rv).as_matrix()
            c = cents[i]
            out.append(({a: R @ (v - c) + c + tr for a, v in fd.items()},
                        {a: R @ (v - c) + c + tr for a, v in fp.items()}))
        return out

    def resid(x):
        pf = place(x)
        r = []
        for i in range(1, L):
            r.append(w_bond * (np.linalg.norm(pf[i - 1][0]["O3'"] - pf[i][0]["P"]) - O3P_BOND))
            r.append(w_bond * (np.linalg.norm(pf[i][1]["C"] - pf[i - 1][1]["N"]) - AMIDE_BOND))
        r.extend((w_ref * x).tolist())
        return np.array(r)

    x0 = np.zeros(6 * L)
    sol = least_squares(resid, x0, method="lm", max_nfev=20000)
    _regularize.report = dict(cost=round(float(sol.cost), 4), nfev=int(sol.nfev))
    return place(sol.x)


def build_duplex(tpl: Template, dna_seq: str, pna_display: str,
                 blank: bool = True, regularize: bool = True,
                 gamma_positions=None):
    """Build an antiparallel aeg-PNA.DNA duplex of arbitrary length.

    The backbone is grown by repeatedly superimposing the template's best-fitted
    base-pair step onto the growing terminus and appending the second unit of
    that step, so every inter-residue bond is the experimentally observed one
    rather than the product of an accumulated helical operator. Bases are then
    substituted locally by superposition onto each residue's own backbone, which
    leaves the backbone - and therefore the bonding - unchanged.

    dna_seq     : target 5'->3'
    pna_display : PNA N->C, '_' at the abasic monomer
    blank       : True  -> blank monomer (base + arm removed, secondary amine)
                  False -> labelled product (natural arm minus carbonyl oxygen)
    gamma_positions : 1-based PNA positions that carry a gamma side chain. On a
                  gamma template the crystal's gamma substituent stub is then
                  kept ONLY at those positions and stripped elsewhere, so a
                  probe that is gamma-modified at a few positions is not drawn
                  as if it were modified throughout. None keeps the template
                  default for every residue.
    """
    L = len(dna_seq)
    assert len(pna_display) == L, (len(pna_display), L)
    ka, kb = tpl.best_step
    (dka, dva), (pka, pva) = tpl.units[ka]
    (dkb, dvb), (pkb, pvb) = tpl.units[kb]
    bb_a = [("A", a) for a in DNA_BB if a in dva] + [("B", a) for a in PNA_BB if a in pva]
    bb_b = [("A", a) for a in DNA_BB if a in dvb] + [("B", a) for a in PNA_BB if a in pvb]
    bb = [nm for nm in bb_a if nm in bb_b]

    def _unit_coords(u_dna, u_pna):
        return np.array([(u_dna if c == "A" else u_pna)[a] for c, a in bb])

    def _donor(dbase):
        return tpl.donor_unit(dbase)

    # Each position is a complete, correctly Watson-Crick-paired template base
    # pair of the required type, moved as a rigid body: first onto the frame of
    # the step's trailing unit (so it sits in the helix like that unit), then by
    # the step superposition onto the growing terminus.
    frames = []
    for i, dbase in enumerate(dna_seq):
        dd, dp = _donor(dbase)
        if i == 0:
            R0, t0 = kabsch(_unit_coords(dd, dp), _unit_coords(dva, pva))
            frames.append((_apply(R0, t0, dd), _apply(R0, t0, dp)))
            continue
        Rn, tn = kabsch(_unit_coords(dd, dp), _unit_coords(dvb, pvb))
        cand_d, cand_p = _apply(Rn, tn, dd), _apply(Rn, tn, dp)
        cur_d, cur_p = frames[-1]
        Rm, tm = kabsch(_unit_coords(dva, pva), _unit_coords(cur_d, cur_p))
        frames.append((_apply(Rm, tm, cand_d), _apply(Rm, tm, cand_p)))

    if regularize and L > 1:
        frames = _regularize(frames, L)

    dna_out, pna_out = {}, {}
    for i, dbase in enumerate(dna_seq):
        fd, fp = frames[i]
        dna_out[i + 1] = (DNA_RES[dbase], fd)
        p_idx = L - i                       # PNA position, N->C
        ch = pna_display[p_idx - 1]
        want = {"A": "T", "T": "A", "G": "C", "C": "G"}[dbase]
        if ch != "_":
            assert ch == want, (ch, dbase)
        atoms = fp
        if gamma_positions is not None and tpl.cfg["sidechain"]:
            if p_idx not in set(gamma_positions):
                atoms = {a: v for a, v in atoms.items()
                         if a not in tpl.cfg["sidechain"]}
        if ch == "_":
            if blank:
                drop = set(ARM) | set(BASE_ATOMS[want])
                atoms = {a: v for a, v in atoms.items() if a not in drop}
                rn = "BLK"
            else:
                atoms = {a: v for a, v in atoms.items() if a != "O7'"}
                rn = "FIL"
        else:
            rn = PNA_RES[ch]
        pna_out[p_idx] = (rn, atoms)
    # 5'-terminal DNA residue has no phosphate
    rn, av = dna_out[1]
    dna_out[1] = (rn, {a: v for a, v in av.items() if a not in ("P", "OP1", "OP2")})
    # C-terminal amide cap, placed from the template's own NH2 residue
    if tpl.cap is not None:
        kc = min(tpl.pna)
        (pk, pv) = tpl.pna[kc]
        shared = [a for a in PNA_BB if a in pv and a in pna_out[L][1]]
        Rc, tc = kabsch(np.array([pv[a] for a in shared]),
                        np.array([pna_out[L][1][a] for a in shared]))
        pna_out[L + 1] = ("NH2", _apply(Rc, tc, tpl.cap))
    return dna_out, pna_out


def write_pdb(path: str, dna_out: dict, pna_out: dict, title: str = ""):
    el = lambda a: ("C" if a[0] == "C" else "N" if a[0] == "N" else
                    "O" if a[0] == "O" else "P" if a[0] == "P" else a[0])
    lines, serial = [], 1
    if title:
        lines.append(f"TITLE     {title[:70]}")
    for ch, out in (("A", dna_out), ("B", pna_out)):
        for ri in sorted(out):
            rn, atoms = out[ri]
            for a, v in atoms.items():
                lines.append(
                    f"ATOM  {serial:>5} {a:<4}{'':1}{rn:>3} {ch}{ri:>4}{'':4}"
                    f"{v[0]:>8.3f}{v[1]:>8.3f}{v[2]:>8.3f}{1.0:>6.2f}{0.0:>6.2f}"
                    f"{'':10}{el(a):>2}")
                serial += 1
        lines.append("TER")
    lines.append("END")
    open(path, "w").write("\n".join(lines) + "\n")
    return path


# --- measurements -------------------------------------------------------------
def backbone_continuity(dna_out, pna_out):
    dna_b = [float(np.linalg.norm(dna_out[i][1]["O3'"] - dna_out[i + 1][1]["P"]))
             for i in sorted(dna_out)[:-1] if "P" in dna_out[i + 1][1]]
    pna_keys = [k for k in sorted(pna_out) if pna_out[k][0] != "NH2"]
    pna_b = [float(np.linalg.norm(pna_out[i][1]["C"] - pna_out[i + 1][1]["N"]))
             for i in pna_keys[:-1]]
    return dna_b, pna_b


def wc_distances(dna_out, pna_out, dna_seq):
    L = len(dna_seq)
    rows = []
    for i, db in enumerate(dna_seq, start=1):
        p = L - i + 1
        prn, pv = pna_out[p]
        if prn in ("BLK", "FIL", "NH2"):
            continue
        pb = pna_base(prn)
        key = (db, pb) if (db, pb) in WC_PAIRS else (pb, db)
        if key not in WC_PAIRS:
            continue
        pur_is_dna = key[0] == db
        for a_pur, a_pyr in WC_PAIRS[key]:
            A = dna_out[i][1] if pur_is_dna else pv
            B = pv if pur_is_dna else dna_out[i][1]
            if a_pur in A and a_pyr in B:
                rows.append(dict(dna_pos=i, pair=f"{db}:{pb}",
                                 atoms=f"{a_pur}...{a_pyr}",
                                 d=round(float(np.linalg.norm(A[a_pur] - B[a_pyr])), 2)))
    return rows


def template_arm_span(tpl: Template):
    """Experimental N4'...N9/N1 distance across the natural amide arm."""
    out = []
    for k, (pk, pv) in tpl.pna.items():
        b = pna_base(pk[2])
        gn = GLYCOSYL_N[b]
        if "N4'" in pv and gn in pv:
            out.append(float(np.linalg.norm(pv["N4'"] - pv[gn])))
    return out


# --- real gamma side chains ---------------------------------------------------
# The template carries only the crystal's gamma METHYL stub (C2M). These build
# the actual DestiNA side chains onto it, keeping the template's experimentally
# observed gamma configuration - (S) in 3PA0, which is what an L-amino-acid
# derived gamma monomer requires. Note the CIP descriptor of the finished
# residue depends on the side chain: gamma-L-Glu reads (S) while the
# serine-like blank reads (R) from the SAME spatial arrangement, because
# CH2-OH outranks the backbone CH2-N and swaps the middle two priorities.
GAMMA_SIDECHAIN_ATOMS = {"Glu": ["CB", "CG", "CD", "OE1", "OE2"],
                         "Ser": ["CB", "OG"]}


def nerf(a, b, c, bond, angle_deg, torsion_deg):
    """Place an atom from three predecessors by bond length, angle and torsion."""
    ang, tor = np.radians(angle_deg), np.radians(torsion_deg)
    bc = c - b
    bc = bc / np.linalg.norm(bc)
    n = np.cross(b - a, bc)
    n = n / np.linalg.norm(n)
    m = np.cross(n, bc)
    d = np.array([-bond * np.cos(ang),
                  bond * np.sin(ang) * np.cos(tor),
                  bond * np.sin(ang) * np.sin(tor)])
    return c + d[0] * bc + d[1] * m + d[2] * n


def _environment(dna_out, pna_out, skip):
    pts = [v for _ri, (_rn, at) in dna_out.items() for v in at.values()]
    pts += [v for ri, (_rn, at) in pna_out.items() if ri != skip for v in at.values()]
    return np.array(pts)


def add_gamma_sidechains(dna_out, pna_out, gamma_positions, blank_pos=None,
                         blank_side="Ser", gamma_side="Glu"):
    """Grow real gamma side chains on a built duplex.

    gamma_positions : 1-based PNA positions carrying a gamma monomer; each must
                      already have the template stub C2M, which becomes CB.
    blank_pos       : position of the abasic blank, if it is a CHIRAL blank
                      (*L-Ser* / *GL*); its side chain is placed by transferring
                      the gamma vector from a built gamma residue.
    Torsions are chosen by scanning for the rotamer with the largest minimum
    contact to the rest of the duplex. Returns a report per position.
    """
    rep = {}
    ref = None
    for i in gamma_positions:
        at = pna_out[i][1]
        if "C2M" not in at:
            raise ValueError(f"PNA residue {i} has no gamma stub C2M - build the "
                             f"duplex on a gamma template with gamma_positions set")
        if ref is None:
            ref = {k: at[k].copy() for k in ("N", "C2'", "C3'", "C2M")}
        env = _environment(dna_out, pna_out, i)
        cb = at.pop("C2M")
        at["CB"] = cb
        best = None
        for chi1 in range(0, 360, 10):
            cg = nerf(at["N"], at["C2'"], cb, 1.52, 114.0, chi1)
            for chi2 in range(0, 360, 20):
                cd = nerf(at["C2'"], cb, cg, 1.52, 112.0, chi2)
                oe1 = nerf(cb, cg, cd, 1.25, 118.0, 0.0)
                oe2 = nerf(cb, cg, cd, 1.25, 118.0, 180.0)
                new = np.array([cg, cd, oe1, oe2])
                dmin = float(np.min(np.linalg.norm(
                    env[:, None, :] - new[None, :, :], axis=2)))
                if best is None or dmin > best[0]:
                    best = (dmin, cg, cd, oe1, oe2, chi1, chi2)
        at.update(CG=best[1], CD=best[2], OE1=best[3], OE2=best[4])
        rep[i] = dict(side=gamma_side, min_contact=round(best[0], 2),
                      chi1=best[5], chi2=best[6])
    if blank_pos is not None and blank_side:
        at = pna_out[blank_pos][1]
        assert ref is not None, "need at least one gamma residue as the vector donor"
        nm = ["N", "C2'", "C3'"]
        R, t = kabsch(np.array([ref[a] for a in nm]), np.array([at[a] for a in nm]))
        at["CB"] = R @ ref["C2M"] + t
        env = _environment(dna_out, pna_out, blank_pos)
        bond, ang = (1.42, 111.0) if blank_side == "Ser" else (1.52, 114.0)
        best = None
        for chi in range(0, 360, 5):
            x = nerf(at["N"], at["C2'"], at["CB"], bond, ang, chi)
            d = float(np.min(np.linalg.norm(env - x, axis=1)))
            if best is None or d > best[0]:
                best = (d, x, chi)
        at["OG" if blank_side == "Ser" else "CG"] = best[1]
        rep[blank_pos] = dict(side=blank_side, min_contact=round(best[0], 2),
                              chi1=best[2])
    return rep


def gamma_configuration(atoms, side="Glu"):
    """CIP descriptor at the gamma carbon of a built residue.

    Priority order differs by side chain: for Glu (and any plain alkyl) the
    backbone CH2-N outranks the side chain, for Ser the side-chain CH2-O
    outranks it - which is why the same spatial arrangement reads (S) for
    gamma-L-Glu and (R) for the serine-like blank.
    """
    first = "CB" if side == "Ser" else "C3'"
    second = "C3'" if side == "Ser" else "CB"
    t = float(np.dot(atoms["N"] - atoms["C2'"],
                     np.cross(atoms[first] - atoms["C2'"],
                              atoms[second] - atoms["C2'"])))
    return "S" if t > 0 else "R"
