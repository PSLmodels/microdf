# The `agg` function

Use `agg` to see the effect of a $10,000 UBI by marital status.

## Setup

import numpy as np
import pandas as pd

import taxcalc as tc
import microdf as mdf

tc.__version__

## Load data

Start with a standard `DataFrame`, then add a UBI manually in a reform copy.

base = mdf.calc_df(group_vars=['expanded_income', 'MARS', 'XTOT'],
                   metric_vars='aftertax_income')

reform = base.copy(deep=True)
UBI_PP = 10000
reform['ubi'] = reform.XTOT * UBI_PP
reform['aftertax_income'] = reform.aftertax_income + reform.ubi
mdf.add_weighted_metrics(reform, 'aftertax_income')

## `agg`

### Change in aftertax income by marital status.

mdf.agg(base, reform, 'MARS', 'aftertax_income')

### Also sum baseline `expanded_income`

mdf.agg(base, reform, 'MARS', 'aftertax_income', 'expanded_income')

### Also sum UBI amount

mdf.add_weighted_metrics(reform, 'ubi')  # Creates ubi_m = ubi * s006 / 1e6.

mdf.agg(base, reform, 'MARS', 'aftertax_income', reform_metrics='ubi_m')