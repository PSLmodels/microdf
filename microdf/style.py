import matplotlib as mpl
import matplotlib.font_manager as fm
import seaborn as sns


TITLE_COLOR = '#212121'
AXIS_COLOR = '#757575'
GRID_COLOR = '#eeeeee'  # Previously lighter #f5f5f5.


def set_plot_style():
    """ Set plot style.

    Args:
        None.

    Returns:
        Nothing. Sets style.
    """
    sns.set_style('white')
    DPI = 200
    mpl.rc('savefig', dpi=DPI)
    mpl.rcParams['figure.dpi'] = DPI
    mpl.rcParams['figure.figsize'] = 6.4, 4.8  # Default.
    
    # Set up Roboto. Must be downloaded in the current directory.
    # See https://stackoverflow.com/a/51844978/1840471.
    fm.fontManager.ttflist += fm.createFontList(['Roboto-Regular.ttf'])
    mpl.rcParams['font.sans-serif'] = 'Roboto'
    mpl.rcParams['font.family'] = 'sans-serif'
        
    # Set title text color to dark gray (https://material.io/color) not black.
    mpl.rcParams['text.color'] = TITLE_COLOR
        
    # Axis titles and tick marks are medium gray.
    mpl.rcParams['axes.labelcolor'] = AXIS_COLOR
    mpl.rcParams['xtick.color'] = AXIS_COLOR
    mpl.rcParams['ytick.color'] = AXIS_COLOR

    # Grid is light gray.
    mpl.rcParams['grid.color'] = GRID_COLOR

    # Equivalent to seaborn.despine(left=True, bottom=True).
    mpl.rcParams['axes.spines.left'] = False
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
    mpl.rcParams['axes.spines.bottom'] = False
