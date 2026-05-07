# Provenance

This document records the origin, access, and processing chain for the Kampala Law Reports Subject Index dataset in this repository. It exists to make the dataset's lineage auditable: anyone reviewing this repository should be able to trace each artefact back to its source.

## Source

| | |
|---|---|
| Title | Kampala Law Reports - Subject Index |
| Compiler | Jolly Kibalama |
| Format (original) | Microsoft Excel (.xlsx), password-protected |
| Time period covered | 1989–1999 |
| Part of | A broader collection of East African legal materials compiled and made publicly available by Mr. Kibalama |
| Source location | [GOOGLE_DRIVE_FOLDER_URL](https://drive.google.com/drive/folders/1F3G_nreQiXbeGEu0eHAp3kTO8y4Lpj3L?usp=drive_link) |

## Access

| | |
|---|---|
| Discovered via | LinkedIn post by Valentine Onoke (repost on behalf of Jolly Kibalama) |
| Discovery URL | [LinkedIn post by Valentine Onoke](https://www.linkedin.com/posts/val-onoke_legalresearch-caselaw-accesstojustice-activity-7453412390957703168-FoO7?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAADVVnVkBe7A_TjDC96DuPlagg6LQM5-DcwA) |
| Date discovered | 25th April 2026 |
| Date CSV exported | 4th May 2026 |
| Password access | The password for the Excel file was publicly distributed alongside the file (in a `.txt` file in the same Drive folder). It is not reproduced in this repository; the same channel through which it was discovered remains the source. |

## Processing

The source `.xlsx` file was opened with the publicly available password and saved as `.csv` to enable cleaning workflows without depending on the password and to make the data more portable. The CSV preserves the layout-oriented structure of the original spreadsheet — one cell per visual row of the source — rather than one row per case. Restructuring it into a per-case dataset is the focus of the code in `src/`.

Files retained:

- `data/raw/KAMPALA LAW REPORT - SUBJECT INDEX.csv` - committed to this repository as the working source of truth.
- The original `.xlsx` is gitignored to avoid redistributing the password-protected binary; it remains the canonical original on Mr. Kibalama's Google Drive.

## Communication with the compiler

Initial contact with Mr. Kibalama was made via LinkedIn on 5th May 2026. The conversation regarding scope, attribution, and publishing approach is ongoing. Any substantive decisions arising from it are reflected in the README and in this document.

## Citation

To cite the original source and this derivative dataset, see [`CITATION.cff`](CITATION.cff).