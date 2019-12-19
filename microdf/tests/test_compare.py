import pandas as pd
import microdf as mdf
import os


def differences(actual, expected, f_actual, f_expected):
    """
    Check for differences between results in afilename and efilename files.
    
    Args:
        f_actual: Filename of the actual CSV.
        f_expected: Filename of the expected CSV.
    """
    if not actual.equals(expected):
        msg = 'COMPARE RESULTS DIFFER\n'
        msg += '-------------------------------------------------\n'
        msg += '--- NEW RESULTS IN {} FILE ---\n'
        msg += '--- if new OK, copy {} to  ---\n'
        msg += '---                 {}     ---\n'
        msg += '---            and rerun test.                ---\n'
        msg += '-------------------------------------------------\n'
        raise ValueError(msg.format(f_actual, f_actual, f_expected))


def test_scf_percentile_agg_compare(tests_path):
    SCF2016 = 'https://www.federalreserve.gov/econres/files/scfp2016s.zip'
    COLS = ['wgt', 'networth']
    df = mdf.read_stata_zip(SCF2016, columns=COLS)
    mdf.add_weighted_quantiles(df, 'networth', 'wgt')
    percentile_sum = df.groupby('networth_percentile')[COLS].sum()
    F_ACTUAL = 'scf_percentile_actual.csv'
    F_EXPECTED = 'scf_percentile_expected.csv'
    percentile_sum.to_csv(os.path.join(tests_path, F_ACTUAL))
    expected = pd.read_csv(os.path.join(tests_path, F_EXPECTED))
    differences(percentile_sum, expected, F_ACTUAL, F_EXPECTED)
