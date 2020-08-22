import microdf as mdf
import pytest

try:
    import taxcalc as tc

    _HAVE_TAXCALC = True
except ImportError:
    _HAVE_TAXCALC = False


def test_calc_df():
    if not _HAVE_TAXCALC:
        pytest.skip("taxcalc is not installed")
    df = mdf.calc_df()


def test_static_baseline_calc():
    if not _HAVE_TAXCALC:
        pytest.skip("taxcalc is not installed")
    recs = tc.Records.cps_constructor()
    calc = mdf.static_baseline_calc(recs, 2020)
