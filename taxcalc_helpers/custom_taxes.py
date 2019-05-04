"""Fucntions and data for estimating taxes outside the income tax system.
   Examples include value added tax, financial transaction tax, and carbon tax."""

import numpy as np
import pandas as pd
import taxcalc_helpers as tch

# Source: https://www.taxpolicycenter.org/briefing-book/who-would-bear-burden-vat
VAT_INCIDENCE = pd.Series(
        index=[-1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 99.9],
        data=[3.9, 3.9, 3.6, 3.6, 3.6, 3.6, 3.6, 3.4, 3.4, 3.2, 2.8, 2.5, 2.5])
VAT_INCIDENCE /= 100

# Source: Table 5 in https://www.treasury.gov/resource-center/tax-policy/tax-analysis/Documents/WP-115.pdf
CARBON_TAX_INCIDENCE = pd.Series(
        index=[-1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 99.9],
        data=[0.8, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.8, 1.8, 1.8, 1.6, 1.4, 0.7])
CARBON_TAX_INCIDENCE /= 100

# Source: Figure 1 in https://www.taxpolicycenter.org/sites/default/files/alfresco/publication-pdfs/2000587-financial-transaction-taxes.pdf
FTT_INCIDENCE = pd.Series(
        index=[-1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 99.9],
        data=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.4, 0.8, 1.0])
FTT_INCIDENCE /= 100


def add_custom_tax(df, segment_income, w, base_income, incidence, prefix):
    """Add a custom tax based on incidence analysis driven by percentiles.

    Args:
        df: DataFrame.
        segment_income: Income measure used to segment tax units into quantiles.
        w: Weight used to segment into quantiles (either s006 or XTOT_m).
        base_income: Income measure by which incidence is multiplied to estimate
            liability.
        incidence: pandas Series indexed on the floor of an income percentile,
            with values for the tax rate.
        prefix: Prefix for columns added.

    Returns:
        Nothing. Adds two columns to df:
        * [prefix]_incidence: Rate.
        * [prefix]_liability: Rate * base_income.
        df is also sorted by segment_income.
    """
    df.sort_values(segment_income, inplace=True)
    income_percentile = 100 * df[w].cumsum() / df[w].sum()
    df[prefix + 'incidence'] = incidence.iloc[
        pd.cut(income_percentile,
               # Add a right endpoint. Should be 100 but sometimes a decimal gets added.
               bins=incidence.index.tolist() + [101],
               labels=False)].values
    df[prefix + '_liability'] = df[prefix + '_incidence'] * df[base_income]
    

def add_vat(df):
    """Add value added tax based on incidence estimate from Tax Policy Center.
    
    Args:
        df: DataFrame with columns for tpc_eci, XTOT_m, and aftertax_income.

    Returns:
        Nothing. Adds two columns to df:
        * vat_incidence: Rate.
        * vat_liability: Rate * aftertax_income.
        df is also sorted by tpc_eci.
    """
    add_custom_tax(df, 'tpc_eci', 'XTOT_m', 'aftertax_income', VAT_INCIDENCE, 'vat')


def add_carbon_tax(df):
    """Add carbon tax based on incidence estimate from the US Treasury Department.
    
    Args:
        df: DataFrame with columns for tpc_eci, XTOT_m, and aftertax_income.

    Returns:
        Nothing. Adds two columns to df:
        * carbon_tax_incidence: Rate.
        * carbon_tax_liability: Rate * aftertax_income.
        df is also sorted by tpc_eci.
    """
    add_custom_tax(df, 'tpc_eci', 'XTOT_m', 'aftertax_income',
                   CARBON_TAX_INCIDENCE, 'carbon_tax')

    
def add_ftt(df):
    """Add financial transaction tax based on incidence estimate from Tax Policy Center.
    
    Args:
        df: DataFrame with columns for tpc_eci, XTOT_m, and aftertax_income.

    Returns:
        Nothing. Adds two columns to df:
        * ftt_incidence: Rate.
        * ftt_liability: Rate * aftertax_income.
        df is also sorted by tpc_eci.
    """
    add_custom_tax(df, 'tpc_eci', 'XTOT_m', 'aftertax_income', FTT_INCIDENCE, 'ftt')
