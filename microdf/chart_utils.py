import matplotlib as mpl


def currency_format(currency="USD", suffix=""):
    """Dollar formatter for matplotlib.

    :param currency: Name of the currency, e.g. 'USD', 'GBP'.
    :param suffix: Suffix to append, e.g. 'B'. Defaults to ''.
    :returns: FuncFormatter.

    """
    
    prefix = {
        "USD": "$",
        "GBP": "£"
    }[currency]

    return mpl.ticker.FuncFormatter(
        lambda x, _: prefix + format(int(x), ",") + suffix
    )