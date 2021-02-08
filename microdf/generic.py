import numpy as np
import pandas as pd
from typing import Union, Optional


class MicroSeries(pd.Series):
    def __init__(self, *args, weights=None, **kwargs):
        """A Series-inheriting class for weighted microdata.
        Weights can be provided at initialisation, or using
        set_weights.

        :param weights: Array of weights.
        :type weights: np.array
        """
        super().__init__(*args, **kwargs)
        self.set_weights(weights)

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
        if weights is None:
            self.weights = pd.Series(np.ones_like(self.values))
        else:
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
    def count(self):
        """Calculates the weighted count of the MicroSeries.

        :returns: The weighted count.
        """
        return self.weights.sum()

    @handles_zero_weights
    def mean(self):
        """Calculates the weighted mean of the MicroSeries

        :returns: The weighted mean.
        """
        return np.average(self.values, weights=self.weights)

    @handles_zero_weights
    def quantile(self, quantiles):
        """Calculates weighted quantiles of the MicroSeries.

        Doesn't exactly match unweighted quantiles of stacked values.
        See stackoverflow.com/q/21844024#comment102342137_29677616.

        :param quantiles: Array of quantiles to calculate.
        :type quantiles: np.array

        :return: Array of weighted quantiles.
        :rtype: np.array
        """
        values = np.array(self.values)
        quantiles = np.array(quantiles)
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

    def __add__(self, other):
        return MicroSeries(super().__add__(other), weights=self.weights)

    def __sub__(self, other):
        return MicroSeries(super().__sub__(other), weights=self.weights)

    def __mul__(self, other):
        return MicroSeries(super().__mul__(other), weights=self.weights)

    def __truediv__(self, other):
        return MicroSeries(super().__truediv__(other), weights=self.weights)

    def __floordiv__(self, other):
        return MicroSeries(super().__floordiv__(other), weights=self.weights)

    def __iadd__(self, other):
        return MicroSeries(super().__iadd__(other), weights=self.weights)

    def __isub__(self, other):
        return MicroSeries(super().__isub__(other), weights=self.weights)

    def __imul__(self, other):
        return MicroSeries(super().__imul__(other), weights=self.weights)

    def __idiv__(self, other):
        return MicroSeries(super().__idiv__(other), weights=self.weights)

    def __neg__(self, other):
        return MicroSeries(super().__neg__(other), weights=self.weights)

    def __pos__(self, other):
        return MicroSeries(super().__pos__(other), weights=self.weights)

    def __lt__(self, other):
        return MicroSeries(super().__lt__(other), weights=self.weights)

    def __le__(self, other):
        return MicroSeries(super().__le__(other), weights=self.weights)

    def __eq__(self, other):
        return MicroSeries(super().__eq__(other), weights=self.weights)

    def __ne__(self, other):
        return MicroSeries(super().__ne__(other), weights=self.weights)

    def __ge__(self, other):
        return MicroSeries(super().__ge__(other), weights=self.weights)

    def __gt__(self, other):
        return MicroSeries(super().__gt__(other), weights=self.weights)


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
        Weights can be provided at initialisation, or using set_weights
        or set_weight_col.

        :param weights: Array of weights.
        :type weights: np.array
        """
        super().__init__(*args, **kwargs)
        self.set_weights(weights)
        self._link_all_weights()

    def get_args_as_micro_series(*kwarg_names):
        """Decorator for auto-parsing column names into MicroSeries objects.
        If given, kwarg_names limits arguments checked to keyword arguments
        specified.

        :param arg_names: argument names to restrict to.
        :type arg_names: str
        """

        def arg_series_decorator(fn):
            def series_function(self, *args, **kwargs):
                new_args = []
                new_kwargs = {}
                if len(kwarg_names) == 0:
                    for value in args:
                        if isinstance(value, str):
                            if value not in self.columns:
                                raise Exception("Column not found")
                            new_args += [self[value]]
                        else:
                            new_args += [value]
                    for name, value in kwargs.items():
                        if isinstance(value, str) and (
                            len(kwarg_names) == 0 or name in kwarg_names
                        ):
                            if value not in self.columns:
                                raise Exception("Column not found")
                            new_kwargs[name] = self[value]
                        else:
                            new_kwargs[name] = value
                return fn(self, *new_args, **new_kwargs)

            return series_function

        return arg_series_decorator

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        self._link_all_weights()

    def _link_weights(self, column):
        # self[column] = ... triggers __setitem__, which forces pd.Series
        # this workaround avoids that
        self[column].__class__ = MicroSeries
        self[column].set_weights(self.weights)

    def _link_all_weights(self):
        for column in self.columns:
            if column != self.weights_col:
                self._link_weights(column)

    def set_weights(self, weights):
        """Sets the weights for the MicroDataFrame. If a
        string is received, it will be assumed to be the column
        name of the weight column.

        :param weights: Array of weights.
        :type weights: np.array
        """
        if isinstance(weights, str):
            self.weights_col = weights
            self.weights = pd.Series(self[weights])
        else:
            self.weights_col = None
            self.weights = pd.Series(weights)
            self._link_all_weights()

    def set_weight_col(self, column):
        """Sets the weights for the MicroDataFrame by
        specifying the name of the weight column.

        :param weights: Array of weights.
        :type weights: np.array
        """
        self.weights = np.array(self[column])
        self.weight_col = column
        self._link_all_weights()

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

    @get_args_as_micro_series()
    def poverty_count(
        self,
        income: Union[MicroSeries, str],
        threshold: Union[MicroSeries, str],
    ) -> int:
        """Calculates the number of entities with income below a poverty threshold.

        :param income: income array or column name
        :type income: Union[MicroSeries, str]

        :param threshold: threshold array or column name
        :type threshold: Union[MicroSeries, str]

        return: number of entities in poverty
        rtype: int
        """
        in_poverty = income < threshold
        x = in_poverty.sum()
        return x.count()
