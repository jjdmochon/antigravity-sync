"""Exact chemical construction of aeg-PNA probes, SMART nucleobase aldehyde
reagents, and the dynamic-chemical-labelling product, with computed masses.

Backbone: N-(2-aminoethyl)glycine. A residue written N->C is
    -NH-CH2CH2-N(R)-CH2-C(=O)-
where R = C(=O)-CH2-base (methylenecarbonyl arm) for a normal monomer, R = H for
the abasic "blank" monomer (a free secondary amine), and R = CH2-CH2-base for the
labelled product after reductive amination.

The natural arm (N4'-CO-CH2-N9, i.e. the carbonyl carbon is the one bonded to
the backbone nitrogen - verified from PDB 1NR8) and the DCL product arm
(N4'-CH2-CH2-N9) both span three bonds from the backbone nitrogen to the base
nitrogen: the product is isosteric with a natural monomer, with the amide
carbonyl replaced by a methylene. In the product the carbon bonded to N4' is
the former aldehyde carbon of the reagent. GAMMA-MODIFIED (CHIRAL) BACKBONES
---------------------------------
The gamma position is the backbone carbon bonded to the N-terminal amine
(C2' in aeg PDB atom naming; CA in the gamma-PNA structure 3PA0). Numbering the
residue as a pseudo-peptide from its carbonyl: alpha = CH2 next to C=O, then the
tertiary nitrogen, then beta, then gamma next to the backbone NH. A gamma
substituent therefore sits on the carbon written immediately after the residue's
opening N in an N->C fragment:
    -NH-C*H(side)-CH2-N(R)-CH2-C(=O)-
Verified against the DestiNA catalogue monomer SMILES: in every chiral monomer
the stereocentre's neighbours are the backbone amine N, one CH2 leading to the
tertiary nitrogen, and the side chain.

Do NOT confuse this with alpha-modified PNA: PDB 1NR8 (D-Lys chiral PNA.DNA) is
ALPHA-modified - its side chain sits on the carbon bonded to the backbone
carbonyl. PDB 3PA0 is the gamma-modified PNA.DNA structure.

Side-chain stereochemistry is named L / D after the parent amino acid, as the
catalogue names them. Beware: the CIP descriptor does NOT track the L/D label
across side-chain families, because the priority order changes. In the gamma-Glu
series L-Glu gives (S); in the gamma-Ser series L-Ser gives (R) and D-Ser gives
(S) - the side-chain CH2-O outranks the backbone CH2-N, swapping the middle two
priorities. Both facts were computed from the catalogue SMILES. The chiral tags
below (L_TAG / D_TAG) are therefore NOT reasoned from CIP: they were fixed by
exact InChIKey identity against the catalogue's protected monomers, in this
module's N->C fragment write-order (the tag inverts if the write-order changes).
validate() re-checks that identity so the tags cannot silently rot.

Reagent structures (base-CH2-CHO) per Kanlidere Z, Jochim O, Cal M,
Diederichsen U, Beilstein J Org Chem 2016, 12, 2136-2144, Figure 3. The tagged
flagship reagent (SMART C REX PEG12-biotin) and every monomer in
destina_monomers.json come from the DestiNA chemical catalogue v4.0.
"""
import json
import os
import sys

from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

# Nucleobase as a substituent, attached through N9 (purines) / N1 (pyrimidines).
BASE_SUBST = {
    "A": "n1cnc2c(N)ncnc12",
    "G": "n1cnc2c1nc(N)[nH]c2=O",
    "C": "n1ccc(N)nc1=O",
    "T": "n1cc(C)c(=O)[nH]c1=O",
}
# Expected formulas of the N-methyl bases, used to validate BASE_SUBST.
_NMETHYL_REF = {"A": "C6H7N5", "G": "C6H7N5O", "C": "C5H7N3O", "T": "C6H8N2O2"}

# SMART nucleobase aldehydes: base-CH2-CHO (untagged)
SMART_ALDEHYDE = {f"{b}CHO": "O=CC" + s for b, s in BASE_SUBST.items()}

