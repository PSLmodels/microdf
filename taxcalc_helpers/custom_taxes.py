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
