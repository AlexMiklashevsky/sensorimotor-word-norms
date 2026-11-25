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

## datasets.csv

The overview table: one row per paper and language. 161 rows.

| Column | Description |
|---|---|
| Language | Language of the rated words. |
| Year | Official publication year. |
| Authors | Paper label (author-year); identifies the paper in all files. |
| Publication type | Type of publication and source (journal, volume, pages), and the role of the ratings in the paper. |
| Study type | norming study; stimulus ratings in experimental study; thesis; model-generated (LLM ratings); other. |
| Sensorimotor variables | Sensorimotor variables rated, as described in the paper. |
| Construct (coded) | Coded construct(s) of the sensorimotor variables (e.g., perceptual strength, effector relatedness, BOI); several separated by semicolons. |
| Granularity | How finely the variables are split: single score, per modality, per effector, per modality + per effector, multiple attributes. |
| 1 Global sensory experience | "core" if at least one rating scale of the dataset belongs to category 1; empty otherwise. |
| 2 Experience per sense | "core" if at least one rating scale of the dataset belongs to category 2; empty otherwise. |
| 3 Perceptual features | "core" if at least one rating scale of the dataset belongs to category 3; empty otherwise. |
| 4 Bodily involvement (no body part named) | "core" if at least one rating scale of the dataset belongs to category 4; empty otherwise. |
| 5 Specific body part / effector | "core" if at least one rating scale of the dataset belongs to category 5; empty otherwise. |
| 6 Body-object interaction | "core" if at least one rating scale of the dataset belongs to category 6; empty otherwise. |
| Number of items | Number of rated items in the dataset (the rated pool, not the subset selected for an experiment). |
| Items (category) | Number of items in bins: 30-99, 100-299, 300-999, 1,000-2,999, 3,000-9,999, 10,000+ (steps of about x3). |
| Items (details) | Breakdown of the items, selected subsets, or why the number is missing. |
| Item type | Kind of rated items (e.g., single words, phrases) and, where given, presentation mode. |
| Parts of speech | Word classes of the items: one class; several classes with counts in brackets where reported; "Mixed (not specified)"; "Other" (classifiers, compounds, ideophones, reduplicated words). |
| POS group | Parts of speech for filtering: Nouns, Verbs, Adjectives, Mixed, Other, Not reported. |
| Item sampling | How the items were selected. |
| Rating scale | Scale range, anchors and don't-know option. |
| Raters (total) | Total number of raters. |
| Ratings per item | Number of ratings per item. |
| Rater population | Who the raters were (as described in the paper). |
| Rater type | human or LLM. |
| Rater group | Rater group for filtering (e.g., general adults, children, L2 bilinguals; n/a for LLM ratings). |
| Perspective | Whose experience is rated: own; typical person; child; possible vs. actual; not specified (wording asks about association without reference to a person); empty if the wording is not available. |
| Collection mode | How the ratings were collected (e.g., online platform, paper questionnaire). |
| Reliability reported | Reliability measures reported in the paper. |
| Item SDs reported | Whether item-level standard deviations are reported. |
| Data level | Level of the published data (e.g., item means, item level / trial level, not published). |
| Data repository / license | Where the data are published and under which license. |
| Other variables | Non-sensorimotor variables rated in the same study. |
| Paper link | Link to the paper (DOI where available). |
| Data link | Link to the published data. |
| Comments | Further notes, including item restrictions and excluded scales. |

## scales.csv

One row per rating scale of each paper and language, with its coding. 712 rows.

| Column | Description |
|---|---|
| Authors | Paper label (author-year), as in datasets.csv. |
| Language | Language of the rated words. |
| Scale | Name of the rating scale. |
| Category | Category or categories of the scale (1-6; see above); empty if the scale is outside the categories or excluded. |
| Rating relation (R code) | Rating relation code (see above). |
| Construct (coded) | Coded construct of the scale. |
| Wording | Instruction wording, verbatim where printed in the paper. |
| Wording type | Source of the wording: verbatim; verbatim translation; quoted from paper; paper's description; paraphrase / summary. |
| Scale range and anchors | Scale range and anchor labels. |
| Don't-know option | Whether raters could indicate that they did not know a word. |
| Original language / translation | Language of the original instruction and translation status. |
| Where in paper | Where the wording was found. |
| Full text available in | Source the coding is based on (paper, supplement, repository, abstract / secondary source). |
| Notes | Further notes on the scale. |

## citation_links.csv

Citation links between the papers of the overview, found in the reference lists of the papers. 844 rows.

| Column | Description |
|---|---|
| Citing paper | Paper whose reference list contains the citation (label as in datasets.csv). |
| Cited paper | Paper that is cited. |
| Cited paper is newer | "yes" if the cited paper has a later publication year than the citing paper (cited as preprint or in press); empty otherwise. |
| Decision | How the link was confirmed: auto (author, year and title match); checked (proposed by script, verified by hand); manual (found or verified by hand). |
| Method | Matching step that found the link. |
| Reference entry (excerpt) | Excerpt of the citing paper's reference list around the matched entry. |
