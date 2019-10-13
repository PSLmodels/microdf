import numpy as np
import pandas as pd
import microdf as mdf


def gini(x, w=None, negatives=None):
    """Calculates Gini index.

    Args:
        x: A float numpy array of data to calculate Gini index on.
        w: An optional float numpy array of weights. Should be the same length as x.
        negatives: An optional string indicating how to treat negative values of x:
                   'zero' replaces negative values with zeroes.
                   'shift' subtracts the minimum value from all values of x, 
                   when this minimum is negative. That is, it adds the absolute minimum value.
                   Defaults to None, which leaves negative values as they are.

    Returns:
        A float, the Gini index.
    """
    # Requires float numpy arrays (not pandas Series or lists) to work.
    x = np.array(x).astype('float')
    if negatives=='zero':
        x[x < 0] = 0
    if negatives=='shift' and np.amin(x) < 0:
        x -= np.amin(x)
    if w is not None:
        w = np.array(w).astype('float')
        sorted_indices = np.argsort(x)
        sorted_x = x[sorted_indices]
        sorted_w = w[sorted_indices]
        cumw = np.cumsum(sorted_w)
        cumxw = np.cumsum(sorted_x * sorted_w)
        return (np.sum(cumxw[1:] * cumw[:-1] - cumxw[:-1] * cumw[1:]) /
                (cumxw[-1] * cumw[-1]))
    else:
        sorted_x = np.sort(x)
        n = len(x)
        cumxw = np.cumsum(sorted_x)
        # The above formula, with all weights equal to 1 simplifies to:
        return (n + 1 - 2 * np.sum(cumxw) / cumxw[-1]) / n


def top_x_pct_share(val, top_x_pct, w=None):
    threshold  = mdf.weighted_quantile(val, 1 - top_x_pct, w)
    top_x_pct_sum = (val[val > threshold] * w[val > threshold]).sum()
    total_sum = (val * w).sum()
    return top_x_pct_sum / total_sum


def bottom_x_pct_share(val, bottom_x_pct, w=None):
    return 1 - top_x_pct_share(val, 1 - bottom_x_pct, w, top=False)


def bottom_50_pct_share(val, w=None):
    return bottom_x_pct_share(val, 0.5, w)


def top_50_pct_share(val, w=None):
    return top_x_pct_share(val, 0.5, w)


def top_10_pct_share(val, w=None):
    return top_x_pct_share(val, 0.1, w)


def top_1_pct_share(val, w=None):
    return top_x_pct_share(val, 0.01, w)


def top_0_1_pct_share(val, w=None):
    return top_x_pct_share(val, 0.001, w)

def t10_b50(val, w=None):
    return top_10_pct_share(val, w) / bottom_50_pct_share(val, w)
