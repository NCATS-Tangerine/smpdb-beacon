from swagger_server.models.beacon_concept_category import BeaconConceptCategory  # noqa: E501
from swagger_server.models.beacon_knowledge_map_statement import BeaconKnowledgeMapStatement  # noqa: E501
from swagger_server.models.beacon_knowledge_map_object import BeaconKnowledgeMapObject
from swagger_server.models.beacon_knowledge_map_subject import BeaconKnowledgeMapSubject
from swagger_server.models.beacon_knowledge_map_predicate import BeaconKnowledgeMapPredicate
from swagger_server.models.beacon_predicate import BeaconPredicate  # noqa: E501
from swagger_server.models.namespace import Namespace
from swagger_server.models.local_namespace import LocalNamespace

from beacon_controller.providers import pandas_helper as dh
import beacon_controller.biolink_model as blm

from itertools import product
from collections import defaultdict, Counter

import functools

from prefixcommons.curie_util import default_curie_maps as cmaps

def prefix_to_uri(prefix):
    """
    Pulls the default curie map from prefixcommons and gets the uri from it
    """
    prefix = prefix.upper()

    for cmap in cmaps:
        for key, value in cmap.items():
            if prefix.lower() == key.lower():
                return value
    else:
        return f'http://identifiers.org/{prefix.lower()}/'

@functools.lru_cache()
def get_concept_categories():  # noqa: E501
    """get_concept_categories

    Get a list of concept categories and number of their concept instances documented by the knowledge source. These types should be mapped onto the Translator-endorsed Biolink Model concept type classes with local types, explicitly added as mappings to the Biolink Model YAML file. A frequency of -1 indicates the category can exist, but the count is unknown.  # noqa: E501


    :rtype: List[BeaconConceptCategory]
    """
    df = dh.load_nodes()
    d = df.groupby('category').size().to_dict()
    categories = []
    for category, frequency in d.items():
        c = blm.get_class(category)
        if c is not None:
            local_category = category
            description = c.description
        else:
            category = 'named thing'
            local_category = category
            description = None

        categories.append(BeaconConceptCategory(
            category=category,
            local_category=local_category,
            description=description,
            frequency=frequency,
        ))
    return categories


def prefix(s):
    if isinstance(s, str) and ':' in s:
        prefix, local_id = s.rsplit(':', 1)
        return prefix
    else:
        return s

@functools.lru_cache()
def get_knowledge_map():  # noqa: E501
    """get_knowledge_map

    Get a high level knowledge map of the all the beacons by subject semantic type, predicate and semantic object type  # noqa: E501


    :rtype: List[BeaconKnowledgeMapStatement]
    """
    df = dh.load_edges()
    groups = df.groupby(['subject_category', 'edgelabel', 'relation', 'object_category'])
    d = groups.size().to_dict()

    kmaps = []
    for (subject_category, edge_label, relation, object_category), frequency in d.items():
        s = blm.get_slot(edge_label)

        edges = df[df['relation'] == relation]

        subject_prefixes = edges.subject_id.apply(prefix).unique()
        object_prefixes = edges.object_id.apply(prefix).unique()

        subject_prefixes = [s for s in list(subject_prefixes) if s is not None]
        object_prefixes = [s for s in list(object_prefixes) if s is not None]

        s = BeaconKnowledgeMapSubject(
            category=subject_category,
            prefixes=subject_prefixes,
        )

        p = BeaconKnowledgeMapPredicate(
            edge_label=edge_label,
            relation=relation,
            negated=False,
        )

        o = BeaconKnowledgeMapObject(
            category=object_category,
            prefixes=object_prefixes,
        )

        kmaps.append(BeaconKnowledgeMapStatement(
            subject=s,
            predicate=p,
            object=o,
            frequency=frequency
        ))

    return kmaps

@functools.lru_cache()
def get_predicates():  # noqa: E501
    """get_predicates

    Get a list of predicates used in statements issued by the knowledge source  # noqa: E501


    :rtype: List[BeaconPredicate]
    """
    df = dh.load_edges()
    d = df.groupby(['edgelabel', 'relation']).size().to_dict()

    predicates = []
    for (edge_label, relation), frequency in d.items():
        s = blm.get_slot(edge_label)

        predicates.append(BeaconPredicate(
            edge_label=edge_label,
            relation=relation,
            description=s.description,
            frequency=frequency,
        ))
    return predicates

def get_prefix(curie:str) -> str:
    prefix, _ = curie.rsplit(':', 1)
    return prefix

@functools.lru_cache()
def get_namespaces():  # noqa: E501
    """get_namespaces

    Get a list of namespace (curie prefixes) mappings that this beacon can perform with its /exactmatches endpoint  # noqa: E501


    :rtype: List[LocalNamespace]
    """
    df = dh.load_nodes()

    d = defaultdict(set)
    l = []

    def fill_metadata(row):
        prefix = get_prefix(row.id)
        if isinstance(row.xrefs, str):
            xrefs = [get_prefix(curie) for curie in row.xrefs.split(';') if curie.lower() != row.id.lower()]
            if xrefs != []:
                d[prefix].update(xrefs)
                l.append(prefix)


    df.apply(fill_metadata, axis=1)

    count = Counter(l)

    local_namespaces = []
    for local_prefix, curie_mappings in d.items():
        namespaces = []
        for prefix in curie_mappings:
            namespaces.append(Namespace(prefix=prefix, uri=prefix_to_uri(prefix)))

        local_namespaces.append(LocalNamespace(
            local_prefix=local_prefix,
            clique_mappings=namespaces,
            uri=prefix_to_uri(local_prefix),
            frequency=count[local_prefix]
        ))

    return local_namespaces
