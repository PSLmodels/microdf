import pandas as pd


def tax_from_mtrs(val, brackets, rates):
    # Calculates tax liability based on a marginal tax rate schedule.
    #
    # Args:
    #     val: Value to assess tax on, e.g. wealth or income (list or Series).
    #     brackets: Left side of each bracket (list or Series).
    #     rates: Rate corresponding to each bracket.
    #
    # Returns:
    #     Series of tax liabilities with the same size as val.
    df_tax = pd.DataFrame({'brackets': brackets, 'rates': rates})
    df_tax['base_tax'] = df_tax.brackets.\
                         sub(df_tax.brackets.shift(fill_value=0)).\
                         mul(df_tax.rates.shift(fill_value=0)).cumsum()
    rows = df_tax.brackets.searchsorted(val, side='right') - 1
    income_bracket_df = df_tax.loc[rows].reset_index(drop=True)
    return pd.Series(val).sub(income_bracket_df.brackets).\
        mul(income_bracket_df.rates).add(income_bracket_df.base_tax)
