# An RNA Language Model trained on sequence alone reveals the structural logic of Internal Ribosome Entry Sites

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Table on PDF page 1 (4)](../assets/table/table-p0001-003.jpg)

*Table retained as an image; cells were not reliably transcribed.*

# **SUMMARY**

Millions of RNA sequences are readily available, but the structures that determine their function 16 are not. Picornaviruses initiate translation through Internal Ribosome Entry Sites (IRESes), 17 RNA elements that recruit ribosomes independent of the 5<sup>_′_</sup> cap. These elements are large and 18 highly divergent, and structural understanding remains limited to a handful of cases. We address 19 this bottleneck by introducing an RNA language model (Albatross), trained purely on sequence, 20 that predicts high-quality IRES structures at scale. We collect _in cellulo_ chemical probing data 21 for 96 full-length IRESes from divergent viruses and show that Albatross achieves far higher 22 precision (0.80) than state-of-the-art predictions (0.47). Analyzing 75,000 IRES structures, we 23 discover a novel Type II structural subclass and validate it experimentally. We demonstrate 24 the pipeline broadly generalizes to identify functional structures, including tertiary contacts and 25 alternative riboswitch structures. These findings establish Albatross as a scalable framework 26 that accelerates RNA structure discovery and antiviral targeting. 27

# **KEYWORDS**

[Table on PDF page 1 (8)](../assets/table/table-p0001-007.jpg)

*Table retained as an image; cells were not reliably transcribed.*

# **INTRODUCTION**

RNA structures are known to mediate crucial cellular and viral functions, including translation, 31 transcription, and immune response<sup>1</sup> . Predicting such structures from sequence would enable 32 high-throughput characterization and study of complex host-viral interactions. Such functional 33 RNA structures are highlighted by picornaviruses ( _Picornaviridae_ ), a diverse and widespread 34 family of RNA viruses with historic, ongoing, and emergent global health impacts, particularly 35 among pediatric populations<sup>2–8</sup> . Members of this ubiquitous viral family are capable of infect36 ing a wide variety of tissues, including neural, hepatic, cardiac, gastrointestinal, and respiratory, 37 with outcomes ranging from asymptomatic infections to permanently debilitating diseases<sup>9–13</sup> . In 38

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

66 67

70 71

72 73

76 77

78 79

80 81

82 83 84 85

86 87 88

addition to human disease, picornaviruses infect nearly all known vertebrates, posing a substantial risk of zoonotic spillover<sup>14</sup> . These viruses currently have high pandemic potential<sup>15</sup> but no approved antiviral therapeutics<sup>16</sup> .

Picornaviruses typically encode a single polyprotein from their small ( _∼_ 8 kb), positive-sense RNA genomes, with cap-independent translation initiation driven by large ( _>_ 300 nt) structured RNA elements called Internal Ribosome Entry Sites (IRESes)<sup>9</sup> . IRESes are known to exhibit tissue and host-specific activities, helping determine spillover risk and severity of disease<sup>10,17</sup> . Beyond their biological significance, IRESes have found broad utility in biotechnology, with the EMCV IRES being a standard tool in bioengineering and gene therapy<sup>18–20</sup> . A more global understanding of rules governing IRES structure would provide paths toward improved pandemic readiness and inform the future design of targeted antivirals.

Although individual IRESes have been extensively studied, family-wide rules governing IRES function and tropism remain poorly understood. Massively parallel DNA synthesis enables highthroughput studies of short ( _∼_ 200 nt) IRES fragments, but it cannot yet produce at scale the full-length sequences (400–1500 nt) needed to capture complete IRES structures. As a result, our understanding of full-length IRES architecture and function is largely limited to individual prototypical examples, and most IRES structures remain experimentally unresolved.

Thermodynamics-based RNA folding algorithms perform well on short sequences ( _<_ 100nt) but require experimentally-derived constraints to obtain accurate structures for longer sequences such as IRESes<sup>21–23</sup> . Such models also become computationally intractable when accounting for many unknown nested, higher-order, or long-range interactions<sup>24,25</sup> . Meanwhile, predictive methods using machine learning have suffered from limited availability of high-quality RNA structure training data. Many models perform well on shorter sequences or in specific contexts but quickly fail when asked to extrapolate into new RNA families<sup>23,26–28</sup> .

Covariation analysis remains one of the best approaches for determining high-confidence RNA secondary structures<sup>29–31</sup> . However, these approaches depend on multiple sequence alignments of several closely related sequences with mutated and compensated base pairs to inform the analysis, which are often lacking, especially for highly divergent RNA elements like IRESes.

An additional difficulty in RNA structure analysis arises from the fact that any RNA will thermodynamically fold into some structure. However, it is unclear whether any of these substructures are functional or are simply a consequence of RNA’s tendency to base-pair. Systematic approaches have addressed this by requiring candidate structures to associate with a measured regulatory outcome<sup>32</sup> , which limits discovery to phenotypes that can be assayed at scale.

For this work, we sought to find broad, family-wide patterns in IRES activity and structure. Because precise IRES boundaries are often ill-defined, especially for divergent or understudied viruses, we generally use the term ”IRES” throughout to refer to full picornaviral 5<sup>_′_</sup> UTRs, while acknowledging that not all sequences within these regions necessarily contribute to translation initiation. For example, enteroviruses have a well-characterized cloverleaf structure at the 5<sup>_′_</sup> terminus that is critical for genome replication rather than translation initiation<sup>9,33</sup> .

To address the structural bottleneck, we developed Albatross, an RNA Language Model obtained by continued pretraining of RiNALMo on _∼_ 50,000 IRES sequences using only genomic RNA sequence data and a masked-token prediction objective<sup>34</sup> . Despite receiving no external knowledge of secondary structure, base pairing rules, or thermodynamics, the model learned an encoding of IRES structure from sequence alone<sup>35</sup> . We validated Albatross’s performance on a library of 96 full-length IRESes. Our _in cellulo_ chemical probing data found that IRES structures were consistent across multiple cell types. Albatross independently recapitulated these experimental structures with very high precision, outperforming co-variation analysis (Infernal<sup>30,31</sup> ), machine-learning based structure predictions (eFold<sup>23</sup> ) and purely thermodynamic based models (RNAstructure)<sup>21</sup> .

In parallel, we measured translation driven by all 96 IRESes across six cell types, generating

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

89 90 91 92 93 94 95 96 97 98 99

a comprehensive functional atlas of IRES activity. This revealed that the recently described Type V IRESes drive roughly twice the translational activity of the widely used EMCV IRES, and that many IRESes show significant cell-type-specific activity.

We probed Albatross’s mode of inference and found that it selectively predicts conserved, and thus likely functional structures rather than learning thermodynamics. This behavior allows us to prioritize predicted structures for experimental follow-up. We also generated high-quality structure maps for _∼_ 75,000 IRESes available at `http://www.albatrossrna.org` . The large IRES structural data set allowed us to discover and validate a previously unreported divergent structural subclass of Type II IRES.

Finally, we show that this continued pretraining strategy improves with model size and generalizes beyond IRESes. Applying continued pretraining to hantavirus genome, we recovered known pseudo-circularization interactions; applying it to bacterial riboswtiches we identified conflicting base-pairing dependencies that reflected their two mutually exclusive functional states, that correspond to canonical forms. The model uncovered features such as tertiary contacts, pseudoknots, and alternative conformations, which are notoriously difficult for existing computational tools to predict. We thus propose Albatross approach as a general strategy for structural discovery across RNA biology.

101

102

103

104

105

# **RESULTS**

## **Albatross predicts IRES structure from sequence alone**

Studying IRESes as a comprehensive class remains a challenge, in large part limited by difficulties in accurate high throughput RNA structure measurement or prediction. To address this challenge, we instead sought to extract structure information directly from sequence. This is motivated by the fact that sequenced molecules must have survived evolutionary pressures and so implicitly as an aggregated whole they encode structural and functional constraints.

Recently, da Silva et. al demonstrated that dependency mapping is able to predict secondary structure of functional RNAs ( _e.g._ tRNAs, RNAseP) using an Large Language Model (LLM) trained on sequences alone<sup>35</sup> . LLMs capture relations between tokens (base identity in the case of RNA) in their higher-dimensional encoding. Dependency mapping uses a trained LLM to measure how the prediction of a given nucleotide depends on a single point mutation elsewhere in the sequence, revealing a variety of structural elements. This approach is, in part, motivated by covariation analysis. If a mutation in one base leads to a changed prediction in another base, this indicates base pairing interactions (Figure 1A).

Several pre-trained RNA Language Models exist<sup>34,36,37</sup> . However, these models have been trained on extremely broad and divergent sequences and accordingly, performed poorly in our use case. For example, dependency mapping of the EMCV IRES returned noise (Figure 1B). Nonetheless, they capture some general patterns of RNA sequences internally so we decided to leverage this basis and continue pretraining an RNA Language Model on IRES sequences.

We started from RiNALMo, a 650M-parameter base model pre-trained on 36M non-coding RNA sequences<sup>34</sup> . Rather than training from scratch, we continued pretraining this model on IRES sequences, a transfer learning strategy widely employed in natural language processing and computer vision to adapt pre-trained models to new domains. We collected _∼_ 10,000 picornaviral 5<sup>_′_</sup> UTRs from the NCBI Virus Database<sup>38</sup> . For each, we performed a BLAST alignment against the nt database and collected the top 500 results<sup>39</sup> . After deduplication, this yielded _∼_ 200,000 IRESes for continued pretraining of RiNALMo. Importantly, training was done exclusively on RNA sequences with no explicit information on structure or base pairing rules. We dubbed the resulting model Albatross.

108 109 110 111 112

113

114

115

116

117

118 119

120

121

122

123 124

125

126

127

128

129

130

131

132

133

134

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

Dependency mapping of the EMCV IRES using Albatross revealed antidiagonal dependencies corresponding to stems in the experimentally validated secondary structure (Figure 1C, D)<sup>40,41</sup> .

135 136 137

# **Experimentally derived IRES structures are stable across cell types**

While Albatross was able to predict a well-studied canonical structure, we wanted to test it against an expanded range of ground truth structures. We generated a library of 96 IRESes from a range of hosts and IRES structural types (Figure 2A)<sup>42</sup> . Approximately half of the IRESes come from viruses with human as the primary host, while the rest span vertebrate hosts including amphibians, ungulates, and non-human primates. Each construct consisted of a barcode, IRES, and firefly luciferase. We procured a final mixed RNA library in both linear and circRNA formats.

139 140 141 142 143 144 145

We used DMS-MaPseq to generate experimentally constrained _in vitro_ and _in cellulo_ structure 146 models for our library<sup>43–45</sup> . Our Enterovirus A71, EMCV, and Salivirus models showed high 147 agreement with published structures (Figure 2B)<sup>40</sup> . We found that IRES structure generally 148 exhibited minimal conformational differences between circular and linear topologies and across 149 three cell types, with the biggest differences found between _in cellulo_ and _in vitro_ refolded RNAs 150 (Figure 2C). Given the high concordance between cell types, we proceeded with the HEK293T _in_ 151 _cellulo_ structures as our “ground truth”, where we had sufficient coverage on 95 sequences. We 152 provide DMS-MaPseq constrained structure models for all 95 IRESes at `www.rnandria.org`<sup>23</sup> . 153 The same set of barcoded constructs used to generate this structural ground truth also let us 154 measure IRES translational output, providing a matched dataset for asking how structure relates 155 to function. 156

The same set of barcoded constructs used to generate this structural ground truth also let us measure IRES translational output, providing a matched dataset for asking how structure relates to function.

# **Type V IRES activity doubles that of standard biotech IRESes**

Our IRES library was among the largest reported for full-length IRESes, spanning 365 nt to 1431 nt, in contrast to previous studies that screened _∼_ 200 nt or smaller IRES fragments<sup>46–48</sup> . This provided us an opportunity to create the largest public IRES activity atlas.

IRES activity is traditionally screened for using dual reporter assays. However, these assays are confounded by multiple sources of false positives. The test sequence may harbor cryptic promoters or splice sites that generate monocistronic transcripts of the downstream reporter and translational readthrough ranges from 0.1 to 1.5%<sup>49–52</sup> . The circular architecture of our library overcomes these challenges by containing a single ORF driven by the IRES and no 5<sup>_′_</sup> end.

We used polysome profiling to characterize the activity of our entire library in a single experiment<sup>53</sup> . Our optimized protocol enabled us to consistently recover highly resolved polysome fractions up to heptasomes across a variety of cell types, with high reproducibility across biological and technical replicates (Figure S3).

We profiled IRES activity in a total of six cell lines representing a range of tissues, namely HEK293T (renal), HCT-8 (colorectal), Huh7 (hepatic), N2A (neural murine), SH-SY5Y (neural), and U2OS (osteal) (Figure 2D, S1, S2, S3). The cell lines in these experiments represent a wide range of tissues, most of which are relevant in picornaviral infections. Crucially, this atlas is comprised of identical experimental, collection, and analysis procedures across the cell types ensuring the data is directly comparable and representative of cell type specific effects.

In HEK293Ts IRES activity spanned approximately half an order of magnitude (Figure 2E). Notably, the EMCV IRES, typically used in synthetic constructs and gene therapy designs, exhibited comparatively poor performance (87<sup>th</sup> /96). Surprisingly, the top ten expressing IRESes in HEK293Ts were all Type V, from viruses with either ungulate or canine natural hosts. Type V

157

158 159 160 161 162 163 164 165 166 167 168 169

170 171 172 173 174 175

176 177 178 179

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

is the most recently classified IRES, first identified in 2011, and remains the least studied of the five types, with only a handful of individual members functionally characterized to date<sup>54</sup> .

To confirm that the polysome profiling data corresponded to an alternative method of translational readout we turned to a classic dual luciferase reporter assay (Figure S4). We tested the top two and bottom two performing IRESes, the median performing IRES (Poliovirus 2), and the EMCV IRES. All IRESes corresponded to the rank order from polysome profiling (Figure S4). Beyond rank order the two assays recapitulated relative expression ( _e.g._ Caprine kobovirus 12Q108 had 2.07 ± 0.25 and 2.26 ± 0.25 fold activity compared to EMCV in polysome profiling and dual luciferase respectively).

Type V’s advantage was not limited to HEK293Ts: across the full panel of cell lines, Type V IRESes matched or exceeded the other structural types in our library in every condition tested (Figure 2F, S5), raising the possibility that Type V’s unique architecture leads to higher translational output. On the other hand, Type IV IRESes showed the opposite pattern, consistently ranking lowest across all six cell types (Figure S5).

180 181 182 183 184 185 186 187 188 189 190 191 192 193

# **IRESes exhibit moderate tissue-specific activity**

On a broad scale, the rank order of IRES activity was preserved between cell lines (Figure 2D), consistent with the common translation factors shared across these cell types and the classification of IRESes into a limited number of large-scale structural types that serve as central scaffolds across many hosts and tissues<sup>9</sup> . Nonetheless, IRESes that deviated from such ordering were identifiable in every cell comparison.

