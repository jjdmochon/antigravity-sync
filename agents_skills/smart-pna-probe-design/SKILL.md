---
name: smart-pna-probe-design
description: "Design DestiNA DGL / SMART PNA probe panels for Dynamic Chemical Labelling (DCL) PCR-free nucleic acid and microRNA detection, and build PNA.DNA duplex structural models. Use when scanning a target miRNA to place an abasic blank monomer; designing or evaluating abasic/blank peptide nucleic acid probes built from achiral aeg or chiral gamma-L-glutamyl (Aglu/Cglu/Gglu/Tglu) monomers with glutamic-like (*GL*) or serine-like (*L-Ser*/*D-Ser*) abasic blanks; choosing which target base to interrogate and which SMART nucleobase aldehyde reagent (GCHO/CCHO/ACHO/TCHO or SMART C REX PEG12-biotin) to use; predicting PNA/DNA duplex Tm; computing probe and labelled-product masses for LC-MS/MALDI QC; or modelling the abasic cavity and the filled product in 3D."
---

# DestiNA DGL / SMART PNA probe design (abasic PNA + Dynamic Chemical Labelling)

Scans a target for blank placement, designs and ranks abasic PNA probes on
achiral aeg or chiral gamma-modified backbones, computes exact construct and
labelled-product masses, and builds template-based PNA.DNA duplex models of the
probe before and after labelling.

## Assay background (verified, not assumed)

- An **abasic aeg-PNA monomer** replaces one nucleobase, leaving a free
  **secondary amine** on the backbone nitrogen N4'. It is placed opposite the
  target base to be read.
- A **SMART nucleobase aldehyde** (`base-CH2-CHO`: GCHO, CCHO, ACHO, TCHO) is
  captured only when it Watson-Crick pairs with the interrogated base. The
  iminium is reduced by NaBH3CN to a stable **tertiary** amine.
- Net mass change of labelling is **probe + reagent - O** (condensation loses
  H2O, reduction returns H2) - asserted in `pna_chem.validate()`.
- The product arm `N4'-CH2-CH2-N9/N1` is **isosteric** with the natural
  `N4'-CO-CH2-N9/N1` arm: three bonds, carbonyl replaced by methylene.

**Register (the thing most easily got backwards).** In the antiparallel
PNA.DNA duplex the PNA N-terminus faces the target **3'** end, so the **PNA
written N->C is the reverse complement of the target written 5'->3'**. The
blank interrogates the target base opposite it. Verified independently on PDB
1NR8, 1PDT and 3PA0; `pna_design.revcomp` encodes it.

## DestiNA DGL probe chemistry (which monomers to use)

Production DGL probes are **chiral**, not plain aeg. The gamma position is the
backbone carbon bonded to the N-terminal amine - verified from the catalogue
monomer SMILES (the stereocentre's neighbours are that amine, one CH2 to the
tertiary nitrogen, and the side chain) and from PDB 3PA0.

| Role | Codes | Side chain at gamma | Notes |
|---|---|---|---|
| Base-bearing, chiral | `Aglu` `Cglu` `Gglu` `Tglu` | gamma-L-glutamyl | pre-organises a right-handed helix, raises affinity, suppresses aggregation; free COOH after cleavage (anionic) |
| Base-bearing, achiral | `A` `C` `G` `T` | none | standard Fmoc aeg monomers |
| Abasic blank, chiral | `*GL*` | glutamic-like (L) | `Boc-gamma-L-Glu-PNA-COOH` |
| Abasic blank, chiral | `*L-Ser*` `*D-Ser*` | serine-like | free CH2OH after cleavage |
| Abasic blank, chiral | `*L-DAPA*` `*D-DAPA*` | CH2NH2 | cationic; for amine functionalisation |
| Abasic blank, achiral | `*aeg*` | none | `Fmoc-Aeg-OH`, unhindered pocket |
| Also available | `Cpeg` `Tpeg` `Clys` `Tlys` | mini-PEG / L-Lys | solubilising / cationic |
| Spacer | `X` | - | Fmoc-AEEA-OH (mini-PEG-2); the `xx-` prefix in DestiNA probe strings |

`pna_chem.monomer_registry()` returns all of these with catalogue name, formula,
MW and protected SMILES (from the DESTINA chemical catalogue v4.0) - use it for
synthesis planning and ordering.

### Probe notation and the production miR-122 probes

Probes are written as whitespace-separated monomer codes, N->C, with `x` for
each AEEA spacer. `pna_chem.parse_probe()` reads this directly and
`build_probe()` builds it:

