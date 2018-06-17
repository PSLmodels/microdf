import numpy as np
import pandas as pd
import taxcalc as tc

def gini(x, w=None, zero_negatives=True):
    """Calculates Gini index.

    Args:
        x: A float numpy array of data to calculate Gini index on.
        w: An optional float numpy array of weights. Should be the same length as x.
        zero_negatives: An optional boolean indicating whether negative values of x
            should be replaced with zeroes. Defaults to True.

    Returns:
        A float, the Gini index.
    """
    # Requires float numpy arrays (not pandas Series or lists) to work.
    x = np.array(x).astype('float')
    if zero_negatives:
        x[x < 0] = 0
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


def fpl(XTOT):
    """Calculates the federal poverty guideline for a household of a certain size.

    Args:
        XTOT: The number of people in the household.

    Returns:
        The federal poverty guideline for the contiguous 48 states.
    """
    return 7820 + 4320 * XTOT

def weight(df, col):
    """Calculates the weighted value of a column in a Tax-Calculator pandas DataFrame.

    Args:
        df: A pandas DataFrame containing Tax-Calculator data.
        col: A string indicating the column in the DataFrame to weight.

    Returns:
        A pandas Series multiplying the column by its weight (s006).
    """
    return df[col] * df.s006

def weighted_sum(df, col):
    """Calculates the weighted sum of a column in a Tax-Calculator pandas DataFrame.

    Args:
        df: A pandas DataFrame containing Tax-Calculator data.
        col: A string indicating the column in the DataFrame.

    Returns:
        The s006-weighted sum of a DataFrame's column.
    """

    return (df[col] * df.s006).sum()
    
def weighted_mean(df, col):
    """Calculates the weighted mean of a column in a Tax-Calculator pandas DataFrame.

    Args:
        df: A pandas DataFrame containing Tax-Calculator data.
        col: A string indicating the column in the DataFrame.

    Returns:
        The s006-weighted mean of a DataFrame's column.
    """
    return weighted_sum(df, col) / df.s006.sum()

def add_weighted_quantiles(df, col):
    """Adds weighted quantiles of a column to a Tax-Calculator pandas DataFrame.

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
        df: A pandas DataFrame containing Tax-Calculator data.
        col: A string indicating the column in the DataFrame to calculate.

    Returns:
        Nothing. Columns are added in place.
    """
    df.sort_values(by=col, inplace=True)
    col_pctile = col + '_percentile_exact'
    df[col_pctile] = 100 * df.s006.cumsum() / df.s006.sum()
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

def static_baseline_calc(recs, year):
    """Creates a static Calculator object.

    Args:
        recs: Records object.
        year: Year to advance to.

    Returns:
        Calculator object.
    """
    calc = tc.Calculator(records=recs, policy=tc.Policy())
    calc.advance_to_year(year)
    calc.calc_all()
    return calc

def add_weighted_metrics(df, metric_vars):
    """Adds s006-weighted metrics in millions to a Tax-Calculator pandas DataFrame.

    Columns are renamed to *_m.

    Args:
        df: A pandas DataFrame containing Tax-Calculator data.
        metric_vars: A list of column names to weight.

    Returns:
        Nothing. Weighted columns are added in place.
    """
    df['s006_m'] = df.s006 / 1e6
    for metric_var in metric_vars:
        df[metric_var + '_m'] = df[metric_var] * df.s006_m

def calc_df(records=None,
            policy=None,
            year=2018,
            reform=None,
            group_vars=None,
            metric_vars=None):
    """Creates a pandas DataFrame for given Tax-Calculator data.
    
    s006 is always included, and RECID is used as an index.

    Args:
        records: An optional Records object. If not provided, uses CPS records.
        policy: An optional Policy object. If not provided, uses default Policy.
        year: An optional year to advance to. If not provided, defaults to 2018.
        reform: An optional reform to implement for the Policy object.
        group_vars: An optional list of column names to include in the DataFrame.
        metric_vars: An optional list of column names to include and calculate
             weighted sums of (in millions named as *_m) in the DataFrame.

    Returns:
        A pandas DataFrame.
    """
    # Assign defaults.
    if records is None:
        records = tc.Records.cps_constructor()
    if policy is None:
        policy = tc.Policy()
    if reform is not None:
        policy.implement_reform(reform)
    # Calculate.
    calc = tc.Calculator(records=records, policy=policy, verbose=False)
    calc.advance_to_year(year)
    calc.calc_all()
    # Get a deduplicated list of all columns.
    all_cols = list(set(['RECID', 's006'] + group_vars + metric_vars))
    df = calc.dataframe(all_cols)
    # Add calculated columns for metrics.
    add_weighted_metrics(df, metric_vars)
    # Set RECID to int and set it as index before returning.
    df['RECID'] = df.RECID.map(int)
    return df.set_index('RECID')
