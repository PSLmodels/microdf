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
    return base[base_cols + cols].join(
        reform[reform_cols + cols],
        lsuffix='_base', rsuffix='_reform')

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
    groupby = tch.listify(groupby)
    metrics = tch.listify(metrics)
    metrics_m = [i + '_m' for i in metrics]
    combined = base[groupby + metrics_m].join(
        reform[metrics_m], lsuffix='_base', rsuffix='_reform')
    
    for i in metrics:
        combined[i + '_pctchg'] = (
            combined[i + '_m_reform'] / combined[i + '_m_base'] - 1)
    return combined
