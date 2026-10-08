# DestiNA DGL probe design - miR-122-5p

Target `5'-UGGAGUGUGACAAUGGUGUUUG-3'` (22 nt)

Blank monomer: `*L-Ser*`   gamma: `7,12,15`

**Not interrogable** (within the flank constraint of 4 matched bases each side): positions 1, 2, 3, 4, 19, 20, 21, 22. Extend the target sequence if any of these must be read.


## Scan - what each target position can deliver

| pos | base | reagent | designs | best score | L | window | blank N/C | Tm | Tm range | probe N->C |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | G | CCHO | 10 | 0.8331 | 14 | 1-14 | 10/5 | 53.0 | 36.4-62.1 | `ATTGTCACA_TCCA` |
| 6 | T | ACHO | 19 | 0.7569 | 14 | 1-14 | 9/6 | 53.3 | 32.7-62.3 | `ATTGTCAC_CTCCA` |
| 7 | G | CCHO | 27 | 0.9348 | 14 | 1-14 | 8/7 | 52.9 | 34.0-62.0 | `ATTGTCA_ACTCCA` |
| 8 | T | ACHO | 34 | 0.8529 | 15 | 1-15 | 8/8 | 55.2 | 35.0-62.9 | `CATTGTC_CACTCCA` |
| 9 | G | CCHO | 40 | 0.9875 | 17 | 1-17 | 9/9 | 60.1 | 32.3-62.3 | `ACCATTGT_ACACTCCA` |
| 10 | A | TCHO | 44 | 0.8586 | 15 | 3-17 | 8/8 | 58.2 | 40.2-65.6 | `ACCATTG_CACACTC` |
| 11 | C | GCHO | 46 | 0.8213 | 17 | 3-19 | 9/9 | 58.1 | 27.6-61.4 | `ACACCATT_TCACACTC` |
| 12 | A | TCHO | 46 | 0.88 | 15 | 5-19 | 8/8 | 59.6 | 36.4-64.7 | `ACACCAT_GTCACAC` |
| 13 | A | TCHO | 44 | 0.88 | 15 | 6-20 | 8/8 | 60.4 | 36.4-64.7 | `AACACCA_TGTCACA` |
| 14 | T | ACHO | 40 | 0.91 | 15 | 7-21 | 8/8 | 57.3 | 33.6-63.1 | `AAACACC_TTGTCAC` |
| 15 | G | CCHO | 34 | 1.0 | 15 | 8-22 | 8/8 | 57.1 | 36.8-62.9 | `CAAACAC_ATTGTCA` |
| 16 | G | CCHO | 27 | 0.9559 | 13 | 10-22 | 7/7 | 51.7 | 34.8-62.9 | `CAAACA_CATTGT` |
| 17 | T | ACHO | 19 | 0.8084 | 15 | 8-22 | 6/10 | 57.4 | 38.0-63.2 | `CAAAC_CCATTGTCA` |
| 18 | G | CCHO | 10 | 0.8543 | 15 | 8-22 | 5/11 | 57.1 | 40.3-62.9 | `CAAA_ACCATTGTCA` |

## Panel - one probe per SMART reagent

| probe | reads | reagent | L | window | blank N/C | Tm | seq score | rank | yield score | formula | avg mass | + tagged |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DGL-122_4.6 | G9 | CCHO | 18 | 1-18 | 10/9 | 61.4 | 0.9536 | 6/440 | 1.0 | C212H284N100O65 | 5273.24 | 6293.49 |
| miR-122-5p_P1 | G15 | CCHO | 15 | 8-22 | 8/8 | 57.1 | 1.0 | - | 0.9126 | C182H244N88O54 | 4528.52 | 5548.77 |
| miR-122-5p_P2 | C11 | GCHO | 17 | 3-19 | 9/9 | 58.1 | 0.8213 | - | 1.0 | C201H271N93O62 | 4981.97 | 6002.22 |
| miR-122-5p_P3 | T14 | ACHO | 15 | 7-21 | 8/8 | 57.3 | 0.91 | - | 0.9126 | C181H244N86O55 | 4504.49 | 5524.74 |
| miR-122-5p_P4 | A12 | TCHO | 15 | 5-19 | 8/8 | 59.6 | 0.88 | - | 0.9126 | C180H243N87O54 | 4489.48 | 5509.73 |

Placement flags:

- **miR-122-5p_P1**: gamma at blank-1: electrostatically clean but 5.3 A from the incoming base site
- **miR-122-5p_P3**: gamma at blank-1: electrostatically clean but 5.3 A from the incoming base site
- **miR-122-5p_P4**: gamma at blank-1: electrostatically clean but 5.3 A from the incoming base site

Sequences (N->C, `_` = abasic blank):

- **DGL-122_4.6** `CACCATTGT_ACACTCCA`
- **miR-122-5p_P1** `CAAACAC_ATTGTCA`
- **miR-122-5p_P2** `ACACCATT_TCACACTC`
- **miR-122-5p_P3** `AAACACC_TTGTCAC`
- **miR-122-5p_P4** `ACACCAT_GTCACAC`

## Supplied probe

- **sequence (N->C)**: `CACCATTGT_ACACTCCA`
- **length**: 18-mer
- **gamma positions**: [7, 12, 15]
- **blank**: *L-Ser* at 10 from N / 9 from C
- **formula**: C212H284N100O65
- **monoisotopic / average**: 5270.199 / 5273.24
- **labelled (SMART-C-REX-PEG12-biotin)**: 6293.49 (+1020.25)
- **found in scan**: reads G9 via CCHO, Tm 61.4 C, rank 6/440

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