# Tagged production reagent (DestiNA catalogue): N1-formylmethyl cytosine with a
# C5 propylamide-REX arm, monodisperse PEG12 spacer and D-biotin.
SMART_TAGGED = {
    "SMART-C-REX-PEG12-biotin": (
        "Nc1nc(=O)n(CC=O)cc1CCCNC(=O)CCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCC"
        "NC(=O)CCCC[C@@H]1SC[C@@H]2NC(=O)N[C@@H]21"),
}
_SMART_TAGGED_REF = {"SMART-C-REX-PEG12-biotin": ("C46H81N7O17S", 1036.25)}

# Deprotected gamma side chains, as the cleaved probe carries them. The tBu /
# Boc / OtBu groups in the catalogue monomers are removed on TFA cleavage.
GAMMA_SIDE = {
    "Glu":     "CCC(=O)O",        # gamma-glutamyl -> free carboxylate (anionic at pH 7)
    "Ser":     "CO",              # gamma-serinyl -> primary alcohol
    "DAPA":    "CN",              # gamma-diaminopropionyl -> primary amine (cationic)
    "Lys":     "CCCCN",           # gamma-lysyl -> primary amine (cationic)
    "miniPEG": "CCOCCOCCOC",      # gamma-(mini-PEG), methoxy-terminated
}
# SMILES chiral tags in THIS module's N->C fragment write-order. Fixed by exact
# InChIKey identity against the catalogue's protected monomers - not by CIP
# reasoning - and re-checked in validate(). They invert if the write-order does.
L_TAG, D_TAG = "@@", "@"

# Abasic ("blank") monomer catalogue codes -> (gamma side chain, chirality).
BLANK_TYPES = {
    "aeg":      (None, None),     # Fmoc-Aeg-OH, achiral
    "GL":       ("Glu", "L"),     # Boc-gamma-L-Glu-PNA-COOH
    "L-Ser":    ("Ser", "L"),
    "D-Ser":    ("Ser", "D"),
    "L-DAPA":   ("DAPA", "L"),
    "D-DAPA":   ("DAPA", "D"),
}


# Monomer-code suffixes used in DestiNA probe strings -> gamma side chain.
CODE_SUFFIX = {"glu": "Glu", "ser": "Ser", "dapa": "DAPA",
               "lys": "Lys", "peg": "miniPEG"}
SPACER_CODES = {"x"}          # Fmoc-AEEA-OH, monomer code X
CTERM_CODES = {"k": "Lys"}    # C-terminal lysine written explicitly

# Reference production probes, in DestiNA notation. Both share the base
# sequence of the published 18-mer abasic miR-122 capture probe and differ only
# in backbone chemistry: gamma-L-Glu monomers at positions 7, 12 and 15 and the
# abasic blank type. _4.6 (serine-like blank) is the current default - it gives
# the best assay performance.
REFERENCE_PROBES = {
    "DGL-122_4.6": "x x C A C C A T Tglu G T *L-Ser* A Cglu A C Tglu C C A",
    "DGL-122_4.3": "x x C A C C A T Tglu G T *GL* A Cglu A C Tglu C C A",
}
REFERENCE_PROBE_DEFAULT = "DGL-122_4.6"


