import matplotlib as mpl
import seaborn as sns

TITLE_COLOR = '#212121'
AXIS_COLOR = '#757575'

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
    mpl.rcParams['font.sans-serif'] = 'Roboto'
    mpl.rcParams['font.family'] = 'sans-serif'
        
    # Set title text color to dark gray (https://material.io/color) not black.
    mpl.rcParams['text.color'] = TITLE_COLOR
        
    # Axis titles and tick marks are medium gray.
    mpl.rcParams['axes.labelcolor'] = AXIS_COLOR
    mpl.rcParams['xtick.color'] = AXIS_COLOR
    mpl.rcParams['ytick.color'] = AXIS_COLOR