We found that 77/96 IRESes displayed significant tropism ( _i.e._ cell type specific activity) (Figure 2G). Using Gini Index (a measure of statistical dispersion) as a measure of effect size, we found 38 of these ( _∼_ 40% of the total) exhibited moderate tropism(Figure 2G). For example, Rhimavirus A had a 1.9 ± 0.1 fold expression (N2A/U2OS) and Seal Picornavirus type 1 had 1.6 ± 0.2 fold expression (293T/U2OS). Whereas, Caprine kobovirus 12Q108 (Type V) had barely any tropism at 1.2 ± 0.2 fold expression (293T/HCT-8).

At the extreme ends of expression within human cells, which matter most for RNA therapeutics<sup>19,47</sup> and viral host barriers<sup>55</sup> , IRES type was the strongest predictor of activity (Figure S5). Yet new picornaviruses are sequenced and deposited much faster than their IRESes can be structurally characterized<sup>38</sup> We wanted to capture the full spectrum of structural diversity within and across types among these sequences. Chemical probing is laborious, slow ,and impractical for thousands of IRESes. The ideal is an equally good approach that is fast and cheap and can accurately predict the structure, and therefore inform the function, directly from sequence.

195 196 197 198 199

200 201

202

203 204 205

206 207

208 209 210 211 212

213 **Albatross predicts diverse IRES structures and complex tertiary contacts**

To test the performance of Albatross on structure prediction from sequence, we used our 95 HEK293T DMS-MaPseq constrained structure models as “ground truth”. While these models are imperfect representations of reality, no other large-scale dataset of full-length IRES structures exists and the current state-of-the-art for mapping full-length IRESes remains chemical probing<sup>40,48,56</sup> . Importantly, all of our models had AUC-ROC values between 0.79-0.93, indicating high agreement between the predicted structures and the underlying DMS reactivity data (Figure S6)<sup>57,58</sup> .

From the dependency maps, we generated explicit structures by applying a binary filter to assign base pairing (Methods). Our filtering did not specify base pairing rules, allowing for noncanonical base pairs. Crucially, Albatross never had access to structural data before or while it made a prediction. All analysis followed from the output dependency maps. Because no

214

215 216 217 218 219

220

221

222 223 224

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

structural information entered training, whether a benchmark sequence appeared in the training set has no bearing on the model’s access to its structure. Sequence overlap between training and evaluation sets therefore does not confound this comparison.

We postulated that a greater training set could improve performance so we developed a larger training set, prioritizing the expansion of small clusters for a total of _∼_ 500,000 sequences. We compared the microF1 over 10 epochs of training (Figure 3A). While the 500k training set performed better than 200k, both rapidly reached a peak microF1 and worsened with longer training. The surprising degradation of performance indicated some form of over-training was occurring. We speculated that with more learning steps Albatross had worse scores through two mechanisms: 1) Albatross over-optimized for the highly represented sequences leading to worse performance on lowly represented sequences; 2) Albatross starts to forget its pretraining as we overtrain on these sequences<sup>59</sup> .

We considered if a smaller but more diverse training set could recapitulate the “ground truth” structures better. We truncated our 500k training set down to _∼_ 50,000 sequences, prioritizing balanced inclusion from each _>_ 70% similarity cluster (Methods)<sup>60</sup> . This smaller library attained a substantially better microF1 than the two larger libraries (Figure 3B). In addition to improved performance, the smaller data set required less training, taking only twelve hours on one GPU. We evaluated F1 for each individual IRES using the best microF1 checkpoint for each training set. F1 scores trended upwards from the 200k to 500k to 50k training sets (Figure 3A). The best structure, for WUHARV Enterovirus 2, a Type I IRES, had an F1 of 0.89.

Across the 95 IRESes, Albatross achieved consistently high precision, with a median of 0.80 and individual structures reaching as high as 1.0 (Figure 3C, S7, Table 1)<sup>40,41,61,62</sup> . This means that when Albatross predicts a base pair, that pair is usually present in the experimental data. We decided to move forward with the 50k Albatross model for the remainder of the paper.

While family wide structures for IRESes are unavailable, specific examples have been well studied. We compared the Albatross predictions to the literature structures of EMCV (Type II), A71 (Type I), and Salivirus (Type V) (Figure 3D, E, S7)<sup>40,41,62,63</sup> . In each case Albatross successfully predicted most stems and crucially did so with few false positive base pairs.

There are no full-length crystal structures of picornaviral IRESes but several fragments have been resolved. We compared the Albatross-derived dependency map of the Coxsackievirus B3 IRES against the recently solved crystal structure of the eIF4G-binding domain V<sup>64</sup> . Albatross correctly predicted 19 of 21 base pair interactions, outperforming the thermodynamics-based RNAstructure algorithm, which successfully identified only 16 interactions (Figure 3F–H). Notably, Albatross independently predicted both a non-canonical A _•_ C pair and an isolated single G _•_ C base pair stabilizing interaction first revealed by the crystal structure (Figure 3G, H). These findings demonstrate the potential for dependency maps to identify base interactions missed by conventional RNA secondary structure prediction approaches.

225 226

227

228 229 230 231 232 233 234 235

236

237

238 239 240 241 242 243 244

245

246 247 248

249 250 251 252

253 254 255 256 257

258 259 260 261

262 **Albatross achieves dramatically higher base-pair precision than state-ofthe-art RNA structure prediction methods** 263

We wanted to compare Albatross with state-of-the-art analysis methods. To that end, we chose Infernal with CaCoFold to represent covariation analysis, eFold to represent machine intelligence methods, and RNAstructure to represent thermodynamic prediction<sup>21,23,30,31</sup> . We also tested using the Albatross predicted base pairs as hard constraints on RNAstructure’s predictions. The “ground truth” data uses DMS reactivity to constrain RNAstructure giving the RNAstructure method an inherent advantage in this comparison. For Infernal, we used Rfam’s curated family alignments and therefore represents the strongest available covariation-derived structure for these families.

264 265 266 267 268 269 270 271

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

We compared F1, precision, and recall for each IRES (Figure 4A–C, Table 2). On F1, Albatross outperforms both Infernal and eFold and was comparable to RNAstructure alone, while Albatross-constrained RNAstructure exceeds every other method (median F1 0.64; Figure 4A). Albatross alone achieved much higher precision than all other methods, with a median of 0.80 against 0.47 for Infernal, 0.44 for eFold, and 0.47 for RNAstructure, and it occupied its own statistical group (Figure 4B). Its recall was not significantly different from that of Infernal or eFold (Figure 4C). All Albatross values use the cross-validated filter threshold (Methods).

These data position Albatross as complementary to thermodynamic prediction rather than as a replacement for it. Thermodynamic models score every possible structure by free energy minimization and return the most stable one, so they recover a larger fraction of the true pairs but also call many pairs the RNA does not form. Albatross calls a smaller set but far more reliably, because it reports only the pairings that are constrained within a given family sequence variation. Combining the two methods therefore captures both strengths: supplying Albatross pairs as hard constraints raises RNAstructure’s median precision from 0.47 to 0.58 and its median F1 from 0.55 to 0.64, with recall rising from 0.66 to 0.73, the highest of any method tested (Figure 4A–C).

272 273 274 275 276 277 278

279 280 281 282 283 284 285 286

**Albatross uses sequence context to complement covariation data in its** 287 **predictions** 288

Given that dependency mapping is conceptually similar to covariation analysis we wanted to know how Albatross was able to correctly predict base pairs that covariation was not. One of the most striking cases was a highly divergent Gallivirus IRES whose GNRA elbow structure aligned to only four sequences in the training data, with a single mutation among them (Figure 4D)<sup>65</sup> . With so few related sequences, covariation analysis is effectively impossible, and accordingly Infernal failed to predict this structure. Yet Albatross predicted it correctly.

If Albatross cannot rely on covariation for the Gallivirus IRES, it must be using a different strategy. We hypothesized that the model had learned to associate specific sequence motifs with structural outcomes, namely that GNRA tetraloops are consistently followed by elbow structures. To test this, we performed dependency mapping on the Gallivirus IRES with mutations in the GNRA motif: substitution to all As, all Cs, or complete deletion (Figure 4E–G, S8). The wild-type sequence produced clear dependencies corresponding to the elbow. Even a conservative GU to AA substitution introduced substantial noise in the GNRA stem, and substitution to CCCC further increased noise that propagated into the second stem of the elbow (Figure 4E, H, S8). Deletion of the GNRA motif eliminated the stem entirely, confirming that both motif identity and spacing drive the prediction (Figure 4E, S8). These results demonstrate that Albatross has learned to associate sequence motifs with structural context, a capability that extends beyond what covariation analysis can access.

289 290 291

292 293 294

295

296 297 298

299

300 301

302

303

304 305

306

# **Thermodynamic stability is not sufficient for structure prediction**

For the Gallivirus mutants, our filtering protocol could still reconstruct the correct structure despite this noise. This led us to investigate the underlying logic used by Albatross to drive its predictions. If Albatross relies on fundamental physical principles ( _e.g._ thermodynamics), it should predict most structural features of the target RNA. If instead, the model predictions are driven by sequence context, its predictions would be focused on common structure features learned from examples in the training set. For that to occur the predicted structures have to be evolutionarily maintained in the training data, which would imply they provide a functional benefit to the virus. Fundamentally, the model’s mode of reasoning changes the interpretation of the predicted signals.

307

308 309

310

311

312

313 314 315 316

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

We trained a smaller, more focused model on _∼_ 8,500 A71 IRES sequences. We identified two equal length regions in the A71 sequence that were predicted as either structured (12-6 hairpin loop) or unstructured by the model and in the literature (Figure 5A, S9). We designed a synthetic sequence that forms a 12 base pair hairpin (by thermodynamics) and did not appear anywhere in the training set (Figure S9). If the model’s predictions are driven by thermodynamics, replacing the unstructured region with the synthetic stem should predict the hairpin. However, no structure was predicted (Figure 5B). The naturally structured region was unaffected.

These data show that the model does not simply apply generalized thermodynamic rules, corroborating the negative data from IRES predictions using the base RiNALMo (Figure 1B). Therefore dependency mapping cannot be broadly used on base models when investigating new RNA classes. Instead, continued pretraining, as in this work, is required.

We then took the same synthetic hairpin sequence and replaced the naturally structured region (Figure 5C). Even though the same sequence was being analyzed, in this context, the model correctly predicts the structure. This supports the premise that Albatross learns structural conservation that depends on sequence context.

Though Albatross does not apply generalized thermodynamic rules in its predictions, we wanted to investigate whether the model understood the physical constraints within its predictions. Earlier, we demonstrated that the model predicts non-canonical base pairs so it is not strictly held to Watson–Crick–Franklin base pairing rules (Figure 3G). However, the predicted A _•_ C pairing in that example is physically possible<sup>64</sup> .

We designed another synthetic sequence of equal length to the hairpin but deliberately unstructured (Figure S9). When replacing the natural hairpin with this sequence, Albatross no longer predicted a stem indicating the model has internalized some physical constraints on pairing (Figure 5D).

These data altogether indicate that thermodynamic stability alone is not sufficient for prediction and dependency maps report spatial and evolutionary coupling rather than base pairing. Albatross identifies nucleotides whose identities constrain one another, which are typically proximal in three-dimensional space, including canonical helices (Figures 1D, 3D, 3E) and non-canonical pairs (Figure 3G).

# **Albatross predicts a subset of base pairs associated with IRES activity**

RNA’s propensity to base-pair generates many stable substructures that are not maintained by selection, and it is difficult to separate them from functional ones. To ask whether the pairs Albatross retains carry functional information, we compared predicted structure content against ribosomal loading in HEK293T cells. The number of Albatross-predicted paired nucleotides per IRES correlated with ribosomal loading (R<sup>2</sup> = 0.19), as did the number of predicted stems (R<sup>2</sup> = 0.20) (Figure 5E, S10A). The same metrics computed on the DMS-MaPseq constrained structures showed little relationship (R<sup>2</sup> = 0.12, 0.10 respectively) (Figure S10B, C), similar to thermodynamic predictions from RNAstructure (R<sup>2</sup> = 0.12, 0.11 respectively) (Figure S10D, E).

Because the dependency map predicted pairs are a subset of those supported by chemical probing, we partitioned each measured structure by whether Albatross recovered the pair. Pairs recovered by Albatross tracked ribosomal loading (R<sup>2</sup> = 0.17), while pairs the model missed did not (R<sup>2</sup> = 0.00) (Figure 5F, G). The correlation is modest, as expected for a coarse metric of structure tested against a single function measured in cultured cells. It is nonetheless specific to the pairs Albatross recovered.

_in cellulo_ chemical probing reports all base pairing an RNA adopts, both elements maintained by selection and pairing that forms because the sequence permits it. In contrast, Albatross selectively predicts structures that are likely to carry function.

317 318 319 320 321 322 323 324 325 326 327

328 329 330 331

332 333 334 335

336

337 338 339 340

341

342 343 344 345

346

347 348 349 350 351 352 353 354 355 356 357

358 359 360

361 362 363

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **Dependency mapping at scale identifies a novel Type II structural subclass**

We then sought to analyze picornaviral IRESes as a class. We ran _∼_ 75,000 unique IRES sequences through Albatross, generating a dependency map for each and manually labeling them by IRES type. These maps and predicted structures are freely available at `www.albatrossrna. org` .

365 366 367

368

We sought to analyze the structure predictions as a collective family of structures. To that end, utilized a modified alignment algorithm on the resulting dependency maps (Methods). In short, each dependency map was transformed, mapping each antidiagonal of the _n x n_ map to a column of a _n x_ (2 _n−_ 1) matrix. An adjusted Needleman–Wunsch algorithm aligns corresponding stems and provides a similarity score (Figure 6A).

369

370 371 372 373

Hierarchical clustering on these alignments naturally groups IRESes by type without prelabeling (Figure 6B). This clustering allowed us to label 10,000s of IRES sequences that were previously labeled largely based on species rather than IRES structure or not previously labeled at all. When comparing to the manual annotation there was substantial agreement (ARI = 0.78), but with the advantage of being done purely computationally.

374 375 376 377 378

Interestingly, within each type we saw subgroupings. We investigated what was driving the subclustering. Many subclusters resulted from Albratross missing a stem, but some of the divergent clusters resulted from _bona fide_ newly predicted structures. One such cluster composed of 107 sequences including chicken Sicinivirus IRESes featuring a novel extended stem. We present Sicinivirus MW684796 as a specific example for follow-up experiments<sup>66</sup> .

379 380 381 382 383

The cluster retained hallmark Type II features including the GNRA-containing Domain I and the eIF4G-binding Domains J-K, with Domain J exhibiting high sequence and structure identity to EMCV (Figure 6C, D). However, the novel group harbored an extended AAG stem in Domain I not present in canonical Type II IRESes (Figure 6C–F).

384 385 386 387 388 389 390

The extended stem contains two conserved AAG motifs, with spacing from the RAAA stem to the first AAG matching that of EMCV, potentially enabling a similar contact with uS19 as recently reported<sup>67</sup> .

We performed DMS-MaPseq on the Sicinivirus MW684796 IRES, which experimentally validated that the IRES folds into the extended AAG stem conformation (Figure 6G–I). Indeed Domain I, containing the extended stem had particularly high chemical signal agreement to the predicted structure (Figure 6I).

