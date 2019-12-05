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


