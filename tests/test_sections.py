"""Tests for src/sections.py — category normalisation."""
from src.sections import _normalise


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
