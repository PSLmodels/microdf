import pytest
import microdf as mdf


def test_tax():
    # Consider a MTR schedule of 0% up to 10,000, then 10% after that.
    BRACKETS = [0, 10e3]
    RATES = [0, 0.1]
    INCOME = [0, 5e3, 10e3, 10e3 + 1, 20e3]
    EXPECTED = [0, 0, 0, 0.1, 1e3]
    res = mdf.tax_from_mtrs(INCOME, BRACKETS, RATES)
    assert res.tolist() == EXPECTED
