"""Tests for src/sections.py — category normalisation and section detection."""
from pathlib import Path

import pandas as pd

from src.load import load_raw
from src.sections import _normalise, detect_sections

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "admin_law_sample.csv"


def test_normalise_full_transform():
    """_normalise should strip whitespace, remove trailing period, and uppercase."""
    result = _normalise("  ADVOCATES. ")
    assert result == "ADVOCATES"


def test_normalise_non_string_guard():
    """_normalise should return empty string for non-string values (None, NaN, etc)."""
    assert _normalise(None) == ""
    assert _normalise(float("nan")) == ""


def test_normalise_convergence():
    """_normalise should produce the same result for equivalent forms from different sources."""
    assert _normalise("ADVOCATES.") == _normalise("Advocates")


def test_detect_sections_assigns_administrative_law_for_admin_law_sample():
    """detect_sections should tag rows from admin_law_sample.csv with Administrative Law after the header."""
    df = load_raw(FIXTURE_PATH)
    result = detect_sections(df)

    # Rows before the first header row should remain NaN.
    assert result.loc[result["source_row"] < 4, "category"].isna().all()

    # All rows from the first header row onwards should be Administrative Law.
    assert (result.loc[result["source_row"] >= 4, "category"] == "Administrative Law").all()


def test_detect_sections_returns_copy_and_preserves_input():
    """detect_sections should return a new DataFrame and not mutate the original input."""
    df = load_raw(FIXTURE_PATH)
    original = df.copy()
    result = detect_sections(df)

    assert "category" not in df.columns
    assert df.equals(original)
    assert "category" in result.columns
    assert result is not df


def test_detect_sections_full_raw_csv_yields_thirty_one_categories():
    """The full raw CSV should produce exactly 31 distinct detected categories."""
    raw_path = PROJECT_ROOT / "data" / "raw" / "KAMPALA LAW REPORT - SUBJECT INDEX.csv"
    df = load_raw(raw_path)
    result = detect_sections(df)

    distinct_categories = result["category"].dropna().unique()
    assert len(distinct_categories) == 31
