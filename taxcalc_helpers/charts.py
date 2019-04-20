import taxcalc_helpers as tch
import matplotlib as mpl
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
        Axis.
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
    ax.grid(color=tch.GRID_COLOR, axis='y')
    return ax


def quantile_pct_chg_plot(v1, v2, w1=None, w2=None, q=np.arange(0.1, 1, 0.1)):
    """ Create stem plot with percent change in decile boundaries.

    Args:
        v1: First set of values.
        v2: Second set of values.
        w1: First set of weights. Defaults to equal weight.
        w2: Second set of weights. Defaults to equal weight.
        q: Quantiles. Defaults to decile boundaries.

    Returns:
        Axis.
    """
    # Calculate weighted quantiles.
    df = tch.quantile_chg(v1, v2, w1, w2, q).transpose()
    # Prepare dataset for plotting.
    df.columns = ['base', 'reform']
    df['pct_chg'] = df.reform / df.base - 1
    df['index_newline'] = np.where(df.index == '5th (median)', '5th\n(median)', df.index)
    # Plot.
    fig, ax = plt.subplots()
    markerline, stemlines, baseline = ax.stem(df.index_newline, df.pct_chg)
    plt.setp(baseline, color='gray', linewidth=0)
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(
        lambda x, _: '{:.0%}'.format(x)))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
    plt.title('Change to disposable income deciles', loc='left')
    plt.ylabel('Change in disposable income at the decile boundary')
    plt.xlabel('Disposable income decile')
    sns.despine(left=True, bottom=True)
    ax.grid(color=tch.GRID_COLOR, axis='y')
    plt.xticks(rotation=0)
    return ax