```python
pc.REFERENCE_PROBES["DGL-122_4.6"]
# 'x x C A C C A T Tglu G T *L-Ser* A Cglu A C Tglu C C A'
probe = pc.build_probe(pc.REFERENCE_PROBES["DGL-122_4.6"])
```

| Probe | Blank | Formula | Avg mass | + tagged reagent |
|---|---|---|---|---|
| **DGL-122_4.6** (current default) | `*L-Ser*` | C212H284N100O65 | 5273.24 | 6293.49 |
| DGL-122_4.3 | `*GL*` | C214H286N100O66 | 5315.28 | 6335.53 |

Both are **18-mers with the same base sequence**, `CACCATTGT_ACACTCCA`, which
is also the sequence of the published abasic miR-122 capture probe: blank 10th
from N / **9th from the C-terminus**, interrogating **G9** of mature miR-122
with a SMART cytosine. They differ only in backbone chemistry - gamma-L-glutamyl
monomers at positions **7, 12 and 15**, and the abasic blank. _4.6 (serine-like
blank) is the current default: it gives the best assay performance. The two
differ by exactly 42.04 Da (C2H2O), so they are resolvable by MS.

**Naming convention:** a blank monomer is named after the amino acid it is made
from, not after the CIP descriptor of the finished monomer. `*L-Ser*` is made
from gamma-L-serine, which is (S) as the free amino acid, but the centre in the
assembled PNA monomer is **(R)** because the substituent priorities change - see
the stereochemistry note below.

Backbone chemistry does **not** change the base-pairing register or which target
base a blank reads, so the sequence scan runs on sequence alone and the monomer
chemistry is applied afterwards in `build_pna(gamma=..., blank_type=...)`.

**Stereochemistry trap (and a known catalogue error).** The CIP descriptor does
not track the L/D label across side-chain families. In the gamma-**Glu** series
L-Glu stays (S): reducing the alpha-COOH to CH2-N leaves it ranked second
(CH2-N is (N,H,H), the other side chain (C,H,H)). In the gamma-**Ser** series it
does not: CH2-OtBu is (O,H,H) and outranks CH2-N, so the middle two priorities
swap and the descriptor inverts with the spatial configuration unchanged -
**gamma-L-Ser is (R)** and **gamma-D-Ser is (S)**.

This is confirmed by DestiNA: the `*L-Ser*` monomer is named for the
gamma-L-serine it is made from, which is (S) as the amino acid, while the centre
in the finished PNA monomer is (R) under CIP.

The consequence for anyone reading the catalogue: the **monomer-code names are
by parent amino acid (correct by convention), but the explicit CIP descriptors
in the `iupac` and `role` text fields of the serine-route entries are stale** -
they repeat the amino acid's (S) for all six L-route entries and (R) for
`*D-Ser*`, instead of the finished monomer's descriptor. Computing CIP from the
catalogue's own SMILES along that route gives Fmoc-L-Ser(tBu)-OH (S) - correct
for L-serine - then (R) for the alcohol, (S) for the aldehyde, and (R) for the
backbone, the PNA-OMe and the `*L-Ser*` blank. The **SMILES are the field to
trust**: they track one unchanging spatial configuration, and a reference
L-serine with its COOH replaced by CH2-NHMe computes as (R), exactly as the
route predicts. The gamma-Glu entries are self-consistent across all fields,
because there the priority order does not swap.

So never infer @/@@ from "L", and do not "correct" the statement above to match
the catalogue's descriptor text. The tags in `pna_chem` are pinned by exact
InChIKey identity to the catalogue **SMILES**, and `validate()` re-checks that
identity on every load.

## Workflow

1. **Scan around the target first.** This is how DGL probes are designed: walk
   the probe window across the whole target at every allowed length and blank
   offset, then look at what each interrogable position can deliver.
   ```python
   res  = pna_scan("UGGAGUGUGACAAUGGUGUUUG", "miR-122-5p")
   scan = res["scan"]            # one row per interrogated position, 5'->3'
   res["unreachable"]            # positions no probe can read (target ends)
   ```
   Each scan row gives the interrogated base, the SMART reagent that position
   forces, how many designs reach it, the Tm spread available there, and the
   best design's window / blank offsets / sequence. Read this before choosing
   where to put the blank.

