import microdf as mdf
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import labellines as ll


def quantile_chg_plot(
    v1,
    v2,
    w1=None,
    w2=None,
    q=np.arange(0.1, 1, 0.1),
    label1="Base",
    label2="Reform",
):
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
    df = mdf.quantile_chg(v1, v2, w1, w2, q)
    # Make shades of green, removing the lightest 10 shades.
    with sns.color_palette(sns.color_palette("Greens", q.size + 11)[11:]):
        ax = df.plot()
    # Label the start and end points.
    plt.xticks([0, 1], [label1, label2])
    # Label the lines instead of using a legend.
    ax.get_legend().remove()
    # Move line labels closer to the center.
    ll.labelLines(plt.gca().get_lines(), xvals=(0.1, 0.9))
    # Formatting.
    plt.title("Change in disposable income percentiles")
    plt.ylim(0, None)
    ax.grid(color=mdf.GRID_COLOR, axis="y")
    ax.yaxis.set_major_formatter(mdf.dollar_format())
    ax.yaxis.set_minor_formatter(mdf.dollar_format())
    sns.despine(left=True, bottom=True)
    ax.axhline(0, color="lightgray", zorder=-1)
    # Looks better narrower.
    plt.gcf().set_size_inches(4, 6)
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
    df = mdf.quantile_chg(v1, v2, w1, w2, q).transpose()
    # Prepare dataset for plotting.
    df.columns = ["base", "reform"]
    df["pct_chg"] = df.reform / df.base - 1
    # Multiply by 100 pending github.com/matplotlib/matplotlib/issues/17113
    df.pct_chg *= 100
    df["index_newline"] = np.where(
        df.index == "50th (median)", "50th\n(median)", df.index
    )
    # Plot.
    fig, ax = plt.subplots()
    markerline, stemlines, baseline = ax.stem(
        df.index_newline, df.pct_chg, use_line_collection=True
    )
    plt.setp(baseline, color="gray", linewidth=0)
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(xmax=100))
    plt.title("Change to percentiles", loc="left")
    plt.ylabel("Change at the percentile boundary")
    plt.xlabel("Percentile")
    sns.despine(left=True, bottom=True)
    ax.grid(color=mdf.GRID_COLOR, axis="y")
    plt.xticks(rotation=0)
    return ax
