import pytest
import pandas as pd
import microdf as mdf


def test_tax():
    # Consider a MTR schedule of 0% up to 10,000, then 10% after that.
    BRACKETS = [0, 10e3]
    RATES = [0, 0.1]
    INCOME = [0, 5e3, 10e3, 10e3 + 1, 20e3]
    EXPECTED = [0, 0, 0, 0.1, 1e3]
    res = mdf.tax_from_mtrs(INCOME, BRACKETS, RATES)
    pd.testing.assert_series_equal(res, pd.Series(EXPECTED))
    # Try with 10% avoidance.
    EXPECTED_10PCT_AVOIDANCE = [0, 0, 0, 0, 800]
    res_10pct_avoidance = mdf.tax_from_mtrs(INCOME, BRACKETS, RATES, 0.1)
    pd.testing.assert_series_equal(res_10pct_avoidance, EXPECTED_10PCT_AVOIDANCE)