2. **Pick the panel.** `pna_design_panel(target, id)` returns the ranked
   designs plus one best design per SMART reagent class, so all four target
   bases become readable and each probe is a specificity control for the others.
   Each `Design` carries `pna_display` (N->C, `_` = blank), the target window,
   `blank_pos`, `blank_from_cterm`, `interrogated_pos/base`, `smart_reagent`,
   `tm_pna`, flank lengths, and **every scoring component separately** so the
   ranking can be re-weighted (`pna_design.WEIGHTS`, `REAGENT_TIER`).

3. **Specificity.** `pna_design.flank_mismatch_scan(design, target)` returns the
   Tm penalty for every single-base target mismatch under the footprint,
   excluding the interrogated position.

4. **Build the real chemistry and weigh it.**
   ```python
   pd_, pc, ps = pna_modules()
   probe = pc.build_pna(d.pna_display, gamma="all", gamma_type="Glu",
                        blank_type="GL")        # H-AEEA-AEEA-[gamma-Glu PNA]-Lys-NH2
   pc.masses(probe)
   pc.labelled_product(probe, pc.SMART_TAGGED["SMART-C-REX-PEG12-biotin"])
   ```
   `blank_type` picks the abasic monomer (`GL`, `L-Ser`, `D-Ser`, `L-DAPA`,
   `D-DAPA`, `aeg`); `gamma` is `"all"`, `None`, or a list of 1-based positions.
   **Use `labelled_product` with the reagent you actually run.** The tagged
   production reagent adds **+1020.25 Da** (average) versus +137.14 for bare
   CCHO - a 7.4x difference that will make a MALDI/LC-MS window wrong if you
   quote the untagged increment.

