import numpy as np
import pandas as pd

import microdf as mdf


def gini(x, w=None, negatives=None):
    """Calculates Gini index.

    :param x: A float numpy array of data to calculate Gini index on.
    :param w: An optional float numpy array of weights. Should be the same
        length as x. (Default value = None)
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
    x = np.array(x).astype("float")
    if negatives == "zero":
        x[x < 0] = 0
    if negatives == "shift" and np.amin(x) < 0:
        x -= np.amin(x)
    if w is not None:
        w = np.array(w).astype("float")
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


def top_x_pct_share(val, top_x_pct, w=None):
    """Calculates top x% share.

    :param val: Value (list-like).
    :param top_x_pct: Decimal between 0 and 1 of the top %, e.g. 0.1, 0.001.
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the top x%.

    """
    val = pd.Series(val)
    if w is None:
        w = np.ones(val.size)
    w = pd.Series(w)
    threshold = mdf.weighted_quantile(val, 1 - top_x_pct, w)
    filt = val >= threshold
    top_x_pct_sum = (val[filt] * w[filt]).sum()
    total_sum = (val * w).sum()
    return top_x_pct_sum / total_sum


def bottom_x_pct_share(val, bottom_x_pct, w=None):
    """Calculates bottom x% share.

    :param val: Value (list-like).
    :param bottom_x_pct: Decimal between 0 and 1 of the bottom %, e.g. 0.1,
        0.001.
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the bottom x%.

    """
    return 1 - top_x_pct_share(val, 1 - bottom_x_pct, w, top=False)


def bottom_50_pct_share(val, w=None):
    """Calculates bottom 50% share.

    :param val: Value (list-like).
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the bottom 50%.

    """
    return bottom_x_pct_share(val, 0.5, w)


def top_50_pct_share(val, w=None):
    """Calculates top 50% share.

    :param val: Value (list-like).
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the top 50%.

    """
    return top_x_pct_share(val, 0.5, w)


def top_10_pct_share(val, w=None):
    """Calculates top 10% share.

    :param val: Value (list-like).
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the top 10%.

    """
    return top_x_pct_share(val, 0.1, w)


def top_1_pct_share(val, w=None):
    """Calculates top 1% share.

    :param val: Value (list-like).
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the top 1%.

    """
    return top_x_pct_share(val, 0.01, w)


def top_0_1_pct_share(val, w=None):
    """Calculates top 0.1% share.

    :param val: Value (list-like).
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the top 0.1%.

    """
    return top_x_pct_share(val, 0.001, w)


def t10_b50(val, w=None):
    """Calculates ratio between the top 10% and bottom 50% shares.

    :param val: Value (list-like).
    :param w: Weight (list-like, same length as val). (Default value = None)
    :returns: The share of w-weighted val held by the top 10% divided by
        the share of w-weighted val held by the bottom 50%.

    """
    return top_10_pct_share(val, w) / bottom_50_pct_share(val, w)
