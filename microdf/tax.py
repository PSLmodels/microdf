import pandas as pd


def tax_from_mtrs(val, brackets, rates, avoidance_rate=0):
    # Calculates tax liability based on a marginal tax rate schedule.
    #
    # Args:
    #     val: Value to assess tax on, e.g. wealth or income (list or Series).
    #     brackets: Left side of each bracket (list or Series).
    #     rates: Rate corresponding to each bracket.
    #     avoidance_rate: Constant avoidance/evasion rate in percentage terms.
    #                     Defaults to zero. 
    #
    # Returns:
    #     Series of tax liabilities with the same size as val.
    df_tax = pd.DataFrame({'brackets': brackets, 'rates': rates})
    df_tax['base_tax'] = df_tax.brackets.\
        sub(df_tax.brackets.shift(fill_value=0)).\
        mul(df_tax.rates.shift(fill_value=0)).cumsum()
    taxable = pd.Series(val) * (1 - avoidance_rate)
    rows = df_tax.brackets.searchsorted(taxable, side='right') - 1
    income_bracket_df = df_tax.loc[rows].reset_index(drop=True)
    return pd.Series(taxable).sub(income_bracket_df.brackets).\
        mul(income_bracket_df.rates).add(income_bracket_df.base_tax)
