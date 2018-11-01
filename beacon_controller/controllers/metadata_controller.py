from swagger_server.models.beacon_concept_category import BeaconConceptCategory  # noqa: E501
from swagger_server.models.beacon_knowledge_map_statement import BeaconKnowledgeMapStatement  # noqa: E501
from swagger_server.models.beacon_knowledge_map_object import BeaconKnowledgeMapObject
from swagger_server.models.beacon_knowledge_map_subject import BeaconKnowledgeMapSubject
from swagger_server.models.beacon_knowledge_map_predicate import BeaconKnowledgeMapPredicate
from swagger_server.models.beacon_predicate import BeaconPredicate  # noqa: E501

from beacon_controller.providers import pandas_helper as dh
import beacon_controller.biolink_model as blm
from itertools import product
import functools

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
    d = df.groupby(['subject_category', 'predicate', 'object_category']).size().to_dict()

    kmaps = []
    for (subject_category, predicate, object_category), frequency in d.items():
        s = blm.get_slot(predicate)
        if s is not None:
            edge_label = predicate
            relation = predicate
        else:
            edge_label = 'related_to'
            relation = predicate

        edges = df[df['predicate'] == predicate]

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
    d = df.groupby('predicate').size().to_dict()

    predicates = []
    for predicate, frequency in d.items():
        s = blm.get_slot(predicate)
        if s is not None:
            edge_label = predicate
            relation = predicate
            description = s.description
        else:
            edge_label = 'related_to'
            relation = predicate
            description = None

        predicates.append(BeaconPredicate(
            edge_label=edge_label,
            relation=relation,
            description=description,
            frequency=frequency,
        ))
    return predicates
