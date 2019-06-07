import pandas as pd
import taxcalc_helpers as tch

def combine_base_reform(base, reform, base_cols=None,
                        cols=None, reform_cols=None):
    """ Combine base and reform with certain columns.
    
    Args:
        base: Base DataFrame. Index must match reform.
        reform: Reform DataFrame. Index must match base.
        base_cols: Columns in base to keep.
        cols: Columns to keep from both base and reform.
        reform_cols: Columns in reform to keep.
    
    Returns:
        DataFrame with columns for base ("_base") and 
            reform ("_reform").
    """
    all_base_cols = tch.listify([base_cols] + [cols])
    all_reform_cols = tch.listify([reform_cols] + [cols])
    return base[all_base_cols].join(reform[all_reform_cols],
                                    lsuffix='_base',
                                    rsuffix='_reform')


def pctchg_base_reform(combined, metric):
    """ Calculates the percentage change in a metric for a combined
        dataset.

    Args:
        combined: Combined DataFrame with _base and _reform columns.
        metric: String of the column to calculate the difference.
                Must exist as metric_m_base and metric_m_reform in combined.

    Returns:
        Series with percentage change.
    """
    return combined[metric + '_m_reform'] / combined[metric + '_m_base'] - 1


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
    metrics_m = [i + '_m' for i in tch.listify(metrics)]
    combined = combine_base_reform(base, reform,
                                   base_cols=groupby, cols=metrics_m)
    grouped = combined.groupby(groupby).sum()
    for metric in metrics:
         grouped[metric + '_pctchg'] = pctchg_base_reform(grouped, metric)
    return grouped
