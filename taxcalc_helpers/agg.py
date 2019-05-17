import pandas as pd

def agg(base, reform, groupby, metrics, w='s006'):
    """ Aggregates.

    Args:
        base: Base DataFrame. Index must match reform.
        reform: Reform DataFrame. Index must match base.
        groupby: Variable in base to group on.
        metrics:
        w: Weight column. Defaults to s006.

    Returns:
        DataFrame with groupby and metrics
    """
    combined = base[[groupby] + metrics].join(reform[metrics])
    