def parse_probe(spec: str) -> dict:
    """Parse a DestiNA probe string into build_pna() arguments.

    Tokens are whitespace-separated, read N->C:
      x                         Fmoc-AEEA-OH spacer (monomer code X)
      A C G T                   achiral aeg monomer
      Tglu Cglu Aglu Gglu       chiral gamma-L-glutamyl monomer
      Cpeg Tpeg / Clys Tlys     gamma-(mini-PEG) / gamma-L-Lys monomer
      *GL* *L-Ser* *D-Ser*      chiral abasic blank
      *L-DAPA* *D-DAPA* *aeg*   chiral / achiral abasic blank
      K                         C-terminal lysine

    Returns display, gamma (position -> side chain), blank_type, blank_pos,
    nterm and cterm, ready to splat into build_pna(). Positions are 1-based
    over the PNA residues only, spacers excluded, which is how blank_pos is
    quoted in probe names.
    """
    toks = spec.replace("-", " ").split() if "|" in spec else spec.split()
    nterm, cterm, pna = [], [], []
    for t in toks:
        low = t.lower()
        if low in SPACER_CODES:
            (nterm if not pna else cterm).append("AEEA")
        elif low in CTERM_CODES and pna:
            cterm.append(CTERM_CODES[low])
        else:
            pna.append(t)
    display, gamma, blank_type, blank_pos = "", {}, None, None
    for i, t in enumerate(pna, start=1):
        if t.startswith("*") and t.endswith("*"):
            code = t.strip("*")
            key = "aeg" if code.lower() == "aeg" else code
            if key not in BLANK_TYPES:
                raise ValueError(f"unknown blank monomer {t!r}; "
                                 f"known: {sorted(BLANK_TYPES)}")
            display += "_"
            blank_type, blank_pos = key, i
            continue
        base, suffix = t[0].upper(), t[1:].lower()
        if base not in "ACGT":
            raise ValueError(f"unknown monomer token {t!r}")
        display += base
        if suffix:
            if suffix not in CODE_SUFFIX:
                raise ValueError(f"unknown monomer suffix in {t!r}; "
                                 f"known: {sorted(CODE_SUFFIX)}")
            gamma[i] = CODE_SUFFIX[suffix]
    if blank_type is None:
        raise ValueError(f"no abasic blank monomer in probe spec: {spec!r}")
    return dict(display=display, gamma=gamma, blank_type=blank_type,
                blank_pos=blank_pos, blank_from_cterm=len(pna) - blank_pos + 1,
                nterm=tuple(nterm), cterm=tuple(cterm) or ("Lys",),
                n_residues=len(pna))


def build_probe(spec: str, blank_fill: str | None = None, **kw) -> Chem.Mol:
    """Build a construct straight from a DestiNA probe string."""
    p = parse_probe(spec)
    args = dict(display=p["display"], gamma=p["gamma"],
                blank_type=p["blank_type"], nterm=p["nterm"], cterm=p["cterm"])
    args.update(kw)
    return build_pna(blank_fill=blank_fill, **args)


def _tag(chirality) -> str:
    if chirality in (None, "none"):
        return ""
    try:
        return {"L": L_TAG, "D": D_TAG}[chirality]
    except KeyError:
        raise ValueError(f"chirality must be 'L' or 'D', got {chirality!r}")


