import io
import zipfile
from urllib.request import urlopen

import pandas as pd


def read_stata_zip(url: str, **kwargs) -> pd.DataFrame:
    """Reads zipped Stata file by URL.

    From https://stackoverflow.com/a/59122689/1840471

    Pending native support in
    https://github.com/pandas-dev/pandas/issues/26599.

    :param url: URL string of .zip file containing a single
            .dta file.
    :param **kwargs: Arguments passed to pandas.read_stata().
    :returns: DataFrame.

    """
    with urlopen(url) as request:
        data = io.BytesIO(request.read())
    with zipfile.ZipFile(data) as archive:
        with archive.open(archive.namelist()[0]) as stata:
            return pd.read_stata(stata, **kwargs)
