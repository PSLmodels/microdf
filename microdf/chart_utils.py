import matplotlib as mpl


def dollar_format(suffix=""):
    """ Dollar formatter for matplotlib.

    Args:
        suffix: Suffix to append, e.g. 'B'. Defaults to ''.

    Returns:
        FuncFormatter.
    """
    return mpl.ticker.FuncFormatter(
        lambda x, _: "$" + format(int(x), ",") + suffix
    )
