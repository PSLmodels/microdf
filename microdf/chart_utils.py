import matplotlib as mpl


def dollar_format(suffix=""):
    """Dollar formatter for matplotlib.

    :param suffix: Suffix to append, e.g. 'B'. Defaults to ''.
    :returns: FuncFormatter.

    """
    return mpl.ticker.FuncFormatter(
        lambda x, _: "$" + format(int(x), ",") + suffix
    )

def gbp_format(suffix=""):
    """GB Pound formatter for matplotlib/

    :param suffix: Suffix to append, default is empty.
    :returns: FuncFormatter.

    """
    return mpl.ticker.FuncFormatter(
        lambda x, _: "£" + format(int(x), ",") + suffix
    )