import os
import pandas as pd

from astropy.table import Table

_datadir = os.path.dirname(__file__)

__all__ = [
        "load_targets",
        "load_Malo13"
        ]

def load_targets():
    """
    Returns DataFrame of targets.csv
    """
    return pd.read_csv(os.path.join(_datadir, "../data/targets.csv"))


def load_Malo13(df=True):
    """
    Returns DataFrame of Malo+2013 table of bona-fide nearby moving group members
    """
    fn = os.path.join(_datadir, "../data/Malo/table3.dat")
    fnreadme = os.path.join(_datadir, "../data/Malo/ReadMe")
    malo = Table.read(fn, format='ascii.cds', readme=fnreadme)
    if not df:
        return malo
    return malo.to_pandas()
