import numpy as np
import microdf as mdf
import pytest


def test_weighted_quantile():
    X = [1, 5, 2]
    W = [4, 1, 1]
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
