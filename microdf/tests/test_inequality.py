import microdf as mdf


def test_top_pct():
    """ """
    x = list(range(1, 11))  # 1 to 10. Sum = 10 * 11 / 2 = 55.
    assert mdf.top_10_pct_share(x) == 10 / 55
    x = list(range(1, 4))
    w = x
    # This is equivalent to [1, 2, 2, 3, 3, 3]
    # Sum = 14, top half is 9.
    assert mdf.top_50_pct_share(x, w) == 9 / 14