5. **Structural model.**
   ```python
   qc = pna_model_duplex(d, target, out_prefix="P1", pdb_id="3PA0")
   ```
   Writes `P1_abasic.pdb` / `P1_labelled.pdb` and returns geometry QC plus the
   helical parameters. Report it: junction bonds should be 1.600 A (O3'-P) and
   1.330 A (amide C-N), WC H-bonds ~2.6-3.1 A. `.pdb` renders in the Mol*
   viewer. The rigid-body regularisation is a least-squares fit over all base
   pairs: budget ~1-3 min for an 18-mer, and build both states in one cell.

## Scoring — the complete scheme

There are **two independent scores**. Never add them: they answer different
questions and have different standing.

| | `Design.score` | `yield_score()` |
|---|---|---|
| rates | the **sequence** choice: where the blank goes and what that forces | the **monomer placement** on a chosen sequence |
| inputs | target window, blank position, interrogated base | blank side chain, gamma positions |
| decides | which window and blank position to pick | which monomers to build it from |
| standing | screening heuristic, uncalibrated | 2 terms measured from structure, 4 are rules |

### 1. Sequence score — `Design.score`

`score = (sum of w_i * s_i) * self_structure_multiplier`, every `s_i` in 0-1,
weights summing to 1. All components are reported on every Design so the
ranking can be re-weighted (`pna_design.WEIGHTS`).

| component | w | scores 1.0 when |
|---|---|---|
| `reagent` | 0.30 | reads **G** (CCHO, the validated reagent). ACHO 0.70, TCHO 0.60, GCHO 0.55 — `REAGENT_TIER` |
| `central` | 0.20 | blank exactly mid-probe |
| `tm` | 0.20 | Tm in 55-70 C (flat), ramping from 40, down to 85 |
| `arm` | 0.10 | equal matched flanks (7/7 beats 9/5) |
| `fpyr` | 0.10 | pyrimidine fraction 0.35-0.60 (flat) |
| `agg` | 0.10 | no purine tract >5, no G-run >3 |
| `selfstruct` | x | multiplier, bites only on self-complementarity >4 bp |

Three things to know before trusting a ranking:

- **Reagent precedent dominates.** CCHO vs GCHO is 0.135 score units, more than
  any realistic deficit elsewhere combined. In practice the top of any ranking
  is "best G-reading probes"; non-CCHO designs first appear around rank 20-30.
  For reagent diversity use the panel view, which forces one per class.
- **Three terms are plateaus, not gradients.** Anything inside the window
  scores identically, so exact ties are common and the order among them is
  arbitrary. Treat near-ties as a set to choose from on other grounds.
- **`fpyr` partly double-counts `tm`**, which already carries -26.13*f_pyr.
  It is the largest single reason a pyrimidine-rich real probe can rank below
  a blander one.

Runs and self-complementarity are evaluated with the blank as a **break** —
the abasic monomer interrupts a tract and cannot pair, so scoring the
base-only string invents G-runs that do not exist in the molecule.

### 2. Placement yield score — `yield_score(display, gamma, blank_type)`

Rates the backbone chemistry of a built DGL probe for its likely effect on
reductive-amination yield. Returns every component plus flags.

| component | w | source | rationale |
|---|---|---|---|
| `blank` | 0.30 | **measured** | side chain on the blank itself. `L-Ser`/`D-Ser` 1.00, `aeg` 0.80, `GL` 0.40, DAPA **0.0** |
| `electrostatic` | 0.20 | **measured** | chance any gamma carboxylate reaches the ion-pair window at the reactive amine |
| `steric` | 0.15 | **measured** | closest approach of a gamma side chain to the volume the incoming SMART base occupies |
| `framing` | 0.15 | hypothesis | a gamma unit on **both** sides of the blank at offset 2-4 |
| `distribution` | 0.10 | design rule | gamma spread along the duplex (gaps of 2-5), not clustered |
| `loading` | 0.10 | design rule | gamma on 15-45% of residues |

**The measured part.** `GAMMA_OFFSET_GEOMETRY` was computed on an 18-mer
gamma-template duplex by placing a gamma-L-glutamyl side chain at every offset
from the blank, scanning all non-clashing rotamers, and recording how many
reach the 2.6-3.3 A ion-pair window at the blank's reactive secondary amine,
and how close any side-chain atom comes to the incoming SMART nucleobase. The
result is **sharply localised, not graded**:

| position of the carboxylate | closest to amine | ion-pair rotamers | closest to base site |
|---|---|---|---|
| **on the blank itself (`*GL*`)** | 1.89 A | ~10% | — (same residue) |
| blank **+1** | 2.88 A | 2.2% | **2.97 A** |
| blank **-1** | 6.06 A | 0% | 5.27 A |
| every \|offset\| >= 2 | >= 7.7 A | 0% | >= 6.2 A |

So the structural risk is concentrated in exactly two places: the blank's own
side chain, and +1. Everything else is clean, which is why the score does not
try to grade placement smoothly with distance.

**The chemistry behind the `blank` term.** At the pH 6 of the DCL step the
secondary amine must be free base to attack the aldehyde. A carboxylate on the
same residue can form an intramolecular ammonium-carboxylate pair, stabilising
the protonated form and lowering the free-base fraction. A neutral CH2OH
cannot. DAPA blanks score zero and are flagged outright: their free **primary**
amine is a better nucleophile than the backbone secondary amine and competes
for the aldehyde, giving non-templated labelling.

**What this score is not.** It is a design-rule encoder, not a calibrated
predictor; no term is fitted to measured yield. The only experimental anchor is
one ordered pair — _4.6 (serine blank) outperforms _4.3 (glutamic blank) — and
`validate_yield_score()` checks the ranking reproduces it (0.820 vs 1.000,
through the measured `blank` term alone). Note the circularity to avoid: the
`framing`, `distribution` and `loading` windows were drawn around _4.6's own
layout, so _4.6 scoring 1.000 is partly by construction and is **not**
evidence. The two measured terms are independent of it; the three rule terms
are not.

## Design rules encoded

- **Minimum 4 matched flanking bases** each side of the blank (`MIN_ARM`);
  blank centrality is weighted, since published work places the blank towards
  the middle of the probe.
- **Reagent precedent tiers.** CCHO (reads G) is the reagent used in validated
  abasic-PNA DCL miRNA assays and is tiered highest. The others are
  demonstrated in the same dynamic-chemistry framework with less PNA assay
  precedent. `REAGENT_TIER` is a tunable dict - override it with in-house data.
- **Runs and self-complementarity are evaluated with the blank as a break**,
  because the abasic monomer physically interrupts a tract and cannot pair.
  Scoring the base-only string invents G-tracts that do not exist.

## Tm model and its caveats

Giesen et al. (NAR 1998, 26, 5004-5006) empirical regression:
`Tm = 20.79 + 0.83*Tm(DNA/DNA) - 26.13*f_pyr + 0.44*length`, with Tm(DNA/DNA)
from nearest-neighbour **stacks only** (end effects zeroed, as that regression
specifies) and `f_pyr` the pyrimidine **fraction** of the PNA strand.

- Stated accuracy is +/- 5 K for >90% of sequences: **rank with it, do not
  quote it as an absolute prediction.**
- The coefficients were verified against an independent restatement (Metaferia
  et al., PLOS ONE 2013, 8, e58870), which writes the pyrimidine term as a
  *count* - dimensionally impossible (26.13 x 4 = 105 K). It is the fraction.
- Mismatch Tm uses DNA/DNA internal-mismatch parameters scaled by 1.36 for
  PNA.DNA. **Indicative only** - the Giesen regression is matched-duplex only.

## Structural modelling notes

No PNA-aware co-folding model exists (Boltz-2, Chai-1, OpenFold3 cannot treat
an aminoethylglycine backbone as a polymer), so this is **template-based**, on
one of two experimental PNA.DNA duplexes auto-downloaded by `pna_template()`:

| Template | Res. | Modification | Use for | Helix (built model) |
|---|---|---|---|---|
| **3PA0** (default) | 1.60 A | **gamma** - substituent on the carbon bonded to the backbone amine, every residue, C-terminal Lys | gamma-Glu / gamma-Ser DGL probes | 23.7 deg twist, 2.94 A rise, ~15.2 bp/turn |
| **1NR8** | 1.66 A | **alpha** - D-Lys on the carbon bonded to the backbone carbonyl, 3 of 10 residues | achiral aeg probes | 25.2 deg twist, 3.16 A rise, ~14.3 bp/turn |

**Do not mistake 1NR8 for a gamma template.** Its chiral side chain sits at
alpha, not gamma; only 3PA0 carries the substituent at the position DestiNA's
gamma-Glu/gamma-Ser monomers use. 3PA0's PNA chain is numbered **C->N** in the
deposited file (the Lys at residue 1 is the C-terminus, confirmed from
C(i+1)-N(i) amide bonds of 1.29-1.49 A while C(i)-N(i+1) is ~10.5 A); it is
renumbered on load. Its gamma carbon is named `CA` where aeg uses `C2'`, and
the thymine 5-methyl is `C7` where 1NR8 uses `C5M`. Its only adenine is the
5'-terminal DNA residue and so carries no phosphate; P/OP1/OP2 are grafted
from a phosphate-bearing residue by sugar superposition (`donor_unit`).
The 3PA0 models keep the crystal's gamma **methyl** (`C2M`) as a stub marking
where a glutamyl/serinyl chain would project - it is not that side chain.

The abasic cavity comes out the same on either template (6.4-9.1 A from the
blank's secondary amine to the interrogated guanine's WC face on 1NR8,
6.7-9.1 A on 3PA0), so that conclusion is template-independent.

### Building the real gamma side chains

`build_duplex(..., gamma_positions=[...])` keeps the template's gamma **methyl
stub** only where the probe is actually modified - but a methyl is not a
glutamyl chain. To model the real thing:

```python
d_, p_ = ps.build_duplex(tpl, window, display, blank=True, gamma_positions=[7,12,15])
rep = ps.add_gamma_sidechains(d_, p_, [7, 12, 15], blank_pos=10, blank_side="Ser")
ps.gamma_configuration(p_[7][1], "Glu")   # 'S'
ps.gamma_configuration(p_[10][1], "Ser")  # 'R'
```

This grows CB/CG/CD/OE1/OE2 for gamma-Glu and CB/OG for the serine-like blank,
choosing each torsion by the rotamer with the largest minimum contact to the
rest of the duplex, and reports that contact so a strained placement is
visible. The blank's side chain is placed by transferring the gamma vector from
a built gamma residue, so its configuration follows the template rather than
being guessed.

The configuration check is worth running: the crystal's gamma carbon is **(S)**,
which is what an L-amino-acid-derived gamma monomer requires, and from that one
unchanged spatial arrangement the built residues read **(S) for gamma-L-Glu and
(R) for the serine-like blank** - the priority swap described above, reproduced
independently in 3D.

Method, after two measured failures: averaging per-step screw transforms leaves
O3'-P at 3.3 A (the crystal duplex is not regular - its terminal steps are the
worst-fitted); a global helical operator with local base substitution closes
one strand at the other's expense and stretches a WC bond to 4.4 A. What works
is placing a **complete, correctly paired template base pair as a rigid body**
at each position via iterated superposition of the best-fitted interior step,
then a rigid-body regularisation that closes junction bonds while holding each
pair internally rigid. Pairing is therefore exact by construction.

