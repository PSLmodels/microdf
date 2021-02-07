import numpy as np
import pandas as pd

import microdf as mdf


class MicroSeries(pd.Series):
    def __init__(self, *args, weights=None, **kwargs):
        """A Series-inheriting class for weighted microdata.
        Weights can be provided at initialisation, or using set_weights.

        :param weights: Array of weights.
        :type weights: np.array
        """
        super().__init__(*args, **kwargs)
        self.set_weights(weights)

    def _init_micro(self, weights=None):
        self.weights = weights

    def handles_zero_weights(fn):
        def safe_fn(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except ZeroDivisionError:
                return np.NaN

        return safe_fn

    def set_weights(self, weights):
        """Sets the weight values.

        :param weights: Array of weights.
        :type weights: np.array.
        """
        self.weights = pd.Series(weights)

    @handles_zero_weights
    def weight(self):
        """Calculates the weighted value of the MicroSeries.

        :returns: A Pandas Series multiplying the MicroSeries by its weight.
        """
        return self.multiply(self.weights)

    @handles_zero_weights
    def sum(self):
        """Calculates the weighted sum of the MicroSeries.

        :returns: The weighted sum.
        """
        return self.multiply(self.weights).sum()

    @handles_zero_weights
    def mean(self):
        """Calculates the weighted mean of the MicroSeries

        :returns: The weighted mean.
        """
        return np.average(self.values, weights=self.weights)

    @handles_zero_weights
    def quantile(self, q):
        """Calculates weighted quantiles of the MicroSeries.

        Doesn't exactly match unweighted quantiles of stacked values.
        See stackoverflow.com/q/21844024#comment102342137_29677616.

        :param q: Array of quantiles to calculate.
        :type q: np.array

        :return: Array of weighted quantiles.
        :rtype: np.array
        """
        values = np.array(self.values)
        quantiles = np.array(q)
        if self.weights is None:
            sample_weight = np.ones(len(values))
        else:
            sample_weight = np.array(self.weights)
        assert np.all(quantiles >= 0) and np.all(
            quantiles <= 1
        ), "quantiles should be in [0, 1]"
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]
        weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
        weighted_quantiles /= np.sum(sample_weight)
        return np.interp(quantiles, weighted_quantiles, values)

    @handles_zero_weights
    def median(self):
        """Calculates the weighted median of the MicroSeries.

        :returns: The weighted median of a DataFrame's column.
        """
        return self.quantile(0.5)

    def gini(self, negatives: str = None) -> float:
        """Calculates Gini index.

        :param negatives: An optional string indicating how to treat negative
            values of x:
            'zero' replaces negative values with zeroes.
            'shift' subtracts the minimum value from all values of x,
            when this minimum is negative. That is, it adds the absolute
            minimum value.
            Defaults to None, which leaves negative values as they are.
        :type q: str
        :returns: Gini index.
        :rtype: float
        """
        x = np.array(self).astype("float")
        if negatives == "zero":
            x[x < 0] = 0
        if negatives == "shift" and np.amin(x) < 0:
            x -= np.amin(x)
        if self.weights is not None:
            sorted_indices = np.argsort(self.weights)
            sorted_x = self[sorted_indices]
            sorted_w = self.weights[sorted_indices]
            cumw = np.cumsum(sorted_w)
            cumxw = np.cumsum(sorted_x * sorted_w)
            return np.sum(cumxw[1:] * cumw[:-1] - cumxw[:-1] * cumw[1:]) / (
                cumxw[-1] * cumw[-1]
            )
        else:
            sorted_x = np.sort(self)
            n = len(x)
            cumxw = np.cumsum(sorted_x)
            # The above formula, with all weights equal to 1 simplifies to:
            return (n + 1 - 2 * np.sum(cumxw) / cumxw[-1]) / n

    def top_x_pct_share(self, top_x_pct: float) -> float:
        """Calculates top x% share.

        :param top_x_pct: Decimal between 0 and 1 of the top %, e.g. 0.1,
            0.001.
        :type top_x_pct: float
        :returns: The weighted share held by the top x%.
        :rtype: float
        """
        threshold = self.quantile(1 - top_x_pct)
        top_x_pct_sum = self[self >= threshold].sum()
        total_sum = self.sum()
        return top_x_pct_sum / total_sum

    def bottom_x_pct_share(self, bottom_x_pct) -> float:
        """Calculates bottom x% share.

        :param bottom_x_pct: Decimal between 0 and 1 of the top %, e.g. 0.1,
            0.001.
        :type bottom_x_pct: float
        :returns: The weighted share held by the bottom x%.
        :rtype: float
        """
        return 1 - self.top_x_pct_share(1 - bottom_x_pct)

    def bottom_50_pct_share(self) -> float:
        """Calculates bottom 50% share.

        :returns: The weighted share held by the bottom 50%.
        :rtype: float
        """
        return self.bottom_x_pct_share(0.5)

    def top_50_pct_share(self) -> float:
        """Calculates top 50% share.

        :returns: The weighted share held by the top 50%.
        :rtype: float
        """
        return self.top_x_pct_share(0.5)

    def top_10_pct_share(self) -> float:
        """Calculates top 10% share.

        :returns: The weighted share held by the top 10%.
        :rtype: float
        """
        return self.top_x_pct_share(0.1)

    def top_1_pct_share(self) -> float:
        """Calculates top 1% share.

        :returns: The weighted share held by the top 50%.
        :rtype: float
        """
        return self.top_x_pct_share(0.01)

    def top_0_1_pct_share(self) -> float:
        """Calculates top 0.1% share.

        :returns: The weighted share held by the top 0.1%.
        :rtype: float
        """
        return self.top_x_pct_share(0.001)

    def t10_b50(self):
        """Calculates ratio between the top 10% and bottom 50% shares.

        :returns: The weighted share held by the top 10% divided by
            the weighted share held by the bottom 50%.

        """
        t10 = self.top_10_pct_share()
        b50 = self.bottom_50_pct_share()
        return t10 / b50
    def groupby(self, *args, **kwargs):
        gb = super().groupby(*args, **kwargs)
        gb.__class__ = MicroSeriesGroupBy
        gb.weights = pd.Series(self.weights).groupby(*args, **kwargs)
        return gb

    def __getitem__(self, key):
        result = super().__getitem__(key)
        if isinstance(result, pd.Series):
            weights = self.weights.__getitem__(key)
            return MicroSeries(result, weights=weights)
        return result


