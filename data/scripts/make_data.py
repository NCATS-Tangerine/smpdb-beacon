import pandas as pd
from typing import List
import sys

metabolites_path = sys.argv[1]
proteins_path = sys.argv[2]
pathways_path = sys.argv[3]

def make_node_set(df):
    return df.reindex(columns=['id', 'name', 'category', 'description', 'synonyms', 'xrefs'])

def make_edge_set(df):
    return df.reindex(columns=['subject_id', 'predicate', 'object_id'])

def build_pathways(path) -> pd.DataFrame:
    """
    Builds the pathway node set
    """
    df = pd.read_csv(path, dtype=str)
    df = df.rename(columns={
        'SMPDB ID' : 'id',
        'Name' : 'name',
        'Description' : 'description'
    })

    df['category'] = 'pathway'
    df['id'] = df.apply(lambda row: f"SMP:{row['id']}", axis=1)

    df = make_node_set(df)

    return df

def build_metabolites(path) -> (pd.DataFrame, pd.DataFrame):
    """
    Builds the metabolite node set and edge set for the chemical_to_pathway_association
    predicate.
    """
    def build(row):
        options = [
            ('ChEBI ID', 'CHEBI'),
            ('KEGG ID', 'KEGG'),
            ('HMDB ID', 'HMDB'),
            ('DrugBank ID', 'DRUGBANK'),
            ('Metabolite ID', 'PW'),
        ]
        for column, prefix in options:
            if isinstance(row[column], str):
                return '{}:{}'.format(prefix, row[column])
        print(row)
        raise Exception('Could not find a metabolite ID')

    df = pd.read_csv(path, dtype=str)

    df['id'] = df.apply(build, axis=1)
    df = df.drop_duplicates('id')

    df['SMPDB ID'] = df.apply(lambda row: f"SMP:{row['SMPDB ID']}", axis=1)

    nodes = df
    edges = df

    nodes['category'] = 'metabolite'
    nodes = nodes.rename(columns={
        'Metabolite Name' : 'name',
        'IUPAC' : 'synonyms',
    })

    edges['predicate'] = 'chemical_to_pathway_association'
    edges = df.rename(columns={
        'id' : 'subject_id',
        'SMPDB ID' : 'object_id',
    })

    nodes = make_node_set(nodes)
    edges = make_edge_set(edges)

    return nodes, edges


def build_proteins(path) -> (pd.DataFrame, pd.DataFrame):
    """
    Builds the protein node set and edge set for the chemical_to_pathway_association
    predicate.
    """
    def build(row):
        options = [
            ('Uniprot ID', 'UNIPROT'),
            ('DrugBank ID', 'DRUGBANK'),
            ('HMDBP ID', 'HMDB'),
            ('GenBank ID', 'GENBANK'),
        ]
        # xrefs = []
        for column, prefix in options:
            if isinstance(row[column], str):
                return '{}:{}'.format(prefix, row[column])
                # xrefs.append(f'{prefix}:{row[column]}')
        # if xrefs == []:
        #     raise Exception('Cannot find ID for above row')
        # else:
        #     row['id'] = xrefs[0]
        #     row['xrefs'] = ';'.join(xrefs[1:])
        # return row

    df = pd.read_csv(path, dtype=str)

    df['id'] = df.apply(build, axis=1)

    df = df.drop_duplicates('id')

    df['SMPDB ID'] = df.apply(lambda row: f"SMP:{row['SMPDB ID']}", axis=1)

    nodes = df
    edges = df

    nodes['category'] = 'protein'
    nodes = nodes.rename(columns={
        'Protein Name' : 'name',
        'Gene Name' : 'synonyms',
    })

    edges['predicate'] = 'chemical_to_pathway_association'
    edges = df.rename(columns={
        'id' : 'subject_id',
        'SMPDB ID' : 'object_id',
    })

    nodes = make_node_set(nodes)
    edges = make_edge_set(edges)

    return nodes, edges

def infer_edges(chemical_to_pathway_edges) -> List[pd.DataFrame]:
    e = chemical_to_pathway_edges.drop(columns='predicate')

    A = e.rename(columns={'subject_id' : 'A'})
    B = e.rename(columns={'subject_id' : 'B'})
    df = A.merge(B, on='object_id', how='inner')
    df = df[df['A'] < df['B']]
    df = df.drop(columns='object_id')
    df = df.rename(columns={'A' : 'subject_id', 'B' : 'object_id'})
    df['predicate'] = 'shares_pathway_with'
    df = make_edge_set(df)

    return pd.concat([chemical_to_pathway_edges, df])

if __name__ == '__main__':
    print('building proteins')
    p_node, p_edge = build_proteins(proteins_path)
    print('building metabolites')
    m_node, m_edge = build_metabolites(metabolites_path)
    print('building pathways')
    pathway_nodes = build_pathways(pathways_path)

    nodes = pd.concat([p_node, m_node, pathway_nodes])
    nodes.to_csv('nodes.csv', index=False)

    edges = pd.concat([p_edge, m_edge])

    edges = infer_edges(edges)
    edges.to_csv('edges.csv', index=False)
