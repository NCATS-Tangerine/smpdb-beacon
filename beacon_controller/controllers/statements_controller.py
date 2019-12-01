from swagger_server.models.beacon_statement import BeaconStatement
from swagger_server.models.beacon_statement_with_details import BeaconStatementWithDetails
from swagger_server.models.beacon_statement_annotation import BeaconStatementAnnotation
from swagger_server.models.beacon_statement_object import BeaconStatementObject
from swagger_server.models.beacon_statement_predicate import BeaconStatementPredicate
from swagger_server.models.beacon_statement_subject import BeaconStatementSubject

import beacon_controller.providers.pandas_helper as dh
import beacon_controller.biolink_model as blm

def get_statement_details(statement_id, keywords=None, offset=None, size=None):  # noqa: E501
    """get_statement_details

    Retrieves a details relating to a specified concept-relationship statement include &#39;is_defined_by and &#39;provided_by&#39; provenance; extended edge properties exported as tag &#x3D; value; and any associated annotations (publications, etc.)  cited as evidence for the given statement.  # noqa: E501

    :param statement_id: (url-encoded) CURIE identifier of the concept-relationship statement (\&quot;assertion\&quot;, \&quot;claim\&quot;) for which associated evidence is sought
    :type statement_id: str
    :param keywords: an array of keywords or substrings against which to  filter annotation names (e.g. publication titles).
    :type keywords: List[str]
    :param offset: offset (cursor position) to next batch of annotation entries of amount &#39;size&#39; to return.
    :type offset: int
    :param size: maximum number of evidence citation entries requested by the client; if this  argument is omitted, then the query is expected to returned all of the available annotation for this statement
    :type size: int

    :rtype: BeaconStatementWithDetails
    """
    print(statement_id)
    subject_id, edge_label, relation, object_id = statement_id.split('|')
    s = get_statements(s=[subject_id], edge_label=edge_label, relation=relation, t=[object_id], offset=0, size=1)
    for statement in s:
        return BeaconStatementWithDetails(
            id=statement_id,
            is_defined_by='http://smpdb.ca/',
            provided_by='starinformatics',
            qualifiers=[],
            annotation=[],
            evidence=[],
        )



