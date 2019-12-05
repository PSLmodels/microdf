import microdf as mdf
import pytest
import taxcalc as tc


def test_calc_df():
    df = mdf.calc_df()


def test_static_baseline_calc():
    recs = tc.Records.cps_constructor()
    calc = mdf.static_baseline_calc(recs, 2020)