We performed DMS-MaPseq on the Sicinivirus MW684796 IRES, which experimentally vali391 dated that the IRES folds into the extended AAG stem conformation (Figure 6G–I). Indeed Do392 main I, containing the extended stem had particularly high chemical signal agreement to the 393 predicted structure (Figure 6I). 394 We investigated the effects of the AAG stem extension on IRES activity. We cloned the 395 Sicinivirus MW684796 IRES into our dual luciferase vector and transfected the construct into 396 UMNSAH/DF1 chicken embryonic fibroblast cells. We also included series of mutants that short397 ened the extended stem. “Estem” replaced the extended AAG stem with the AAG stem from 398 EMCV as a maximally conservative mutant. The _α_ mutant shortened the stem to match the 399 length and spacing of typical Type II architecture. The ∆ mutant deleted the extended AAG stem 400 entirely (Figure 6J). 401 The Sicinivirus MW684796 IRES exhibited low but measurable activity in this cell type as 402 compared to the no IRES control (Figure 6K). Meanwhile, each of the extended AAG stem mu403 tants were indistinguishable from the negative control, implying a feature in the extended stem 404 is important for IRES activity in this subtype(Figure 6K). 405

[Table on PDF page 9 (19)](../assets/table/table-p0009-018.jpg)

*Table retained as an image; cells were not reliably transcribed.*

In natural language processing model size typically correlates with performance and we wanted to investigate if the same pattern applies to dependency analysis of RNA Language Models<sup>68</sup> .

408 409

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

We followed a similar methodology as above on three version of RiNALMo: micro, mega, and giga (33M, 150M, and 650M parameters, respectively). For this experiment, we only trained on _∼_ 38,000, Type I IRES sequences. Similar to natural language processing, when a Type I IRESes, the giga model predicted more stems correctly (Figure 7A).

We tested the the Type I only models against Type II and Type V IRESes in our “ground truth” data. Model size correlated with improved F1 score, regardless of the IRES type (Figure 7A). This implies the larger models are able to better capture general rules that apply across IRES types.

Together these suggest a larger model could lead to more accurate and generalizable predictions of the secondary structure. Accordingly, this presents a strong argument for training larger models in future works.

410 411 412 413

414 415 416 417 418 419 420

# 421 **Continued pretraining of RNA language models enables structure prediction of diverse RNA families** 422

In this work we showed that continued pretraining of an RNA language model on IRES sequences led to structure prediction with very high precision. However, we wanted to test if this approach generalizes to other RNA families.

In this work we showed that continued pretraining of an RNA language model on IRES se423 quences led to structure prediction with very high precision. However, we wanted to test if this 424 approach generalizes to other RNA families. 425 In the midst of the 2026 hantavirus outbreak, turned our approach toward the novel strain<sup>69</sup> . 426 Hantavirus genomes consist of three pseudo-circularized segments (L, M, S), each coated by 427 the nucleoprotein for the majority of the life cycle (Figure 7B)<sup>70</sup> . 428 We continued pretraining a model on 5041 concatenated 5<sup>_′_</sup> +3<sup>_′_</sup> UTRs drawn from S, M, and 429 L segments across Orthohantavirus (Figure 7B)<sup>38</sup> . The resulting predictions on the novel strain 430 correctly identified the long-range pseudo-circularization (Figure 7C). The model did not pre431 dict any additional structure, which is in line with the fact that hantaviruses RNA is coated by 432 nucleoprotein for the majority of the life cycle and thus unable to for complex structure<sup>70</sup> . 433 Branching out beyond viral RNAs, we turned to bacterial riboswitches, RNAs that change 434 structure in response to metabolites to control gene expression (Figure 7D)<sup>71</sup> . This family has 435 the added complexity of inherently having two mutually exclusive functional states with conflicting 436 base-pairing interactions. 437

We continued pretraining a model on 76,829 bacterial riboswitches spanning ten ligand 438 classes, extending each aptamer 150 nt into its downstream expression platform<sup>31,72,73</sup> . The 439 model recapitulated the canonical structure of the _B. subtilis_ adenine riboswitch and predicted 440 correct structures for other adenine riboswitches and for glycine riboswitches (Figure 7D, E, 441 S11)<sup>74,75</sup> . Within a single map, it assigned individual nucleotides two mutually exclusive pairing 442 partners that correspond to the apo and holo conformations. The model received no ligand, no 443 structural label, and no indication that these RNAs adopt more than one state, and recovered the 444 conformational switch from sequence alone. The same map also contained the L2–L3 kissing445 loop interaction, the tertiary contact that holds P2 and P3 in parallel across the purine riboswitch 446 family<sup>76</sup> (Figure 7E). 447

Dependency maps are therefore not restricted to a single nested structure per sequence. They report the set of constraints an RNA is under, including cases where one nucleotide is held by two partners in two functional states, which positions this approach for discovery of RNAs whose function depends on conformational change rather than on a fixed fold.

Importantly, none of these structure features could be captured by base RiNALMo model. The Albatross strategy allows discovery of conserved structures across kingdoms of life using sequence-only continuous pretraining.

448 449 450 451

452 453 454

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **DISCUSSION**

This work aimed to study picornaviral IRESes as a comprehensive family rather than as individual RNAs. In doing so, we generated large-scale functisonal (96 IRESes across 6 cell types) and structural ( _∼_ 75,000 dependency maps) atlases. These data are available in Supplementary Data S1 and at `www.albatrossrna.org` , respectively. Comparable cell-type-resolved activity measurements have been made for cellular 5<sup>_′_</sup> and 3<sup>_′_</sup> UTRs and used to design untranslated regions with tailored cell-type specificity<sup>77</sup> ; our atlas provides the equivalent resource for full-length viral IRESes.

A recent study examining IRES context effects corroborates our activity rankings in overlapping cell types<sup>48</sup> . Across our atlas, Type V IRESes consistently showed strong activity in all cell types tested, and most IRESes exhibited significant tissue tropism. The strongest acting of these came from animal hosts, potentially because the human cells lack antiviral response mechanisms optimized by coevolution to suppress the activity.

456 457 458 459 460 461 462

463 464 465 466 467

The structure of the Type V eIF4G-binding domain offers a possible explanation for its activ468 ity. This domain is distinct from Type I and Type II in its overall architecture, but its apex carries 469 a motif resembling the Type II eIF4G-contacting element alongside a GNRA tetraloop shared 470 with domain V of the Type I Coxsackievirus B3 IRES<sup>54,61</sup> , the domain we compare against a 471 crystal structure in Figure 3F–H. Combining elements of both other eIF4G-dependent classes 472 may support more robust engagement of the initiation machinery, which would fit activity that 473 holds across tissues rather than peaking in one. Type IV IRESes sit at the opposite end, ranking 474 lowest in every cell type we profiled. These elements bind the 40S subunit directly, bypassing 475 eIF4G and recruiting no ITAFs<sup>78</sup> , a comparatively minimal mechanism that may cap their output 476 in this context. Distinguishing either explanation from alternatives requires mutating the indi477 vidual motifs, as we did for the extended AAG stem in Sicinivirus MW684796, and measuring 478 activity across far more IRESes than the 96 profiled here. 479

Using dependency mapping, we generated 75,000 IRES structural maps. Albatross was trained on sequence alone, given no knowledge of structure or thermodynamics, yet predicted base pairs with high precision, outperforming state-of-the-art methods by median precision and F1, with comparable recall. Notably, the Infernal combines curated covariation with folding grammar<sup>79,80</sup> , itself trained on thousands of known RNA structures, whereas Albatross received no structural information of any kind. This advantage likely stems from covariation analysis yielding a single consensus structure per family, which is then mapped onto the query sequence. Dependency mapping instead predicts a structure for each individual sequence, capturing features that a family consensus cannot represent. Divergence remains a constraint on covariation approaches, since a family must first be recognized and populated with enough homologs to model as illustrated by the Gallivirus IRES. Albatross requires no family assignment or homolog set, making it applicable to divergent sequences that covariation methods cannot reach.

Crucially, through multiple experiments, we demonstrate that the Albatross dependency mapping approach learns generalized patterns that it then can apply to divergent but related contexts (Figure 4D–G, 5, 7A). Furthermore, this approach has high precision and preferentially predicts structures using sequence context (Figure 3A–C, 5, Table 2). These properties are particularly useful in comparison to pure thermodynamic models as the Albatross predicted stems are more likely to have functional significance.

A fraction of ”false positive” pairs are due to the model extending a predicted stem through what the canonical structure marks as a bulge( Figure S11) because the dependency map shows a clear coupling between the two bases that would otherwise sit unpaired across from each other ( _e.g_ A _•_ C). A thermodynamic model will not pair these, which suggests that Albatross reports on the spatial coupling between nucleotides proximal in three-dimensional space.

480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497

498 499 500 501 502

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

The Albatross approach toward RNA structure prediction has the additional strength of depending only on sequence data. As compared to high-quality RNA structure data, sequences are orders of magnitude more readily available or obtainable. For example, while only a handful of IRES structures have been experimentally resolved, Albatross generated _>_ 75,000, enabling comparison at scale.

503 504 505 506 507

In analyzing the bulk data, using a new structure clustering method, we discover a previously unreported subclass of IRESes with an extended AAG stem. We experimentally confirm the extension and find it is enhances IRES activity in the context of this subclass (Figure 6G–K).

In analyzing the bulk data, using a new structure clustering method, we discover a previously 508 unreported subclass of IRESes with an extended AAG stem. We experimentally confirm the 509 extension and find it is enhances IRES activity in the context of this subclass (Figure 6G–K). 510 Overall, we provide a family-scale analysis of IRESes through multiple high-throughput av511 enues. Our functional data can be applied to biotechnology and infectious disease research 512 investigating picornaviral tropism. Meanwhile, we establish continued pretraining of RNA lan513 guage models with dependency mapping as a viable approach for high-throughput structural 514 analysis of diverse RNA families (Figure 7B–E). 515 Our work demonstrates that information on functional RNA structure is contained and can 516 be learned from sequences alone. This likely comes from selective pressure that gave raise 517 to the particular arrangement of nucleotides, which survived millions of years of evolution. The 518 approach we develop does not recognize all stable structures but very specific conserved ones, 519 which makes this analysis broadly applicable for discovery of functional RNA structures and 520 structure switches across multiple kingdoms of life. 521

# **Limitations of the study**

This study focused picornaviral IRESes and did not include IRESes or similar non-canonical translation elements from other sources. Type III IRESes are relatively homogeneous in sequence and can be more easily mapped to the canonical structure. Nonetheless our ground truth structure data set lacked Type IIIs so we do not test model performance on this type. Albatross’s high precision is offset slightly by a lower recall. Though this is a useful feature for constricting the search space for functional structures, it also means some substructures are likely missed in any given prediction. The Sicinivirus MW684796 IRES was tested in an easily accessible and transfectable gallinaceous cell type where it exhibited weak activity. Future follow ups on the mechanisms employed by the extended stem will need to evaluate other cell types to better assess the IRES function. Finally, we use a generous definition of IRES throughout for what is more precisely a “picornaviral 5<sup>_′_</sup> UTR”.

522

523 524 525

526 527 528 529 530 531 532 533

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **RESOURCE AVAILABILITY**

[Table on PDF page 13 (4)](../assets/table/table-p0013-003.csv)

| **Lead contact** | 535 |
| --- | --- |
| Requests for further information and resources should be directed to and will be fulfilled by the<br>lead contact, Silvi Rouskin (silvi@hms.harvard.edu). | 536<br>537 |
| **Materials availability** | 538 |
| Plasmids generated in this study are available upon request from the lead contact. | 539 |
| **Data and code availability** | 540 |
| • DMS-MaPseq and polysome profiling sequencing data have been deposited at GEO and<br>are publicly available as of the date of publication under accession number GEO: GSE34725<br>(DMS-MaPseq) and GSE347508 (poysome profiling). Albatross dependency maps for ap-<br>proximately 75,000 IRESes are available at`https://albatrossrna.org`, and DMS-MaPseq<br>derived structure models are available at`https://www.rnandria.org`.<br>• All original code used for training is available at`https://github.com/rouskinlab/albatros`<br>• Albatross model weights, and the sequence datasets are archived at Zenodo: `https://`<br>`doi.org/10.5281/zenodo.22920917`.<br>• Any additional information required to reanalyze the data reported in this paper is available<br>from the lead contact upon request. | 541<br>5542<br>543<br>544<br>545<br>`s`546<br>547<br>548<br>549<br>550 |
| **ACKNOWLEDGMENTS** | 551 |
| We thank Julien Gagneur for providing insight and suggestions for applying dependency map-<br>ping to a new context. We further thank M´elissa L´eger-Abraham for allowing us to use the gra-<br>dient station in her lab. Additionally, we thank Olivier Pourqui´e for providing the UMNSAH/DF1<br>cells.<br>A. S. was partially supported by the National Institute of Allergy and Infectious Diseases<br>Training Grant NIHT21AI007245-40. A. S. and P. B. were partially supported by the Giovanni<br>Armenise Foundation. This research was supported by the the Giovanni Armenise Foundation,<br>Massachusetts Consortium on Pathogen Readiness, Massachusetts Life Sciences Center, and<br>the Advanced Research Projects Agency for Health. | 552<br>553<br>554<br>555<br>556<br>557<br>558<br>559<br>560 |

[Table on PDF page 13 (5)](../assets/table/table-p0013-004.csv)

| **AUTHOR CONTRIBUTIONS** | 561 |
| --- | --- |
| Conceptualization: A.S., R.A.W, N.B., S.R. Data Curation: A.S., P.B., G.Y., A.I. Formal Analysis: | 562 |
| A.S., P.B., A.I. Funding Acquisition: A.S., S.R. Investigation: A.S., P.B., G.Y., A.I., S.R. Methodol- | 563 |
| ogy: A.S., P.B., J.R. R.A.W., S.R. Project Administration: A.S., S.R. Resources: A.S., P.B., G.Y., | 564 |
| R.A.W Software: A.S., P.B. Supervision: S.R. Validation: A.S., P.B., G.Y. Visualization: A.S., P.B. | 565 |
| G.Y. Writing – Original Draft: A.S., P.B., G.Y., S.R. Writing – Review & Editing: A.I., J.R., R.A.W.,<br>N.B. | 566<br>567 |

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

**DECLARATION OF INTERESTS** 568 R.A.W. is an inventor on patents and patent applications relating to circular RNA compositions 569 and methods, including those cited in this work. The rest of the authors declare no competing 570 interests. 571

[Table on PDF page 14 (3)](../assets/table/table-p0014-002.csv)

| **DECLARATION OF GENERATIVE AI AND AI-ASSISTED TECH-** | 572 |
| --- | --- |
| **NOLOGIES** | 573 |
| The authors did not use generative AI for writing initial draft but AI tools were used for grammar,<br>flow editing, condensing word count, and catching errors within the text. Tools including Claude<br>and Codex, were also used for assistance in coding. The authors reviewed the code to ensure<br>that it was accurate. | 574<br>575<br>576<br>577 |

[Table on PDF page 14 (4)](../assets/table/table-p0014-003.jpg)

*Table retained as an image; cells were not reliably transcribed.*

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 15 (3)](../assets/figure/figure-p0015-002.jpg)

