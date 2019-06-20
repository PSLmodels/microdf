import matplotlib as mpl

def dollar_format():
    """ Dollar formatter for matplotlib.

    Args:
        None.

    Returns:
        FuncFormatter.
    """
    return mpl.ticker.FuncFormatter(lambda x, _: '$' + format(int(x), ','))
