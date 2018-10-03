from beacon_controller.providers.search import search as _search

import data, os, re
import pandas as pd
import numpy as np

from typing import List, Union, Dict
from .curie_builders import smpdb

df = None

def load():
    global df

    if df is None:
        df = pd.read_csv(os.path.join(data.path, 'smpdb_pathways.csv'))
        df = df.replace({np.nan : None})
        df['smpdb_curie'] = df.apply(smpdb, axis=1)
        df['category'] = 'pathway'

    return df

def search(keywords:Union[List[str], str], min_score=0):
    return _search(
        df=load(),
        columns=['Name', 'Description', 'SMPDB ID'],
        keywords=keywords,
        min_score=min_score,
        column_multiplier={'Name' : 3}
    )

def search_by_pathway_curie(curie):
    return _search(
        df=load(),
        columns='smpdb_curie',
        keywords=curie,
        unique_columns='smpdb_curie'
    )