Figure 1: **Albatross predicts IRES secondary structure from sequence alone.** ( **A** ) Schematic of the dependency mapping approach. IRES sequences are used for continued pretraining of an RNA language model. For each position, the effect of every possible point mutation on nucleotide predictions is measured, generating a dependency map from which structure is inferred. ( **B** ) Dependency map of the EMCV IRES using the pre-trained model (before additional continued pretraining), showing no discernible structural signal. ( **C** ) Dependency map of the EMCV IRES after four epochs of continued pretraining. Antidiagonal features (dashed boxes) correspond to base-paired stems. ( **D** ) Albatross-predicted structure of the EMCV IRES overlaid on the experimentally validated secondary structure. Colors of the stems correspond to colored squares in C. Inset shows the dependency map for a stem region with corresponding sequence.

# **MAIN FIGURE TITLES AND LEGENDS**

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 16 (2)](../assets/figure/figure-p0016-001.jpg)

Figure 2: **Experimental structure-function altas of 96 IRESes.** ( **A** ) Library composition by host (outer) and IRES type (inner). ( **B** ) DMS-MaPseq predicted structure in HEK293T cells AUC-ROC for three ground truth literature IRES structures. ( **C** ) Pearson R/Construct between DMS-MaPseq experimental replicates and conditions. circRNA and linearRNA refer to the in vitro probed library; labels naming a cell type refer to the same library probed in cells. ( **D** ) Heatmap of ribosomes/RNA for all 96 IRESes across six cell types, with hierarchical clustering. Color scale indicates ribosomes/RNA. (n = 4/cell type). ( **E** ) IRES activity (ribosomes/RNA) ranked across 96 IRESes in HEK293T cells. Select IRESes are labeled. EMCV activity relative to the top-performing Caprine kobuvirus 12Q108 is indicated. _p_ -values from Student’s t-test, n = 4 replicates. ( **F** ) Ribosomes/RNA grouped by IRES structural type. _p_ -values from Kruskal-Wallis H test with Dunn post-hoc analysis and Bonferroni correction, n = 4 replicates. ( **G** ) Tropism significance (p-value) versus effect size (Gini Index) for each IRES. Dashed line indicates significance threshold after Bonferroni correction. 38 IRESes with moderate to strong tropism. _p_ -values from ANOVA.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 17 (2)](../assets/figure/figure-p0017-001.jpg)

Figure 3: **Albatross predicts IRES structure with high precision.** ( **A** ) MicroF1 over training steps for the 200k, 500k, and 50k training sets. Dashed line, pre-trained baseline. ( **B** ) F1 score per structure across training sets. ( **C** ) Precision per structure across training sets. ( **D, E** ) Representative IRES secondary structures for EMCV (Type II) and Enterovirus A71 (Type I). Base pairs predicted by Albatross that agree with the consensus literature structures are colored as true positives (green), while Albatross predictions absent from the consensus literature structures are colored as false positives (pink). ( **F** ) Albatross dependency map of the Coxsackievirus B3 eIF4G-binding Domain V. ( **G** ) Albatross-predicted base pairs compared to the crystal structure, with predicted interactions in black and missed interactions in red. Albatross correctly identifies (I) a non-canonical A _•_ C pair and (II) an isolated single G _•_ C stabilizing interaction. ( **H** ) RNAstructure Fold thermodynamic prediction for the same region.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 18 (2)](../assets/figure/figure-p0018-001.jpg)

Figure 4: **Albatross outperforms state-of-the-art prediction methods on IRESes.** ( **A** ) Violin plots comparing per-structure F1 scores between Albatross, Infernal, eFold, RNAstructure, and Albatross constraining RNAstructure predictions ( _p_ = 1 _._ 20 _×_ 10<sup>_−_14</sup> by Welch’s ANOVA, grouped by Dunn Post-Hoc Test with Holm method adjustment, n = 95 IRESes). ( **B** ) Violin plots comparing per-structure precision between Albatross, Infernal, eFold, RNAstructure, and Albatross constraining RNAstructure predictions ( _p_ = 1 _._ 21 _×_ 10<sup>_−_26</sup> by Welch’s ANOVA, grouped by Dunn Post-Hoc Test with Holm method adjustment, n = 95 IRESes). ( **C** ) Violin plots comparing perstructure recall between Albatross, Infernal, eFold, RNAstructure, and Albatross constraining RNAstructure predictions ( _p_ = 5 _._ 74 _×_ 10<sup>_−_24</sup> by Welch’s ANOVA, grouped by Dunn Post-Hoc Test with Holm method adjustment, n = 95 IRESes). ( **D** ) Per-IRES comparison of precision, colored as in ( **B** ): Albatross scored higher for 87 IRESes, Infernal for 4. ( **D** ) BLAST alignment of the Gallivirus Pf-CHK1/GV GNRA tetraloop region (bold) against the Albatross training set. Only four related sequences exist, with the divergent nucleotide in each marked in red. ( **E** ) Signal-to-noise ratio of the GNRA stem signal in dependency maps of the Gallivirus IRES bearing different tetraloop sequences: aGNRA (AAAA), cGNRA (CCCC), ∆GNRA (loop deleted), and wild-type GNRA (GUAA). ( **F,G** ) Dependency maps of the Gallivirus IRES with the wild-type GNRA tetraloop (GUAA, **G** ) or the CCCC substitution ( **H** ).

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 19 (2)](../assets/figure/figure-p0019-001.jpg)

Figure 5: **Albatross predicts a context-dependent subset of base pairs that is associated with IRES activity.** ( **A–D** ) Dependency maps for the natively unstructured (left) and natively structured (right) region of the A71 IRES; central schematic highlights both regions and the secondary structure. Synthetic sequences shown in Figure S9. ( **A** ) Native A71. ( **B** ) A thermodynamically stable synthetic stem (green) in the unstructured region: no dependency map signal. ( **C** ) The same stem in the structured region: dependency signal observed. ( **D** ) A synthetic sequence of low thermodynamic stability (orange) in the structured region: no signal. ( **E** ) Albatross-predicted paired nucleotides per IRES versus ribosomal loading in HEK293T cells. ( **F, G** ) DMS-MaPseq pairs recovered by Albatross ( **F** ) and missed by Albatross ( **G** ), against ribosomal loading. Red line, linear fit; _R_<sup>2</sup> and error bars, SD of n = 4.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 20 (2)](../assets/figure/figure-p0020-001.jpg)

Figure 6: **Structural clustering across a large IRES dataset reveals an extended stem in a Type II subclass.** ( **A** ) Schematic of the dependency-map alignment procedure: predicted structures (left) are aligned to one another with gaps inserted as needed (middle), yielding pairwise similarity scores (right) used for hierarchical clustering. ( **B** ) Hierarchical clustering of alignment similarity scores across _∼_ 75,000 predicted IRES structures. Colored bars below the matrix show post-hoc manual type labels not available to the unsupervised clustering(Type I, teal; Type II, pink; Type V, purple), demonstrating strong agreeement. ( **C** ) Dependency map of the Sicinivirus MW684796 IRES, with the GNRA stem (magenta), RAAA stem (gold), and extended AAG stem (red) boxed. ( **D** ) Secondary structure of the Sicinivirus MW684796 IRES Domain I, with the same three stems highlighted. Red circles mark the two conserved AAG motifs within the extended stem. ( **E** ) Dependency map of the canonical Type II EMCV IRES, boxed as in ( **C** ) for comparison. ( **F** ) Secondary structure of the EMCV IRES Domain I, highlighted as in ( **D** ). EMCV contains a single AAG motif rather than the extended, two-motif stem seen in Sicinivirus MW684796. ( **G** ) DMS-MaPseq validation of the Albatross-predicted Sicinivirus MW684796 IRES structure. Nucleotides are colored by DMS reactivity (scale in **H** ); agreement between predicted base-pairing and reactivity across the full IRES is AUC-ROC = 0.926. Boxed region is enlarged in ( **H** ). ( **H** ) Enlarged view of the boxed Domain I region in ( **G** ). Red-outlined nucleotides mark the two conserved AAG motifs within the extended stem. ( **I** ) DMS mutation rate (bars, left axis) and rolling-window AUC-ROC (green line, right axis) across the Sicinivirus MW684796 IRES. Shaded regions mark the GNRA (pink), RAAA (gold), and extended AAG (red) stems as in ( **C–F** ); black bars below indicate the annotated Domain I and Domains J-K regions. ( **J** ) Visual summary of Sicinivirus MW684796 mutants screened in dual luciferase assay. ( **K** ) Dual luciferase assay of Sicinivirus MW684796 mutants in UMNSAH/DF1 cells. _p_ -values from Welch’s ANOVA with Dunn Post-Hoc Test with Holm method adjustment.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 21 (2)](../assets/figure/figure-p0021-001.jpg)

Figure 7: **Generalizability of Albatross across RNA families.** ( **A** ) Relative macro-F1 versus the micro model. One checkpoint was selected per model size by macro-F1 on Type I, II, and V. ( **B** ) Hantavirus virion schematic: the three genomic segments (L, M, S), coated by nucleocapsid protein (blue) and pseudo-circularized, packaged within the envelope glycoprotein lattice. Training input: hantavirus L segment UTRs, each with a 5’ (black) and 3’ (red) terminus, concatenated across strains for training. ( **C** ) Dependency map of the concatenated L UTRs from the 2026 outbreak isolate (PZ385161.1). The model correctly predicts pairing between the 5’ (black) and 3’ (red) termini, capturing pseudo-circularization, with no additional structure predicted. ( **D** ) Structures of the _B. subtilis_ adenine riboswitch in the ligand-bound (holo) and unbound (apo) states. Shaded orange and shaded purple boxed stems correspond to the boxes in **E** . ( **E** ) Dependency map of the riboswitch. Boxed regions mark nucleotides with conflicting predicted pairing partners, consistent with the mutually exclusive holo and apo states in ( **D** ).

The blue box marks the L2–L3 kissing-loop interaction, a tertiary contact common to both states, predicted alongside the state-specific pairs.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **MAIN TABLES, INCLUDING TITLES AND LEGENDS**

## **Table 1. Model Performances**

[Table on PDF page 22 (6)](../assets/table/table-p0022-005.csv)

| **Model** | **F1** | **F1** | **Precision** | **Precision** | **Recall** | **Recall** |
| --- | --- | --- | --- | --- | --- | --- |
|  | **Mean** | **Median** | **Mean** | **Median** | **Mean** | **Median** |
| pretrained | 0.06 ± 0.06 | 0.05 | 0.14 ± 0.24 | 0.05 | 0.06 ± 0.06 | 0.05 |
| Albatross 200k | 0.48 ± 0.20 | 0.54 | 0.67 ± 0.23 | 0.72 | 0.39 ± 0.18 | 0.44 |
| Albatross 500k | 0.50 ± 0.18 | 0.54 | 0.68 ± 0.23 | 0.76 | 0.41 ± 0.16 | 0.43 |
| Albatross 50k | **0.54 ± 0.21** | **0.60** | **0.73 ± 0.22** | **0.80** | **0.44 ± 0.19** | **0.48** |

## **Table 2. Comparison of RNA structure prediction models**

[Table on PDF page 22 (8)](../assets/table/table-p0022-007.csv)

|  | **Albatross**<br>**(50k)** | **Infernal** | **eFold** | **RNAstructure** | **Albatross +**<br>**RNAstructure** |
| --- | --- | --- | --- | --- | --- |
| **F1 Mean** | 0.54 ± 0.21 | 0.46 ± 0.21 | 0.48 ± 0.10 | 0.55 ± 0.14 | **0.62 ± 0.11** |
| **F1 Median** | 0.60 | 0.51 | 0.48 | 0.55 | **0.64** |
| **Precision Mean** | **0.73 ± 0.22** | 0.44 ± 0.20 | 0.45 ± 0.09 | 0.48 ± 0.13 | 0.55 ± 0.11 |
| **Precision Median** | **0.80** | 0.47 | 0.44 | 0.47 | 0.58 |
| **Recall Mean** | 0.44 ± 0.19 | 0.49 ± 0.22 | 0.51 ± 0.10 | 0.63 ± 0.15 | **0.71 ± 0.12** |
| **Recall Median** | 0.48 | 0.54 | 0.51 | 0.66 | **0.73** |

586

587

588

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **References**

1. Spitale, R.C., and Incarnato, D. (2023). Probing the dynamic RNA structurome and its func590 tions. Nature Reviews Genetics _24_ , 178–196. doi: `10.1038/s41576-022-00546-w` . 591 

2. Winther, B., Hayden, F.G., and Hendley, J.O. (2006). Picornavirus infections in children 592 diagnosed by rt-pcr during longitudinal surveillance with weekly sampling: Association with 593 symptomatic illness and effect of season. Journal of Medical Virology _78_ , 644–650. doi: 594 `10.1002/jmv.20588` . 595 

3. Lal, B.B., Sood, V., Snehavardhan, P., Khanna, R., Pasupuleti, S.S.R., Siloliya, M., Kumar, 596 G., and Alam, S. (2020). A novel, bedside, etiology specific prognostic model (peds-hav) in 597 hepatitis a induced pediatric acute liver failure. Hepatology International _14_ , 483–490. doi: 598 `10.1007/s12072-020-10050-0` . 599

4. Akinnurun, O.M., Encalada, M.N., Orth, J., Petzold, M., B¨ottcher, S., Diedrich, S., Smitka, 600 M., and Schr¨ottner, P. (2023). Enterovirus a71-associated acute flaccid paralysis in a pe601 diatric patient: a case report. Journal of Medical Case Reports _17_ , 310. doi: `10.1186/` 602 `s13256-023-04041-6` . 603

5. Yang, S., Li, P., Huang, Y., Li, W., Ma, L., Wu, L., Wang, N., Lu, J., Chen, W., ming Liu, G., 604 Xiong, Y., Chen, Y., and Zhang, Y. (2018). Factors associated with fatal outcome of children 605 with enterovirus a71 infection: a case series. Epidemiology and Infection _146_ , 788–798. 606 doi: `10.1017/S0950268818000468` . 607 

6. Moe, N., Pedersen, B., Nordbø, S.A., Skanke, L.H., Krokstad, S., Smyrnaios, A., and 608 Døllner, H. (2016). Respiratory virus detection and clinical diagnosis in children attending 609 day care. PLOS ONE _11_ , e0159196. doi: `10.1371/journal.pone.0159196` . 610 

7. Messacar, K., Spence-Davizon, E., Osborne, C., Press, C., Schreiner, T.L., Martin, J., 611 Messer, R., Maloney, J., Burakoff, A., Barnes, M., Rogers, S., Lopez, A.S., Routh, J., Ger612 ber, S.I., Oberste, M.S., Nix, W.A., Abzug, M.J., Tyler, K.L., Herlihy, R., and Dominguez, S.R. 613 (2020). Clinical characteristics of enterovirus a71 neurological disease during an outbreak 614 in children in colorado, usa, in 2018: an observational cohort study. The Lancet Infectious 615 Diseases _20_ , 230–239. doi: `10.1016/S1473-3099(19)30632-2` . 616 

8. Badizadegan, K., Kalkowska, D.A., and Thompson, K.M. (2022). Polio by the numbers—a 617 global perspective. The Journal of Infectious Diseases _226_ , 1309–1318. doi: `10.1093/` 618 `infdis/jiac130` . 619 

