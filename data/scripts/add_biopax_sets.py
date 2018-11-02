import pandas as pd
from beacon_controller.providers.curie import make_curie
import sys
import requests

if len(sys.argv) < 5:
    print('Required args: edge_path node_path biopax_edge_path biopax_node_path')
    quit()

edge_path = sys.argv[1]
node_path = sys.argv[2]
biopax_edge_path = sys.argv[3]
biopax_node_path = sys.argv[4]

def make_node_set(df):
    return df.reindex(columns=['id', 'name', 'category', 'description', 'synonyms', 'xrefs'])

def make_edge_set(df):
    return df.reindex(columns=['subject_id', 'predicate', 'object_id'])

def ensure_curie_or_None(s):
    if ':' in s:
        return s
    else:
        try:
            return make_curie(s)
        except:
            return s

def get_curie_from_genesymbol(s):
    # Gene symbols are sometimes used as ID's. We will search for
    # HGNC identifiers for the given symbols
    # try:
    uri='https://www.uniprot.org/uniprot/?query={s}&format=tab&columns=id,protein%20names,genes&sort=score&limit=100'.format(s=s)
    print(uri)
    df = pd.read_csv(uri, sep='\t')
    records = df.to_dict(orient='records')
    # import pudb; pu.db
    for record in records:
        for column, value in record.items():
            for term in str(value).split(' '):
                # print(column, term)
                if term.lower() == s.lower():
                    print('Mapped gene symbol {s} to {curie}'.format(s=s, curie=curie))
                    return record['Entry']
    return None

def is_not_curie(s):
    return ':' not in s

def infer_category(category):
    if category == 'SmallMoleculeReference':
        return 'chemical substance'
    elif category == 'ProteinReference':
        return 'protein'
    elif category == 'RnaReference':
        return 'RNA product'
    elif category == 'DnaReference':
        return 'genomic entity'
    else:
        raise Exception('Unknown category {category}'.format(category=category))

if __name__ == '__main__':
    print('loading biopax files')
    biopax_edges = pd.read_csv(biopax_edge_path, sep='\t', dtype=str, header=None, names=['subject_id', 'predicate', 'object_id'])
    biopax_nodes = pd.read_csv(biopax_node_path, sep='\t', dtype=str, header=0, names=['id', 'category', 'name', 'xrefs', 'RELATIONSHIP_XREF'])

    biopax_nodes['category'] = biopax_nodes['category'].apply(infer_category)
    biopax_edges['predicate'] = biopax_edges['predicate'].apply(lambda x: x.replace('-', '_'))

    biopax_edges = make_edge_set(biopax_edges)
    biopax_nodes = make_node_set(biopax_nodes)

    edges = pd.read_csv(edge_path)
    nodes = pd.read_csv(node_path)

    print('Concatenating biopax files to original files')
    edges = pd.concat([edges, biopax_edges])
    nodes = pd.concat([nodes, biopax_nodes])

    edges = edges.drop_duplicates()
    nodes = nodes.drop_duplicates('id')

    print('Ensuring all identifiers are curies')
    edges.subject_id = edges.subject_id.apply(ensure_curie_or_None)
    edges.object_id = edges.object_id.apply(ensure_curie_or_None)
    nodes.id = nodes.id.apply(ensure_curie_or_None)

    c1, c2 = edges.shape[0], nodes.shape[0]

    # Build up a map of gene symbols (id's that cannot be made into curies) to HMDB id's.
    # d = {}
    # for series in [edges.subject_id, edges.object_id, nodes.id]:
    #     for symbol in series[series.apply(is_not_curie)].unique():
    #         if symbol not in d:
    #             d[symbol] = get_curie_from_genesymbol(symbol)
    #
    # edges.subject_id = edges.subject_id.apply(lambda x: d[x] if x in d else x)
    # edges.object_id = edges.object_id.apply(lambda x: d[x] if x in d else x)
    # nodes.id = nodes.id.apply(lambda x: d[x] if x in d else x)

    edges = edges[(edges.subject_id.isnull() == False) & (edges.object_id.isnull() == False)]
    nodes = nodes[nodes.id.isnull() == False]

    print('threw away {} many edges'.format(edges.shape[0] - c1))
    print('threw away {} many nodes'.format(nodes.shape[0] - c2))

    print('Overwriting original files')
    edges.to_csv(edge_path, index=False)
    nodes.to_csv(node_path, index=False)
