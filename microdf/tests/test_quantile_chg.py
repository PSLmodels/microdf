import microdf as mdf


def test_quantile_chg():
    mdf.quantile_chg(v1=[1, 2, 3], v2=[4, 5, 6],
                     w1=[7, 8, 9], w2=[10, 11, 12])


def test_quantile_chg_plot():
    mdf.quantile_chg_plot(v1=[1, 2, 3], v2=[4, 5, 6],
                          w1=[7, 8, 9], w2=[10, 11, 12])
