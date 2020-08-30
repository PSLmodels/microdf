import matplotlib as mpl


def dollar_format(suffix=""):
    """Dollar formatter for matplotlib.

    :param suffix: Suffix to append, e.g. 'B'. Defaults to ''.
    :returns: FuncFormatter.

    """
    return mpl.ticker.FuncFormatter(
        lambda x, _: "$" + format(int(x), ",") + suffix
    )
