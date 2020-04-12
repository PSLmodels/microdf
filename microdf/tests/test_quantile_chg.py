import microdf as mdf

V1 = [1, 2, 3]
V2 = [4, 5, 6]
W1 = [7, 8, 9]
W2 = [10, 11, 12]

def test_quantile_chg():
    mdf.quantile_chg(v1=V1, v2=V2, w1=W1, w2=W2)


def test_quantile_chg_plot():
    mdf.quantile_chg_plot(v1=V1, v2=V2, w1=W1, w2=W2)


def test_quantile_pct_chg_plot():
    mdf.quantile_pct_chg_plot(v1=V1, v2=V2, w1=W1, w2=W2)
