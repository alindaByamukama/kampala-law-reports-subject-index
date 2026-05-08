"""
Extract test fixtures from the source CSV.

Reads the raw KLR Subject Index CSV and saves specified row ranges
as small fixture files for use in pipeline tests.

Run from the project root: python tests/fixtures/extract_fixtures.py
"""
from pathlib import Path
import pandas as pd

# Path setup - resolves regardless of where the script is invoked from.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_CSV = PROJECT_ROOT / "data" / "raw" / "KAMPALA LAW REPORT - SUBJECT INDEX.csv"
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"

# Fixture definitions: name -> (start_row, end_row, description)
# Row numbers are 0-indexed. Spreadsheet row N corresponds to index N-1.
FIXTURES = {
    "admin_law_sample": (
        0, 100,
        "First 100 rows: title, header row, ADMINISTRATIVE LAW section header, "
        "Works Ltd case (multi-row name edge case), Wyclief Kiggundu Kato case "
        "(clean), and subsequent cases in the section."
    ),
}


def main():
    """Extract fixtures from the source CSV."""
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Source CSV not found at {SOURCE_CSV}")
    
    df = pd.read_csv(SOURCE_CSV, header=None, dtype=str, encoding='cp1252')
    print(f"Loaded source: {len(df)} rows, {len(df.columns)} columns")
    
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    
    for name, (start, end, desc) in FIXTURES.items():
        fixture = df.iloc[start:end].copy()
        output_path = FIXTURES_DIR / f"{name}.csv"
        fixture.to_csv(output_path, index=False, header=False, encoding='utf-8')
        print(f"\n  Created {output_path.name}")
        print(f"    Rows {start}–{end} ({len(fixture)} rows)")
        print(f"    {desc}")


if __name__ == "__main__":
    main()