9. Francisco-Velilla, R., Embarc-Buh, A., Abellan, S., and Martinez-Salas, E. (2022). Picor620 navirus translation strategies. FEBS Open Bio _12_ , 1125–1141. doi: `10.1002/2211-5463.` 621 `13400` . 622 

10. Kauder, S.E., and Racaniello, V.R. (2004). Poliovirus tropism and attenuation are deter623 mined after internal ribosome entry. Journal of Clinical Investigation _113_ , 1743–1753. doi: 624 `10.1172/JCI21323` . 625 

11. Dunn, J.J., Chapman, N.M., Tracy, S., and Romero, J. (2000). Genomic determinants of 626 cardiovirulence in coxsackievirus b3 clinical isolates: Localization to the 5’ nontranslated 627 region. Journal of Virology _74_ , 4787–4794. doi: `10.1128/jvi.74.10.4787-4794.2000` . 628

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Table on PDF page 24 (2)](../assets/table/table-p0024-001.csv)

| 12. Hao, W., Bernard, K., Patel, N., Ulbrandt, N., Feng, H., Svabek, C., Wilson, S., Stracener,<br>C., Wang, K., Suzich, J., Blair, W., and Zhu, Q. (2012). Infection and propagation of human<br>rhinovirus c in human airway epithelial cells. Journal of Virology _86_, 13524–13532. doi:<br>`10.1128/JVI.02094-12`. | 629<br>630<br>631<br>632 |
| --- | --- |
| 13. Flynn, C.T., Kimura, T., Frimpong-Boateng, K., Harkins, S., and Whitton, J.L. (2017). Im-<br>munological and pathological consequences of coxsackievirus rna persistence in the heart.<br>Virology_512_, 104–112. doi: `10.1016/j.virol.2017.09.017`. | 633<br>634<br>635 |
| 14. Deschamps, A.M., DeRocco, A.J., Bok, K., and Patterson, L.J. (2023). Prototype pathogens<br>for vaccine and monoclonal antibody countermeasure development: Niaid workshop pro-<br>cess and outcomes for viral families of pandemic potential. The Journal of Infectious Dis-<br>eases_228_, S355–S358. doi: `10.1093/infdis/jiac465`. | 636<br>637<br>638<br>639 |
| 15. Andino, R., Kirkegaard, K., Macadam, A., Racaniello, V.R., and Rosenfeld, A.B. (2023). The<br>Picornaviridae family: Knowledge gaps, animal models, countermeasures, and prototype<br>pathogens. The Journal of Infectious Diseases _228_, S427–S445. doi: `10.1093/infdis/`<br>`jiac426`. | 640<br>641<br>642<br>643 |
| 16. Lee, M.F., Tham, S.K., and Poh, C.L. (2025). Antiviral strategies targeting enteroviruses:<br>Current advances and future directions. Viruses_17_, 1178. doi: `10.3390/v17091178`. | 644<br>645 |
| 17. Whitton, J.L., Cornell, C.T., and Feuer, R. (2005). Host and virus determinants of pi-<br>cornavirus pathogenesis and tropism.<br>Nature Reviews Microbiology _3_, 765–776. doi:<br>`10.1038/nrmicro1284`. | 646<br>647<br>648 |
| 18. Martin, P., Albagli, O., Poggi, M.C., Boulukos, K.E., and Pognonec, P. (2006). Development<br>of a new bicistronic retroviral vector with strong ires activity. BMC Biotechnology _6_, 4. doi:<br>`10.1186/1472-6750-6-4`. | 649<br>650<br>651 |
| 19. Wesselhoeft, R.A., Kowalski, P.S., and Anderson, D.G. (2018). Engineering circular rna<br>for potent and stable translation in eukaryotic cells. Nature Communications _9_, 2629. doi:<br>`10.1038/s41467-018-05096-6`. | 652<br>653<br>654 |
| 20. Ko, H.L., Park, H.J., Kim, J., Kim, H., Youn, H., and Nam, J.H. (2019). Development of an rna<br>expression platform controlled by viral internal ribosome entry sites. Journal of Microbiology<br>and Biotechnology_29_, 127–140. doi: `10.4014/jmb.1811.11019`. | 655<br>656<br>657 |
| 21. Reuter, J.S., and Mathews, D.H. (2010). Rnastructure: software for rna secondary structure<br>prediction and analysis. BMC bioinformatics_11_, 129. doi: `10.1186/1471-2105-11-129`. | 658<br>659 |
| 22. Hofacker, I.L., Fontana, W., Stadler, P.F., Bonhoeffer, L.S., Tacker, M., and Schuster, P.<br>(1994). Fast folding and comparison of rna secondary structures. Monatshefte fur Chemie<br>Chemical Monthly_125_, 167–188. doi: `10.1007/BF00818163`. | 660<br>661<br>662 |
| 23. de Lajarte, A.A., des Taillades, Y.J.M., Aruda, J., Bongrand, P., Wightman, F.F., Salazar, D.,<br>Allan, M.F., Kalicki, C., L’Esperance-Kerckhoff, C., Kashi, A., Jossinet, F., and Rouskin, S.<br>(2026). Diverse database and machine learning model to narrow the generalization gap in<br>rna structure prediction. Science Advances_12_. doi: `10.1126/sciadv.adz4967`. | 663<br>664<br>665<br>666 |
| 24. Ren, J., Rastegari, B., Condon, A., and Hoos, H.H. (2005). Hotknots: Heuristic prediction of<br>rna secondary structures including pseudoknots. RNA _11_, 1494–1504. doi: `10.1261/rna.`<br>`7284905`. | 667<br>668<br>669 |

[Table on PDF page 25 (1)](../assets/table/table-p0025-000.csv)

| .<br>CC-BY 4.0 International license<br>perpetuity. It is made available under a<br>preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in<br>The copyright holder for this<br>this version posted September 24, 2026.<br>;<br>https://doi.org/10.64898/2026.05.19.726202<br>doi:<br>bioRxiv preprint |  |
| --- | --- |
| 25. Rivas, E., and Eddy, S.R. (1999). A dynamic programming algorithm for rna structure pre-<br>diction including pseudoknots 1 1edited by i. tinoco.<br>Journal of Molecular Biology _285_,<br>2053–2068. doi: `10.1006/jmbi.1998.2436`. | 670<br>671<br>672 |
| 26. Fu, L., Cao, Y., Wu, J., Peng, Q., Nie, Q., and Xie, X. (2022). Ufold:<br>fast and ac-<br>curate rna secondary structure prediction with deep learning.<br>Nucleic Acids Research<br>_50_, e14–e14. URL:`https://doi.org/10.1093/nar/gkab1074`. doi:`10.1093/nar/gkab1074`.<br>`arXiv:https://academic.oup.com/nar/article-pdf/50/3/e14/42544495/gkab1074.pdf`. | 673<br>674<br>675<br>676 |
| 27. Singh, J., Hanson, J., Paliwal, K., and Zhou, Y. (2019). Rna secondary structure prediction<br>using an ensemble of two-dimensional deep neural networks and transfer learning. Nature<br>Communications_10_, 5407. doi: `10.1038/s41467-019-13395-9`. | 677<br>678<br>679 |
| 28. Wang, W., Feng, C., Han, R., Wang, Z., Ye, L., Du, Z., Wei, H., Zhang, F., Peng, Z., and<br>Yang, J. (2023). trrosettarna: automated prediction of rna 3d structure with transformer<br>network. Nature Communications_14_, 7266. doi: `10.1038/s41467-023-42528-4`. | 680<br>681<br>682 |
| 29. Rivas, E., Clements, J., and Eddy, S.R. (2017). A statistical test for conserved rna structure<br>shows lack of evidence for structure in lncrnas. Nature Methods _14_, 45–48. doi: `10.1038/`<br>`nmeth.4066`. | 683<br>684<br>685 |
| 30. Rivas, E. (2020). Rna structure prediction using positive and negative evolutionary informa-<br>tion. PLOS Computational Biology_16_, e1008387. doi: `10.1371/journal.pcbi.1008387`. | 686<br>687 |
| 31. Nawrocki, E.P., and Eddy, S.R. (2013). Infernal 1.1: 100-fold faster rna homology searches.<br>Bioinformatics_29_, 2933–2935. | 688<br>689 |
| 32. Goodarzi, H., Najafabadi, H.S., Oikonomou, P., Greco, T.M., Fish, L., Salavati, R., Cristea,<br>I.M., and Tavazoie, S. (2012). Systematic discovery of structural elements governing stabil-<br>ity of mammalian messenger RNAs. Nature_485_, 264–268. doi: `10.1038/nature11112`. | 690<br>691<br>692 |
| 33. Andino, R., Rieckhof, G.E., and Baltimore, D. (1990). A functional ribonucleoprotein complex<br>forms around the 5’ end of poliovirus rna. Cell _63_, 369–380. doi: `10.1016/0092-8674(90)`<br>`90170-J`. | 693<br>694<br>695 |
| 34. Peni´c, R.J., Vlaˇsi´c, T., Huber, R.G., Wan, Y., and <sup>ˇ</sup>Siki´c, M. (2025). Rinalmo: general-purpose<br>rna language models can generalize well on structure prediction tasks. Nature Communi-<br>cations_16_, 5671. doi: `10.1038/s41467-025-60872-5`. | 696<br>697<br>698 |
| 35. da Silva, P.T., Karollus, A., Hingerl, J., Galindez, G.S.T., Wagner, N., Hernandez-Alias,<br>X., Incarnato, D., and Gagneur, J. (2025). Nucleotide dependency analysis of genomic<br>language models detects functional elements. Nature Genetics _57_, 2589–2602. doi: `10.`<br>`1038/s41588-025-02347-3`. | 699<br>700<br>701<br>702 |
| 36. Zou, S., Tao, T., Mahbub, S., Ellington, C.N., Algayres, R., Li, D., Zhuang, Y., Wang, H.,<br>Song, L., and Xing, E.P. (2024). A large-scale foundation model for rna function and struc-<br>ture prediction. . doi: `10.1101/2024.11.28.625345`. | 703<br>704<br>705 |
| 37. Chen, J., Hu, Z., Sun, S., Tan, Q., Wang, Y., Yu, Q., Zong, L., Hong, L., Xiao, J., Shen, T.,<br>King, I., and Li, Y. (2022). Interpretable rna foundation model from unannotated data for<br>highly accurate rna structure and function predictions. . doi: `10.1101/2022.08.06.503062`. | 706<br>707<br>708 |
| 38. for Biotechnology Information, N.C. (2024). Ncbi virus. . URL:`https://www.ncbi.nlm.nih.`<br>`gov/labs/virus/vssi/`. | 709<br>710 |

- bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license. 

- 39. Altschul, S.F., Gish, W., Miller, W., Myers, E.W., and Lipman, D.J. (1990). Basic local align711 ment search tool. Journal of Molecular Biology. doi: `10.1016/S0022-2836(05)80360-2` . 712 

- 40. Maloney, A., and Joseph, S. (2024). Validating the emcv ires secondary struc713 ture with structure–function analysis. Biochemistry _63_ , 107–115. URL: `https:` 714 `//doi.org/10.1021/acs.biochem.3c00579` . doi: `10.1021/acs.biochem.3c00579` . 715 `arXiv:https://doi.org/10.1021/acs.biochem.3c00579` . PMID: 38081770. 716 

- 41. Imai, S., Suzuki, H., Fujiyoshi, Y., and Shimada, I. (2023). Dynamically regulated two-site 717 interaction of viral rna to capture host translation initiation factor. Nature Communications 718 _14_ , 4977. doi: `10.1038/s41467-023-40582-6` . 719 

- 42. Wesselhoeft, R.A., Ott, K., Barnes, T., Motz, G., Becker, A.M., Horhota, A.T., Goodman, B., 720 Shu, H., and Shivashankar, V. (2022). Circular rna compositions and methods. . 721 

- 43. Tomezsko, P.J., Corbin, V.D.A., Gupta, P., Swaminathan, H., Glasgow, M., Persad, S., Ed722 wards, M.D., Mcintosh, L., Papenfuss, A.T., Emery, A., Swanstrom, R., Zang, T., Lan, 723 T.C.T., Bieniasz, P., Kuritzkes, D.R., Tsibris, A., and Rouskin, S. (2020). Determination 724 of rna structural diversity and its role in hiv-1 rna splicing. Nature _582_ , 438–442. doi: 725 `10.1038/s41586-020-2253-5` . 726 

- 44. Zubradt, M., Gupta, P., Persad, S., Lambowitz, A.M., Weissman, J.S., and Rouskin, S. 727 (2017). Dms-mapseq for genome-wide or targeted rna structure probing in vivo. Nature 728 Methods _14_ , 75–82. doi: `10.1038/nmeth.4057` . 729 

- 45. Allan, M.F., Aruda, J., Plung, J.S., Grote, S.L., des Taillades, Y.J.M., de Lajarte, A.A., Bathe, 730 M., and Silvi, R. (2024). Discovery and quantification of long-range rna base pairs in coro731 navirus genomes with search-map and seismic-rna. bioRxiv. 732 

- 46. Weingarten-Gabbay, S., Elias-Kirma, S., Nir, R., Gritsenko, A.A., Stern-Ginossar, N., 733 Yakhini, Z., Weinberger, A., and Segal, E. (2016). Systematic discovery of cap-independent 734 translation sequences in human and viral genomes. Science _351_ . doi: `10.1126/science.` 735 `aad4939` . 736 

- 47. Chen, R., Wang, S.K., Belk, J.A., Amaya, L., Li, Z., Cardenas, A., Abe, B.T., Chen, C.K., 737 Wender, P.A., and Chang, H.Y. (2023). Engineering circular rna for enhanced protein pro738 duction. Nature Biotechnology _41_ , 262–272. doi: `10.1038/s41587-022-01393-0` . 739 

- 48. Huang, Y., Chen, Y.Q., Lou, S.Y., Gao, X., Liu, Y.X., Zhang, Y.L., Nan, F., Chen, L.L., and 740 Yang, L. (2026). Ires–cargo interplay structurally modulates circular rna translation. Cell 741 Research _36_ , 377–380. doi: `10.1038/s41422-026-01233-9` . 742 

- 49. Loughran, G., Andreev, D.E., Terenin, I.M., Namy, O., Mikl, M., Yordanova, M.M., McManus, 743 C.J., Firth, A.E., Atkins, J.F., Fraser, C.S., Ignatova, Z., Iwasaki, S., Kufel, J., Larsson, O., 744 Leidel, S.A., Mankin, A.S., Mariotti, M., Tanenbaum, M.E., Topisirovic, I., V´azquez-Laslop, 745 N., Viero, G., Caliskan, N., Chen, Y., Clark, P.L., Dinman, J.D., Farabaugh, P.J., Gilbert, 746 W.V., Ivanov, P., Kieft, J.S., M¨uhlemann, O., Sachs, M.S., Shatsky, I.N., Sonenberg, N., 747 Steckelberg, A.L., Willis, A.E., Woodside, M.T., Valasek, L.S., Dmitriev, S.E., and Baranov, 748 P.V. (2025). Guidelines for minimal reporting requirements, design and interpretation of ex749 periments involving the use of eukaryotic dual gene expression reporters (mindr). Nature 750 Structural & Molecular Biology _32_ , 418–430. doi: `10.1038/s41594-025-01492-x` . 751 

