import connexion
import six

from swagger_server.models.beacon_concept_category import BeaconConceptCategory  # noqa: E501
from swagger_server.models.beacon_knowledge_map_statement import BeaconKnowledgeMapStatement  # noqa: E501
from swagger_server.models.beacon_predicate import BeaconPredicate  # noqa: E501
from swagger_server.models.local_namespace import LocalNamespace  # noqa: E501
from swagger_server import util

import beacon_controller

def get_concept_categories():  # noqa: E501
    """get_concept_categories

    Get a list of concept categories and number of their concept instances documented by the knowledge source. These types should be mapped onto the Translator-endorsed Biolink Model concept type classes with local types, explicitly added as mappings to the Biolink Model YAML file. A frequency of -1 indicates the category can exist, but the count is unknown.  # noqa: E501


    :rtype: List[BeaconConceptCategory]
    """
    return beacon_controller.get_concept_categories()


def get_knowledge_map():  # noqa: E501
    """get_knowledge_map

    Get a high level knowledge map of the all the beacons by subject semantic type, predicate and semantic object type  # noqa: E501


    :rtype: List[BeaconKnowledgeMapStatement]
    """
    return beacon_controller.get_knowledge_map()


def get_namespaces():  # noqa: E501
    """get_namespaces

    Get a list of namespace (curie prefixes) mappings that this beacon can perform with its /exactmatches endpoint  # noqa: E501


    :rtype: List[LocalNamespace]
    """
    return beacon_controller.get_namespaces()


def get_predicates():  # noqa: E501
    """get_predicates

    Get a list of predicates used in statements issued by the knowledge source  # noqa: E501


    :rtype: List[BeaconPredicate]
    """
    return beacon_controller.get_predicates()
