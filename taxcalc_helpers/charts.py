import taxcalc_helpers as tch
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import labellines as ll

def quantile_chg_plot(v1, v2, w1=None, w2=None, q=np.arange(0.1, 1, 0.1),
                      label1='Base', label2='Reform'):
    """ Create plot with one line per quantile boundary between base and
        reform.

    Args:
        v1: First set of values.
        v2: Second set of values.
        w1: First set of weights. Defaults to equal weight.
        w2: Second set of weights. Defaults to equal weight.
        q: Quantiles. Defaults to decile boundaries.
        label1: Label for left side of x-axis. Defaults to 'Base'.
        label2: Label for right side of x-axis. Defaults to 'Reform'.

    Returns:
        Nothing. Print plot.
    """
    # Calculate weighted quantiles.
    df = tch.quantile_chg(v1, v2, w1, w2, q)
    ax = df.plot()
    # Label the start and end points.
    plt.xticks([0, 1], [label1, label2])
    sns.despine(left=True, bottom=True)
    # Label the lines instead of using a legend.
    ax.get_legend().remove()
    ll.labelLines(plt.gca().get_lines())
    return ax
