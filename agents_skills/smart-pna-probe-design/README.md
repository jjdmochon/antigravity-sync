# DestiNA DGL / SMART PNA probe design

Design abasic PNA probes for Dynamic Chemical Labelling against any target
sequence: scan the target for where the blank can go, rank the designs, pick a
panel, compute exact construct and labelled-product masses for the real monomer
chemistry, and build a 3D PNA·DNA duplex model.

Three ways in — **app**, **script**, or **library** — all driving the same
engine, so none of them can drift from the others.

---

## Install

```bash
pip install rdkit biopython numpy scipy
```

Python 3.10+. That is the whole dependency list; the app uses only the standard
library on top of it. No internet is needed except the first time you build a
3D model (the template PDB is fetched once from RCSB and cached).

## 1. The app

```bash
python destina_probe_app.py
```

Opens `http://127.0.0.1:8765` in your browser. Paste a target, choose the
abasic monomer and which positions are γ-modified, press **Design probes**.
You get the scan table, a four-probe panel with masses, CSV downloads, and a
box to weigh and locate an existing probe written in DestiNA notation. It runs
entirely on your machine — nothing is uploaded.

`--port 9000` to change port, `--no-browser` to suppress the tab.
Open `destina_app_example.html` to see what the output looks like first.

## 2. The script

```bash
# scan a mature miRNA
python destina_probe_design.py -t UGGAGUGUGACAAUGGUGUUUG -i miR-122-5p -o out

# chiral DGL probes with a serine-like blank, plus 3D models with real side chains
python destina_probe_design.py -t UGGAGUGUGACAAUGGUGUUUG -i miR-122-5p -o out \
    --blank L-Ser --gamma 7,12,15 --model --sidechains

# weigh and locate an existing probe
python destina_probe_design.py -t UGGAGUGUGACAAUGGUGUUUG \
    --probe "x x C A C C A T Tglu G T *L-Ser* A Cglu A C Tglu C C A"

# a whole FASTA of targets - also writes panel_cross_check.csv
python destina_probe_design.py -f targets.fa -o out
```

With more than one target the run ends with a **multiplex cross-check**: every
probe is slid over every other target and flagged only if it both matches well
*and* presents its cognate base opposite the blank — i.e. would hybridise *and*
fire. A good match with the wrong base opposite the blank costs signal but is
not a false positive; that is the DCL specificity advantage over plain
hybridisation.

Writes per target: `_scan.csv`, `_designs.csv`, `_panel.csv`,
`_P*_mismatch.csv`, `_report.md`, and with `--model` the duplex PDBs.
`--help` lists every option.

## 3. The library

```python
import pna_design as pd_, pna_chem as pc, pna_struct as ps

scan, designs = pd_.scan_target("UGGAGUGUGACAAUGGUGUUUG", "miR-122-5p")
probe = pc.build_probe(pc.REFERENCE_PROBES["DGL-122_4.6"])
pc.masses(probe)                                             # formula, mono, avg
pc.labelled_product(probe, pc.SMART_TAGGED["SMART-C-REX-PEG12-biotin"])
pc.monomer_registry()                                        # 23 catalogue monomers
```

---

## Probe notation

Whitespace-separated monomer codes, read N→C:

| Token | Meaning |
|---|---|
| `x` | Fmoc-AEEA-OH spacer (monomer code X) |
| `A C G T` | achiral aeg monomer |
| `Aglu Cglu Gglu Tglu` | chiral γ-L-glutamyl monomer |
| `Cpeg Tpeg` / `Clys Tlys` | γ-(mini-PEG) / γ-L-Lys monomer |
| `*GL*` | chiral abasic blank, glutamic-like side chain |
| `*L-Ser*` `*D-Ser*` | chiral abasic blank, serine-like side chain |
| `*L-DAPA*` `*D-DAPA*` | chiral abasic blank, aminomethyl side chain |
| `*aeg*` | achiral abasic blank |
| `K` | C-terminal lysine |

`pna_chem.REFERENCE_PROBES` holds the two production miR-122 probes:

```
DGL-122_4.6   x x C A C C A T Tglu G T *L-Ser* A Cglu A C Tglu C C A
DGL-122_4.3   x x C A C C A T Tglu G T *GL*    A Cglu A C Tglu C C A
```

Both are 18-mers with base sequence `CACCATTGT_ACACTCCA`, γ-L-Glu at positions
7/12/15, blank 9th from the C-terminus, reading G9 of mature miR-122 with a
SMART cytosine. _4.6 is the current default. They differ by 42.04 Da (C₂H₂O),
so they are resolvable by MS.

## Self-test

```python
import pna_chem as pc; pc.validate()
```

Checks base-substituent formulas, labelling stoichiometry (product =
probe + reagent − O), the tagged reagent against its catalogue formula, the
γ chiral tags by exact InChIKey identity against the catalogue monomers, and
both reference probes. A scan of mature miR-122 must also recover the published
18-mer probe `CACCATTGT_ACACTCCA` — it lands at rank 6 of 440.

## Two scores

`seq score` rates the **sequence** choice — where the blank goes, which reagent
that forces, Tm, flanks. `yield score` rates the **monomer placement** — the
blank's side chain and the γ positions — for likely labelling yield. They are
independent and must never be added. Two of the yield terms are measured from a
duplex model (can a γ carboxylate ion-pair with the reactive amine; does a side
chain intrude where the incoming SMART base must sit); the rest encode design
rules. Neither is fitted to measured yield. `SKILL.md` has the full breakdown.

Use `--gamma auto`: it places γ by offset from **each probe's own blank**
(−3/+2/+5, never the blank or ±1). A fixed list like `7,12,15` means something
different on a 15-mer whose blank is at 8, where position 7 *is* blank−1.

## Reading the numbers

- **Tm ranks, it does not predict.** Giesen PNA/DNA regression, ±5 K for >90%
  of sequences. An RNA target is folded to DNA; PNA·RNA duplexes are more
  stable and γ modification adds more, so values are conservative for a miRNA.
- **γ stabilisation is not quantified.** `pna_design.GAMMA_TM_OFFSET` is 0.0;
  set it from your own melting data if you want it in the ranking.
- **Use the tagged reagent for mass windows.** SMART C REX PEG12-biotin adds
  **+1020.25 Da**, not the +137.14 of a bare nucleobase aldehyde.
- **Off-target cross-hybridisation is not screened.** That needs the rest of
  the panel plus the background transcriptome.
- **3D models are template-based**, not refined or energy-minimised: good for
  register and cavity geometry, not for affinity. Side-chain torsions are
  chosen by a clash scan, so treat the arms as a plausible projection.

## Files

| File | |
|---|---|
| `destina_probe_app.py` | local web app |
| `destina_probe_design.py` | command-line tool |
| `pna_design.py` | scan, scoring, Tm, mismatch analysis |
| `pna_chem.py` | monomers, constructs, masses, probe notation |
| `pna_struct.py` | PNA·DNA duplex models, γ side chains |
| `destina_monomers.json` | 23-monomer catalogue registry |
| `SKILL.md` | full method notes, caveats and references |
| `kernel.py` | helpers used when loaded as a Claude skill |
| `destina_app_example.html` | rendered example of the app output |
| `example_output/` | example CLI run on miR-122 |
