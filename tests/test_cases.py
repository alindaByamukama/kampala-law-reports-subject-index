"""Tests for src/cases.py — case block detection."""
from pathlib import Path

import pandas as pd
import pytest

from src.load import load_raw
from src.sections import detect_sections
from src.cases import detect_case_blocks, CASE_BLOCK_COL

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "admin_law_sample.csv"


@pytest.fixture(scope="module")
def fixture_df():
    return detect_case_blocks(detect_sections(load_raw(FIXTURE_PATH)))


# ---------------------------------------------------------------------------
# State classification — rows that must always be NaN
# ---------------------------------------------------------------------------


def test_pre_section_rows_are_nan(fixture_df):
    """Rows before the first section header (source_row 0–3) get NaN."""
    pre = fixture_df[fixture_df["source_row"] < 4]
    assert pre[CASE_BLOCK_COL].isna().all()


def test_section_header_row_is_nan(fixture_df):
    """The 'ADMINISTRATIVE LAW' header row (source_row 4) gets NaN."""
    row = fixture_df[fixture_df["source_row"] == 4]
    assert row[CASE_BLOCK_COL].isna().all()


def test_between_case_blank_is_nan(fixture_df):
    """Blank row between case 1 and case 2 (source_row 19) gets NaN."""
    row = fixture_df[fixture_df["source_row"] == 19]
    assert row[CASE_BLOCK_COL].isna().all()


def test_within_case_blank_is_nan(fixture_df):
    """Blank row inside case 1 (source_row 9, between issue and Held) gets NaN."""
    row = fixture_df[fixture_df["source_row"] == 9]
    assert row[CASE_BLOCK_COL].isna().all()


# ---------------------------------------------------------------------------
# ID assignment — correct integer values on content rows
# ---------------------------------------------------------------------------


def test_metadata_row_gets_integer(fixture_df):
    """The Works Ltd metadata row (source_row 6, year=1990-91) gets case_block 1."""
    row = fixture_df[fixture_df["source_row"] == 6]
    assert row[CASE_BLOCK_COL].iloc[0] == 1


def test_post_metadata_content_row_gets_same_id(fixture_df):
    """A Held paragraph row after a within-case blank (source_row 10) gets case_block 1."""
    row = fixture_df[fixture_df["source_row"] == 10]
    assert row[CASE_BLOCK_COL].iloc[0] == 1


def test_preamble_row_gets_same_id_as_metadata_row(fixture_df):
    """Case-name preamble row before the metadata row (source_row 5) gets case_block 1."""
    row = fixture_df[fixture_df["source_row"] == 5]
    assert row[CASE_BLOCK_COL].iloc[0] == 1


def test_second_case_gets_next_id(fixture_df):
    """The Wyclief Kiggundu metadata row (source_row 20) gets case_block 2."""
    row = fixture_df[fixture_df["source_row"] == 20]
    assert row[CASE_BLOCK_COL].iloc[0] == 2


# ---------------------------------------------------------------------------
# Contract — immutability and return value
# ---------------------------------------------------------------------------


def test_returns_copy_and_does_not_mutate_input():
    """detect_case_blocks returns a new DataFrame and does not mutate the input."""
    df = detect_sections(load_raw(FIXTURE_PATH))
    original = df.copy()
    result = detect_case_blocks(df)

    assert CASE_BLOCK_COL not in df.columns
    assert df.equals(original)
    assert CASE_BLOCK_COL in result.columns
    assert result is not df


# ---------------------------------------------------------------------------
# Integration — counts and grouping on the fixture and the full CSV
# ---------------------------------------------------------------------------


def test_fixture_has_exactly_five_cases(fixture_df):
    """The admin_law_sample fixture (100 rows) contains exactly 5 distinct cases.

    Cases 1–4 are documented in expected/admin_law_sample.json. Case 5 starts at
    source_row 98 (Uganda Blanket Manufacturers) and is truncated by the fixture.
    """
    assert fixture_df[CASE_BLOCK_COL].dropna().nunique() == 5


def test_case_1_row_set_matches_expected(fixture_df):
    """df[case_block == 1] contains exactly the non-blank rows of the Works Ltd case.

    Source rows 5–18 belong to case 1; blank rows 9, 14, 16 within that range
    stay NaN and are excluded from the group.
    """
    case1_source_rows = set(
        fixture_df[fixture_df[CASE_BLOCK_COL] == 1]["source_row"].tolist()
    )
    assert case1_source_rows == {5, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18}


