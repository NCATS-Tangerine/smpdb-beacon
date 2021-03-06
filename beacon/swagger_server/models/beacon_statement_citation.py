# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class BeaconStatementCitation(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: str=None, uri: str=None, name: str=None, evidence_type: str=None, date: str=None):  # noqa: E501
        """BeaconStatementCitation - a model defined in Swagger

        :param id: The id of this BeaconStatementCitation.  # noqa: E501
        :type id: str
        :param uri: The uri of this BeaconStatementCitation.  # noqa: E501
        :type uri: str
        :param name: The name of this BeaconStatementCitation.  # noqa: E501
        :type name: str
        :param evidence_type: The evidence_type of this BeaconStatementCitation.  # noqa: E501
        :type evidence_type: str
        :param date: The date of this BeaconStatementCitation.  # noqa: E501
        :type date: str
        """
        self.swagger_types = {
            'id': str,
            'uri': str,
            'name': str,
            'evidence_type': str,
            'date': str
        }

        self.attribute_map = {
            'id': 'id',
            'uri': 'uri',
            'name': 'name',
            'evidence_type': 'evidence_type',
            'date': 'date'
        }

        self._id = id
        self._uri = uri
        self._name = name
        self._evidence_type = evidence_type
        self._date = date

    @classmethod
    def from_dict(cls, dikt) -> 'BeaconStatementCitation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The BeaconStatementCitation of this BeaconStatementCitation.  # noqa: E501
        :rtype: BeaconStatementCitation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this BeaconStatementCitation.

        CURIE-encoded identifier to a citation to evidence supporting the given statement (e.g. PMID of a pubmed abstract)   # noqa: E501

        :return: The id of this BeaconStatementCitation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this BeaconStatementCitation.

        CURIE-encoded identifier to a citation to evidence supporting the given statement (e.g. PMID of a pubmed abstract)   # noqa: E501

        :param id: The id of this BeaconStatementCitation.
        :type id: str
        """

        self._id = id

    @property
    def uri(self) -> str:
        """Gets the uri of this BeaconStatementCitation.

        (optional) expansion of the citation CURIE   # noqa: E501

        :return: The uri of this BeaconStatementCitation.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri: str):
        """Sets the uri of this BeaconStatementCitation.

        (optional) expansion of the citation CURIE   # noqa: E501

        :param uri: The uri of this BeaconStatementCitation.
        :type uri: str
        """

        self._uri = uri

    @property
    def name(self) -> str:
        """Gets the name of this BeaconStatementCitation.

        canonical human readable and searchable name of the citation (i.e. publication title, comment, etc.)   # noqa: E501

        :return: The name of this BeaconStatementCitation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this BeaconStatementCitation.

        canonical human readable and searchable name of the citation (i.e. publication title, comment, etc.)   # noqa: E501

        :param name: The name of this BeaconStatementCitation.
        :type name: str
        """

        self._name = name

    @property
    def evidence_type(self) -> str:
        """Gets the evidence_type of this BeaconStatementCitation.

        class of evidence supporting the statement made in an edge - typically a class from the ECO ontology (e.g. ECO:0000220 'sequencing assay evidence', see [Evidence Ontology](http://purl.obolibrary.org/obo/eco.owl)   # noqa: E501

        :return: The evidence_type of this BeaconStatementCitation.
        :rtype: str
        """
        return self._evidence_type

    @evidence_type.setter
    def evidence_type(self, evidence_type: str):
        """Sets the evidence_type of this BeaconStatementCitation.

        class of evidence supporting the statement made in an edge - typically a class from the ECO ontology (e.g. ECO:0000220 'sequencing assay evidence', see [Evidence Ontology](http://purl.obolibrary.org/obo/eco.owl)   # noqa: E501

        :param evidence_type: The evidence_type of this BeaconStatementCitation.
        :type evidence_type: str
        """

        self._evidence_type = evidence_type

    @property
    def date(self) -> str:
        """Gets the date of this BeaconStatementCitation.

        publication date of annotation (generally of format 'yyyy-mm-dd')   # noqa: E501

        :return: The date of this BeaconStatementCitation.
        :rtype: str
        """
        return self._date

    @date.setter
    def date(self, date: str):
        """Sets the date of this BeaconStatementCitation.

        publication date of annotation (generally of format 'yyyy-mm-dd')   # noqa: E501

        :param date: The date of this BeaconStatementCitation.
        :type date: str
        """

        self._date = date
