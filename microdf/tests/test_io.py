import pytest
import microdf as mdf


def test_read_stata_zip():
    SCF2016 = 'https://www.federalreserve.gov/econres/files/scfp2016s.zip'
    df = mdf.read_stata_zip(SCF2016)
