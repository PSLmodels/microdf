import io
import pandas as pd
from urllib.request import urlopen
import zipfile

def read_stata_zip(url):
    """Reads zipped Stata file by URL.

       From https://stackoverflow.com/a/59122689/1840471

       Pending native support in https://github.com/pandas-dev/pandas/issues/26599. 
    
    Args:
        url: URL string of .zip file containing a single
            .dta file.

    Returns:
        DataFrame.
    """
    with urlopen(url) as request:
        data = BytesIO(request.read())
    with zipfile.ZipFile(data) as archive:
        with archive.open(archive.namelist()[0]) as stata:
            return pd.read_stata(stata)