- 50. Palma, M., and Lejeune, F. (2021). Deciphering the molecular mechanism of stop codon 752 readthrough. Biological Reviews _96_ , 310–329. doi: `10.1111/brv.12657` . 753

- bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license. 

- 51. Yang, Y., and Wang, Z. (2019). Ires-mediated cap-independent translation, a path leading 754 to hidden proteome. Journal of Molecular Cell Biology _11_ , 911–919. doi: `10.1093/jmcb/` 755 `mjz091` . 756 

- 52. Dabrowski, M., Bukowy-Bieryllo, Z., and Zietkiewicz, E. (2015). Translational readthrough 757 potential of natural termination codons in eucaryotes – the impact of rna sequence. RNA 758 Biology _12_ , 950–958. doi: `10.1080/15476286.2015.1068497` . 759 

- 53. Maˇsek, T., Val´aˇsek, L., and Posp´ıˇsek, M. (2011). Polysome Analysis and RNA Purification 760 from Sucrose Gradients. Humana Press. doi: `10.1007/978-1-59745-248-9_20` . 761 

- 54. Yu, Y., Sweeney, T.R., Kafasla, P., Jackson, R.J., Pestova, T.V., and Hellen, C.U. (2011). The 762 mechanism of translation initiation on aichivirus rna mediated by a novel type of picornavirus 763 ires. The EMBO Journal _30_ , 4423–4436. doi: `10.1038/emboj.2011.306` . 764 

- 55. Kloc, A., Rai, D.K., and Rieder, E. (2016). Modification of the internal ribosome entry site 765 element impairs the growth of foot-and-mouth disease virus in porcine-derived cells. Journal 766 of General Virology _97_ , 875–884. doi: `10.1099/jgv.0.000406` . 767 

- 56. Siegfried, N.A., Busan, S., Rice, G.M., Nelson, J.A.E., and Weeks, K.M. (2014). Rna motif 768 discovery by shape and mutational profiling (shape-map). Nature Methods _11_ , 959–965. 769 doi: `10.1038/nmeth.3029` . 770 

- 57. Allan, M.F., Brivanlou, A., and Rouskin, S. (2023). Rna levers and switches controlling viral 771 gene expression. Trends in Biochemical Sciences _48_ , 391–406. doi: `10.1016/j.tibs.` 772 `2022.12.002` . 773 

- 58. Lan, T.C.T., Allan, M.F., Malsick, L.E., Woo, J.Z., Zhu, C., Zhang, F., Khandwala, S., Nyeo, 774 S.S.Y., Sun, Y., Guo, J.U., Bathe, M., N¨a¨ar, A., Griffiths, A., and Rouskin, S. (2022). Sec775 ondary structural ensembles of the sars-cov-2 rna genome in infected cells. Nature Com776 munications _13_ , 1128. doi: `10.1038/s41467-022-28603-2` . 777 

- 59. Biderman, D., Portes, J., Ortiz, J.J.G., Paul, M., Greengard, P., Jennings, C., King, D., 778 Havens, S., Chiley, V., Frankle, J., Blakeney, C., and Cunningham, J. (2024). Lora learns 779 less and forgets less. LoRA Learns Less and Forgets Less. URL: `https://arxiv.org/abs/` 780 `2405.09673` . 781 

- 60. Li, W., and Godzik, A. (2006). Cd-hit: a fast program for clustering and comparing large 782 sets of protein or nucleotide sequences. Bioinformatics _22_ , 1658–1659. doi: `10.1093/` 783 `bioinformatics/btl158` . 784 

- 61. Sweeney, T.R., Abaeva, I.S., Pestova, T.V., and Hellen, C.U.T. (2014). The mechanism 785 of translation initiation on type 1 picornavirus iress. The EMBO Journal _33_ , 76–92. doi: 786 `10.1002/embj.201386124` . 787 

- 62. Sweeney, T.R., Dhote, V., Yu, Y., and Hellen, C.U.T. (2012). A distinct class of in788 ternal ribosomal entry site in members of the kobuvirus and proposed salivirus and 789 paraturdivirus genera of the picornaviridae. Journal of Virology _86_ , 1468–1486. 790 URL: `https://journals.asm.org/doi/abs/10.1128/jvi.05862-11` . doi: `10.1128/jvi.` 791 `05862-11` . `arXiv:https://journals.asm.org/doi/pdf/10.1128/jvi.05862-11` . 792 

- 63. Xi, J., Ye, F., Wang, G., Han, W., Wei, Z., Yin, B., Yuan, J., Qiang, B., and Peng, X. 793 (2019). Polypyrimidine tract-binding protein regulates enterovirus 71 translation through 794 interaction with the internal ribosomal entry site. Virologica Sinica _34_ , 66–77. doi: 795 `10.1007/s12250-019-00089-1` . 796

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

64. Banna, H.A., Das, N.K., Kalinina, M., Lu, G., Usman, M., and Koirala, D. (2026). Structures 797 of the eif4g-binding rna domains among picornaviral ires types are topologically conserved. 798 Nature Communications _17_ , 2758. doi: `10.1038/s41467-026-69554-2` . 799 

65. Akos<sup>´</sup> Boros, Pankovics, P., Ad´am<sup>´</sup> Adonyi, Fenyvesi, H., Day, J.M., Phan, T.G., Delwart, 800 E., and Reuter, G. (2016). A diarrheic chicken simultaneously co-infected with multiple pi801 cornaviruses: Complete genome analysis of avian picornaviruses representing up to six 802 genera. Virology _489_ , 63–74. doi: `10.1016/j.virol.2015.12.002` . 803 

66. Kwok, K.T.T., de Rooij, M.M.T., Messink, A.B., Wouters, I.M., Smit, L.A.M., Cotten, M., 804 Heederik, D.J.J., Koopmans, M.P.G., and Phan, M.V.T. (2022). Establishing farm dust as a 805 useful viral metagenomic surveillance matrix. Scientific Reports _12_ , 16308. doi: `10.1038/` 806 `s41598-022-20701-x` . 807 

67. Das, D., and Hussain, T. (2025). Structural insights into the recruitment of viral type 2 ires 808 to ribosomal preinitiation complex for protein synthesis. . doi: `10.7554/eLife.107788.1` . 809 

68. Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., Gray, S., Rad810 ford, A., Wu, J., and Amodei, D. (2020). Scaling laws for neural language models. . URL: 811 `https://arxiv.org/abs/2001.08361` . `arXiv:2001.08361` . 812 

69. van den Berg, O.E., Severi, E., Mutoka-Banza, F., van Vugt, M., Schadd, E.M., Reyes, 813 M.C.C., Larr´egola, L.S., Prieto, P.V., Lescure, F.X., Cachia, M.A., Singal, M., Faber, M., 814 Zingg, W., Ismail, N.A., te Wierik, M.J., Leenstra, T., Reusken, C., and van den Hof, S. 815 (2026). Andes virus outbreak linked to expedition cruise ship travel, multi-country investiga816 tion and response, april to june 2026. Eurosurveillance _31_ . doi: `10.2807/1560-7917.ES.` 817 `2026.31.24.2600477` . 818 

70. Meier, K., Thorkelsson, S.R., Quemin, E.R.J., and Rosenthal, M. (2021). Hantavirus 819 replication cycle—an updated structural virology perspective. Viruses _13_ , 1561. doi: 820 `10.3390/v13081561` . 821 

71. Kavita, K., and Breaker, R.R. (2023). Discovering riboswitches: the past and the future. 822 Trends in Biochemical Sciences _48_ , 119–141. doi: `10.1016/j.tibs.2022.08.009` . 823 

72. Ontiveros-Palacios, N., Cooke, E., Nawrocki, E.P., Triebel, S., Marz, M., Rivas, E., Griffiths824 Jones, S., Petrov, A.I., Bateman, A., and Sweeney, B. (2025). Rfam 15: Rna families 825 database in 2025. Nucleic acids research _53_ , D258–D267. 826 

73. Benson, D.A., Cavanaugh, M., Clark, K., Karsch-Mizrachi, I., Lipman, D.J., Ostell, J., and 827 Sayers, E.W. (2012). Genbank. Nucleic Acids Research _41_ , D36–D42. doi: `10.1093/nar/` 828 `gks1195` . 829 

74. Marcano-Vel´azquez, J.G., and Batey, R.T. (2015). Structure-guided mutational analysis of 830 gene regulation by the bacillus subtilis pbue adenine-responsive riboswitch in a cellular 831 context. Journal of Biological Chemistry _290_ , 4464–4475. doi: `10.1074/jbc.M114.613497` . 832 

75. Drogalis, L.K., and Batey, R.T. (2020). Requirements for efficient ligand-gated co833 transcriptional switching in designed variants of the b. subtilis pbue adenine-responsive 834 riboswitch in e. coli. PLOS ONE _15_ , e0243155. doi: `10.1371/journal.pone.0243155` . 835 

76. Serganov, A., Yuan, Y.R., Pikovskaya, O., Polonskaia, A., Malinina, L., Phan, A.T., 836 H¨obartner, C., Micura, R., Breaker, R.R., and Patel, D.J. (2004). Structural basis for discrim837 inative regulation of gene expression by adenine- and guanine-sensing mrnas. Chemistry 838 & Biology _11_ , 1729–1741. doi: `10.1016/j.chembiol.2004.11.018` . 839

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

77. Khoroshkin, M., Zinkevich, A., Aristova, E., Yousefi, H., Lee, S.B., Mittmann, T., Mane840 gold, K., Penzar, D., Raleigh, D.R., Kulakovskiy, I.V., and Goodarzi, H. (2024). A generative 841 framework for enhanced cell-type specificity in rationally designed mRNAs. bioRxiv. doi: 842 `10.1101/2024.12.31.630783` . 843 

78. Li, . (2024). Structure and function of type iv ires in picornaviruses. Frontiers in Microbiology. 844 79. Rivas, E., Lang, R., and Eddy, S.R. (2012). A range of complex probabilistic models for RNA 845 secondary structure prediction that includes the nearest-neighbor model and more. RNA 846 _18_ , 193–212. doi: `10.1261/rna.030049.111` . 847 

80. Karan, A., and Rivas, E. (2025). All-at-once RNA folding with 3d motif prediction 848 framed by evolutionary information. Nature Methods _22_ , 2094–2106. doi: `10.1038/` 849 `s41592-025-02833-w` . 850 

81. Loshchilov, I., and Hutter, F. (2017). Fixing weight decay regularization in adam. CoRR 851 _abs/1711.05101_ . URL: `http://arxiv.org/abs/1711.05101` . `arXiv:1711.05101` . 852 

82. Needleman, S.B., and Wunsch, C.D. (1970). A general method applicable to the search for 853 similarities in the amino acid sequence of two proteins. Journal of Molecular Biology _48_ , 854 443–453. doi: `10.1016/0022-2836(70)90057-4` . 855

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **STAR METHODS**

## **Experimental model and study participant details**

### **Cell lines**

[Table on PDF page 30 (7)](../assets/table/table-p0030-006.jpg)

*Table retained as an image; cells were not reliably transcribed.*