def test_full_csv_has_1443_cases():
    """The full raw CSV produces exactly 1443 distinct case_block values."""
    raw_path = PROJECT_ROOT / "data" / "raw" / "KAMPALA LAW REPORT - SUBJECT INDEX.csv"
    df = detect_case_blocks(detect_sections(load_raw(raw_path)))
    assert df[CASE_BLOCK_COL].dropna().nunique() == 1443


# ---------------------------------------------------------------------------
# Edge cases — already-assigned guard
# ---------------------------------------------------------------------------


def _make_preamble_after_blank_df():
    """Minimal DataFrame: case 2 has a preamble row separated from case 1 by a blank.

    Layout:
      row 0: pre-section
      row 1: section header
      row 2: case 1 metadata
      row 3: case 1 Held paragraph
      row 4: blank separator
      row 5: case 2 preamble (case-name line, no year)
      row 6: case 2 metadata
      row 7: case 2 Held paragraph

    This is the pattern present in 104 of the 1,443 cases in the full dataset.
    Recon confirmed that every adjacent case pair is separated by at least one
    blank (0 no-blank pairs found), so pass 2A's backward fill never bleeds into
    the preceding case's content — it always stops at the blank at row 4.

    What this test exercises is pass 2B's already-assigned guard: the forward fill
    carries case 1's ID through the blank (row 4) and would overwrite the preamble
    (row 5) with case 1's ID if the guard were absent. The guard detects that row 5
    was pre-assigned to case 2 by pass 2A and switches the forward-fill context to
    case 2 instead of overwriting.

    Pass 2A's own already-assigned guard (the no-blank scenario) is not exercised
    here because of the blank at row 4. That guard is theoretical safety against a
    data pattern that does not exist in this dataset.
    """
    rows = [
        # pre-section
        {"subject_matter": "Title", "year": None, "vol": None, "court": None, "page": None, "category": None},
        # header
        {"subject_matter": "Test Category", "year": None, "vol": None, "court": None, "page": None, "category": "Test Category"},
        # case 1 metadata
        {"subject_matter": "Alpha v Beta", "year": "1990", "vol": "I", "court": "HCCS", "page": "1", "category": "Test Category"},
        # case 1 Held paragraph
        {"subject_matter": "Held: something.", "year": None, "vol": None, "court": None, "page": None, "category": "Test Category"},
        # blank separator between cases
        {"subject_matter": None, "year": None, "vol": None, "court": None, "page": None, "category": "Test Category"},
        # case 2 preamble (case name line with no year — metadata is on the next row)
        {"subject_matter": "Gamma v Delta", "year": None, "vol": None, "court": None, "page": None, "category": "Test Category"},
        # case 2 metadata
        {"subject_matter": "continued name", "year": "1991", "vol": "II", "court": "HCCS", "page": "2", "category": "Test Category"},
        # case 2 Held paragraph
        {"subject_matter": "Held: other.", "year": None, "vol": None, "court": None, "page": None, "category": "Test Category"},
    ]
    df = pd.DataFrame(rows)
    df["source_row"] = range(len(df))
    return df


def test_pass2b_guard_switches_context_at_preamble_row():
    """Pass 2B's already-assigned guard correctly hands off from case 1 to case 2.

    The forward fill carries case 1's ID through the blank separator. Without the
    guard, it would overwrite the preamble row (pre-assigned to case 2 by pass 2A)
    with case 1's ID. The guard detects the preamble row is already assigned and
    switches the carry to case 2 instead.
    """
    df = _make_preamble_after_blank_df()
    result = detect_case_blocks(df)

    assert result.loc[3, CASE_BLOCK_COL] == 1, "case 1 Held row → case_block 1"
    assert pd.isna(result.loc[4, CASE_BLOCK_COL]), "blank separator → NaN"
    assert result.loc[5, CASE_BLOCK_COL] == 2, "case 2 preamble → case_block 2"
    assert result.loc[6, CASE_BLOCK_COL] == 2, "case 2 metadata → case_block 2"
    assert result.loc[7, CASE_BLOCK_COL] == 2, "case 2 Held → case_block 2"
