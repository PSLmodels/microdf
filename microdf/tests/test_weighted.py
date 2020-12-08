import pandas as pd

import microdf as mdf


X = [1, 5, 2]
W = [4, 1, 1]
df = pd.DataFrame({"x": X, "w": W})
# Also make a version with groups.
df2 = df.copy(deep=True)
df2.x *= 2
dfg = pd.concat([df, df2])
dfg["g"] = ["a"] * 3 + ["b"] * 3


def test_weighted_quantile():
    Q = [0, 0.5, 1]
    mdf.weighted_quantile(df, "x", "w", Q).tolist()


def test_weighted_median():
    assert mdf.weighted_median(df, "x") == 2
    mdf.weighted_median(df, "x", "w")
    # Test with groups.
    mdf.weighted_median(dfg, "x", "w", "g")


def test_weighted_mean():
    assert mdf.weighted_mean(df, "x") == 8 / 3
    assert mdf.weighted_mean(df, "x", "w") == 11 / 6
    mdf.weighted_mean(dfg, "x", "w", "g")


def test_weighted_sum():
    assert mdf.weighted_sum(df, "x") == 8
    assert mdf.weighted_sum(df, "x", "w") == 11
    mdf.weighted_sum(dfg, "x", "w", "g")
