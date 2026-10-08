"""SMART PNA (abasic / dynamic-chemical-labelling) probe design engine.

Conventions established from experimental templates PDB 1NR8 and 1PDT:
  an antiparallel PNA.DNA duplex has the PNA N-terminus facing the target 3' end,
  so the PNA sequence written N->C equals the reverse complement of the target
  written 5'->3'.

Architecture follows the validated DCL probe of Rissin DM, Lopez-Longarela B,
Pernagallo S, Ilyine H, Vliegenthart ADB, Dear JW, Diaz-Mochon JJ, Duffy DC,
PLOS ONE 2017, 12, e0179669 (10.1371/journal.pone.0179669): an abasic "blank" aeg-PNA monomer presenting a
free secondary amine sits opposite the interrogated target base; a nucleobase
aldehyde (base-CH2-CHO; GCHO/CCHO/ACHO/TCHO) is captured as an iminium under
Watson-Crick templating and reduced to a stable tertiary amine by NaBH3CN.

DestiNA DGL probes are built from CHIRAL monomers, not the achiral aeg backbone:
base-bearing positions use gamma-L-glutamyl PNA monomers (Aglu/Cglu/Gglu/Tglu)
and the abasic position uses a chiral blank bearing either a glutamic-like
(*GL*) or serine-like (*L-Ser* / *D-Ser*) side chain at gamma. The gamma
substituent pre-organises the PNA into a right-handed helix, raising target
affinity and suppressing sequence-dependent aggregation. Backbone chemistry does
not change the base-pairing register or which target base a blank interrogates,
so this module's scan is run on sequence alone; the monomer chemistry is chosen
separately and built/weighed in pna_chem (see build_pna(gamma=..., blank_type=...)).

TARGET STRAND. These probes are usually read against mature miRNA, i.e. an RNA
target, but the Tm regression below is calibrated on PNA/DNA. U is folded to T
and a PNA/DNA Tm is returned. PNA.RNA duplexes are generally MORE stable than
the PNA.DNA duplex of the same sequence, and the gamma substituent adds further
stabilisation, so absolute values here are conservative for an RNA target. Use
them to RANK designs; calibrate magnitude against your own melting data.

Thermodynamics: Tm of the matched PNA/DNA duplex from the empirical regression of
Giesen et al. NAR 1998 26:5004,
    Tm_PNA = 20.79 + 0.83*Tm_DNA - 26.13*f_pyr + 0.44*length
with Tm_DNA the nearest-neighbour value for the analogous DNA/DNA duplex
EXCLUDING end effects (as the regression specifies) and f_pyr the pyrimidine
fraction of the PNA strand. Stated accuracy of the regression is +/- 5 K for
>90% of sequences, so values are used for ranking, not as absolute predictions.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, asdict

from Bio.SeqUtils import MeltingTemp as mt

# --- Giesen regression coefficients (NAR 1998 26:5004-5006) ------------------
# The primary paper is PDF-gated (its PMC record carries metadata only), so the
# coefficients were taken from an independent restatement with verifiable text:
# Metaferia B, Wei JS, Song YK, Evangelista J, Aschenbach K, Johansson P, Wen X,
# Chen Q, Lee A, Hempel H, Gheeya JS, Getty S, Gomez R, Khan J, "Development of
# Peptide Nucleic Acid Probes for Detection of the HER2 Oncogene",
# PLOS ONE 2013, 8, e58870
# (10.1371/journal.pone.0058870), Methods: "Tm (DNA-PNA) = c0 + c1*Tm (DNA) +
# c2 * ... + c3*length, where c0 = 20.79, c1 = 0.83, c2 = -26.13, c3 = 0.44".
#
# CAVEAT on the pyrimidine term: that restatement writes it as the *number* of
# pyrimidines, which cannot be dimensionally right - a 12-mer with 4 pyrimidines
# would lose 26.13*4 = 105 K. Giesen's own abstract says the model "includ[es]
# terms for the pyrimidine content", so the term is the pyrimidine FRACTION of
# the PNA strand, which is what f_pyr() returns and what is used here (4/11
# pyrimidines -> -9.5 K, a sane magnitude).
GIESEN = dict(intercept=20.79, c_tm=0.83, c_fpyr=-26.13, c_len=0.44)

# Nearest-neighbour stacks only: zero every initiation / terminal-fray term,
# because the Giesen regression was calibrated on Tm_DNA "not including end
# effects" (Allawi & SantaLucia 1997 stacks, Biopython DNA_NN3).
NN_NO_ENDS = copy.deepcopy(mt.DNA_NN3)
for _k in ("init", "init_A/T", "init_G/C", "init_oneG/C", "init_allA/T", "init_5T/A"):
    NN_NO_ENDS[_k] = (0, 0)

# Hybridisation condition used for the DNA/DNA reference calculation.
TM_COND = dict(Na=100, dnac1=2000.0, dnac2=2000.0, saltcorr=5)

COMP = {"A": "T", "T": "A", "G": "C", "C": "G", "U": "A"}
PYRIMIDINES = set("CT")

# SMART nucleobase aldehyde required for each interrogated target base, and a
# precedent tier used in ranking. CCHO (interrogating G) is the reagent used in
# the validated abasic-PNA DCL miRNA assays; ACHO/TCHO/GCHO are demonstrated in
# the same dynamic-chemistry framework but with less assay precedent on PNA.
# (On a flexible threoninol-DNA backbone GCHO was the most selective reagent,
# Kanlidere Z, Jochim O, Cal M, Diederichsen U, Beilstein J Org Chem 2016, 12,
# 2136-2144 - backbone-dependent,
# so these tiers are deliberately exposed as a tunable dict.)
SMART_REAGENT = {"G": "CCHO", "C": "GCHO", "A": "TCHO", "T": "ACHO"}
REAGENT_TIER = {"CCHO": 1.00, "ACHO": 0.70, "TCHO": 0.60, "GCHO": 0.55}

MIN_ARM = 4          # minimum flanking matched bases on each side of the blank
# Probe lengths to enumerate. The upper bound covers the published 18-mer
# abasic miR-122 capture probe, so a scan of a full-length mature miRNA can
# reproduce real probes; shorter windows remain available because gamma
# modification raises affinity and permits shorter probes.
LEN_RANGE = (9, 18)

# Additive Tm offset (K) applied when the probe is built from gamma-modified
# chiral monomers. gamma substitution pre-organises the helix and RAISES Tm, but
# the magnitude is sequence-, side-chain- and salt-dependent and NO value for it
# is asserted here: the default is 0.0, i.e. the reported Tm is the unmodified
# PNA/DNA regression value. Set it from your own melting data if you want the
# ranking to reflect it (a constant offset does not change the ordering of
# designs that are all gamma-modified; it matters only when comparing modified
# with unmodified probes).
GAMMA_TM_OFFSET = 0.0


def revcomp(seq: str) -> str:
    return "".join(COMP[b] for b in reversed(seq.upper().replace("U", "T")))


def f_pyr(pna_bases: str) -> float:
    """Pyrimidine fraction of the PNA strand (blank position excluded)."""
    return sum(b in PYRIMIDINES for b in pna_bases) / len(pna_bases)


def tm_dna(seq: str) -> float:
    """Nearest-neighbour DNA/DNA Tm, stacks only (no end effects)."""
    return mt.Tm_NN(seq, nn_table=NN_NO_ENDS, **TM_COND)


def tm_pna(pna_bases: str, gamma_offset: float | None = None) -> float:
    """Giesen regression Tm for the matched PNA/DNA duplex.

    gamma_offset: additive K for a gamma-modified chiral backbone; defaults to
    GAMMA_TM_OFFSET (0.0, i.e. the unmodified regression value). See the note on
    GAMMA_TM_OFFSET - no stabilisation magnitude is asserted by this module.
    """
    g = GIESEN
    off = GAMMA_TM_OFFSET if gamma_offset is None else gamma_offset
    return (g["intercept"] + g["c_tm"] * tm_dna(pna_bases)
            + g["c_fpyr"] * f_pyr(pna_bases) + g["c_len"] * len(pna_bases) + off)


def tm_dna_mismatch(probe_bases: str, target_window: str) -> float:
    """DNA/DNA Tm with internal mismatches (Allawi & SantaLucia IMM parameters).

    Used only to rank flank mismatch discrimination; the Giesen regression is
    calibrated on fully matched duplexes and is not applied to mismatches.
    """
    return mt.Tm_NN(probe_bases, c_seq=target_window[::-1], nn_table=NN_NO_ENDS,
                    imm_table=mt.DNA_IMM1, **TM_COND)


def longest_run(seq: str, alphabet: str) -> int:
    best = cur = 0
    for b in seq:
        cur = cur + 1 if b in alphabet else 0
        best = max(best, cur)
    return best


def max_self_complement(seq: str) -> int:
    """Longest antiparallel self-complementary stretch (self-dimer proxy).

    `seq` may carry '_' for the abasic blank monomer, which cannot base-pair and
    therefore always breaks a run.
    """
    rev = seq[::-1]
    best = 0
    for off in range(-(len(seq) - 1), len(seq)):
        run = 0
        for i in range(len(seq)):
            j = i + off
            ok = (0 <= j < len(rev) and seq[i] != "_" and rev[j] != "_"
                  and COMP.get(seq[i]) == rev[j])
            run = run + 1 if ok else 0
            best = max(best, run)
    return best


# --- component scores (each 0..1, all reported so ranking can be re-weighted) -
def _plateau(x, lo_zero, lo_one, hi_one, hi_zero):
    if x <= lo_zero or x >= hi_zero:
        return 0.0
    if x < lo_one:
        return (x - lo_zero) / (lo_one - lo_zero)
    if x <= hi_one:
        return 1.0
    return (hi_zero - x) / (hi_zero - hi_one)


def score_tm(tm):        return _plateau(tm, 40, 55, 70, 85)
def score_fpyr(fp):      return _plateau(fp, 0.15, 0.35, 0.60, 0.80)
def score_central(b, L): return 1.0 - 2.0 * abs(b - (L + 1) / 2) / (L - 1)
def score_arm(aL, aR):   return min(aL, aR) / max(aL, aR)


def score_agg(bases):
    """Synthesis / aggregation risk: long purine tracts and G runs."""
    pur, grun = longest_run(bases, "AG"), longest_run(bases, "G")
    return max(0.0, 1.0 - 0.25 * max(0, pur - 5) - 0.34 * max(0, grun - 3))


def score_selfstruct(bases):
    return max(0.0, 1.0 - 0.30 * max(0, max_self_complement(bases) - 4))


WEIGHTS = dict(reagent=0.30, central=0.20, tm=0.20, arm=0.10, fpyr=0.10, agg=0.10)


@dataclass
class Design:
    target_id: str
    probe_len: int
    target_start: int      # 1-based inclusive window on the target
    target_end: int
    blank_pos: int         # 1-based position in the PNA, numbered N->C
    blank_from_cterm: int
    interrogated_pos: int  # 1-based position on the target (5'->3')
    interrogated_base: str
    smart_reagent: str
    pna_display: str       # N->C with '_' at the blank
    pna_bases: str         # N->C, blank omitted (thermodynamics substrate)
    arm_n: int
    arm_c: int
    tm_pna: float
    tm_dna: float
    f_pyr: float
    purine_run: int
    g_run: int
    self_comp: int
    s_reagent: float
    s_central: float
    s_tm: float
    s_arm: float
    s_fpyr: float
    s_agg: float
    s_selfstruct: float
    score: float


def enumerate_designs(target: str, target_id: str = "target",
                      len_range=LEN_RANGE, min_arm=MIN_ARM,
                      reagent_tier=None) -> list[Design]:
    """All (window, blank-position) probe designs that satisfy the arm constraint."""
    tier = REAGENT_TIER if reagent_tier is None else reagent_tier
    tgt = target.upper().replace("U", "T")
    out = []
    for L in range(len_range[0], len_range[1] + 1):
        for start in range(0, len(tgt) - L + 1):          # 0-based
            window = tgt[start:start + L]
            pna = revcomp(window)                          # N->C
            for b in range(1, L + 1):                      # 1-based blank in PNA
                arm_n, arm_c = b - 1, L - b
                if min(arm_n, arm_c) < min_arm:
                    continue
                # PNA position b (N->C) pairs with target position L-b+1 of the window
                it_in_window = L - b           # 0-based index into window
                it_pos = start + it_in_window + 1  # 1-based on full target
                it_base = window[it_in_window]
                reagent = SMART_REAGENT[it_base]
                bases = pna[:b - 1] + pna[b:]
                display = pna[:b - 1] + "_" + pna[b:]
                t_pna, t_dna, fp = tm_pna(bases), tm_dna(bases), f_pyr(bases)
                # Aggregation / self-structure are properties of the molecule as
                # synthesised, where the abasic monomer physically interrupts a
                # tract and cannot pair -> evaluate on the display string.
                s = dict(reagent=tier[reagent], central=score_central(b, L),
                         tm=score_tm(t_pna), arm=score_arm(arm_n, arm_c),
                         fpyr=score_fpyr(fp), agg=score_agg(display))
                ss = score_selfstruct(display)
                total = sum(WEIGHTS[k] * v for k, v in s.items()) * ss
                out.append(Design(
                    target_id=target_id, probe_len=L,
                    target_start=start + 1, target_end=start + L,
                    blank_pos=b, blank_from_cterm=L - b + 1,
                    interrogated_pos=it_pos, interrogated_base=it_base,
                    smart_reagent=reagent, pna_display=display, pna_bases=bases,
                    arm_n=arm_n, arm_c=arm_c,
                    tm_pna=round(t_pna, 1), tm_dna=round(t_dna, 1), f_pyr=round(fp, 3),
                    purine_run=longest_run(display, "AG"), g_run=longest_run(display, "G"),
                    self_comp=max_self_complement(display),
                    s_reagent=round(s["reagent"], 3), s_central=round(s["central"], 3),
                    s_tm=round(s["tm"], 3), s_arm=round(s["arm"], 3),
                    s_fpyr=round(s["fpyr"], 3), s_agg=round(s["agg"], 3),
                    s_selfstruct=round(ss, 3), score=round(total, 4)))
    out.sort(key=lambda d: -d.score)
    return out


def flank_mismatch_scan(d: Design, target: str, pna_factor: float = 1.36):
    """ DNA-equivalent Tm penalty for every single-base target mismatch under the
    probe's footprint, excluding the interrogated position.

    pna_factor scales the DNA penalty to an indicative PNA.DNA value: a single
    mismatch in a mixed 15-mer lowers PNA.DNA Tm by up to ~15 C versus ~11 C for
    DNA.DNA (Giesen et al. 1998, as reviewed by Pellestor et al. 2005), i.e.
    ~1.36x. Indicative only - not a calibrated prediction.
    """
    tgt = target.upper().replace("U", "T")
    window = tgt[d.target_start - 1:d.target_end]
    # target window as seen by the probe, blank column removed
    keep = [i for i in range(len(window)) if i != (d.probe_len - d.blank_pos)]
    ref_tgt = "".join(window[i] for i in keep)
    tm0 = tm_dna_mismatch(d.pna_bases, ref_tgt)
    rows = []
    for k, i in enumerate(keep):
        for alt in "ACGT":
            if alt == window[i]:
                continue
            mut = list(ref_tgt); mut[k] = alt
            tm = tm_dna_mismatch(d.pna_bases, "".join(mut))
            rows.append(dict(target_pos=d.target_start + i, wt=window[i], alt=alt,
                             dTm_dna=round(tm - tm0, 2),
                             dTm_pna_est=round((tm - tm0) * pna_factor, 2)))
    return tm0, rows


def scan_target(target: str, target_id: str = "target", designs=None, **kw):
    """Scan every interrogable position along the target - the first step of the
    DestiNA design workflow ("scan around the target miRNA").

    Walks the probe window across the target at every allowed length and blank
    offset, then reduces the enumeration to ONE ROW PER INTERROGATED TARGET
    POSITION: the best-scoring design that reads that base, plus how many
    designs reach it and the Tm spread available there. This is the table to
    read when choosing where to put the blank; enumerate_designs gives the full
    unreduced list.

    Returns (scan_rows, designs) with scan_rows ordered along the target 5'->3'.
    """
    if designs is None:
        designs = enumerate_designs(target, target_id, **kw)
    by_pos: dict[int, list] = {}
    for d in designs:
        by_pos.setdefault(d.interrogated_pos, []).append(d)
    rows = []
    for pos in sorted(by_pos):
        ds = sorted(by_pos[pos], key=lambda x: -x.score)
        best = ds[0]
        tms = [x.tm_pna for x in ds]
        rows.append(dict(
            target_id=target_id, interrogated_pos=pos,
            interrogated_base=best.interrogated_base,
            smart_reagent=best.smart_reagent, n_designs=len(ds),
            best_score=best.score, best_len=best.probe_len,
            best_window=f"{best.target_start}-{best.target_end}",
            best_blank_pos=best.blank_pos, best_blank_from_cterm=best.blank_from_cterm,
            best_tm=best.tm_pna, tm_min=min(tms), tm_max=max(tms),
            best_arms=f"{best.arm_n}/{best.arm_c}", best_pna=best.pna_display))
    return rows, designs


def uncovered_positions(target: str, scan_rows) -> list[int]:
    """Target positions no probe can interrogate under the arm constraint.

    With MIN_ARM matched bases required on each side, positions within MIN_ARM
    of either target end cannot be read without more flanking sequence.
    """
    reachable = {r["interrogated_pos"] for r in scan_rows}
    return [i for i in range(1, len(target) + 1) if i not in reachable]


def to_records(designs) -> list[dict]:
    return [asdict(d) for d in designs]

def cross_check(d: Design, probe_target_id: str, targets: dict,
                min_match_frac: float = 0.70) -> list[dict]:
    """Worst-case match of one probe against every NON-cognate target.

    The skill does not screen a background transcriptome, but within a
    multiplex panel you can and should check the members against each other.
    This slides the probe's base sequence over each other target, counts
    Watson-Crick matches with the blank column excluded, and records which base
    would sit opposite the blank.

    A window is flagged (`fires` = 'YES') only when BOTH conditions hold: it
    matches at or above `min_match_frac`, and the base opposite the blank is
    the cognate base for the probe's SMART reagent - i.e. it would hybridise
    AND the templated chemistry would fire. A good match presenting the wrong
    base opposite the blank costs signal but does not create a false positive,
    which is the specificity advantage of DCL over plain hybridisation.
    """
    bases, L, bpos = d.pna_bases, d.probe_len, d.blank_pos
    cognate = {"G": "CCHO", "C": "GCHO", "T": "ACHO", "A": "TCHO"}
    want = [b for b, rg in cognate.items() if rg == d.smart_reagent][0]
    rows = []
    for tid, seq in targets.items():
        if tid == probe_target_id:
            continue
        t = seq.upper().replace("U", "T")
        if len(t) < L:
            continue
        worst = None
        for s in range(0, len(t) - L + 1):
            win = t[s:s + L]
            col = L - bpos                       # 0-based blank column
            keep = [i for i in range(L) if i != col]
            m = sum(COMP[win[i]] == bases[k] for k, i in enumerate(keep))
            if worst is None or m > worst[0]:
                worst = (m, s + 1, win[col], win)
        m, start, opp, win = worst
        frac = m / (L - 1)
        rows.append(dict(probe_target=probe_target_id, off_target=tid,
                         matches=m, of=L - 1, match_frac=round(frac, 3),
                         window_start=start, window=win,
                         base_opposite_blank=opp, needs=want,
                         fires="YES" if (opp == want and frac >= min_match_frac)
                               else "no"))
    return rows

# ===========================================================================
# gamma-placement YIELD score
# ===========================================================================
# The Design score above ranks SEQUENCE choices (where the blank goes, which
# reagent that forces, Tm, flanks). It says nothing about the backbone
# chemistry. This second, independent score rates the MONOMER PLACEMENT of a
# built DGL probe for its likely effect on reductive-amination yield.
#
# Two of its terms are measured from the structural model, one is a stated
# hypothesis, and three are design-rule encoders. KEEP THAT DISTINCTION: this
# is a design-rule scorer, NOT a calibrated yield predictor. The only
# experimental anchor available is a single ordered pair (DGL-122_4.6 with a
# serine-like blank outperforms _4.3 with a glutamic-like blank), which
# validate_yield_score() checks the ranking reproduces. One data point is not
# a validation set.
#
# GAMMA_OFFSET_GEOMETRY was computed on an 18-mer gamma-template duplex model
# (blank at position 10) by placing a gamma-L-glutamyl side chain at every
# offset, scanning all non-clashing rotamers, and recording (a) the fraction
# reaching the 2.6-3.3 A ion-pair window against the blank's reactive
# secondary amine N4', and (b) the closest approach of any side-chain atom to
# the volume the incoming SMART nucleobase occupies. The result is sharply
# localised rather than graded: ONLY offset +1 can ion-pair (2.2% of rotamers)
# or contact the base site (2.97 A); offset -1 is electrostatically clean but
# sterically close (5.27 A); every |offset| >= 2 is clear on both counts. A
# glutamic-like side chain on the BLANK ITSELF is the worst case (1.89 A,
# ~10% of rotamers in the ion-pair window).
GAMMA_OFFSET_GEOMETRY = {
    -9: (0.000, 17.44), -8: (0.000, 17.79), -7: (0.000, 18.49), -6: (0.000, 18.18),
    -5: (0.000, 17.10), -4: (0.000, 14.91), -3: (0.000, 12.45), -2: (0.000, 9.96),
    -1: (0.000, 5.27),
     1: (0.022, 2.97),   2: (0.000, 6.15),   3: (0.000, 9.45),   4: (0.000, 11.91),
     5: (0.000, 14.02),  6: (0.000, 17.20),  7: (0.000, 18.88),  8: (0.000, 19.70),
}
GAMMA_GEOMETRY_FALLBACK = (0.000, 20.0)      # far offsets: clean

# Blank side chain, scored for the reactive secondary amine it must present.
# Ser: neutral CH2OH, nothing can sequester the amine -> reference.
# aeg: also neutral but contributes no pre-organisation at the cavity.
# GL : anionic carboxylate on the same residue, able to ion-pair with the
#      protonated amine at the pH 6 of the DCL step and lower the free-base
#      fraction that has to attack the aldehyde.
# DAPA: free PRIMARY amine side chain - a better nucleophile than the backbone
#      secondary amine, so it competes for the aldehyde and gives
#      non-templated labelling. Disqualifying for a DCL blank; the catalogue
#      itself lists these monomers "for amine functionalization".
BLANK_YIELD = {"L-Ser": 1.00, "D-Ser": 1.00, "aeg": 0.80,
               "GL": 0.40, "L-DAPA": 0.0, "D-DAPA": 0.0}

YIELD_WEIGHTS = dict(blank=0.30, electrostatic=0.20, steric=0.15,
                     framing=0.15, distribution=0.10, loading=0.10)


def _geo(off):
    return GAMMA_OFFSET_GEOMETRY.get(off, GAMMA_GEOMETRY_FALLBACK)


def yield_score(display: str, gamma, blank_type: str, weights=None) -> dict:
    """Rate a built DGL probe's monomer PLACEMENT for labelling yield.

    display    : PNA N->C with '_' at the blank (as produced by the designer)
    gamma      : iterable of 1-based gamma positions, or a {pos: side} dict
    blank_type : key of BLANK_YIELD

    Returns every component separately plus the total, so the ranking can be
    re-weighted or individual terms ignored. Components marked (measured) come
    from GAMMA_OFFSET_GEOMETRY; the rest encode design rules.
    """
    w = dict(YIELD_WEIGHTS if weights is None else weights)
    L = len(display)
    b = display.index("_") + 1
    g = sorted(int(p) for p in (gamma or {}))
    offs = [p - b for p in g]
    if blank_type not in BLANK_YIELD:
        raise ValueError(f"blank_type must be one of {sorted(BLANK_YIELD)}")

    s_blank = BLANK_YIELD[blank_type]
    # (measured) electrostatic: chance ANY gamma carboxylate can ion-pair with
    # the reactive amine. Independent-rotamer approximation across positions.
    p_free = 1.0
    for o in offs:
        p_free *= (1.0 - _geo(o)[0])
    s_elec = p_free
    # (measured) steric: closest approach of any gamma side chain to the volume
    # the incoming SMART nucleobase must occupy.
    d_site = min([_geo(o)[1] for o in offs], default=20.0)
    s_steric = _plateau(d_site, 2.0, 6.0, 1e3, 1e4)
    # (hypothesis) framing: rigidity where it should matter most is a gamma unit
    # on BOTH sides of the blank, close enough to frame the cavity but outside
    # the +/-1 exclusion. Supported by the observation that a flexible backbone
    # loses templated selectivity, not by a calibration.
    near = [o for o in offs if 2 <= abs(o) <= 4]
    s_frame = (1.0 if any(o < 0 for o in near) and any(o > 0 for o in near)
               else 0.6 if near else 0.2)
    # (design rule) distribution: pre-organisation wants the modifications
    # spread along the duplex, not clustered.
    if len(g) >= 2:
        gaps = [j - i for i, j in zip(g, g[1:])]
        ok = sum(2 <= gp <= 5 for gp in gaps) / len(gaps)
        s_dist = 0.3 + 0.7 * ok
    else:
        s_dist = 0.3
    # (design rule) loading: enough gamma to pre-organise, not so much that
    # charge, cost and synthesis difficulty climb for no further benefit.
    frac = len(g) / max(L - 1, 1)
    s_load = _plateau(frac, 0.0, 0.15, 0.45, 0.80)

    parts = dict(blank=s_blank, electrostatic=s_elec, steric=s_steric,
                 framing=s_frame, distribution=s_dist, loading=s_load)
    total = sum(w[k] * v for k, v in parts.items())
    flags = []
    if blank_type in ("L-DAPA", "D-DAPA"):
        flags.append("DAPA blank presents a competing primary-amine nucleophile "
                     "- not suitable as a DCL reactive site")
    if blank_type == "GL":
        flags.append("glutamic-like blank: carboxylate can ion-pair with the "
                     "reactive amine (~10% of rotamers); a serine-like blank "
                     "removes this")
    for o in offs:
        if o == 1:
            flags.append("gamma at blank+1: only offset that both reaches the "
                         "ion-pair window and contacts the incoming base site")
        elif o == -1:
            flags.append("gamma at blank-1: electrostatically clean but 5.3 A "
                         "from the incoming base site")
    return dict(total=round(total, 4), components={k: round(v, 3) for k, v in parts.items()},
                weighted={k: round(w[k] * v, 4) for k, v in parts.items()},
                blank_pos=b, gamma=g, offsets=offs, d_to_smart_site=d_site,
                flags=flags)


def validate_yield_score() -> None:
    """The one experimental anchor: 4.6 (serine blank) must beat 4.3 (glutamic)."""
    d, g = "CACCATTGT_ACACTCCA", [7, 12, 15]
    a = yield_score(d, g, "L-Ser")["total"]
    b = yield_score(d, g, "GL")["total"]
    assert a > b, (a, b)
    # the +1 exclusion must cost something
    assert yield_score(d, [7, 11, 15], "L-Ser")["total"] < a
    # a DAPA blank must be heavily penalised and flagged
    r = yield_score(d, g, "L-DAPA")
    assert r["components"]["blank"] == 0.0 and r["flags"]



GAMMA_PATTERN = (-3, 2, 5, -6, 8, -9)


def propose_gamma(probe_len: int, blank_pos: int, pattern=None, side="Glu") -> dict:
    """Default gamma placement, as offsets from THIS probe's blank.

    Follows the DGL-122_4.6 layout (blank 10, gamma 7/12/15 = offsets -3/+2/+5)
    and applies the exclusions the structural scan supports: never the blank
    itself and never blank+/-1. Returns {position: side} ready for build_pna.

    Use this rather than a fixed position list when designing across probes of
    different length or blank position - offset 7,12,15 means something quite
    different on a 15-mer with the blank at 8, where position 7 IS blank-1.
    """
    pat = GAMMA_PATTERN if pattern is None else pattern
    out = {}
    for off in pat:
        p = blank_pos + off
        if 1 <= p <= probe_len and abs(off) >= 2:
            out[p] = side
    return dict(sorted(out.items()))
