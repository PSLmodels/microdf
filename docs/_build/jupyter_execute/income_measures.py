# Income measures

## Setup

import numpy as np
import pandas as pd

import taxcalc as tc
import microdf as mdf

tc.__version__

## Load data

Start with a `DataFrame` with `expanded_income` and the variables in `expanded_income` excluded from `tpc_eci`.

df = mdf.calc_df(group_vars=['expanded_income', 'wic_ben', 'housing_ben', 
                             'vet_ben', 'mcare_ben', 'mcaid_ben'],
                 metric_vars=['XTOT'])

Calculate `tpc_eci`.

df['tpc_eci'] = mdf.tpc_eci(df)

df.head()