import re

uniprot = '^([A-N,R-Z][0-9][A-Z][A-Z, 0-9][A-Z, 0-9][0-9])|([O,P,Q][0-9][A-Z, 0-9][A-Z, 0-9][A-Z, 0-9][0-9])(\.\d+)?$'
kegg = '^C\d+$'
hmdb = '^HMDB\d+$'

pattern_to_prefix = {
    re.compile(uniprot) : 'UNIPROT',
    re.compile(kegg) : 'KEGG',
    re.compile(hmdb) : 'HMDB',
}

prefix_to_category = {
    'UNIPROT' : 'protein',
    'HMDB' : 'chemical substance',
    'KEGG' : 'chemical substance',
    'CHEBI' : 'chemical substance',
}

prefix_to_uri = {
    'UNIPROT' : 'https://www.uniprot.org/uniprot/',
    'CHEBI' : 'https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:',
    'KEGG' : 'https://www.kegg.jp/entry/',
    'HMDB' : 'http://www.hmdb.ca/metabolites/'
}

prefix_fix_dict = {
    'KEGG COMPOUND' : 'KEGG',
    'CHEBI:CHEBI' : 'CHEBI',
    'PUBCHEM-COMPOUND' : 'PUBCHEM.COMPOUND',
    'CHEBI:CHEBI' : 'CHEBI',

    'KEGG' : 'KEGG',
    'CHEBI' : 'CHEBI',
    'UNIPROT' : 'UNIPROT',
    'CAS' : 'CAS',
    'CHEMSPIDER' : 'CHEMSPIDER',
    'HMDB' : 'HMDB',
}

def fix_prefix(curie, default=None):
    curie = curie.upper()
    prefix, local_id = curie.rsplit(':', 1)
    if prefix in prefix_fix_dict:
        return f'{prefix_fix_dict[prefix]}:{local_id}'
    else:
        print(f"no prefix match for {curie}")
        return default

def is_valid_id(s:str) -> bool:
    try:
        make_curie(s)
        return True
    except:
        return False

def make_curie(s:str) -> str:
    s = s.upper()
    if s.startswith('CHEBI:'):
        return s
    for pattern, prefix in pattern_to_prefix.items():
        if pattern.match(s):
            return f'{prefix}:{s}'
    raise Exception(f'Could not find a prefix for identifier {s}')

def make_uri(curie:str) -> str:
    prefix, local_id = curie.upper().split(':', 1)
    if prefix in prefix_to_uri:
        return prefix_to_uri[prefix] + local_id
    else:
        return None

def get_category(curie:str) -> str:
    prefix, local_id = curie.upper().split(':', 1)
    if prefix in prefix_to_category:
        return prefix_to_category[prefix]
    else:
        return None

def get_db_identifier(curie:str) -> str:
    if curie.startswith('CHEBI'):
        return curie
    else:
        prefix, local_id = curie.rsplit(':', 1)
        return local_id