**Template gotcha:** in 1NR8 the chiral D-Lys monomers A66/T66/C66 **swap the
two backbone nitrogen names** relative to aeg monomers - their `N` is the
tertiary amide nitrogen (= aeg `N4'`) and their `N1'` is the N-terminal amine
(= aeg `N`), with `CA` = `C5'`. The rename must be applied simultaneously.
Getting it wrong silently corrupts any geometric statistic over those residues
(it manufactures an impossible 5.12 A three-bond arm span). Handled in
`pna_struct.PNA_ALIAS`.

Model limits: heavy atoms only; the labelled model inherits the template's
amide N4'-C7' length (1.36 A) where the reduced product is an amine (~1.47 A);
AEEA spacers and C-terminal Lys are not modelled. It is a regularised
template model for **register and cavity geometry** - not refined, not
energy-minimised, not an affinity prediction.

## Regression test

A scan of mature miR-122 must **recover the published 18-mer abasic capture
probe** as one of its designs, with every property matching. Run this before
trusting a new panel:

```python
pd_, pc, _ = pna_modules()
pc.validate()                                   # catalogue InChIKeys + stoichiometry
res = pna_scan("UGGAGUGUGACAAUGGUGUUUG", "miR-122-5p")
hit = [d for d in res["designs"] if d.pna_display == "CACCATTGT_ACACTCCA"]
assert len(hit) == 1, "published miR-122 probe not recovered"
d = hit[0]
assert (d.probe_len, d.blank_from_cterm) == (18, 9)
assert (d.interrogated_pos, d.interrogated_base, d.smart_reagent) == (9, "G", "CCHO")
```

