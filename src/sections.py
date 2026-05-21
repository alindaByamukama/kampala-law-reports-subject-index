# This file contains the list of categories that are used in the application.
CATEGORIES = [
    "Administrative Law",
    "Administration of Estates",
    "Advocates",
    "Arbitration",
    "Banking",
    "Bankruptcy",
    "Civil Procedure",
    "Commercial Law",
    "Company Law",
    "Constitutional Law",
    "Contract",
    "Copyright",
    "Criminal Law",
    "Criminal Procedure",
    "Damages",
    "Elections",
    "Employment",
    "Evidence",
    "Expropriated Properties",
    "Family Law",
    "International Law",
    "Labour Law",
    "Land Law",
    "Local Administration",
    "Sports Law",
    "Statutory Interpretation",
    "Stare Decisis",
    "Succession",
    "Taxation",
    "Traffic & Road Safety Act",
    "Words & Phrases",
]
# _normalise takes one argument - a raw cell value - and returns a string - if it's not a string, returns an empty string. If it is a string, it trims whitespace, removes trailing periods, and converts it to uppercase.
def _normalise(value):
    if not isinstance(value, str):
        return ""
    return value.strip().rstrip(".").strip().upper()
# Lookup dict mapping normalised category strings to their display forms.
CATEGORY_LOOKUP = {_normalise(category): category for category in CATEGORIES}
def detect_sections(df):
    """Add a category column to df by matching subject_matter against CATEGORIES.

    Each header row is tagged with its category; the value is then forward-filled
    so every row carries the category of the section it falls under. Rows before
    the first header remain None. The DataFrame is not mutated; a copy is returned.
    """
    df = df.copy()
    df["category"] = df["subject_matter"].map(lambda x: CATEGORY_LOOKUP.get(_normalise(x)))
    df["category"] = df["category"].ffill()
    return df
