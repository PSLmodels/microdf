import pytest
import microdf as mdf
import pandas as pd


def test_cartesian_product():
    res = cartesian_product({'a': [1, 2, 3],
                             'b': ['val1', 'val2'],
                             'c': [100, 101]})
    EXPECTED = pd.DataFrame({'a': [1, 1, 1, 1, 2, 2, 2, 2,
                                   3, 3, 3, 3]
                             'b': ['val1', 'val1', 'val2', 'val2',
                                   'val1', 'val1', 'val2', 'val2',
                                   'val1', 'val1', 'val2', 'val2'],
                             'c': [100, 101, 100, 101, 100, 101,
                                   100, 101, 100, 101, 100, 101]})
    pd.testing.assert_frame_equal(res, EXPECTED)


   
