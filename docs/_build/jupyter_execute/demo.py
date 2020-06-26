# `microdf` demo

## Setup

import numpy as np
import pandas as pd

import taxcalc as tc
import microdf as mdf

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

Chart options.

mdf.set_plot_style()

## Generate data

base = mdf.calc_df(group_vars=['expanded_income', 'MARS'],
                   metric_vars=['aftertax_income', 'XTOT'])

base.columns

Define a reform that treats capital gains as ordinary income and sets the top marginal rate to 70%.

CG_REFORM = {
    'CG_nodiff': {2019: True},
    'II_rt7': {2019: 0.7}
}

reform = mdf.calc_df(reform=CG_REFORM, group_vars=['MARS'], group_n65=True, 
                     metric_vars=['aftertax_income', 'XTOT'])

reform.columns

### Calculate senior UBI.

Start with total revenue ($ billions).

new_rev_m = base.aftertax_income_m.sum() - reform.aftertax_income_m.sum()
new_rev_m / 1e3

How many seniors are there?

mdf.add_weighted_metrics(reform, 'n65')

n65_total_m = reform.n65_m.sum()
n65_total_m

Divide.

senior_ubi = new_rev_m / reform.n65_m.sum()
senior_ubi

### Add senior UBI to `aftertax_income` and recalculate

reform['ubi'] = senior_ubi * reform.n65
reform['aftertax_income'] = reform.aftertax_income + reform.ubi
mdf.add_weighted_metrics(reform, 'aftertax_income')

np.allclose(base.aftertax_income_m.sum(), reform.aftertax_income_m.sum())

## Analyze

Gini, FPL, distributional impact chart

### Change to Gini index

mdf.gini(base.aftertax_income, base.s006)

mdf.gini(reform.aftertax_income, reform.s006)

### Change to poverty rate

Add federal poverty line with `mdf.fpl`.

base['fpl'] = mdf.fpl(base.XTOT)
reform['fpl'] = mdf.fpl(reform.XTOT)

base['fpl_XTOT_m'] = np.where(base.aftertax_income < base.fpl,
                              base.XTOT_m, 0)
reform['fpl_XTOT_m'] = np.where(reform.aftertax_income < reform.fpl,
                                reform.XTOT_m, 0)

reform.fpl_XTOT_m.sum() / base.fpl_XTOT_m.sum() - 1

Add chart.

ax = mdf.quantile_chg_plot(base.aftertax_income, reform.aftertax_income,
                           base.XTOT_m, reform.XTOT_m)

