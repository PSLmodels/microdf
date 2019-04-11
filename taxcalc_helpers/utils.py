import numpy as np
import pandas as pd
import taxcalc as tc

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

def n65(age_head, age_spouse, elderly_dependents):
    """Calculates number of people in the tax unit age 65 or older.

    Args:
        age_head: Series representing age_head from taxcalc data.
        age_spouse: Series representing age_spouse from taxcalc data.
        elderly_dependents: Series representing elderly_dependents from taxcalc data.

    Returns:
        Series representing the number of people age 65 or older.
    """
    return ((age_head >= 65).astype(int) +
            (age_spouse >= 65).astype(int) +
            elderly_dependents)
        
def calc_df(records=None,
            policy=None,
            year=2018,
            reform=None,
            group_vars=None,
            metric_vars=None,
            group_n65=False):
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
    if group_n65:
        group_vars = group_vars + ['age_head', 'age_spouse', 'elderly_dependents']
    all_cols = list(set(['RECID', 's006'] + group_vars + metric_vars))
    df = calc.dataframe(all_cols)
    if group_n65:
        df['n65'] = n65(df.age_head, df.age_spouse, df.elderly_dependents)
        df.drop(['age_head', 'age_spouse', 'elderly_dependents'], axis=1, inplace=True)
    # Add calculated columns for metrics.
    add_weighted_metrics(df, metric_vars)
    # Set RECID to int and set it as index before returning.
    df['RECID'] = df.RECID.map(int)
    return df.set_index('RECID')

def cash_income(df):
    """Calculates income after taxes and cash transfers.

    Defined as aftertax_income minus non-cash benefits.

    Args:
        df: A Tax-Calculator pandas DataFrame with columns for
            * aftertax_income
            * snap_ben
            * 
    
    Returns:
        A pandas Series with the cash income for each row in df.
    """
    # Constants for share of each benefit that is cash.
    HOUSING_CASH_SHARE = 0.
    MCAID_CASH_SHARE = 0.
    MCARE_CASH_SHARE = 0.
    # https://github.com/open-source-economics/taxdata/issues/148
    # https://docs.google.com/spreadsheets/d/1g_YdFd5idgLL764G0pZBiBnIlnCBGyxBmapXCOZ1OV4
    OTHER_CASH_SHARE = 0.35
    SNAP_CASH_SHARE = 0.
    SSI_CASH_SHARE = 1.
    TANF_CASH_SHARE = 0.25
    # https://github.com/open-source-economics/C-TAM/issues/62.
    VET_CASH_SHARE = 0.48
    WIC_CASH_SHARE = 0.
    return (df.aftertax_income -
            (1 - HOUSING_CASH_SHARE) * df.housing_ben -
            (1 - MCAID_CASH_SHARE) * df.mcaid_ben -
            (1 - MCARE_CASH_SHARE) * df.mcare_ben -
            (1 - OTHER_CASH_SHARE) * df.other_ben -
            (1 - SNAP_CASH_SHARE) * df.snap_ben -
            (1 - SSI_CASH_SHARE) * df.ssi_ben -
            (1 - TANF_CASH_SHARE) * df.tanf_ben -
            (1 - VET_CASH_SHARE) * df.vet_ben -
            (1 - WIC_CASH_SHARE) * df.wic_ben)

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
    q_print = [ordinal_label((i * 10)) for i in q]
    # TODO: Check if other values are median
    if q[4] == 0.5:
        q_print[4] += ' (median)'
    df.columns = q_print
    return df
