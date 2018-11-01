from typing import List

# import dask.dataframe as dd
import pandas as dd
import numpy as np
import data, os
from beacon_controller.providers import curie

node_path = os.path.join(data.path, 'nodes.csv')
edge_path = os.path.join(data.path, 'edges.csv')

node_df = None
edge_df = None

predicate_list = None

def predicates():
    global predicate_list
    df = load_edges()
    if predicate_list is None:
        predicate_list = list(df['predicate'].unique())
        predicate_list = [p.replace('-', '_') for p in predicate_list]
    return predicate_list

def load_nodes():
    global node_df

    if node_df is None:
        node_df = dd.read_csv(node_path, dtype=str)
        node_df = node_df.drop_duplicates('id')
        node_df = node_df.replace({np.nan : None})
        node_df = node_df[node_df.id.isnull() == False]

    return node_df

def load_edges():
    global edge_df

    if edge_df is None:
        edge_df = dd.read_csv(edge_path, dtype=str)
        edge_df.drop_duplicates()
        edge_df = edge_df.replace({np.nan : None})
        edge_df = edge_df[(edge_df.subject_id.isnull() == False) & (edge_df.object_id.isnull() == False)]

    return edge_df

def get_nodes(curies:List[str]):
    df = load_nodes()

    if isinstance(curies, str):
        curies = [curies]

    q = build_mask(curies, lambda curie: df.id == curie)
    df = df[q == True]

    return df.drop_duplicates('id').to_dict(orient='records')

def find_nodes(keywords:List[str]=None, categories:List[str]=None, offset:int=None, size:int=None):
    return find_nodes_df(keywords, categories, offset, size).to_dict(orient='records')

def find_nodes_df(keywords:List[str]=None, categories:List[str]=None, offset:int=None, size:int=None):
    df = load_nodes()

    q = None
    if isinstance(keywords, list):
        q = build_mask(keywords, lambda k :  df['name'].str.contains(k, case=False, regex=False))
    if isinstance(categories, list):
        q = build_mask(categories, lambda c: df['category'] == c, c=q)

    if q is not None:
        df = df[q == True]

    df = df[offset:]
    df = df[:size]

    return df

def build_mask(items, predicate, d=None, c=None):
    """
    Applies the predicate to each item, taking the disjunction of the results.
    Will add d as a disjunct, and then finally will take that in
    conjunction with c. Returns the value.
    """
    q = None
    for i in items:
        if q is None:
            q = predicate(i)
        else:
            q |= predicate(i)
    if d is not None:
        q = d | q
    if c is not None:
        q = c & q
    return q

def is_not_empty(l:list):
    return isinstance(l, list) and l != []

def find_edges(
    subject_ids,
    subject_keywords,
    subject_categories,
    object_ids,
    object_keywords,
    object_categories,
    predicates,
    offset=None,
    size=None,
):
    df = load_edges()

    q = None

    if is_not_empty(subject_ids):
        q = build_mask(subject_ids, lambda i: df['subject_id'] == i, c=q)

    if is_not_empty(subject_keywords):
        q = build_mask(
            subject_keywords,
            lambda k: df['subject_name'].str.contains(k, case=False, regex=False),
            c=q
        )

    if is_not_empty(subject_categories):
        q = build_mask(subject_categories, lambda c: df['subject_category'] == c.lower(), c=q)

    if is_not_empty(object_ids):
        q = build_mask(object_ids, lambda i: df['object_id'] == i, c=q)

    if is_not_empty(object_keywords):
        q = build_mask(
            object_keywords,
            lambda k: df['object_name'].str.contains(k, case=False, regex=False),
            c=q
        )

    if is_not_empty(object_categories):
        q = build_mask(object_categories, lambda c: df['object_category'] == c.lower(), c=q)

    if is_not_empty(predicates):
        q = build_mask(predicates, lambda p: df['predicate'] == p, c=q)

    if q is not None:
        df = df[q == True]

    df = df[offset:]
    df = df[:size]

    return df.to_dict(orient='records')