It lands at rank 6 of 440 designs (top 1.4%), which is the intended behaviour:
the scan should surface the real probe without being tuned to it - and that
same base sequence is the one both production probes use.

`pc.validate()` additionally re-parses `REFERENCE_PROBES` and asserts the
18-mer sequence, gamma-Glu at 7/12/15, blank 9th from the C-terminus, the two
AEEA spacers, the blank type of each version, and that _4.3 - _4.6 is exactly
C2H2O (42.04 Da).

## Always state with results

- Target provenance, and whether it was read as DNA 5'->3'.
- **RNA targets:** mature miRNA is RNA but the Tm regression is calibrated on
  PNA/DNA. U is folded to T and a PNA/DNA Tm is returned. PNA.RNA duplexes are
  generally more stable, and gamma modification adds further stabilisation, so
  the numbers are conservative for a miRNA target - ranking, not prediction.
- **gamma stabilisation is not quantified here.** `GAMMA_TM_OFFSET` defaults to
  0.0: reported Tm is the unmodified regression value. No stabilisation
  magnitude is asserted; set the offset from your own melting data. A constant
  offset does not reorder designs that are all gamma-modified - it matters only
  when comparing modified with unmodified probes.
- **Off-target cross-hybridisation is not screened** by this skill; it needs
  the rest of the panel plus the background transcriptome.
- **isomiRs.** For a 3'/5'-truncated isomiR, re-run the scan on that isomiR: a
  window pinned near the affected terminus loses flank and may fall below
  `MIN_ARM`. DCL quantification is reported to be insensitive to miR-122
  isomiRs where PCR is not, so a blank placed centrally in a window away from
  the variable terminus is the design that preserves that property.
- Mass windows must use the **tagged** reagent increment (see workflow step 4).

## References

- Giesen U, Kleider W, Berding C, Geiger A, Orum H, Nielsen PE. *Nucleic Acids
  Res* 1998, **26**, 5004-5006. PNA/DNA Tm regression.
- Rissin DM, Lopez-Longarela B, Pernagallo S, Ilyine H, Vliegenthart ADB, Dear
  JW, Diaz-Mochon JJ, Duffy DC. *PLOS ONE* 2017, **12**, e0179669. Abasic PNA
  DCL probe architecture; the 18-mer miR-122 probe used as the regression test.
- Lopez-Longarela B, Morrison EE, Tranter JD, et al. (Dear JW, Diaz-Mochon JJ
  corresponding) *Anal Chem* 2020, 10.1021/acs.analchem.9b05449. Direct
  detection of miR-122 with the DGL-122_4.3 capture probe; LOD 1.32 pM, ROC AUC
  0.98; DCL accurate across miR-122 isomiRs where PCR is not.
- Kanlidere Z, Jochim O, Cal M, Diederichsen U. *Beilstein J Org Chem* 2016,
  **12**, 2136-2144. Nucleobase aldehyde reagent set.
- Metaferia B, Wei JS, Song YK, et al. *PLOS ONE* 2013, **8**, e58870.
  Independent restatement of the Giesen coefficients.
- DESTINA chemical catalogue v4.0 (staff package) - monomer registry source.
- PDB **3PA0** (gamma-PNA.DNA), **1NR8** (alpha-chiral PNA.DNA), **1PDT**
  (aeg PNA.DNA NMR).
