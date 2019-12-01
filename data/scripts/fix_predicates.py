"""
From the /data directory run like:

$ python scripts/fix_predicates.py --file edges.csv
"""

import click
import pandas as pd

relation_to_edgelabel = {
    'chemical_to_pathway_association' : 'chemical_to_pathway_association',

    'shares_pathway_with' : 'in_pathway_with',
    'controls_transport_of_chemical' : 'affects_transport_of',
    'controls_transport_of' : 'affects_transport_of',
    'catalysis_precedes' : 'precedes',
    'used_to_produce' : 'produces',
    'in_complex_with' : 'in_complex_with',
    'interacts_with' : 'interacts_with',
    'chemical_affects' : 'affects',

    'consumption_controlled_by' : 'related_to',
    'reacts_with' : 'related_to',
    'neighbor_of' : 'related_to',
    'controls_state_change_of' : 'related_to',
}

def fix_predicates(row):
    """
    Goes row by row fixing the id and xref prefixes
    """

    if isinstance(row.xrefs, str):
        xrefs = set()
        for xref in row.xrefs.split(';'):
            prefix, local_id = xref.rsplit(':', 1)
            prefix = prefix.upper()
            if prefix in prefix_fix_dict:
                xrefs.add(f'{prefix_fix_dict[prefix]}:{local_id}')
            else:
                xrefs.add(f'{prefix}:{local_id}')
        row['xrefs'] = ';'.join(xrefs)
    else:
        row['xrefs'] = ''

    prefix, local_id = row.id.rsplit(':', 1)
    prefix = prefix.upper()

    if prefix in prefix_fix_dict:
        row['id'] = f'{prefix_fix_dict[prefix]}:{local_id}'
    else:
        row['id'] = f'{prefix}:{local_id}'

    return row

@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), required=True, help='Path to the file to fix')
@click.option('--out', '-o', help='Path to save the output')
@click.option('--separator', '-s', default=',', type=str, help='The separator to use, defaults to comma (",")')
def main(file, out, separator):
    """
    This script splits statement predicates into edge labels and relations.
    """
    df = pd.read_csv(file, sep=separator)

    df = df.rename(columns={'predicate' : 'relation'})
    df['edgelabel'] = df['relation'].apply(lambda relation: relation_to_edgelabel.get(relation, 'related_to'))

    # df = df.apply(fix_predicates, axis=1)

    df.to_csv(out, sep=separator)

if __name__ == '__main__':
    main()
