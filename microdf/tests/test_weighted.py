import numpy as np
import pandas as pd
import microdf as mdf
import pytest


X = [1, 5, 2]
W = [4, 1, 1]
df = pd.DataFrame({'x': X, 'w': W})

def test_weighted_quantile():
    Q = [0, 0.5, 1]
    EXPECTED_UNWEIGHTED = [1, 2, 5]
    res_unweighted = mdf.weighted_quantile(X, Q).tolist()
    assert EXPECTED_UNWEIGHTED == res_unweighted
    res_weighted = mdf.weighted_quantile(X, Q, W).tolist()
    # Waiting for a better test, given the result isn't exactly the same as
    # stacking values.
    # See stackoverflow.com/q/21844024#comment102342137_29677616
    # EXPECTED_WEIGHTED = [1, 1, 5]
    # For now, check that median is less than the unweighted median.
    assert res_weighted[1] < res_unweighted[1]


def test_weighted_mean():
    # TODO: Add None default to w.
    # assert mdf.weighted_mean(df, 'x') == 8 / 3
    assert mdf.weighted_mean(df, 'x', 'w') == 11 / 6


def test_weighted_sum():
    # TODO: Add None default to w.
    # assert mdf.weighted_sum(df, 'x') == 8
    assert mdf.weighted_sum(df, 'x', 'w') == 11
