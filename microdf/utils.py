import numpy as np
import pandas as pd
import microdf as mdf
import collections


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
    """ Produces a DataFrame as a Cartesian product of dictionary
        keys and values.
    
    Args:
        d: Dictionary where each item's key corresponds to a column
           name, and each value is a list of values.
    
    Returns:
        DataFrame with a Cartesian product of each dictionary item.
    """
    index = pd.MultiIndex.from_product(d.values(), names=d.keys())
    return pd.DataFrame(index=index).reset_index()
