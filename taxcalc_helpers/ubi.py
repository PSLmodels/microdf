import numpy as np
import pandas as pd
import taxcalc_helpers as tch

def ubi_or_bens(df, ben_cols, max_ubi='max_ubi', ubi='ubi', bens='bens'):
    """Calculates whether a tax unit will take UBI or benefits,
       and adjusts values accordingly.

    Args:
        df: DataFrame.
        ben_cols: List of columns for benefits.
        max_ubi: Column name of the maximum UBI, before accounting
            for benefits. Defaults to 'max_ubi'.
        ubi: Column name to add representing the UBI. Defaults to 'ubi'.
        bens: Column name to add representing total benefits (after adjustment).
            Defaults to 'bens'.

    Returns:
        Nothing. Benefits in ben_cols are adjusted, and ubi and bens columns
        are added.
    """
    bens = df[ben_cols].sum(axis=1)
    take_ubi = base[max_ubi] > base.bens
    df[ubi] = np.where(take_ubi, base[max_ubi], 0)
    df[ben_cols] *= np.where(take_ubi, 0, 1)
    df[bens] = df[ben_cols].sum(axis=1)

    
    
