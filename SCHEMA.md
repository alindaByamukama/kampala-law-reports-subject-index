# Dataset Schema

This document specifies the structure of the cleaned Kampala Law Reports Subject Index dataset and its audit sidecar. It is the authoritative reference for field names, types, and meanings used by the cleaning pipeline.

## Main dataset: `klr_subject_index.csv`

14 fields, one row per case.

### Identity

| Field | Type | Notes |
|-------|------|-------|
| `case_id` | string | Stable identifier of form `klr_NNNN` (e.g., `klr_0001`). |

### Classification

| Field | Type | Notes |
|-------|------|-------|
| `category` | string | One of 31 legal categories from the source's section headers (Civil Procedure, Criminal Law, etc.). Controlled vocabulary. |

### Title

| Field | Type | Notes |
|-------|------|-------|
| `case_name` | string | Full case name as it appears in the source, concatenated across rows where the case name spans multiple rows. |

### Parties

| Field | Type | Notes |
|-------|------|-------|
| `parties_first` | string (nullable) | First party named in the case. For trial-court cases this is the plaintiff; for appellate cases this is the appellant. Null for non-adversarial cases. |
| `parties_second` | string (nullable) | Second party named. For trial-court cases this is the defendant; for appellate cases this is the respondent. Null for non-adversarial cases. |
| `case_type` | string | Controlled vocabulary: `vs` (adversarial), `in_the_matter` (begins "In the matter of…"), `other`. |

### Citation

| Field | Type | Notes |
|-------|------|-------|
| `year_start` | integer | Earliest year of the case. For single-year cases, equals `year_end`. |
| `year_end` | integer | Latest year. For ranges like "1990-91", `year_start=1990, year_end=1991`. |
| `volume` | string | Roman numeral identifier (I, II, III, IV, V, VI). String because it identifies, not measures. |
| `court` | string | Normalised court code (one of approximately 12–15 values). Original raw value preserved in audit sidecar. |
| `page` | integer | Page reference within the volume. |

### Substance

| Field | Type | Notes |
|-------|------|-------|
| `issue` | string | The question of law before the court, concatenated across multi-row source entries. |
| `holding` | string | The court's ruling or principle, concatenated across multi-row "Held:" passages. |

### Quality

| Field | Type | Notes |
|-------|------|-------|
| `needs_review` | boolean | True for cases where automatic cleaning could not confidently extract all fields, indicating the row may benefit from manual inspection. |

## Audit sidecar: `klr_subject_index_review.csv`

Joins to the main dataset by `case_id`. Supports verification of cleaning decisions.

| Field | Type | Notes |
|-------|------|-------|
| `case_id` | string | Foreign key to the main dataset. |
| `court_raw` | string | Original raw court string from the source CSV before normalisation. |
| `source_row` | integer | Row number in the raw CSV where this case begins. Used for tracing back to source. |

## Naming conventions

- All fields are `snake_case`.
- Identifier prefixes are lowercase (`klr_`).
- Boolean fields are named as positive predicates (`needs_review`, not `is_clean`).

## Design decisions

Decisions made during schema design, recorded for future reference:

- **Year split into `year_start` / `year_end`** rather than a single string. Enables filtering and sorting; the cost of one extra column is worth the queryability gain.
- **Parties named `first` / `second`** rather than `plaintiff` / `defendant`. The plaintiff/defendant convention only applies at trial-court level; at appeal it's appellant/respondent. Neutral naming with documentation handles both correctly without forcing manual classification.
- **`case_type` retained as explicit field** rather than derived from null patterns. Supports direct querying ("show me all `in_the_matter` cases") without forcing users to infer from null patterns.
- **Audit fields in sidecar** (`klr_subject_index_review.csv`) rather than main dataset. Keeps the published dataset clean for general use; verification fields are available via join for those who need them.
- **`needs_review` retained in main dataset** despite being audit-shaped. Quality control is a common user use case, not just an auditor concern, so the flag earns its place in the main dataset.