import microdf as mdf

import pandas as pd

df = pd.DataFrame(
    {
        "income": [-10, 0, 10, 20],
        "threshold": [15, 10, 15, 10],
        "weight": [1, 2, 3, 4],
    }
)


def test_poverty_rate():
    # Unweighted
    assert mdf.poverty_rate(df, "income", "threshold") == 3 / 4
    # Weighted
    assert mdf.poverty_rate(df, "income", "threshold", "weight") == 6 / 10


def test_deep_poverty_rate():
    # Unweighted
    assert mdf.deep_poverty_rate(df, "income", "threshold") == 2 / 4
    # Weighted
    assert mdf.deep_poverty_rate(df, "income", "threshold", "weight") == 3 / 10


def test_poverty_gap():
    # Unweighted
    assert mdf.poverty_gap(df, "income", "threshold") == 25 + 10 + 5
    # Weighted
    assert mdf.poverty_gap(df, "income", "threshold", "weight") == (
        25 * 1 + 10 * 2 + 5 * 3
    )


def test_squared_poverty_gap():
    # Unweighted
    assert mdf.squared_poverty_gap(df, "income", "threshold") == (
        25 ** 2 + 10 ** 2 + 5 ** 2
    )
    # Weighted
    assert mdf.squared_poverty_gap(df, "income", "threshold", "weight") == (
        1 * (25 ** 2) + 2 * (10 ** 2) + 3 * (5 ** 2)
    )
