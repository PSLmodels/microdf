from .agg import (
    combine_base_reform,
    pctchg_base_reform,
    agg
)
from .chart_utils import dollar_format
from .charts import (
    quantile_chg_plot,
    quantile_pct_chg_plot
)
from .custom_taxes import (
    add_custom_tax,
    add_vat,
    add_carbon_tax,
    add_ftt
)
from .income_measures import (
    cash_income,
    tpc_eci,
    market_income
)
from .inequality import (
    gini,
    top_x_pct_share,
    bottom_x_pct_share,
    bottom_50_pct_share,
    top_10_pct_share,
    top_1_pct_share,
    top_0_1_pct_share,
    t10_b50
)
from .io import read_stata_zip
from .poverty import fpl
from .style import set_plot_style
from .tax import (
    mtr,
    tax_from_mtrs
)
from .taxcalc import (
    static_baseline_calc,
    add_weighted_metrics,
    n65,
    calc_df,
    recalculate
)
from .ubi import ubi_or_bens
from .utils import (
    ordinal_label,
    dedup_list,
    listify,
    flatten,
    cartesian_product
)
from .weighted import (
    weight,
    weighted_sum,
    weighted_mean,
    weighted_quantile,
    weighted_median,
    add_weighted_quantiles,
    quantile_chg
)

name = "microdf"
__version__ = "0.1.0"

__all__ = [
    # agg.py
    "combine_base_reform",
    "pctchg_base_reform",
    "agg",
    # chart_utils.py
    "dollar_format",
    # charts.py
    "quantile_chg_plot",
    "quantile_pct_chg_plot",
    # custom_taxes.py
    "add_custom_tax",
    "add_vat",
    "add_carbon_tax",
    "add_ftt",
    # income_measures.py
    "cash_income",
    "tpc_eci",
    "market_income",
    # inequality.py
    "gini",
    "top_x_pct_share",
    "bottom_x_pct_share",
    "bottom_50_pct_share",
    "top_10_pct_share",
    "top_1_pct_share",
    "top_0_1_pct_share",
    "t10_b50",
    # io.py
    "read_stata_zip",
    # poverty.py
    "fpl",
    # style.py
    "set_plot_style",
    # tax.py
    "mtr",
    "tax_from_mtrs",
    # taxcalc.py
    "static_baseline_calc",
    "add_weighted_metrics",
    "n65",
    "calc_df",
    "recalculate",
    # ubi.py
    "ubi_or_bens",
    # utils.py
    "ordinal_label",
    "dedup_list",
    "listify",
    "flatten",
    "cartesian_product",
    # weighted.py
    "weight",
    "weighted_sum",
    "weighted_mean",
    "weighted_quantile",
    "weighted_median",
    "add_weighted_quantiles",
    "quantile_chg",
]