class MicroSeriesGroupBy(pd.core.groupby.generic.SeriesGroupBy):
    def __init__(self, weights=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weights = weights

    def _weighted_agg(func):
        def via_micro_series(row, fn, *args, **kwargs):
            return getattr(MicroSeries(row.a, weights=row.w), fn.__name__)(
                *args, **kwargs
            )

        def _weighted_agg_fn(self, *args, **kwargs):
            arrays = self.apply(np.array)
            weights = self.weights.apply(np.array)
            df = pd.DataFrame(dict(a=arrays, w=weights))
            result = df.agg(
                lambda row: via_micro_series(row, func, *args, **kwargs),
                axis=1,
            )
            return result

        return _weighted_agg_fn

    @_weighted_agg
    def weight(self):
        return MicroSeries.weight(self)

    @_weighted_agg
    def sum(self):
        return MicroSeries.sum(self)

    @_weighted_agg
    def mean(self):
        return MicroSeries.mean(self)

    @_weighted_agg
    def quantile(self, quantiles):
        return MicroSeries.quantile(self, quantiles)

    @_weighted_agg
    def median(self):
        return MicroSeries.median(self)


class MicroDataFrame(pd.DataFrame):
    def __init__(self, *args, weights=None, **kwargs):
        """A DataFrame-inheriting class for weighted microdata.
        Weights can be provided at initialisation, or using set_weights or
        set_weight_col.

        :param weights: Array of weights.
        :type weights: np.array
        """
        super().__init__(*args, **kwargs)
        self.weights = weights
        self.weight_col = None
        self._link_all_weights()

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        self._link_all_weights()

    def _link_weights(self, column):
        # self[column] = ... triggers __setitem__, which forces pd.Series
        # this workaround avoids that
        self[column].__class__ = MicroSeries
        self[column]._init_micro(weights=self.weights)

    def _link_all_weights(self):
        for column in self.columns:
            if column != self.weight_col:
                self._link_weights(column)

    def set_weights(self, weights):
        """Sets the weights for the MicroDataFrame. If a string is received,
        it will be assumed to be the column name of the weight column.

        :param weights: Array of weights.
        :type weights: np.array
        """
        if isinstance(weights, str):
            self.set_weight_col(weights)
        else:
            self.weights = np.array(weights)
            self._link_all_weights()

    def set_weight_col(self, column):
        """Sets the weights for the MicroDataFrame by specifying the name of
        the weight column.

        :param weights: Array of weights.
        :type weights: np.array
        """
        self.weights = np.array(self[column])
        self.weight_col = column
        self._link_all_weights()

    def poverty_rate(self, income: str, threshold: str) -> float:
        """Calculate poverty rate, i.e., the population share with income
        below their poverty threshold.

        :param income: Column indicating income.
        :type income: str
        :param threshold: Column indicating threshold.
        :type threshold: str
        :return: Poverty rate between zero and one.
        :rtype: float
        """
        return mdf.poverty_rate(self, income, threshold, self.weights)

    def deep_poverty_rate(self, income: str, threshold: str) -> float:
        """Calculate deep poverty rate, i.e., the population share with income
        below half their poverty threshold.

        :param income: Column indicating income.
        :type income: str
        :param threshold: Column indicating threshold.
        :type threshold: str
        :return: Deep poverty rate between zero and one.
        :rtype: float
        """
        return mdf.deep_poverty_rate(self, income, threshold, self.weights)

    def poverty_gap(self, income: str, threshold: str) -> float:
        """Calculate poverty gap, i.e., the total gap between income and
        poverty thresholds for all people in poverty.

        :param income: Column indicating income.
        :type income: str
        :param threshold: Column indicating threshold.
        :type threshold: str
        :return: Poverty gap.
        :rtype: float
        """
        return mdf.poverty_gap(self, income, threshold, self.weights)

    def squared_poverty_gap(self, income: str, threshold: str) -> float:
        """Calculate squared poverty gap, i.e., the total squared gap between
        income and poverty thresholds for all people in poverty.
        Also known as the poverty severity index.

        :param income: Column indicating income.
        :type income: str
        :param threshold: Column indicating threshold.
        :type threshold: str
        :return: Squared poverty gap.
        :rtype: float
        """
        return mdf.poverty_gap(self, income, threshold, self.weights)
    def groupby(self, by, *args, **kwargs):
        """Returns a GroupBy object with MicroSeriesGroupBy objects for each column

        :param by: column to group by
        :type by: str

        return: DataFrameGroupBy object with columns using weights
        rtype: DataFrameGroupBy
        """
        gb = super().groupby(by, *args, **kwargs)
        weights = pd.Series(self.weights).groupby(self[by], *args, **kwargs)
        for col in self.columns:  # df.groupby(...)[col]s use weights
            if col != by:
                res = gb[col]
                res.__class__ = MicroSeriesGroupBy
                res.weights = weights
                setattr(gb, col, res)
        return gb
