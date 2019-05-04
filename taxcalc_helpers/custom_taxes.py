"""Fucntions and data for estimating taxes outside the income tax system.
   Examples include value added tax, financial transaction tax, and carbon tax."""

import numpy as np
import pandas as pd
import taxcalc_helpers as tch

# TODO: Make these separate and then create a function to merge them.
INCIDENCE = pd.DataFrame({
    'income_percentile_floor': [-1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 99.9],
    # Source: https://www.taxpolicycenter.org/briefing-book/who-would-bear-burden-vat
    'vat': [3.9, 3.9, 3.6, 3.6, 3.6, 3.6, 3.6, 3.4, 3.4, 3.2, 2.8, 2.5, 2.5],
    # Source: Table 5 in https://www.treasury.gov/resource-center/tax-policy/tax-analysis/Documents/WP-115.pdf
    'carbon_tax': [0.8, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.8, 1.8, 1.8, 1.6, 1.4, 0.7],
    # Source: Figure 1 in https://www.taxpolicycenter.org/sites/default/files/alfresco/publication-pdfs/2000587-financial-transaction-taxes.pdf
    'ftt': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.4, 0.8, 1.0]
})

INCIDENCE[['vat', 'carbon_tax', 'ftt']] /= 100


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
        * [prefix]_tax_incidence: Rate.
        * [prefix]_tax_liability: Rate * base_income.
        df is also sorted by segment_income.
    """
    df.sort_values(segment_income, inplace=True)
    income_percentile = 100 * df[w].cumsum() / df[w].sum()
    df[prefix + '_tax_incidence'] = incidence[
        pd.cut(income_percentile,
               bins=incidence.index.tolist() + [100],
               labels=False)].values
    df[prefix + '_tax_liability'] = df[prefix + '_tax_incidence'] * df[base_income]
    

def add_carbon_tax(df, incidence=INCIDENCE):
    """Estimate carbon tax liability.

    Args:
        df: DataFrame with tpc_eci and XTOT_m columns. Use TPC methodology to
            align with their incidence estimate.
        incidence: DataFrame with income_percentile_floor and carbon_tax columns.

    Returns:
        Nothing. Two columns are added:
        * carbon_tax_incidence: Share of income.
        * carbon_tax_liability: Liability (carbon_tax_incidence * aftertax_income).
        It also sorts df by tpc_eci as part of the calculation.
    """
    df.sort_values('tpc_eci', inplace=True)
    income_percentile = df.XTOT_m.cumsum() / df.XTOT_m.sum()
    df['carbon_tax_incidence'] = INCIDENCE.vat[
        pd.cut(income_percentile,
               bins=INCIDENCE.income_percentile_floor.tolist() + [100],
               labels=False)].values
    df['carbon_tax_liability'] = df.carbon_tax_incidence * df.aftertax_income