All cell lines were grown in DMEM (ThermoFisher Scientific #10564011) with 10% FBS (Ther859 moFisher Scientific #A5209402) supplementation at 37<sup>_o_</sup> C with 5% CO2. UMNSAH/DF1 cells 860 were grown at 39<sup>_o_</sup> C with 5% CO2. 861 The following cell lines were used: HEK293T, Female; U2OS, Female; SH-SY5Y, Female; 862 HCT-8, Male; Huh7, Male; N2A (Neuro-2a), Male, ( _Mus musculus_ , A/J); UMNSAH/DF1, Unspec863 ified, ( _Gallus gallus_ , East Lansing Line 0). Cells were purchased commercially, except UMN864 SAH/DF1. The UMNSAH/DF1 cell identity was confirmed using RNAseq alignment to _Gallus_ 865 _gallus_ genome. 866

## **Method details**

[Table on PDF page 30 (10)](../assets/table/table-p0030-009.csv)

| **eo eas** | 867 |
| --- | --- |
| **Plasmids** | 868 |

All PCR reactions were performed using CloneAmp HiFi PCR Premix (Takara Cat. #639298). 869 Isothermal Assembly was performed using NEBuilder HiFi DNA Assembly Master Mix (NEB 870 E2621L). Constructs were chemically transformed into NEB Stable Competent E. coli (NEB 871 C3040I) or electroporated into NEB 10-beta Competent E. coli (NEB C3019I). 872

[Table on PDF page 30 (12)](../assets/table/table-p0030-011.jpg)

*Table retained as an image; cells were not reliably transcribed.*

cDNA was synthesized using LunaScript RT SuperMix (NEB M3010L). RT-qPCR was performed 874 using either either Luna Universal Probe qPCR Master Mix (NEB M3004L) for probe-based or 875 Luna Universal qPCR Master Mix (NEB M3003) for SYBR-based RT-qPCR as noted throughout. 876

### **Next-generation sequencing**

[Table on PDF page 30 (15)](../assets/table/table-p0030-014.jpg)

*Table retained as an image; cells were not reliably transcribed.*

Next-generation sequencing library preparation was performed using either NEBNext UltraEx878 press RNA Library Prep Kit (NEB E3330L) or NEBNext UltraExpress DNA Library Prep Kit (NEB 879 E3325L) as appropriate. Next-generation sequencing was performed on a Illumina NextSeq 880 using NextSeq 1000/2000 P1 XLEAP-SBS Reagent Kit (300 Cycles) (Illumina 20100982). 881

### **circRNA Plasmid Library**

[Table on PDF page 30 (18)](../assets/table/table-p0030-017.jpg)

*Table retained as an image; cells were not reliably transcribed.*

IRES sequences were obtained from Twist Bioscience in 96-well plate format. Each IRES in883 cluded overhangs to clone into the circRNA generation plasmid provided by the Mass General 884 Hospital RNA Therapeutics Core. The donor circRNA plasmid (p10-Natural-RTC) was amplified 885 using and primers oAS092 and oAS093. IRES and donor plasmid were assembled together 886 using isothermal assembly and transformed into NEB 10-beta Competent E. coli (NEB C3019I). 887 The distribution of IRESes within the plasmid library was confirmed by Next-Generation Se888 quencing a PCR amplicon of the barcode region associated with each IRES (Primers oAS052, 889 oAS077). These data recapitulated the results of sequencing randomly fragmented library by 890 NEBNext dsDNA Fragmentase (NEB M0348S). 891

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **circRNA library generation and analysis**

circRNAs were generated by the Mass General Hospital RNA Therapeutics Core. Distribution within the circRNA library was measured by generating cDNA then sequencing a PCR amplicon of the barcode region. This was validated by sequencing a randomly fragmented library . Circularization was confirmed by probe-based RT-qPCR using primers spanning the splice junction.

893 894 895

896

# **Polysome profiling**

Polysome gradient buffer (PGB) consisted of 20mM Tris-HCl pH 7.5 (Rockland #MB-002), 100mM KCl (Invitrogen AM9640G), 10mM MgCl2 (Thermo Scientific J62411.AD). 10% and 50% sucrose solutions in PGB were set up. 13.2 mL Open-Top Thinwall Ultra-Clear Ultracentrifuge Tubes (Beckman Coulter 344059) were loaded with the 10% sucrose solution up to the level indicated by the BioComp Marker Block (BioComp Instruments 105-914A-R). Using a syringe attached to cannula the 50% sucrose solution was loaded to the bottom of the tube until the total solution was level with the BioComp Gradient Station MagnaBase Tube Holder (BioComp Instruments 105-914A-R). The tubes were capped and the SW41 Rotor, Long Sucrose 10-50% L11 protocol was run on the BioComp Gradient Station (BioComp Instruments 153).

898 899 900

901

902

903 904 905 906

10 cm plates containing transfected cells were treated with 100 _µ_ g/mL cycloheximide (SigmaAldrich C4859-1ML) for 10 minutes at 37<sup>_o_</sup> C. Lysis buffer was made with 1 mL PGB, 500 _µ_ g cycloheximide (Sigma-Aldrich C4859-1ML), 5 _µ_ L NP-40 (BioBasic NDB0385-100ml). 500 _µ_ L of lysis buffer was added to each 10 cm plate. Cells were scraped and transfered in to 1.7 mL tubes on ice for 10 minutes. The lysis was spun down at 4<sup>_o_</sup> C at 11,200 rcf for 5 minutes and supernatant collected into clean tubes.

907

908 909 910 911

912

150 _µ_ L of the lysate was loaded on to each sucrose gradient. The gradient was spun in a SW 41 Ti Rotor (Beckman Coulter 331362) in an L100XP ultracentrifuge (Beckman Coulter 392052) at 36,000 rpm (221,356 rcf) for 1 hour 20 minutes.

150 _µ_ L of the lysate was loaded on to each sucrose gradient. The gradient was spun in a SW 913 41 Ti Rotor (Beckman Coulter 331362) in an L100XP ultracentrifuge (Beckman Coulter 392052) 914 at 36,000 rpm (221,356 rcf) for 1 hour 20 minutes. 915 Sucrose gradients were fractionated using the BioComp Gradient Station (BioComp Instru916 ments 153) collecting fractions that corresponded to polysome peaks. 917 RNA was extracted using 1 mL TRIzol Reagent (ThermoFisher Scientific 15596026) then 918 following manufacturer protocol. cDNA was synthesized as above and barcodes were amplified 919 via PCR reactions using CloneAmp HiFi PCR Premix (Takara Cat. #639298) for 25 cycles. 920 Amplicons were sequenced by next-generation sequencing as above. RNA from the lysis was 921 similarly processed. 922 Barcodes counts were normalized to the total reads then normalized to the fractional repre923 sentation in the lysis. 924

Barcodes counts were normalized to the total reads then normalized to the fractional representation in the lysis.

[Formula on PDF page 31 (21)](../assets/figure/formula-p0031-020.jpg)

# **Luciferase assays**

Cells in a 96 well plate were transfected with 10 ng plasmid DNA via PEI protocol (MedChem Express HY-K2014). Twenty four hours later, media was removed and 80 uL of 1x Passive Lysis Buffer (Promega Cat.# E1910) was added to the cells. Luciferase assays were performed using the Nano-Glo Dual-Luciferase Reporter Assay System (Promega Cat.# N1610) according to manufacturer protocol.

925

926 927 928 929

930

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **DMS-MaPseq**

For _in vitro_ DMS-MaPseq, RNA was suspended to 0.5 _µ_ g/ _µ_ L in 10 L of H2O, incubated at 95°C for 1 min, immediately mixed with 87 _µ_ L of 37<sup>_o_</sup> C preheated refolding buffer (0.4M Sodium cacodylate (Electron Microscopy Sciences #11655), 6 mM MgCl2 (Thermo Scientific J62411.AD)). The reaction was incubated at 37<sup>_o_</sup> C for 30 min. 3% DMS (Sigma-Aldrich #D186309-100ML) was added to each reaction and incubated at 37°C for 5 min before being quenched with 0.6 volumes _β_ -Mercapethanol (Thermo Scientific A15890.0B). RNA was isolated using Monarch Spin RNA Cleanup Kit (NEB T2030L). Next-generation sequencing library preparation was performed using either NEBNext UltraExpress RNA Library Prep Kit (NEB E3330L) but replacing the reverse transcriptase with Induro Reverse Transcriptase (NEB M0681L).

For _in cellulo_ DMS-MaPseq, 5 _µ_ g RNA was transfected into HEK293T, N2As, or HCT-8s in 6-well plates. After 6 hours, cells were treated with 3% DMS (Sigma-Aldrich #D186309-100ML) for 5 minutes at 37<sup>_o_</sup> C. The reaction was quenched with 10 mL 30% _β_ -Mercapethanol (Thermo Scientific A15890.0B) in DPBS (ThermoFisher Scientific #14190144). RNA was isolated using TRIzol extraction and libraries were prepared as described above.

DMS-MaPseq sequencing data was processed using SEISMIC v24.3 ( `https://github.com/ rouskinlab/seismic-rna` ) to map DMS reactivity, cluster alternative structures, and evaluate secondary structure models<sup>45</sup> .

932 933 934

935 936

937 938 939 940

941 942 943 944 945 946 947 948

# **RNA Language Model**

949

We used as a base model RiNALMo giga a 650 Million parameter RNA Language Model. 950 RiNALMo’s architecture was not modified. It is composed of 33 transformer blocks, 1280 951 embedding dim, 20 attention heads. It uses Flash attention. The attention dropout and residual 952 dropout are both set at 0.1. RiNALMo was originally trained on 36M non-coding RNAs, none of 953 which are IRESes. 954 The tokenization was the same as in the original RiNALMo. Each nucleotide is a single 955 token. After collecting the IRESes two transformations were applied: First, the sequence would 956 be uppsercased. Second, uracils were converted to thymines. These transformations were 957 applied to stay in line with RiNALMo’s pretrainining. Therefore, the Albatross vocaulary is made 958 of 4 vocabulary tokens: A, C, G, T; and four special tokens: [CLS], [EOS], [PAD], [MASK], and 959 [UNK]. 960

# **Training data & Preprocessing**

961

Initially we collected the 5<sup>_′_</sup> UTRs of every complete picornaviral genome in the NCBI Virus 962 Database<sup>38</sup> . We then iteratively used BLAST to find the top 500 aligning sequences until we 963 had a total of about 200,000 unique sequences<sup>39</sup> . To make the 500,000 sequence dataset, we 964 used cd-hit to cluster sequences by 70% or greater sequence similarity<sup>60</sup> . We then ran an iter965 ative BLAST on the least represented sequences until we had a total of about 500,000 unique 966 sequences. The 50,000 sequence dataset was generated by using cd-hit to cluster the 500,000 967 dataset by 70% or greater sequence similarity<sup>60</sup> . The representative sequence of each cluster 968 was added to the dataset, then the most divergent sequence of each cluster was added one at 969 a time until the set included about 50,000 sequences. 970 Sequences collected containing any IUPAC ambiguity code were filtered out. Sequences 971 having an exact match to another sequence were also filtered out, in order to avoid overrepre972 sention. 973

Sequences collected containing any IUPAC ambiguity code were filtered out. Sequences having an exact match to another sequence were also filtered out, in order to avoid overrepresention.

The three datasets used in figure 3 are respectively composed of 193,643, 509,944, and 52,129 unique sequences. Three datasets were used throughout this paper; they are available

974 975

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# on `https://github.com/rouskinlab/` .

# **Model Training**

We downloaded the official released weights from RiNALMo and continued pretraining of all 978 650M parameters. We did not use any LoRA, adapters, or layer freezing. Training used se979 quence input only. No structural labels, base pairing rules or thermodynamic priors were given 980 to the model or trained on. 981 The Objective is the same one as used in RiNALMo: a BERT-style masked language mod982 eling at 15% mask rate. This mask would then have the following distribution: 80% [MASK] 983 / 10% random nucleotide / 10% unchanged. Loss was computed on an independent 15% of 984 nucleotides. 985 The optimizer used was AdamW with parameters: _β_ = (0 _._ 9 _,_ 0 _._ 98), _ε_ = 10<sup>_−_6</sup> , learning rate was 986 5 _×_ 10<sup>_−_6</sup> and weight decay was 0.01<sup>81</sup> . 987 A linear warmup was set over 10,000 steps from 0 _._ 01 _·_ lr to lr. There is no decay phase, the 988 learning rate is constant after warmup. 989 The training parameters were: Batch size = 8, Max sequence length = 2048, Gradient clipping 990 1.0, 16-mixed precision, Random seed 42, Up to 10 epochs. 991 Every experiment was run on a single L40 GPU. The 50k run completed in approximately 992 twelve hours. 993 The weights released with this paper are from the 50k dataset, epoch 5, step 39,096. All 994 dependency maps used in this paper and available on `www.albatrossrna.org` were produced 995 from this checkpoint. 996 **Dependency Map Generation** 997 The Methodology used to get the dependency map is the same as described in da Silva et al.<sup>35</sup> . 998 For a sequence of length _N_ , we run 3 _N_ + 1 forward passes (1 for the reference sequence 999 and every single-point substitution to each of the 3 alternative bases). For each of these forward 1000 passes, we extract softmax probability over _{A, C, G, U }_ at every position _j_ . For mutation at 1001 position _i_ to base _m_ and target base _t_ , compute the log-odds shift 1002 _S_ ( _i, j, m, t_ ) = log2 1 _−p_ <u>mut</u> _p_ mut<sup>_−_log2</sup> 1 _−p_ <u>ref</u> _p_ ref<sup>_,_</sup> (1)

1003 where _p_ mut = _P_ ( _xj_ = _t | i → m_ ) and _p_ ref = _P_ ( _xj_ = _t |_ wild type) are the model’s softmax probabilities at position _j_ for target base _t_ , under the mutant and reference sequences respectively. 1004 1005 The dependency map entry is _M_ [ _i, j_ ] = max _m,t |S_ ( _i, j, m, t_ ) _|_ , with _M_ [ _i, i_ ] = 0. Each entry is directed: _M_ [ _i, j_ ] measures the effect of substituting position _i_ on the prediction at _j_ . Maps are not 1006 symmetrized at this stage. 1007

[Table on PDF page 33 (8)](../assets/table/table-p0033-007.csv)

| **Binary Structure Filtering** | 1008 |
| --- | --- |
| Binary filtering and structure prediction consisted of the following algorithm: | 1009 |
| **Algorithm 1: Binary structure filtering from a dependency map.** | 1010 |
| **Input:** dependency map_M ∈_R<sup>_N×N_</sup>; thresholds_τ, γ, α_. | 1011 |
| **Output:** binary contact matrix_B ∈{_0_,_1_}_<sup>_N×N_</sup>. | 1012 |
| 1. Normalize: _M _<sup>_′ _</sup>_←_clip(_M/_20_,_0_,_1). | 1013 |
| 2. Symmetrize: _M _<sup>_′ _</sup>_←_max(_M _<sup>_′_</sup>_, M _<sup>_′⊤_</sup>). | 1014 |

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

3. Threshold: _M_<sup>_′_</sup> [ _i, j_ ] _←_ 0 where where _M_<sup>_′_</sup> [ _i, j_ ] _< τ_ .

3. Threshold: _M_<sup>_′_</sup> [ _i, j_ ] _←_ 0 where where _M_<sup>_′_</sup> [ _i, j_ ] _< τ_ . 1015 4. Diagonal-band exclusion: _M_<sup>_′_</sup> [ _i, j_ ] _←_ 0 where _|i − j| ≤ γ_ . 1016 5. Anti-diagonal connectivity: along each anti-diagonal _{_ ( _i, j_ ) : _i_ + _j_ = _s}_ , retain only entries 1017 belonging to a contiguous run of length _≥ α_ . 1018

[Table on PDF page 34 (4)](../assets/table/table-p0034-003.jpg)

*Table retained as an image; cells were not reliably transcribed.*

Each of the parameter was designed to encode for a different prior: _α_ forces stem to have a 1030 minimum length. This prevents the filter to select isolated base pairs that also can be noise from 1031 the dependency map. _γ_ excludes the base pairs immediately next to the diagonal, as these pairs 1032 cannot form (Triangle inequality). _τ_ is the most significant parameter as it is the threshold to filter 1033 out weak signal. 1034

[Table on PDF page 34 (6)](../assets/table/table-p0034-005.csv)

| **Filter Parameter Selection (5-fold cross-validation)** | 1035 |
| --- | --- |
| In order to select the best set of parameters, we ran a 5-fold cross validation with a grid search<br>on the 95 DMS-MaPseq-constrained IRES structures. | 1036<br>1037 |
| The 5-fold cross validation ran under the following settings: The 95 reference sequences | 1038 |
| were split using `KFold` with _K_ = 5, `shuffle=True`, and `random`<br>`state=42`. For each fold, true | 1039 |
| positives, false positives, and false negatives were aggregated across the held-out sequences, | 1040 |
| and a micro-F1 score was computed. We then reported the mean and standard deviation across | 1041 |
| folds. The grid search covered_α ∈{_3_, . . . ,_8_}_,_τ ∈_[0_,_0_._20], and_γ ∈{_3_,_4_,_5_}_, with micro-F1 used | 1042 |
| as the metric to evaluate each parameter combination. | 1043 |

[Table on PDF page 34 (7)](../assets/table/table-p0034-006.csv)

| **Selected parameters and performance (50k, epoch 5).** | 1044 |
| --- | --- |
| The selected parameters were _α_ = 3, _τ_ = 0_._11, and _γ_ = 4. Using these fixed parameters, | 1045 |
| five-fold cross-validation gave a micro-F1 of0_._57_±_0_._03, micro-precision of0_._79_±_0_._02, and micro- | 1046 |
| recall of0_._44_±_0_._03. Per-IRES scores for this checkpoint are reported in Table 1: F10_._54_±_0_._21 | 1047 |
| (median0_._60), precision0_._73_±_0_._22(median0_._80), and recall0_._44_±_0_._19(median0_._48). | 1048 |

[Table on PDF page 34 (8)](../assets/table/table-p0034-007.jpg)

*Table retained as an image; cells were not reliably transcribed.*

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **Infernal Structure Analysis**

We used Infernal 1.1.5. For each sequence we used cmsearch against the Rfam.cm database. 1054 cmfetch pulled the relevant model for each sequence and cmalign with `--mxsize 8192` aligned 1055 each sequence to its corresponding model, producing the structural alignment used as input to 1056 R-scape. R-scape 2.6.4 was run on each alignment with CaCoFold enabled to generate the 1057 predicted structure. Unless otherwise noted all commands were run with default settings. The 1058 consensus structure was matched to the query sequence for F1, precision, and recall calcu1059 lations. When Infernal returned more than one possible model, the best-scoring model by F1 1060 was used, so the reported Infernal performance represents an upper bound. Because Rfam co1061 variance models are built from curated family alignments, cmalign places each query sequence 1062 within that family’s alignment, so the resulting CaCoFold structure closely tracks the Rfam con1063 sensus structure for that family. 1064

[Table on PDF page 35 (5)](../assets/table/table-p0035-004.csv)

| **eFold structure prediction** | 1065 |
| --- | --- |
| We used eFold released model weights for each of the 95 sequences to predict their secondary | 1066 |
| structure<sup>23</sup>. The default post-processing and code of eFold was used. All the sequences were | 1067 |
| converted to the RNA alphabet, no DMS reactivities were fed to the model. The evaluation of | 1068 |
| precision, recall, and F1 were done using the same methodology as prior. | 1069 |

[Table on PDF page 35 (6)](../assets/table/table-p0035-005.csv)

| **Unconstrained thermodynamic structure prediction** | 1070 |
| --- | --- |
| We used`Fold`from RNAstructure version 6.4 to generate thermodynamics predictions of the 95<br>sequences<sup>21</sup>. Each sequence was folded at 310.15 K (37 <sup>_◦_</sup>C) using the minimum-free-energy | 1071<br>1072 |
| structure. The rest of the parameters were default parameters. No DMS reactivities or base-pair | 1073 |
| constraints were given to the RNAstructure. The predicted structures of each sequence were<br>converted to binary pairing matrix and evaluated with the same methodology described above. | 1074<br>1075 |

[Table on PDF page 35 (7)](../assets/table/table-p0035-006.csv)

| **Albatross-Constrained Thermodynamic Structure Prediction** | 1076 |
| --- | --- |
| The base pairs generated from Albatross with standard parameters were given as hard con-<br>straints to RNAstructure`Fold`version 6.4<sup>21</sup>. The predictions given to the thermodynamic model<br>were restricted to AU, GC, and GU pairs. The sequences were then folded at 310.15 K (37 <sup>_◦_</sup>C)<br>using the constrained minimum-free-energy structure without DMS reactivities. | 1077<br>1078<br>1079<br>1080 |
| **Family-Wide Structure Maps** | 1081 |
| Across the full set of binary maps, we observed a mean of 71.5 base pairs per map, a median of<br>78, and a maximum of 171. After substring-containment deduplication of the 500k pool, 75,229<br>root sequences were retained and used for the family-wide structural analyses. These structures<br>can be found on`https://albatrossrna.org`. | 1082<br>1083<br>1084<br>1085 |

[Table on PDF page 35 (8)](../assets/table/table-p0035-007.jpg)

*Table retained as an image; cells were not reliably transcribed.*

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **Structure alignment and clustering**

Up to 10 sequences were selected from each cd-hit 70% similarity cluster. Binary maps were used as _n x n_ adjacency matrices. Each antidiagonal was projected into the corresponding column of a _n x_ (2 _n −_ 1) matrix and padded with zeros. Columns with no pairs were dropped.

The resulting compressed structure matrices were aligned using a modified NeedlemanWuncsh Algorithm with a gap penalty of -1<sup>82</sup> . Aligned columns _a, b_ were scored as (3 _−∥a − b∥_ 2). For structure clustering, the final modified Needleman-Wuncsh similarity score between struc- _max_ <u>(</u> _S_ <u>)</u> _−Si,j_ tures _i, j_ , _Si,jϵS_ was converted _di,j_ = _max_ ( _S_ ) _−P_ 20( _S_ )<sup>.</sup><sup>_d_wasusedasthedistanceforhierarchical</sup> clustering using `scipy.cluster.hierarchy.linkage` with `method = "average"` .

1092 1093 1094 1095 1096 1097 1098 1099

# **Generalization**

1100

In order to test generalization (Figure 7A), we continued pretraining the three model sizes from RiNALMo micro (33M), mega (150M), and giga (650M) on type I IRES sequences. The dataset was made of 38,223 sequences. These sequences were selected from the 75,229 unique set of IRESes. No Type II, III, IV, nor V IRESes were part of the training. The training settings were the same as described above.

In order to test generalization (Figure 7A), we continued pretraining the three model sizes from 1101 RiNALMo micro (33M), mega (150M), and giga (650M) on type I IRES sequences. The dataset 1102 was made of 38,223 sequences. These sequences were selected from the 75,229 unique set of 1103 IRESes. No Type II, III, IV, nor V IRESes were part of the training. The training settings were the 1104 same as described above. 1105 The dependency maps were also produced using the same methodology. The maps were 1106 produced every 3,125 steps for the 85 Type I, II, and V sequences for which we have _in cellulo_ 1107 DMS-MaPseq ground-truth. The dataset is composed of: 56 Type I, 16 Type II, 13 Type V. The 1108 parameters used to turn the dependency map into a binary map were the same as in the previous 1109 section: _α_ = 3, _τ_ = 0 _._ 11, and _γ_ = 4. 1110

For Figure 7A, one checkpoint was selected per model size using the macro-F1 on the Type 1111 I, II, and V sequences (85 sequences). The checkpoints were: micro 62,500; mega 50,000; giga 1112 53,125. The panel shows the relative micro-F1 versus the micro model. 1113 **Hantavirus** 1114

We collected 15,375 Orthohantavirus nucleotide records from NCBI. As RiNALMo was only trained on non-coding sequences, we had to filter out on coding regions. Only 14,884 sequences had annotated CDS. For each unique sequence, we labeled the left of the CDS: 3<sup>_′_</sup> UTR and the right of the CDS: 5<sup>_′_</sup> UTR. We then, for each of this independent segment, concatenate them. Of the 14,884 CDS-annotated records, 9,843 had no sequence flanking the CDS, so the concatenated UTR was empty and those records were removed. After this filtering, we had: 5,041 sequences. In case of ambiguity code being present in the sequence, the letter would be replace by an N.

We collected 15,375 Orthohantavirus nucleotide records from NCBI. As RiNALMo was only 1115 trained on non-coding sequences, we had to filter out on coding regions. Only 14,884 sequences 1116 had annotated CDS. For each unique sequence, we labeled the left of the CDS: 3<sup>_′_</sup> UTR and the 1117 right of the CDS: 5<sup>_′_</sup> UTR. We then, for each of this independent segment, concatenate them. 1118 Of the 14,884 CDS-annotated records, 9,843 had no sequence flanking the CDS, so the con1119 catenated UTR was empty and those records were removed. After this filtering, we had: 5,041 1120 sequences. In case of ambiguity code being present in the sequence, the letter would be replace 1121 by an N. 1122 We continued pretraining the RiNALMo giga model as above but with a learning rate of 5 _×_ 1123 10<sup>_−_6</sup> , a batch size of 8, and 60,000 training steps. 1124 The dependency maps were generated for the S, M, and L segments of ANDV/Switzerland/Hu- 1125 3337/2026 using the same methodology. For each segment, the genomic 3<sup>_′_</sup> and 5<sup>_′_</sup> UTRs were 1126 concatenated in the same manner as the training sequences. 1127 **Dependency mapping of bacterial riboswitch** 1128 We continued pretraining RiNALMo on 76,829 bacterial riboswitch sequences from 10 ligand 1129 classes taken from the RFAM full-region alignments for RF00050, RF00059, RF00162, RF00167, 1130 RF00168, RF00174, RF00504, RF00522, RF01051 and RF01734<sup>72</sup> . Since Rfam covariance 1131 models contain only the aptamer domain and not the corresponding downstream expression 1132 platform which contains the switch, we extended each hit with 150nt to the 3’ of the aptamer 1133

# **Dependency mapping of bacterial riboswitch**

We continued pretraining RiNALMo on 76,829 bacterial riboswitch sequences from 10 ligand classes taken from the RFAM full-region alignments for RF00050, RF00059, RF00162, RF00167, RF00168, RF00174, RF00504, RF00522, RF01051 and RF01734<sup>72</sup> . Since Rfam covariance models contain only the aptamer domain and not the corresponding downstream expression platform which contains the switch, we extended each hit with 150nt to the 3’ of the aptamer

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Table on PDF page 37 (2)](../assets/table/table-p0037-001.csv)

| from the corresponding full sequence in NCBI<sup>73</sup>. The _b. subtilis_ riboswitch dependency map<br>was generated as described in dependency map generation above using this model. | 1134<br>1135 |
| --- | --- |
| **Quantification and statistical analysis** | 1136 |
| Statistical analysis was performed using python 3.11.5, numpy 2.2.6, scikit-posthocs 0.11.4, and<br>scipy 1.17.1.<br>Statistical methods are noted in relevant figure legends. All error bars represent standard<br>deviation from the mean. | 1137<br>1138<br>1139<br>1140 |
| **Additional resources** | 1141 |
| Albatross Dependency Map Database: `https://albatrossrna.org`<br>DMS-MaPseq Data: `www.rnandria.org` | 1142<br>1143 |

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

# **SUPPLEMENT FIGURES TITLES AND LEGENDS**

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 39 (2)](../assets/figure/figure-p0039-001.jpg)

Figure 1: **Polysome fractionation absorbance at 260nm.** Trace of 260 nm absorbance during polysome fractionation. For each sample, absorbance was shifted equally at each point to set minimum absorbance to 0 A.U. Replicates were similarly shifted upwards for clarity. Vertical lines delineate fractions.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 40 (2)](../assets/figure/figure-p0040-001.jpg)

Figure 2: **IRES representation is consistent across library preparation and sequencing methods.** (A) Correlation between barcode sequencing and random fragmentation sequencing for the plasmid library (Pearson R = 0.978). (B) Same as (A), but for the circRNA library (Pearson R = 0.936). (C) Correlation between plasmid and circRNA library composition measured by barcode sequencing (Pearson R = 0.922). Each point represents one IRES. (D) Fractional representation of individual IRESes in the plasmid and circRNA libraries. Each colored segment corresponds to a single IRES. Shading is consistent between libraries. Lines indicate linear regression fits with 95% confidence intervals.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 41 (2)](../assets/figure/figure-p0041-001.jpg)

Figure 3: **Polysome profiling barcode abundances are reproducible across replicates.** Scatter plots of barcode abundances between biological replicates for each cell type. Spearman correlation coefficients are indicated: HEK293T (R = 0.65), HCT-8 (R = 0.76), Huh7 (R = 0.89), N2A (R = 0.93), SH-SY5Y (R = 0.81), and U2OS (R = 0.80). Each point represents one IRES barcode in a given polysome fraction.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 42 (2)](../assets/figure/figure-p0042-001.jpg)

Figure 4: **Dual luciferase reporter assay validates polysome profiling rank order.** (A) Bicistronic dual luciferase reporter assay schematic (left) and firefly to nano luciferase ratios (fLuc/nLuc) for six selected IRESes: the top two (Caprine kobuvirus 12Q108, Caprine kobuvirus MN1/2018), bottom two (Turdivirus 1, Sicinivirus A), median (Poliovirus 2), and EMCV. Caprine kobuvirus 12Q108 exhibits 2 _._ 26 _±_ 0 _._ 25 fold activity relative to EMCV ( _p_ = 3 _._ 2 _×_ 10<sup>_−_5</sup> ). Data points represent individual replicates; bars indicate the mean. (B) CircRNA construct schematic (top) and ribosomes/RNA from polysome profiling for all 96 IRESes ranked by activity, with the same six IRESes highlighted. Caprine kobuvirus 12Q108 exhibits 2 _._ 07 _±_ 0 _._ 25 fold activity relative to EMCV ( _p_ = 1 _._ 1 _×_ 10<sup>_−_3</sup> ). Rank order and relative expression are concordant between the two assays. All data from HEK293T cells.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 43 (2)](../assets/figure/figure-p0043-001.jpg)

Figure 5: **Type V IRESes exhibit high activity across all cell types.** Same as Figure 2F, but shown individually for all six cell lines: HEK293T, HCT-8, Huh7, N2A, SH-SY5Y, and U2OS. Violin plots display ribosomes/RNA grouped by IRES structural type (I, II, IV, V). _p_ -values from Kruskal-Wallis H test with Dunn posthoc analysis are indicated.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 44 (2)](../assets/figure/figure-p0044-001.jpg)

Figure 6: **DMS-MaPseq AUC-ROC values in three conditions.** AUC-ROC values for three DMS-MaPseq experiments measuring fit of DMS data to the predicting secondary structure model.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 45 (2)](../assets/figure/figure-p0045-001.jpg)

