from beacon_controller.providers.search import search as _search
from .curie_builders import chebi, smpdb, drugbank, hmdb, kegg, metabolite

import data, os, re
import pandas as pd
import numpy as np

from typing import List, Union, Dict

df = None

def load():
    global df

    if df is None:
        df = pd.read_csv(os.path.join(data.path, 'metabolites.csv'))
        df = df.replace({np.nan : None})

        df['chebi_curie'] = df.apply(chebi, axis=1)
        df['smpdb_curie'] = df.apply(smpdb, axis=1)
        df['drugbank_curie'] = df.apply(drugbank, axis=1)
        df['hmdb_curie'] = df.apply(hmdb, axis=1)
        df['kegg_curie'] = df.apply(kegg, axis=1)
        df['metabolite_curie'] = df.apply(metabolite, axis=1)

        df['category'] = 'metabolite'

    return df

def search(keywords:Union[List[str], str], min_score=0):
    return _search(
        df=load(),
        columns=['Metabolite Name', 'Metabolite ID', 'Formula', 'SMPDB ID'],
        keywords=keywords,
        unique_columns='Metabolite ID',
    )

def search_by_pathway_curie(smpdb_curie):
    return _search(
        df=load(),
        columns='smpdb_curie',
        keywords=smpdb_curie,
        unique_columns='Metabolite Name'
    )

def search_by_molecule_curie(curie):
    return _search(
        df=load(),
        columns=['chebi_curie', 'smpdb_curie', 'drugbank_curie', 'hmdb_curie', 'kegg_curie', 'metabolite_curie'],
        keywords=curie,
        unique_columns='Metabolite Name'
    )
