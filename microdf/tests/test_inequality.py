import pytest
import microdf as mdf

def test_top_pct():
    x = list(range(1, 11))  # 1 to 10. Sum = 10 * 11 / 2 = 55.
    assert mdf.top_10_pct_share(x) == 10 / 55
