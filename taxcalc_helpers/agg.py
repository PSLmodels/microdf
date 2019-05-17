import pandas as pd
import taxcalc_helpers as tch

def agg(base, reform, groupby, metrics):
    """ Aggregates differences between base and reform.

    Args:
        base: Base DataFrame. Index must match reform.
        reform: Reform DataFrame. Index must match base.
        groupby: Variable in base to group on.
        metrics: List of variables to agg and calculate the % change of.

    Returns:
        DataFrame with groupby and metrics, and _pctchg metrics.
    """
    groupby = listify(groupby)
    metrics = listify(metrics)
    metrics_m = [i + '_m' for i in metrics]
    combined = base[groupby + metrics_m].join(
        reform[metrics_m], lsuffix='_base', rsuffix='_reform')
    for i in metrics:
        combined[i + '_pctchg'] = (
            combined[i + '_m_reform'] / combined[i + '_m_base'] - 1)
    return combined
