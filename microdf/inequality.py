import numpy as np
import pandas as pd

import microdf as mdf


def gini(df, col, w=None, negatives=None):
    """Calculates Gini index.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param w: Column representing weight in df.
    :param negatives: An optional string indicating how to treat negative
        values of x:
        'zero' replaces negative values with zeroes.
        'shift' subtracts the minimum value from all values of x,
        when this minimum is negative. That is, it adds the absolute
        minimum value.
        Defaults to None, which leaves negative values as they are.
    :returns: A float, the Gini index.

    """
    # Requires float numpy arrays (not pandas Series or lists) to work.
    x = np.array(df[col]).astype("float")
    if negatives == "zero":
        x[x < 0] = 0
    if negatives == "shift" and np.amin(x) < 0:
        x -= np.amin(x)
    if w is not None:
        w = np.array(df[w]).astype("float")
        sorted_indices = np.argsort(x)
        sorted_x = x[sorted_indices]
        sorted_w = w[sorted_indices]
        cumw = np.cumsum(sorted_w)
        cumxw = np.cumsum(sorted_x * sorted_w)
        return np.sum(cumxw[1:] * cumw[:-1] - cumxw[:-1] * cumw[1:]) / (
            cumxw[-1] * cumw[-1]
        )
    else:
        sorted_x = np.sort(x)
        n = len(x)
        cumxw = np.cumsum(sorted_x)
        # The above formula, with all weights equal to 1 simplifies to:
        return (n + 1 - 2 * np.sum(cumxw) / cumxw[-1]) / n


def top_x_pct_share(df, col, top_x_pct, w=None):
    """Calculates top x% share.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param top_x_pct: Decimal between 0 and 1 of the top %, e.g. 0.1, 0.001.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the top x%.

    """
    threshold = mdf.weighted_quantile(df, col, w, 1 - top_x_pct)
    top_x_pct_sum = mdf.weighted_sum(df[df[col] >= threshold], col, w)
    total_sum = mdf.weighted_sum(df, col, w)
    return top_x_pct_sum / total_sum


def bottom_x_pct_share(df, col, bottom_x_pct, w=None):
    """Calculates bottom x% share.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param bottom_x_pct: Decimal between 0 and 1 of the top %, e.g. 0.1, 0.001.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the bottom x%.

    """
    return 1 - top_x_pct_share(df, col, 1 - bottom_x_pct, w, top=False)


def bottom_50_pct_share(df, col, w=None):
    """Calculates bottom 50% share.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the bottom 50%.

    """
    return bottom_x_pct_share(df, col, 0.5, w)


def top_50_pct_share(df, col, w=None):
    """Calculates top 50% share.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the top 50%.

    """
    return top_x_pct_share(df, col, 0.5, w)


def top_10_pct_share(df, col, w=None):
    """Calculates top 10% share.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the top 10%.

    """
    return top_x_pct_share(df, col, 0.1, w)


def top_1_pct_share(df, col, w=None):
    """Calculates top 1% share.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the top 1%.

    """
    return top_x_pct_share(df, col, 0.01, w)


def top_0_1_pct_share(df, col, w=None):
    """Calculates top 0.1% share.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the top 0.1%.

    """
    return top_x_pct_share(df, col, 0.001, w)


def t10_b50(df, col, w=None):
    """Calculates ratio between the top 10% and bottom 50% shares.

    :param df: DataFrame.
    :param col: Name of column in df representing value.
    :param w: Column representing weight in df.
    :returns: The share of w-weighted val held by the top 10% divided by
        the share of w-weighted val held by the bottom 50%.

    """
    return top_10_pct_share(df, col, w) / bottom_50_pct_share(df, col, w)
