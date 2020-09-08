import pandas as pd

import microdf as mdf


X = [1, 5, 2]
W = [4, 1, 1]
df = pd.DataFrame({"x": X, "w": W})


def test_weighted_quantile():
    Q = [0, 0.5, 1]
    mdf.weighted_quantile(df, "x", "w", Q).tolist()


def test_weighted_median():
    # TODO: Add None default to w.
    # assert mdf.weighted_median(df, 'x') == 2
    mdf.weighted_median(df, "x", "w")


def test_weighted_mean():
    # TODO: Add None default to w.
    # assert mdf.weighted_mean(df, 'x') == 8 / 3
    assert mdf.weighted_mean(df, "x", "w") == 11 / 6


def test_weighted_sum():
    """ """
    # TODO: Add None default to w.
    # assert mdf.weighted_sum(df, 'x') == 8
    assert mdf.weighted_sum(df, "x", "w") == 11
