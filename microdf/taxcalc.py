import microdf as mdf
import taxcalc as tc


def static_baseline_calc(recs, year):
    """Creates a static Calculator object.

    Args:
        recs: Records object.
        year: Year to advance to.

    Returns:
        Calculator object.
    """
    calc = tc.Calculator(records=recs, policy=tc.Policy())
    calc.advance_to_year(year)
    calc.calc_all()
    return calc


def add_weighted_metrics(df, metric_vars, w='s006', divisor=1e6, suffix='_m'):
    """Adds weighted metrics in millions to a Tax-Calculator pandas DataFrame.

    Columns are renamed to *_m.

    Args:
        df: A pandas DataFrame containing Tax-Calculator data.
        metric_vars: A list of column names to weight, or a single column name.
        w: Weight column. Defaults to s006.
        divisor: Number by which the product is divided. Defaults to 1e6.
        suffix: Suffix to add to each weighted total. Defaults to '_m'
            to match divisor default of 1e6.

    Returns:
        Nothing. Weighted columns are added in place.
    """
    df[w + suffix] = df[w] / divisor
    metric_vars = mdf.listify(metric_vars)
    for metric_var in metric_vars:
        df[metric_var + suffix] = df[metric_var] * df[w + suffix]


def n65(age_head, age_spouse, elderly_dependents):
    """Calculates number of people in the tax unit age 65 or older.

    Args:
        age_head: Series representing age_head from taxcalc data.
        age_spouse: Series representing age_spouse from taxcalc data.
        elderly_dependents: Series representing elderly_dependents from
            taxcalc data.

    Returns:
        Series representing the number of people age 65 or older.
    """
    return ((age_head >= 65).astype(int) +
            (age_spouse >= 65).astype(int) +
            elderly_dependents)


def calc_df(records=None,
            policy=None,
            year=2019,
            reform=None,
            group_vars=None,
            metric_vars=None,
            group_n65=False):
    """Creates a pandas DataFrame for given Tax-Calculator data.

    s006 is always included, and RECID is used as an index.

    Args:
        records: An optional Records object. If not provided, uses CPS records.
        policy: An optional Policy object. If not provided, uses default
            Policy.
        year: An optional year to advance to. If not provided, defaults to
            2019.
        reform: An optional reform to implement for the Policy object.
        group_vars: An optional list of column names to include in the
            DataFrame.
        metric_vars: An optional list of column names to include and calculate
             weighted sums of (in millions named as *_m) in the DataFrame.
        group_n65: Whether to calculate and group by n65. Defaults to False.

    Returns:
        A pandas DataFrame. market_income is also always calculated.
    """
    # Assign defaults.
    if records is None:
        records = tc.Records.cps_constructor()
    if policy is None:
        policy = tc.Policy()
    if reform is not None:
        policy.implement_reform(reform)
    # Calculate.
    calc = tc.Calculator(records=records, policy=policy, verbose=False)
    calc.advance_to_year(year)
    calc.calc_all()
    # TODO: Make n65, ECI, etc. part of the list of columns you can request.
    # Get a deduplicated list of all columns.
    if group_n65:
        group_vars = group_vars + ['age_head', 'age_spouse',
                                   'elderly_dependents']
    # Include expanded_income and benefits to produce market_income.
    all_cols = listify(['RECID', 's006', 'expanded_income', 'aftertax_income',
                        mdf.BENS, group_vars, metric_vars])
    df = calc.dataframe(all_cols)
    # Create core elements.
    df['market_income'] = mdf.market_income(df)
    df['bens'] = df[mdf.BENS].sum(axis=1)
    df['tax'] = df.expanded_income - df.aftertax_income
    if group_n65:
        df['n65'] = n65(df.age_head, df.age_spouse, df.elderly_dependents)
        df.drop(['age_head', 'age_spouse', 'elderly_dependents'], axis=1,
                inplace=True)
    # Add calculated columns for metrics.
    add_weighted_metrics(df, metric_vars)
    # Set RECID to int and set it as index before returning.
    df['RECID'] = df.RECID.map(int)
    return df.set_index('RECID')


def recalculate(df):
    """ Recalculates fields in the DataFrame for after components have changed.

    Args:
        df: DataFrame for use in microdf.

    Returns:
        Nothing. Updates the DataFrame in place.
    """
    # Recalculate aggregate income measures.
    AGG_INCOME_MEASURES = ['expanded_income', 'aftertax_income', 'tpc_eci']
    cols = df.columns
    if 'tpc_eci' in cols:
        df.tpc_eci = mdf.tpc_eci(df)
    # Recalculate weighted metrics (anything ending in _m).
    mcols = cols[cols.str.endswith('_m')]
    add_weighted_metrics(df, mcols)
    # Might need to edit calc_df to add market_income and/or UBI.
