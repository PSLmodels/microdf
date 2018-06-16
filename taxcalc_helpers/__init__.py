def gini(x, w=None, zero_negatives=True):
    # Requires float numpy arrays (not pandas Series or lists) to work.
    x = np.array(x).astype('float')
    if zero_negatives:
        x[x < 0] = 0
        if w is not None:
            w = np.array(w).astype('float')
            sorted_indices = np.argsort(x)
            sorted_x = x[sorted_indices]
            sorted_w = w[sorted_indices]
            cumw = np.cumsum(sorted_w)
            cumxw = np.cumsum(sorted_x * sorted_w)
            return (np.sum(cumxw[1:] * cumw[:-1] - cumxw[:-1] * cumw[1:]) /
                    (cumxw[-1] * cumw[-1]))
        else:
            sorted_x = np.sort(x)
            n = len(x)
            cumxw = np.cumsum(sorted_x)
            # The above formula, with all weights equal to 1 simplifies to:
            return (n + 1 - 2 * np.sum(cumxw) / cumxw[-1]) / n
