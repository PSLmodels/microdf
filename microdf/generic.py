import numpy as np
import pandas as pd

class MicroSeries(pd.Series):
    def __init__(self, *args, weights=None, **kwargs):
        """A Series-inheriting class for weighted microdata.
        Weights can be provided at initialisation, or using
        set_weights.
    
        :param weights: Array of weights.
        :type weights: np.array
        """
        super().__init__(*args, **kwargs)
        self.weights = weights
      
    def _init_micro(self, weights=None):
      self.weights = weights
    
    def set_weights(self, weights):
        """Sets the weight values.
        
        :param weights: Array of weights.
        :type weights: np.array.

        :returns: A Pandas Series multiplying the MicroSeries by its weight.
        """
        self.weights = weights

    def weight(self):
        """Calculates the weighted value of the MicroSeries.

        :returns: A Pandas Series multiplying the MicroSeries by its weight.
        """
        return self.multiply(self.weights)
    
    def sum(self):
        """Calculates the weighted sum of the MicroSeries.

        :returns: The weighted sum.
        """
        return self.weight().sum()
    
    def mean(self):
        """Calculates the weighted mean of the MicroSeries

        :returns: The weighted mean.
        """
        return np.average(self.values, weights=self.weights)
    
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

    def median(self):
        """Calculates the weighted median of the MicroSeries.

        :returns: The weighted median of a DataFrame's column.
        """
        return self.quantile(0.5)

class MicroDataFrame(pd.DataFrame):
  def __init__(self, *args, weights=None, **kwargs):
    """A DataFrame-inheriting class for weighted microdata.
    Weights can be provided at initialisation, or using set_weights
    or set_weight_col.
    
    :param weights: Array of weights.
    :type weights: np.array
    """
    super().__init__(*args, **kwargs)
    self.weights = weights
    self.weight_col = None

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
    """Sets the weights for the MicroDataFrame. If a 
    string is received, it will be assumed to be the column 
    name of the weight column.
    
    :param weights: Array of weights.
    :type weights: np.array
    """
    if isinstance(weights, str):
        self.set_weight_col(weights)
    else:
        self.weights = np.array(weights)
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