import numpy as np
import pandas as pd
import microdf as mdf
import collections


def fpl(XTOT):
    """Calculates the federal poverty guideline for a household of a certain size.

    Args:
        XTOT: The number of people in the household.

    Returns:
        The federal poverty guideline for the contiguous 48 states.
    """
    return 7820 + 4320 * XTOT


def weight(df, col, w):
    """Calculates the weighted value of a column in a DataFrame.

    Args:
        df: A pandas DataFrame.
        col: A string indicating the column in the DataFrame to weight.
        w: Weight column.

    Returns:
        A pandas Series multiplying the column by its weight.
    """
    return df[col] * df[w]


def weighted_sum(df, col, w):
    """Calculates the weighted sum of a column in a DataFrame.

    Args:
        df: A pandas DataFrame.
        col: A string indicating the column in the DataFrame.
        w: Weight column.

    Returns:
        The weighted sum of a DataFrame's column.
    """

    return (df[col] * df[w]).sum()


def weighted_mean(df, col, w):
    """Calculates the weighted mean of a column in a DataFrame.

    Args:
        df: A pandas DataFrame.
        col: A string indicating the column in the DataFrame.
        w: Weight column.

    Returns:
        The weighted mean of a DataFrame's column.
    """
    return weighted_sum(df, col, w) / df[w].sum()


def add_weighted_quantiles(df, col, w):
    """Adds weighted quantiles of a column to a DataFrame.

    Adds columns for each of these types of quantiles to a DataFrame:
    * *_percentile_exact: Exact percentile.
    * *_percentile: Integer percentile (ceiling).
    * *_2percentile: Integer percentile (ceiling, for each two percentiles).
    * *_ventile: Integer percentile (ceiling, for each five percentiles).
    * *_decile: Integer decile.
    * *_quintile: Integer quintile.
    * *_quartile: Integer quartile.

    Negative values are assigned -1.
    
    Args:
        df: A pandas DataFrame.
        col: A string indicating the column in the DataFrame to calculate.
        w: Weight column.

    Returns:
        Nothing. Columns are added in place.
    """
    df.sort_values(by=col, inplace=True)
    col_pctile = col + '_percentile_exact'
    df[col_pctile] = 100 * df[w].cumsum() / df[w].sum()
    # "Null out" negatives using -1, since integer arrays can't be NaN.
    # TODO: Should these be null floats?
    df[col_pctile] = np.where(df[col] >= 0, df[col_pctile], 0)
    # Reduce top record, otherwise it's incorrectly rounded up.
    df[col_pctile] = np.where(df[col_pctile] >= 99.99999, 99.99999,
                              df[col_pctile])
    df[col + '_percentile'] = np.ceil(df[col_pctile]).astype(int)
    df[col + '_2percentile'] = 2 * np.ceil(df[col_pctile] / 2).astype(int)
    df[col + '_ventile'] = 5 * np.ceil(df[col_pctile] / 5).astype(int)
    df[col + '_decile'] = np.ceil(df[col_pctile] / 10).astype(int)
    df[col + '_quintile'] = np.ceil(df[col_pctile] / 20).astype(int)
    df[col + '_quartile'] = np.ceil(df[col_pctile] / 25).astype(int)


def weighted_quantile(values, quantiles, sample_weight=None, 
                      values_sorted=False, old_style=False):
    """ Very close to numpy.percentile, but supports weights.
    
    From https://stackoverflow.com/a/29677616/1840471.
    
    Args:
        values: numpy array with data.
        quantiles: array-like with many quantiles needed ([0, 1]).
        sample_weight: array-like of the same length as `array`.
        values_sorted: bool, if True, then will avoid sorting of
            initial array
        old_style: if True, will correct output to be consistent
            with numpy.percentile.
    
    Returns:
        numpy.array with computed quantiles.
    """
    values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    assert np.all(quantiles >= 0) and np.all(quantiles <= 1), \
        'quantiles should be in [0, 1]'
    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]
    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    if old_style:
        # To be convenient with numpy.percentile
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]
    else:
        weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)


def ordinal_label(n):
    """ Creates ordinal label from number.

    Adapted from https://stackoverflow.com/a/20007730/1840471.
    
    Args:
        n: Number.
    
    Returns:
        Ordinal label, e.g., 1st, 3rd, 24th, etc.
    """
    n = int(n)
    return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])


def quantile_chg(v1, v2, w1=None, w2=None, q=np.arange(0.1, 1, 0.1)):
    """ Create table with two sets of quantiles.

    Args:
        v1: First set of values.
        v2: Second set of values.
        w1: First set of weights. Defaults to equal weight.
        w2: Second set of weights. Defaults to equal weight.
        q: Quantiles. Defaults to decile boundaries.

    Returns:
        DataFrame with two rows and a column for each quantile.
        Column labels are "xth percentile" and a label is added
        to the median.
    """ 
    q1 = weighted_quantile(v1, q, w1)
    q2 = weighted_quantile(v2, q, w2)
    df = pd.DataFrame([q1, q2])
    # Set decile labels.
    q_print = [ordinal_label((i * 100)) for i in q]
    # TODO: Check if other values are median
    if q[4] == 0.5:
        q_print[4] += ' (median)'
    df.columns = q_print
    return df


def weighted_median(df, col, w):
    """Calculates the weighted median of a column in a DataFrame.

    Args:
        df: A pandas DataFrame containing Tax-Calculator data.
        col: A string indicating the column in the DataFrame.
        w: Weight column.

    Returns:
        The weighted median of a DataFrame's column.
    """
    return weighted_quantile(df[col], 0.5, df[w])


def dedup_list(l):
    """ Remove duplicate items from a list.
    
    Args:
        l: List.

    Returns:
        List with duplicate items removed from l.
    """
    return list(set(l))

    
def listify(x, dedup=True):
    """ Return x as a list, if it isn't one already.

    Args:
        x: A single item or a list.
   
    Returns:
        x if x is a list, otherwise [x]. Also flattens the list
            and removes Nones.
    """
    if not isinstance(x, list):
        x = [x]
    res = flatten(x)
    res = [x for x in res if x is not None]
    if dedup:
        return dedup_list(res)
    return res


def flatten(l):
    """ Flatten list. From https://stackoverflow.com/a/2158532/1840471.

    Args:
        l: List.
    
    Returns:
        Flattened version.
    """
    for el in l:
        if isinstance(el, collections.abc.Iterable) \
           and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def cartesian_product(d):
    # Produces a DataFrame as a Cartesian product of dictionary
    # keys and values.
    #
    # Args:
    #     d: Dictionary where each item's key corresponds to a column
    #        name, and each value is a list of values.
    #
    # Returns:
    #     DataFrame with a Cartesian product of each dictionary item.
    index = pd.MultiIndex.from_product(d.values(), names=d.keys())
    return pd.DataFrame(index=index).reset_index()
