"""
Load and prepare the raw Kampala Law Reports Subject Index CSV.

This module is the entry point for the cleaning pipeline. It reads the
source CSV, drops empty columns, renames the remaining ones, and adds
a row index column for traceability through later stages.
"""
from pathlib import Path
import pandas as pd


def load_raw(csv_path: Path) -> pd.DataFrame:
    """Load and minimally prepare the raw CSV.

    Parameters
    ----------
    csv_path : Path
        Path to the source CSV (or any fixture with the same structure).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: subject_matter, year, vol, court, page, source_row.
        Each row corresponds to one row of the source CSV.
    """
    # 1. Read the CSV
    df = pd.read_csv(csv_path, encoding='cp1252', header=None, dtype=str)

    # 2. Capture source_row from the index BEFORE any drops
    df['source_row'] = df.index

    # 3. Drop empty columns (0, 6, 7, 8)
    df = df.drop(columns=[0, 6, 7, 8])

    # 4. Rename remaining columns to meaningful names
    df = df.rename(columns={1: "subject_matter", 2: "year", 3: "vol", 4: "court", 5: "page"})

    return df