def monomer_registry(path=None) -> dict:
    """DestiNA monomer/reagent registry (codes, names, formulas, MW, SMILES).

    Sourced from the DESTINA chemical catalogue v4.0 staff package; used for
    synthesis planning and ordering, not by the construct builder.
    """
    if path is None:
        here = os.path.dirname(sys._getframe().f_code.co_filename)
        path = os.path.join(here, "destina_monomers.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)

# Terminal / spacer residues, written N->C as -NH-...-C(=O)-
RESIDUES = {
    "AEEA": "NCCOCCOCC(=O)",          # 8-amino-3,6-dioxaoctanoic acid ("O-linker")
    "Lys":  "N[C@@H](CCCCN)C(=O)",    # L-lysine
    "Gly":  "NCC(=O)",
}

H2O_EXACT, H2O_AVG = 18.010565, 18.015


def _backbone(side=None, chirality=None) -> tuple[str, str]:
    """Return (head, tail) of a residue fragment around the tertiary nitrogen.

    head spans NH -> gamma -> beta and tail is the alpha-CH2 + carbonyl, so a
    residue is head + 'N' + optional-(arm) + tail.
    """
    if side is None:
        return "NCC", "CC(=O)"
    return f"N[C{_tag(chirality)}H]({GAMMA_SIDE[side]})C", "CC(=O)"


def _monomer(base: str, side=None, chirality=None) -> str:
    """Normal PNA monomer bearing `base`; gamma-modified when `side` is given."""
    head, tail = _backbone(side, chirality)
    return f"{head}N(C(=O)C{BASE_SUBST[base]}){tail}"


def _blank(side=None, chirality=None) -> str:
    """Abasic monomer: free secondary amine on the backbone nitrogen."""
    head, tail = _backbone(side, chirality)
    return f"{head}N{tail}"


def _filled(base: str, side=None, chirality=None) -> str:
    """Blank monomer after reductive amination with the `base` aldehyde."""
    head, tail = _backbone(side, chirality)
    return f"{head}N(CC{BASE_SUBST[base]}){tail}"


def build_pna(display: str, nterm=("AEEA", "AEEA"), cterm=("Lys",),
              cap: str = "amide", blank_fill: str | None = None,
              gamma=None, gamma_type: str = "Glu", gamma_chirality: str = "L",
              blank_type: str = "aeg") -> Chem.Mol:
    """Assemble a full PNA construct, achiral or gamma-modified.

    display    : PNA sequence N->C using '_' for the abasic blank monomer.
    nterm      : spacer residues prepended at the N-terminus (free amine).
    cterm      : residues appended after the PNA, before the cap.
    cap        : 'amide' -> C-terminal CONH2; 'acid' -> COOH.
    blank_fill : if given, model the labelled (filled) monomer at the blank.
    gamma      : which base-bearing residues carry a gamma side chain -
                 None/'none' (all achiral aeg), 'all', or an iterable of 1-based
                 positions in `display`. The blank is controlled by blank_type,
                 not by this argument.
    gamma_type : side chain for those residues - any key of GAMMA_SIDE.
    gamma_chirality : 'L' or 'D'.
    blank_type : abasic monomer at '_' - any key of BLANK_TYPES ('GL' and
                 'L-Ser'/'D-Ser' are the DestiNA chiral blanks).
    """
    if blank_type not in BLANK_TYPES:
        raise ValueError(f"blank_type must be one of {sorted(BLANK_TYPES)}")
    if gamma_type not in GAMMA_SIDE:
        raise ValueError(f"gamma_type must be one of {sorted(GAMMA_SIDE)}")
    n = len(display)
    if gamma in (None, "none"):
        gmap = {}
    elif gamma == "all":
        gmap = {p: gamma_type for p in range(1, n + 1)}
    elif isinstance(gamma, dict):
        gmap = {int(p): s for p, s in gamma.items()}
    else:
        gmap = {int(p): gamma_type for p in gamma}
    bad = [p for p in gmap if not 1 <= p <= n]
    if bad:
        raise ValueError(f"gamma positions out of range 1..{n}: {sorted(bad)}")
    unknown = sorted(set(gmap.values()) - set(GAMMA_SIDE))
    if unknown:
        raise ValueError(f"unknown gamma side chain(s) {unknown}; "
                         f"known: {sorted(GAMMA_SIDE)}")
    b_side, b_chir = BLANK_TYPES[blank_type]

    frags = [RESIDUES[r] for r in nterm]
    for i, ch in enumerate(display, start=1):
        if ch == "_":
            frags.append(_filled(blank_fill, b_side, b_chir) if blank_fill
                         else _blank(b_side, b_chir))
        else:
            side = gmap.get(i)
            frags.append(_monomer(ch, side, gamma_chirality if side else None))
    frags += [RESIDUES[r] for r in cterm]
    smi = "".join(frags) + ("N" if cap == "amide" else "O")
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        raise ValueError(f"invalid construct SMILES: {smi}")
    return mol


def masses(mol: Chem.Mol) -> dict:
    return dict(formula=rdMolDescriptors.CalcMolFormula(mol),
                monoisotopic=round(Descriptors.ExactMolWt(mol), 3),
                average=round(Descriptors.MolWt(mol), 2))


def reagent_table(include_tagged: bool = True) -> list[dict]:
    """Untagged nucleobase aldehydes and, by default, the tagged production
    reagent. Mass increments on labelling are reagent mass - O (see
    labelled_product)."""
    comp = {"A": "T", "G": "C", "C": "G", "T": "A"}
    out = []
    for name, smi in SMART_ALDEHYDE.items():
        m = Chem.MolFromSmiles(smi)
        out.append(dict(reagent=name, interrogates=comp[name[0]], tagged=False,
                        smiles=smi, **masses(m)))
    if include_tagged:
        for name, smi in SMART_TAGGED.items():
            m = Chem.MolFromSmiles(smi)
            out.append(dict(reagent=name, interrogates="G", tagged=True,
                            smiles=smi, **masses(m)))
    return out


def labelled_product(probe: Chem.Mol, reagent_smiles: str) -> dict:
    """Mass of the probe after dynamic chemical labelling with `reagent_smiles`.

    Net transformation is probe + reagent - O: condensation to the iminium loses
    H2O, cyanoborohydride reduction returns H2. Works for any reagent, tagged or
    not, so the increment is the one the real (tagged) reagent produces rather
    than a bare-nucleobase estimate.
    """
    reag = Chem.MolFromSmiles(reagent_smiles)
    if reag is None:
        raise ValueError(f"invalid reagent SMILES: {reagent_smiles}")
    O_EXACT, O_AVG = 15.994915, 15.999
    mono = Descriptors.ExactMolWt(probe) + Descriptors.ExactMolWt(reag) - O_EXACT
    avg = Descriptors.MolWt(probe) + Descriptors.MolWt(reag) - O_AVG
    return dict(monoisotopic=round(mono, 3), average=round(avg, 2),
                d_monoisotopic=round(Descriptors.ExactMolWt(reag) - O_EXACT, 3),
                d_average=round(Descriptors.MolWt(reag) - O_AVG, 2))


def validate() -> None:
    """Formula checks on the base substituents and on reaction stoichiometry."""
    for b, ref in _NMETHYL_REF.items():
        m = Chem.MolFromSmiles("C" + BASE_SUBST[b])
        got = rdMolDescriptors.CalcMolFormula(m)
        assert got == ref, f"N-methyl {b}: {got} != {ref}"
    # Labelling = condensation to the iminium (-H2O) followed by hydride
    # reduction (+H2): net product = probe + reagent - O.
    probe = build_pna("TTGAGGG_ACGT")
    prod = build_pna("TTGAGGG_ACGT", blank_fill="C")
    reag = Chem.MolFromSmiles(SMART_ALDEHYDE["CCHO"])
    lhs = (Descriptors.ExactMolWt(probe) + Descriptors.ExactMolWt(reag)
           - H2O_EXACT + 2 * 1.0078250319)
    assert abs(lhs - Descriptors.ExactMolWt(prod)) < 1e-6, (lhs, Descriptors.ExactMolWt(prod))
    # the natural monomer and the labelled monomer differ by exactly O -> H2
    nat = Chem.MolFromSmiles("".join([_monomer("C")]) + "N")
    fil = Chem.MolFromSmiles("".join([_filled("C")]) + "N")
    d = Descriptors.ExactMolWt(nat) - Descriptors.ExactMolWt(fil)
    assert abs(d - (15.994915 - 2 * 1.007825)) < 1e-5, d
    # labelled_product must agree with an explicitly built filled construct
    lp = labelled_product(probe, SMART_ALDEHYDE["CCHO"])
    assert abs(lp["monoisotopic"] - round(Descriptors.ExactMolWt(prod), 3)) < 2e-3, lp
    # tagged reagent matches the catalogue formula / MW
    for name, (formula, mw) in _SMART_TAGGED_REF.items():
        m = Chem.MolFromSmiles(SMART_TAGGED[name])
        got = masses(m)
        assert got["formula"] == formula, f"{name}: {got['formula']} != {formula}"
        assert abs(got["average"] - mw) < 0.5, f"{name}: {got['average']} vs {mw}"
    _validate_gamma_tags()
    _validate_reference_probes()


def _validate_reference_probes() -> None:
    """Both production probes must parse to the published 18-mer base sequence
    with gamma-L-Glu at 7/12/15 and the blank 9th from the C-terminus, and must
    differ by exactly the blank side chain (CH2CH2COOH vs CH2OH = C2H2O)."""
    specs = {k: parse_probe(v) for k, v in REFERENCE_PROBES.items()}
    for name, p in specs.items():
        assert p["display"] == "CACCATTGT_ACACTCCA", (name, p["display"])
        assert p["n_residues"] == 18 and p["blank_from_cterm"] == 9, (name, p)
        assert p["gamma"] == {7: "Glu", 12: "Glu", 15: "Glu"}, (name, p["gamma"])
        assert p["nterm"] == ("AEEA", "AEEA"), (name, p["nterm"])
    assert specs["DGL-122_4.6"]["blank_type"] == "L-Ser"
    assert specs["DGL-122_4.3"]["blank_type"] == "GL"
    m46 = Descriptors.ExactMolWt(build_probe(REFERENCE_PROBES["DGL-122_4.6"]))
    m43 = Descriptors.ExactMolWt(build_probe(REFERENCE_PROBES["DGL-122_4.3"]))
    c2h2o = 2 * 12.0 + 2 * 1.0078250319 + 15.994915
    assert abs((m43 - m46) - c2h2o) < 1e-3, (m43 - m46, c2h2o)


# Protected catalogue monomers, as InChIKeys, keyed by the (side, chirality,
# base) they are built from. base=None means the abasic blank monomer. These
# pin the chiral tags: the fragment builders below must reproduce them exactly.
_CAT_IK = {
    ("Glu", "L", "T"):  "QJZFJLHTIZYHET-NRFANRHFSA-N",   # Fmoc-T-gamma-Glu-OH
    ("Glu", "L", "G"):  "QINXCLKOINLORI-HKBQPEDESA-N",   # Fmoc-Gglu(Bhoc)-OH
    ("Glu", "L", None): "NGQZZZMIOIGBKN-FQEVSTJZSA-N",   # blank *GL*
    ("Ser", "L", None): "LBQVHNGCJVJCAP-LJQANCHMSA-N",   # blank *L-Ser*
    ("Ser", "D", None): "LBQVHNGCJVJCAP-IBGZPJMESA-N",   # blank *D-Ser*
}
_FMOC = "C(=O)OCC1c2ccccc2-c2ccccc21"
_SIDE_PROT = {"Glu": "CCC(=O)OC(C)(C)C", "Ser": "COC(C)(C)C"}
_BASE_PROT = {"T": "n1cc(C)c(=O)[nH]c1=O",
              "G": "n1cnc2c1nc(NC(=O)OC(c3ccccc3)c3ccccc3)[nH]c2=O"}


def _validate_gamma_tags() -> None:
    """Re-derive each catalogue monomer from the fragment builders and require an
    exact InChIKey match, so L_TAG / D_TAG cannot drift from the real compounds.
    """
    from rdkit.Chem import inchi
    for (side, chir, base), ref in _CAT_IK.items():
        tag = _tag(chir)
        head = f"N[C{tag}H]({_SIDE_PROT[side]})C"
        arm = f"(C(=O)C{_BASE_PROT[base]})" if base else "(C(=O)OC(C)(C)C)"
        # Fmoc on the backbone amine, free C-terminal acid: the monomer as sold
        smi = f"N({_FMOC}){head[1:]}N{arm}CC(=O)O"
        m = Chem.MolFromSmiles(smi)
        assert m is not None, smi
        got = inchi.MolToInchiKey(m)
        assert got == ref, (
            f"gamma tag check failed for side={side} chirality={chir} base={base}: "
            f"{got} != {ref} (chiral tags or fragment write-order changed)")
