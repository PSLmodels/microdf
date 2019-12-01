import io
import zipfile
import requests

def read_stata_zip(url):
    """Reads zipped Stata file by URL.

       From https://stackoverflow.com/a/59122697/1840471

       Pending native support in https://github.com/pandas-dev/pandas/issues/26599. 
    
    Args:
        url: URL string of .zip file containing a single
            .dta file.

    Returns:
        DataFrame.
    """
    response = requests.get(url)
    a = zipfile.ZipFile(io.BytesIO(response.content))
    b = a.read(a.namelist()[0])
    return pd.read_stata(io.BytesIO(b))