def get_statements(s=None, s_keywords=None, s_categories=None, edge_label=None, relation=None, t=None, t_keywords=None, t_categories=None, offset=None, size=None):  # noqa: E501
    """get_statements

    Given a constrained set of some [CURIE-encoded](https://www.w3.org/TR/curie/) &#39;s&#39; (&#39;source&#39;) concept identifiers, categories and/or keywords (to match in the concept name or description), retrieves a list of relationship statements where either the subject or the object concept matches any of the input source concepts provided.  Optionally, a set of some &#39;t&#39; (&#39;target&#39;) concept identifiers, categories and/or keywords (to match in the concept name or description) may also be given, in which case a member of the &#39;t&#39; concept set should matchthe concept opposite an &#39;s&#39; concept in the statement. That is, if the &#39;s&#39; concept matches a subject, then the &#39;t&#39; concept should match the object of a given statement (or vice versa).  # noqa: E501

    :param s: An (optional) array set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of &#39;source&#39; (&#39;start&#39;) concepts possibly known to the beacon. Unknown CURIES should simply be ignored (silent match failure).
    :type s: List[str]
    :param s_keywords: An (optional) array of keywords or substrings against which to filter &#39;source&#39; concept names and synonyms
    :type s_keywords: List[str]
    :param s_categories: An (optional) array set of &#39;source&#39; concept categories (specified as Biolink name labels codes gene, pathway, etc.) to which to constrain concepts matched by the main keyword search (see [Biolink Model](https://biolink.github.io/biolink-model) for the full list of codes)
    :type s_categories: List[str]
    :param edge_label: (Optional) predicate edge label against which to constrain the search for statements (&#39;edges&#39;) associated with the given query seed concept. The predicate edge_names for this parameter should be as published by the /predicates API endpoint and must be taken from the minimal predicate (&#39;slot&#39;) list of the [Biolink Model](https://biolink.github.io/biolink-model).
    :type edge_label: str
    :param relation: (Optional) predicate relation against which to constrain the search for statements (&#39;edges&#39;) associated with the given query seed concept. The predicate relations for this parameter should be as published by the /predicates API endpoint and the preferred format is a CURIE  where one exists, but strings/labels acceptable. This relation may be equivalent to the edge_label (e.g. edge_label: has_phenotype, relation: RO:0002200), or a more specific relation in cases where the source provides more granularity (e.g. edge_label: molecularly_interacts_with, relation: RO:0002447)
    :type relation: str
    :param t: An (optional) array set of [CURIE-encoded](https://www.w3.org/TR/curie/) identifiers of &#39;target&#39; (&#39;opposite&#39; or &#39;end&#39;) concepts possibly known to the beacon. Unknown CURIEs should simply be ignored (silent match failure).
    :type t: List[str]
    :param t_keywords: An (optional) array of keywords or substrings against which to filter &#39;target&#39; concept names and synonyms
    :type t_keywords: List[str]
    :param t_categories: An (optional) array set of &#39;target&#39; concept categories (specified as Biolink name labels codes gene, pathway, etc.) to which to constrain concepts matched by the main keyword search (see [Biolink Model](https://biolink.github.io/biolink-model) for the full list of codes)
    :type t_categories: List[str]
    :param offset: offset (cursor position) to next batch of statements of amount &#39;size&#39; to return.
    :type offset: int
    :param size: maximum number of concept entries requested by the client; if this argument is omitted, then the query is expected to returned all  the available data for the query
    :type size: int

    :rtype: List[BeaconStatement].
    """
    if size is None:
        size = 10

    edges = dh.find_edges(
        s,
        s_keywords,
        s_categories,
        t,
        t_keywords,
        t_categories,
        [edge_label] if edge_label is not None else [],
        [relation] if relation is not None else [],
        offset,
        size
    )

    statements = []

    for edge in edges:
        s = BeaconStatementSubject(
            id=edge['subject_id'],
            name=edge['subject_name'],
            categories=[edge['subject_category']],
        )

        p = BeaconStatementPredicate(
            edge_label=edge['edgelabel'],
            relation=edge['relation'],
            negated=False,
        )

        o = BeaconStatementSubject(
            id=edge['object_id'],
            name=edge['object_name'],
            categories=[edge['object_category']],
        )

        statements.append(BeaconStatement(
            id=f'{s.id}|{p.edge_label}|{p.relation}|{o.id}',
            subject=s,
            predicate=p,
            object=o
        ))

    return statements



    statements = []
    for source_id in s:
        source_id = source_id.upper()

        if source_id.startswith('SMP'):
            # In this case source_id refers to a pathway

            if edge_label is not None and edge_label != 'chemical_to_pathway_association':
                continue
            if relation is not None and relation != 'chemical to pathway association':
                continue

            p = proteins.search_by_pathway_curie(source_id)
            m = metabolites.search_by_pathway_curie(source_id)

            for concept in p + m:
                concept_id = None
                for key, value in concept.items():
                    if 'curie' in key and value is not None:
                        concept_id = value

                if concept['category'] == 'metabolite':
                    name = concept['Metabolite Name']
                elif concept['category'] == 'protein':
                    name = concept['Protein Name']
                else:
                    raise Exception(f'No category allowed of type {concept["category"]}')

                s = BeaconStatementSubject(
                    id=concept_id,
                    categories=[concept['category']],
                    name=name
                )

                p = BeaconStatementPredicate(
                    edge_label='chemical_to_pathway_association',
                    relation='chemical to pathway association',
                    negated=False
                )

                o = BeaconStatementObject(
                    id=source_id,
                    categories=['pathway'],
                    name=concept['Pathway Name']
                )

                statements.append(BeaconStatement(
                    id=f'{concept_id}:chemical_to_pathway_association:{source_id}',
                    subject=s,
                    predicate=p,
                    object=o
                ))
        else:
            # In this case source_id refers either to a molecule

            if edge_label is not None and edge_label != 'in_pathway_with':
                continue
            if relation is not None and relation != 'in pathway with':
                continue

            p = proteins.search_by_molecule_curie(source_id)
            m = metabolites.search_by_molecule_curie(source_id)

            for concept in p + m:
                concept_id = None
                for key, value in concept.items():
                    if 'curie' in key and value is not None:
                        concept_id = value

                if concept['category'] == 'metabolite':
                    object_name = concept['Metabolite Name']
                elif concept['category'] == 'protein':
                    object_name = concept['Protein Name']
                else:
                    raise Exception(f'No category allowed of type {concept["category"]}')

                statements.append(build_statement(
                    subject_id=concept_id,
                    subject_category=concept['category'],
                    subject_name=object_name,
                    edge_label='chemical_to_pathway_association',
                    object_id=concept['smpdb_curie'],
                    object_name=concept['Pathway Name'],
                    object_category='pathway'
                ))

                if concept['smpdb_curie'] is not None:
                    subjects = proteins.search_by_pathway_curie(concept['smpdb_curie'])
                    subjects += metabolites.search_by_pathway_curie(concept['smpdb_curie'])

                    for subject in subjects:
                        for key, value in subject.items():
                            if 'curie' in key and value is not None:
                                subject_id = value

                        if subject['category'] == 'metabolite':
                            subject_name = subject['Metabolite Name']
                        elif subject['category'] == 'protein':
                            subject_name = subject['Protein Name']
                        else:
                            raise Exception(f'No category allowed of type {concept["category"]}')

                        if subject_name == object_name:
                            continue

                        statements.append(build_statement(
                            subject_id=subject_id,
                            subject_name=subject_name,
                            subject_category=subject['category'],
                            edge_label='in_pathway_with',
                            object_id=concept_id,
                            object_name=object_name,
                            object_category=concept['category']
                        ))

    if offset is not None:
        statements = statements[offset:]

    if size is not None:
        statements = statements[:size]

    d = {}
    for s in statements:
        d[s.id] = s
    statements = list(d.values())

    return statements


def build_statement(
    subject_id,
    subject_name,
    subject_category,
    edge_label,
    object_id,
    object_name,
    object_category
):
    s = BeaconStatementSubject(
        id=subject_id,
        categories=[subject_category],
        name=subject_name
    )

    p = BeaconStatementPredicate(
        edge_label=edge_label,
        relation=edge_label.replace('_', ' '),
        negated=False
    )

    o = BeaconStatementObject(
        id=object_id,
        categories=[object_category],
        name=object_name
    )

    return BeaconStatement(
        id=f'{subject_id}:{edge_label}:{object_id}',
        subject=s,
        predicate=p,
        object=o
    )
