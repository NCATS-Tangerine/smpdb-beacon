import pandas as pd

pd.set_option('display.max_columns', None)

def fill_edges(edges:pd.DataFrame, nodes:pd.DataFrame) -> pd.DataFrame:
    """
    Takes an edge set (having columns subject_id, predicate, object_id), and a
    node set (having columns id, name, category), and returns an edge set with
    the subject and object's name and category columns appended.
    """
    nodes = nodes[['id', 'name', 'category']]
    nodes = nodes.drop_duplicates('id')
    edges = edges.drop_duplicates()

    count = edges.shape[0]

    nodes = nodes.rename(columns={'id' : 'subject_id', 'name' : 'subject_name', 'category' : 'subject_category'})
    edges = edges.merge(nodes, on='subject_id', how='inner')

    nodes = nodes.rename(columns={'subject_id' : 'object_id', 'subject_name' : 'object_name', 'subject_category' : 'object_category'})
    edges = edges.merge(nodes, on='object_id', how='inner')

    edges = edges.drop_duplicates()

    print('Lost {} rows'.format(count - edges.shape[0]))

    return edges

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Arguments: edge_path node_path')
        quit()

    edge_path = sys.argv[1]
    node_path = sys.argv[2]

    edges = pd.read_csv(edge_path)
    nodes = pd.read_csv(node_path)

    edges = fill_edges(edges, nodes)
    edges.to_csv(edge_path, index=False)
