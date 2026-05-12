"""Tests for src/load.py — raw CSV loading and preparation."""
from pathlib import Path

import pandas as pd

from src.load import load_raw


# Path to the fixture, resolved relative to this test file.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "admin_law_sample.csv"


def test_load_raw_returns_expected_columns():
    """load_raw should return a DataFrame with the expected column names in order."""
    df = load_raw(FIXTURE_PATH)
    expected_columns = ["subject_matter", "year", "vol", "court", "page", "source_row"]
    assert list(df.columns) == expected_columns

def test_load_raw_preserves_row_count():
    """load_raw should return a DataFrame with the same number of rows as the source CSV."""
    df = load_raw(FIXTURE_PATH)
    assert len(df) == 100

def test_load_raw_source_row_starts_at_zero():
    """load_raw should create a source_row column that starts at 0 and increments by 1."""
    df = load_raw(FIXTURE_PATH)
    assert df["source_row"].iloc[0] == 0
    assert df["source_row"].iloc[-1] == 99