# Kampala Law Reports Subject Index

![Status](https://img.shields.io/badge/status-in%20development-orange)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-green)](LICENSE)
[![Data License: CC--BY--4.0](https://img.shields.io/badge/data%20license-CC--BY--4.0-blue)](data/LICENSE)

> A structured, queryable dataset of Ugandan case law summaries (1989–1999), derived from the Kampala Law Reports compiled by Jolly Kibalama.

| | |
|---|---|
| Cases | 1,443 |
| Year range | 1989–1999 |
| Legal categories | 31 |
| Source | Kampala Law Reports |
| Original compiler | Jolly Kibalama |
| Status | In development |

## Overview

 This repository provides a structured, queryable version of the Kampala Law Reports Subject Index. It is a curated collection of Ugandan court case summaries spanning 1989 to 1999. 

 The original index was compiled and made publicly available by Jolly Kibalama as a layout-oriented Excel spreadsheet. 

 This project transforms the source into a clean, machine-readable dataset where each row represents one case, with fields for parties, legal category, year, court, page reference, issue, and holding. Its aim is to make the material searchable, citable, and useful for legal research, education, and computational analysis of East African jurisprudence.

## Provenance and attribution

The source data for this dataset is the **Kampala Law Reports Subject Index**, an index of Ugandan case law summaries that forms part of a broader collection of East African legal materials compiled by **Jolly Kibalama**. The collection was made publicly available through Mr. Kibalama's Google Drive and was discovered through [a LinkedIn post by Valentine Onoke](https://www.linkedin.com/posts/val-onoke_legalresearch-caselaw-accesstojustice-activity-7453412390957703168-FoO7?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAADVVnVkBe7A_TjDC96DuPlagg6LQM5-DcwA).

The original Subject Index file is a password-protected Excel workbook, with the password publicly distributed alongside it. This repository works from a CSV export of that source. The underlying case law is public record; the compilation work that brought these materials together is Mr. Kibalama's, and is the canonical source to cite.

Mr. Kibalama has been informed of this project, has confirmed no concerns about how the dataset circulates, and is collaborating on the precise attribution wording. Updated wording will appear here once finalised. For the complete chain of custody, see PROVENANCE.md.

## Scope

This dataset covers the **Kampala Law Reports - Subject Index** specifically, and only that source. The original Excel file from which it derives is one document within a broader collection of East African legal materials compiled by Mr. Kibalama; this dataset does not extend to the rest of that collection.

### In scope

- Case summaries from the Kampala Law Reports
- Time period: **1989 to 1999** (the years actually represented in the source)
- Jurisdiction: **Uganda** (cases heard by Ugandan courts)
- 31 legal categories spanning Civil Procedure, Criminal Law, Evidence, Land Law, Contract, and others
- Per case: case name, parties, year, volume, court, page reference, issue, and holding
- Cases from multiple Ugandan court levels (High Court, Court of Appeal, Supreme Court, and others)

### Out of scope

- **Full judgment text.** This is an index of case summaries, not the full judgments themselves. For full judgments of these cases, see the original [Kampala Law Reports collection on Mr. Kibalama's Google Drive](https://drive.google.com/drive/folders/1F3G_nreQiXbeGEu0eHAp3kTO8y4Lpj3L?usp=drive_link).
- **Other folders in the broader collection.** The broader Drive collection contains additional Ugandan and East African legal materials (other Supreme Court compilations, Court of Appeal cases, commercial court collections, and more); this dataset is the KLR Subject Index only.
- **Other East African jurisdictions.** The broader collection includes Kenyan and Tanzanian materials; this dataset is Uganda-only.
- **Cases outside 1989–1999.** The broader collection reportedly spans 1900–2010, but the Subject Index file itself only covers this decade.
- **Other Ugandan publications and unreported cases.** Cases reported in other Ugandan law reports, or unreported cases, are not included unless they appear in the KLR Subject Index.

### Implications for use

This dataset supports research, education, and computational analysis of Ugandan jurisprudence **within the decade and corpus it actually covers**. It should not be characterised as "comprehensive Ugandan case law" or as a complete representation of Ugandan jurisprudence in any period.

## Known limitations

This section documents known weaknesses in the dataset honestly. Some are inherited from the source; some are inherent to the structure of a curated subject index; a few are choices made during cleaning. We surface them here so users can decide whether the dataset suits their use case rather than discovering issues in production.

### Source data quality

- **Year format inconsistencies.** The source contains a small number of year values that appear to be typos: `199091` (1 occurrence) and `1999-91` (1 occurrence) are almost certainly meant to be `1990-91`. These will be flagged in the cleaning pipeline rather than silently corrected, so verification against the printed reports remains possible.
- **Court abbreviation drift.** The raw `court` column contains 107 unique strings, but most are capitalization variants of the same court (e.g., `Misc.appl`, `Misc.apl`, `Misc.App`, `Misc.app`). Cleaning normalises these to roughly 12-15 actual courts and preserves the original raw value alongside the normalised one.
- **Missing metadata in source.** A small number of case records are missing volume or page values in the source. These remain as nulls in the cleaned dataset rather than being filled by inference.

### Coverage and representation

- **Class imbalance.** Civil Procedure represents approximately 31% of the dataset (450 of 1,443 cases). Anyone training models or computing aggregate statistics on this dataset should account for this skew, it reflects what the original index emphasised, not the actual distribution of legal disputes in Uganda.
- **Long tail.** Eight legal categories contain three or fewer cases each (e.g., Sports Law, International Law, Local Administration). These categories are present for completeness but are not statistically meaningful on their own.
- **Editorial selection by the source.** The Subject Index reflects which cases the original publication chose to include. There is no record of what was excluded; the dataset cannot be treated as a representative sample of Ugandan jurisprudence in this period, only as an index of what the source curated.

### What has not been verified

- **Summaries against original judgments.** This dataset preserves the case summaries as they appear in the original Subject Index. Individual entries have not been cross-referenced against the full judgments they summarise. For research relying on precise legal reasoning, the summaries should be treated as starting points rather than authoritative restatements.
- **Visual formatting fidelity.** The original `.xlsx` uses formatting (bold case names, etc.) that is lost in CSV export. The CSV preserves all textual content, but visual cues from the source are not part of this dataset.

## Intended use and out-of-scope use

This section describes what the dataset is built to support and where it should not be used. Disclosing both protects users from misapplication and clarifies the dataset's place in the wider ecosystem of Ugandan and East African legal resources.

### Intended uses

- **Legal research** on Ugandan case law from 1989–1999, using the structured index to locate cases by category, year, court, parties, or topic.
- **Education** - law students, researchers, and educators studying Ugandan jurisprudence, the development of common law in Uganda, or the structure of legal indexing itself.
- **Computational and NLP work** on East African legal texts: text classification, named entity recognition (parties, courts, statutes), summarisation, retrieval-augmented generation, and other applied machine-learning tasks where structured legal data is hard to come by.
- **Building search and discovery interfaces** for the case index - making it easier for advocates, researchers, and the public to find relevant precedent.
- **Statistical and historical analysis** of how legal disputes were categorised and distributed in the period, with the caveat from Known Limitations about editorial bias in the source.

### Out-of-scope uses

- **Legal advice or authoritative citation in proceedings.** This is summary data drawn from a subject index, not the full judgments. Users in a legal setting should always verify against the original published judgments before citation.
- **Claims of comprehensive Ugandan case law coverage.** As noted in Scope, this dataset covers one publication and one decade. It does not represent the totality of Ugandan jurisprudence in this or any period.
- **Outcome prediction or predictive legal analytics.** The dataset is too narrow in time, too curated in selection, and too summary in detail to support reliable prediction of judicial outcomes. Models trained on it for this purpose will produce results without a sound basis.
- **Substitution for judgment text.** The summaries here are starting points for finding relevant cases, not replacements for reading the actual judgments.

## License

This project uses two licenses, reflecting the conventional split between code and data:

- **Code** (the cleaning pipeline, scripts, and tooling in `src/`) is licensed under the **MIT License**. See [`LICENSE`](/LICENSE) for full text.
- **Data** (the dataset itself, in `data/cleaned/` and `data/raw/`) is licensed under the **Creative Commons Attribution 4.0 International (CC-BY-4.0)** license. See [`data/LICENSE`](data/LICENSE) for full text.

CC-BY-4.0 permits free use, redistribution, and modification of the dataset — including for commercial purposes — provided that proper attribution is given to the original compiler (Jolly Kibalama) and to this derivative work. See the **Citation** section below for the recommended citation format.

## Citation

If you use this dataset in research, software, or publication, please cite both this work and the original source compilation.

**Recommended citation for this dataset:**

> Byamukama, A. (2026). *Kampala Law Reports Subject Index Dataset.* GitHub repository. Available at: https://github.com/alindaByamukama/kampala-law-reports-subject-index

**Recommended attribution for the source:**

> Source materials compiled by Jolly Kibalama as part of his ongoing effort to make East African legal materials publicly accessible. Original collection available through Mr. Kibalama's [Google Drive folder](<DRIVE_URL>).

For machine-readable citation metadata in [Citation File Format](https://citation-file-format.github.io/), see [`CITATION.cff`](CITATION.cff). GitHub will render a "Cite this repository" button on the repo page using that file.

## Acknowledgments

This project would not exist without the work of **Jolly Kibalama**, whose effort to gather, preserve, and make publicly available a substantial collection of East African legal materials is the foundation everything here is built on. His willingness to engage with this initiative and to collaborate openly on attribution wording has been generous and is genuinely appreciated.

Discovery of the source materials came through a [LinkedIn post by **Valentine Onoke**](https://www.linkedin.com/posts/val-onoke_legalresearch-caselaw-accesstojustice-activity-7453412390957703168-FoO7?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAADVVnVkBe7A_TjDC96DuPlagg6LQM5-DcwA), whose advocacy for open access to legal information in East Africa is what made this collection visible in the first place.