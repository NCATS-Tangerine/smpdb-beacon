from beacon_controller.providers.search import search as _search

import data, os, re
import pandas as pd
import numpy as np

from typing import List, Union, Dict
from .curie_builders import smpdb, drugbank, uniprot, hmdbp, genebank

df = None

def load():
    global df

    if df is None:
        df = pd.read_csv(os.path.join(data.path, 'proteins.csv'))
        df = df.replace({np.nan : None})

        df['smpdb_curie'] = df.apply(smpdb, axis=1)
        df['drugbank_curie'] = df.apply(drugbank, axis=1)
        df['uniprot_curie'] = df.apply(uniprot, axis=1)
        df['hmdbp_curie'] = df.apply(hmdbp, axis=1)
        df['genebank_curie'] = df.apply(genebank, axis=1)

        df['category'] = 'protein'

    return df

def search(keywords:Union[List[str], str], min_score=0):
    return _search(
        df=load(),
        columns=['Protein Name', 'Gene Name', 'Locus', 'SMPDB ID'],
        keywords=keywords,
        unique_columns='Protein Name'
    )

def search_by_pathway_curie(curie):
    return _search(
        df=load(),
        columns='smpdb_curie',
        keywords=curie,
        unique_columns='Protein Name'
    )

def search_by_molecule_curie(curie):
    return _search(
        df=load(),
        columns=['smpdb_curie', 'drugbank_curie', 'uniprot_curie', 'hmdbp_curie', 'genebank_curie'],
        keywords=curie,
        unique_columns='Protein Name'
    )
