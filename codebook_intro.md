# Codebook

Data files of "Sensorimotor word norms: An overview" (Miklashevsky, Ulianova, & Platonova, in prep.).

All CSV files are UTF-8 encoded, comma-separated, with one header row. An empty cell means that the information is not reported in the paper, not applicable, or unclear. The CSV files are generated from the source files `work/records.json`, `work/scales/all2.json` and `facets/coded2.json` by `update_all.py`; do not edit them by hand.

Unit of the overview: one row per paper and language (a paper that rates words in three languages has three rows). Only word ratings are included (no picture norms). Papers are identified by an author-year label (e.g., "Lynott et al. (2020)"), with the official publication year and a/b for two papers with the same label.

Categories (assigned per rating scale according to what raters were asked to judge):
1 Global sensory experience (one overall sensory rating, e.g., SER);
2 Experience per sense (one rating per modality);
3 Perceptual features (specific features within a modality, e.g., color, pain, temperature);
4 Bodily involvement, no body part named;
5 Specific body part / effector;
6 Body-object interaction (BOI).

Rating relation (R code): R1 experience ("to what extent do you experience ..."); R1p possible vs. actual experience rated separately; R2a association / relatedness; R2b feature relevance; R3 ease of interaction (BOI-type); R4 object property; R4b feature salience (Binder et al., 2016); R6 categorical choice, yes/no or number; R7 behavior (e.g., frequency of use); "R1 [LLM]" LLM-generated ratings with an experience-type prompt; R? unclear from the available wording.
