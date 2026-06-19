import pandas as pd

CASE_BLOCK_COL = "case_block"

_DATA_COLS = ["subject_matter", "year", "vol", "court", "page"]


def detect_case_blocks(df: pd.DataFrame) -> pd.DataFrame:
    """Add a case_block column grouping rows belonging to the same legal case.

    Each case receives a unique integer ID (1-based, sequential). Blank rows,
    section header rows, and pre-section rows receive pd.NA.

    Requires df to already have a 'category' column (output of detect_sections).

    Three-pass approach:
      Pass 1  — Assign sequential IDs to metadata rows (year non-null, in-section,
                not a header). These are the one-per-case anchors (1,443 in the
                full dataset).
      Pass 2A — Backward fill from each metadata row to its preamble rows: the
                1–3 non-blank case-name lines that directly precede the metadata
                row with no blank between them. Stops at blank / header / pre-
                section / already-assigned rows.
      Pass 2B — Forward fill from metadata rows to Held paragraphs. Carries the
                current case ID forward through non-blank content rows. When it
                encounters a row already assigned in pass 2A (a preamble row of
                the next case), it switches context to that case's ID. Blank rows
                are skipped without resetting the carry, so within-case blanks do
                not break the fill for Held paragraphs that follow them.

    Note: 5 cases in the full dataset have subject_matter = NaN on their metadata
    row (corrupted source entries). They still receive a case_block ID; stage 4
    is responsible for handling the missing case name downstream.
    """
    df = df.copy()

    is_blank = df[_DATA_COLS].isna().all(axis=1)
    is_pre = df["category"].isna()
    # Header row = first row of each category block, by construction of detect_sections:
    # detect_sections forward-fills category from the header row, so the header is the
    # only row where category changes (or goes from NaN to a value).
    is_header = df["category"].notna() & (df["category"] != df["category"].shift(1))
    is_meta = df["year"].notna() & ~is_pre & ~is_header

    n = len(df)
    case_block = [pd.NA] * n

    # Pass 1: Tag each metadata row with a sequential case ID.
    case_id = 0
    for i in range(n):
        if is_meta.iat[i]:
            case_id += 1
            case_block[i] = case_id

    # Pass 2A: Backward fill from each metadata row to its preamble rows.
    # Preamble rows are non-blank case-name lines immediately before the metadata
    # row with no blank between them. 104 of 1,443 cases have 1–3 such rows.
    # In this dataset every pair of adjacent cases is separated by at least one
    # blank (verified by recon: 0 no-blank adjacent pairs), so the backward fill
    # always stops at the blank and never bleeds into the preceding case's content.
    # The is_pre check is unreachable in practice (the section header fires first),
    # and the already-assigned guard is never triggered, but both are kept as
    # defensive stops against unexpected data.
    for i in range(n):
        if not is_meta.iat[i]:
            continue
        cid = case_block[i]
        j = i - 1
        while j >= 0:
            if is_pre.iat[j] or is_header.iat[j] or is_blank.iat[j]:
                break
            if case_block[j] is not pd.NA:
                break
            case_block[j] = cid
            j -= 1

    # Pass 2B: Forward fill from metadata/preamble rows to Held paragraphs.
    # When the fill encounters a row already assigned in pass 2A (a preamble row
    # of the next case), it switches context to that case's ID rather than
    # overwriting it. Blank rows are skipped without resetting the carry so that
    # within-case blanks (between Held paragraphs) do not break the fill.
    current_case = None
    for i in range(n):
        if is_pre.iat[i] or is_header.iat[i]:
            current_case = None
            continue
        if is_blank.iat[i]:
            continue
        if case_block[i] is not pd.NA:
            # Metadata or preamble row — switch to this case's context.
            current_case = int(case_block[i])
            continue
        # Unassigned non-blank content row (issue text or Held paragraph).
        if current_case is not None:
            case_block[i] = current_case

    df[CASE_BLOCK_COL] = pd.array(case_block, dtype=pd.Int64Dtype())
    return df
