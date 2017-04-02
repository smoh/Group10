import os
import numpy as np
import pandas as pd

from astropy.table import Table

_datadir = os.path.dirname(__file__)

def datapath(fn):
    return os.path.join(_datadir, "../data/"+fn)

__all__ = [
        "load_allstars",
        "load_targets",
        "load_Malo13",
        "vxyz_to_vradecr",
        "vradecr_to_vxyz",
        "DataLoader"
        ]


def load_allstars():
    """Returns DataFrame of all stars in catalog"""
    return pd.read_csv(datapath("allstars.csv"))

def load_targets():
    """
    Returns DataFrame of targets.csv
    """
    return pd.read_csv(datapath("targets.csv"))


def load_Malo13(df=True):
    """
    Returns DataFrame of Malo+2013 table of bona-fide nearby moving group members
    """
    fn = datapath("Malo/table3.dat")
    fnreadme = datapath("Malo/ReadMe")
    malo = Table.read(fn, format='ascii.cds', readme=fnreadme)
    if not df:
        return malo
    return malo.to_pandas()

def vxyz_to_vradecr(ra, dec):
    """ ra, dec in degrees"""
    ra = np.atleast_1d(ra)
    dec = np.atleast_1d(dec)
    A = np.array(
        [[[-np.sin(rr), np.cos(rr), 0.],
         [-np.sin(dd)*np.cos(rr), -np.sin(dd)*np.sin(rr), np.cos(dd)],
         [np.cos(dd)*np.cos(rr), np.cos(dd)*np.sin(rr), np.sin(dd)]]
         for rr, dd in zip(np.deg2rad(ra), np.deg2rad(dec))])
    return A

def vradecr_to_vxyz(ra, dec):
    return np.linalg.inv(vxyz_to_vradecr(ra, dec))

def build_covmat(data):
    #names = ['ra', 'dec', 'parallax', 'pmra', 'pmdec']
    names = ['parallax', 'pmra', 'pmdec']
    n = len(names)
    C = np.zeros((n, n))
    # pre-load the diagonal
    for i,name in enumerate(names):
        full_name = "{}_error".format(name)
        C[i,i] = data[full_name]**2
    for i,name1 in enumerate(names):
        for j,name2 in enumerate(names):
            if j <= i:
                continue
            full_name = "{}_{}_corr".format(name1, name2)
            C[i,j] = data[full_name] * np.sqrt(C[i,i]*C[j,j])
            C[j,i] = data[full_name] * np.sqrt(C[i,i]*C[j,j])
    return C

class DataLoader(object):
    def __init__(self):
        self.df = load_allstars()
    
    def get_group(self, gid):
        g = self.df.groupby("group_id").get_group(gid)
        M = vxyz_to_vradecr(g.tgas_ra, g.tgas_dec)#[:,:2,:]
        x = g[['parallax', 'pmra', 'pmdec']].values

        cov = np.array([build_covmat(row) for row in g.to_dict('records')])

        return x, cov, M
