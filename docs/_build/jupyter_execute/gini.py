# `gini` example

import microdf as mdf

x = [-10, -1, 0, 5, 100]
w = [1, 2, 3, 4, 5]

## Simple behavior

mdf.gini(x)

## Dealing with negatives

This will be equivalent to `mdf.gini([0, 0, 0, 5, 100])`.

mdf.gini(x, negatives='zero')

mdf.gini([0, 0, 0, 5, 100])

This will be equivalent to `mdf.gini([0, 9, 10, 15, 110])`.

mdf.gini(x, negatives='shift')

mdf.gini([0, 9, 10, 15, 110])

## Dealing with weights

mdf.gini(x, w)

mdf.gini([-10,
          -1, -1,
          0, 0, 0,
          5, 5, 5, 5,
          100, 100, 100, 100, 100])