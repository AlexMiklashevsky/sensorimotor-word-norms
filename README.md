# Sensorimotor word norms: An overview

An overview of published sensorimotor rating norms for words across languages: perceptual strength and sensory experience, perceptual features, bodily involvement, specific body parts (effectors), manipulability and body-object interaction. Only word ratings are included (no picture norms).

**Web page:** https://alexmiklashevsky.github.io/sensorimotor-word-norms/ (interactive citation network, details, filterable table, help for planning a rating study, references, contact).

## How to cite

Miklashevsky, A., Ulianova, T., & Platonova, O. (in prep.). *Sensorimotor word norms: An overview*. https://github.com/AlexMiklashevsky/sensorimotor-word-norms

Each release is archived on Zenodo with a DOI; please cite the version you used.

## Data

| File | Content |
|---|---|
| `data/datasets.csv` | The overview table: one row per paper and language |
| `data/scales.csv` | One row per rating scale: instruction wording, scale, don't-know option, category and rating relation |
| `data/citation_links.csv` | Citation links between the papers, with the reference entry each link rests on |
| `data/sensorimotor_norms_table.xlsx` | The overview table and the scales as an Excel workbook (with code key) |
| `data/citation_network.xlsx` | Papers, links, rejected candidate links, communities and summary of the network analysis |
| `data/references.md`, `.bib`, `.ris` | All papers of the overview (APA 7, BibTeX, RIS) |
| `data/codebook.md` | Description of every column of the CSV files, categories and codes |
| `figures/citation_network.(png/svg/pdf)` | Static figure of the citation network |
| `docs/index.html` | The web page (served by GitHub Pages) |

All files in `data/`, `figures/` and `docs/` are generated from the source data by `update_all.py`; do not edit them by hand.

## Source data

- `work/records.json` - one record per paper and language (main data file)
- `work/scales/all2.json` - one entry per rating scale (wording, anchors, don't-know option)
- `facets/coded2.json` - coding of each scale: categories 1-6 and rating relation (R code)
- `net/` - confirmed and rejected citation links (`old_v1/edges.json`, `new3.json`, `new_verif.json`, `rejected.json`, `retarget.json`), stored node positions (`positions.json`), availability of full texts (`fulltext_available.json`), and the scripts that build the network and the page
- `refs/` - DOIs (`dois.json`), Crossref metadata (`crossref_refs_meta.json`), structured metadata of references without Crossref entries (`manual_refs_meta.json`), and the reference builder

The full texts of the papers, used to find the citation links, are copyrighted and are not part of this repository.

## Rebuild everything

Requirements: R 4.x with the packages igraph (1.6.0, the version used for the published results) and jsonlite; Python 3.13 with the packages in `requirements.txt`. Optional for the browser tests: Node.js and Playwright.

```
pip install -r requirements.txt
python3 update_all.py
```

This rebuilds the table, the citation network (data assembly in Python; all network analyses in R: `net/analysis/communities.R`, igraph Louvain, best of 100 seeds), the layout, the references, the web page, the figures, the CSV files and the codebook, and ends with `out/check_report.txt`. Fix all ERRORS before publishing and read the WARNINGS.

Options:
- `--table-version T --network-version N` also writes versioned copies to `out/` (e.g., `sensorimotor_norms_table_vT.xlsx`).
- `--relayout` recomputes the whole network layout. Without it, papers keep their stored positions and new papers are placed next to the papers they are linked to.

`tests/run_all.sh` runs the browser tests of the page. The GitHub Action in `.github/workflows/build.yml` runs the full rebuild, the checks and the tests on every push and fails if the committed outputs differ from a fresh build.

## Adding a new study

1. **Record:** copy `templates/new_record_template.json` into `work/records.json` and fill it in (one record per language). Label = official publication year; use a/b if the label already exists.
2. **Scales and coding:** for each rating scale add an entry to `work/scales/all2.json` and a coding entry to `facets/coded2.json` (see `templates/new_scale_template.json`). Use the exact instruction wording where available.
3. **Citations:** with the full texts available locally (`txt/<label>.txt`, never committed), add a title fragment to `net/titles.py`, run `net/make_rows.py`, then `net/match.py` and `net/pass2.py` in `net/`. Check each proposed link against the reference entry; add confirmed links to `net/new3.json` (or `new_verif.json`) and rejected ones to `net/rejected.json`. Check both directions: the new paper's references, and later papers that cite it. Running the build with `txt/` present updates `net/fulltext_available.json`.
4. **Reference:** if the paper has a DOI, run `python3 refs/fetch_crossref.py` (needs internet; optionally set the environment variable SMN_CONTACT_EMAIL). Without a DOI, add an APA entry to the MAN list in `refs/build_refs.py` and its structured metadata to `refs/manual_refs_meta.json`.
5. **Dimensions:** if the check report lists an unrecognized dimension, add a rule in `net/dims.py`.
6. **Run** `python3 update_all.py` and read the check report.
7. **Community texts:** if the report says a community changed, reread the community descriptions in `net/build_page_v2.py` (variable F), adjust them, then run `python3 check_all.py --accept-communities`.
8. **Publish:** commit and push; then create a GitHub release (e.g., v1.1), which Zenodo archives with a new DOI.

All counts, filters, the table, the planning help, the category statistics, the reference list and the last-update time on the page are generated from the data; only the community descriptions (step 7) and the category definitions and quotes are written by hand.

## License

Data, figures, page content and documentation: CC BY 4.0 (see `LICENSE-DATA.md`). Code: MIT License (see `LICENSE`).

## Contact

See the Contact tab of the web page. If your study is missing, please get in touch.