Figure 7: **Albatross-predicted base pairs overlaid on consensus literature structures.** Representative IRES secondary structures for Enterovirus A71 (Type I), EMCV (Type II), and Salivirus (Type V) are shown. Base pairs predicted by Albatross that agree with the consensus literature structures are colored as true positives (green), while Albatross predictions absent from the consensus literature structures are colored as false positives (pink).

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 46 (2)](../assets/figure/figure-p0046-001.jpg)

Figure 8: **Albatross uses motif recognition to predict structure.** ( **A** ) Dependency maps of the Gallivirus IRES with GNRA mutations: wild-type (GUAA), AAAA, CCCC, and deletion. ( **B,C** ) Predicted structures for GNRA variants and deletion mutant.

[Figure on PDF page 46 (4)](../assets/figure/figure-p0046-003.jpg)

Figure 9: **Secondary structures of the four sequence elements for sythnetic sequence prediction experiments.** The natural A71 structured region (magenta) and open region (blue), and two synthetic sequences absent from the A71 training set: a thermodynamically stable synthetic stem (green) and a synthetic sequence with low intrinsic folding stability (orange).

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 47 (2)](../assets/figure/figure-p0047-001.jpg)

Figure 10: **Albatross stem prediction correlates with IRES activity.** ( **A** ) HEK293T activity vs Albatross stem predictions. ( **B** ) HEK293T activity vs DMS-MaPseq stem predictions. ( **C** ) HEK293T activity vs RNAstructure stem predictions.

bioRxiv preprint doi: https://doi.org/10.64898/2026.05.19.726202; this version posted September 24, 2026. The copyright holder for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.

[Figure on PDF page 48 (2)](../assets/figure/figure-p0048-001.jpg)

Figure 11: **Albatross recovers both conformations of the** **_B. subtilis_ adenine riboswitch.** ( **Top** ) Ligand-bound (holo) structure predicted by Albatross, with the adenine ligand drawn at the three-way junction and the loop-loop interaction indicated by dashed lines. ( **Bottom** ) Unbound (apo) structure predicted by Albatross. In both panels, nucleotides are colored by agreement with the published structure: true positive (predicted paired and paired in the published structure), false positive (predicted paired, unpaired in the published structure), true negative (predicted unpaired and unpaired), and false negative (predicted unpaired, paired in the published structure). Related to Figure 7G and H.

[PDF page 49](../assets/figure/page-0049.jpg)

[PDF page 50](../assets/figure/page-0050.jpg)

[PDF page 51](../assets/figure/page-0051.jpg)

[PDF page 52](../assets/figure/page-0052.jpg)

[PDF page 53](../assets/figure/page-0053.jpg)

[PDF page 54](../assets/figure/page-0054.jpg)

[PDF page 55](../assets/figure/page-0055.jpg)

[PDF page 56](../assets/figure/page-0056.jpg)

[PDF page 57](../assets/figure/page-0057.jpg)

[PDF page 58](../assets/figure/page-0058.jpg)

[PDF page 59](../assets/figure/page-0059.jpg)

[PDF page 60](../assets/figure/page-0060.jpg)

[PDF page 61](../assets/figure/page-0061.jpg)

[PDF page 62](../assets/figure/page-0062.jpg)

[PDF page 63](../assets/figure/page-0063.jpg)

[PDF page 64](../assets/figure/page-0064.jpg)

[PDF page 65](../assets/figure/page-0065.jpg)

[PDF page 66](../assets/figure/page-0066.jpg)

## Conversion notes

- Some source pages are available only as linked images; no searchable text is claimed for those pages.
