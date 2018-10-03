"""
This module provides methods for converting the values of columns from the
identifiers as the database represents them, to CURIE identifiers.

The prefixes might not all be proper.
"""

def build_fn(column, str_generator):
    def fn(row):
        try:
            if column not in row:
                return None
            x = row[column]
            if x is None:
                return None
            else:
                return str_generator(x)
        except Exception as e:
            raise Exception(f'Exception thrown for {column}: {str(e)}')
    return fn

def build_prefix_replacer(column, prefix):
    return build_fn(column, lambda x: f'{prefix}:{x.replace(prefix, "")}')

def build_prefix_adder(column, prefix):
    return build_fn(column, lambda x: f'{prefix}:{x}')

smpdb = build_prefix_replacer('SMPDB ID', 'SMP')
drugbank = build_prefix_replacer('DrugBank ID', 'DB')
hmdb = build_prefix_replacer('HMDB ID', 'HMDB')
hmdbp = build_prefix_replacer('HMDBP ID', 'HMDBP')
genebank = build_prefix_replacer('GenBank ID', 'GB')

chebi = build_prefix_adder('ChEBI ID', 'CHEBI')
kegg = build_prefix_adder('KEGG ID', 'KEGG')
uniprot = build_prefix_adder('Uniprot ID', 'UNIPROT')

metabolite = build_fn('Metabolite ID', lambda x: f'PW:{x.replace("PW_", "")}')
