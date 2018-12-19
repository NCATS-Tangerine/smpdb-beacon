"""
From the /data directory run like:

$ python scripts/fix_curies.py --file nodes.csv
"""

import click
import pandas as pd

prefix_fix_dict = {
    'KEGG COMPOUND' : 'KEGG',
    'CHEBI:CHEBI' : 'CHEBI',
    'PUBCHEM-COMPOUND' : 'PUBCHEM.COMPOUND',
    'CHEBI:CHEBI' : 'CHEBI',
}

def fix_prefixes(row):
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

def get_prefixes(df):
    s = set()
    def add_prefixes(curies):
        if isinstance(curies, str):
            curies = curies.split(';')
            for curie in curies:
                prefix, _ = curie.rsplit(':', 1)
                s.add(prefix)
    df.xrefs.apply(add_prefixes)
    df.id.apply(add_prefixes)
    return s

@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), required=True, help='Path to the file to fix')
@click.option('--out', '-o', help='Path to save the output')
@click.option('--separator', '-s', default=',', type=str, help='The separator to use, defaults to comma (",")')
def main(file, out, separator):
    df = pd.read_csv(file, sep=separator)

    print('Prefixes before cleanup:', get_prefixes(df))

    df = df.apply(fix_prefixes, axis=1)

    print('Prefixes after cleanup:', get_prefixes(df))

    df.to_csv(out, sep=separator)

if __name__ == '__main__':
    main()
