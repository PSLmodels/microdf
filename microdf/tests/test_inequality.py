import pytest
import microdf as mdf

def test_top_pct():
    x = list(range(1, 11))  # 1 to 10. Sum = 10 * 9 / 2 = 45.
    assert mdf.top_10_pct_share(x) == 10 / 45
