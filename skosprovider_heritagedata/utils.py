#!/usr/bin/python
# -*- coding: utf-8 -*-

import rdflib
from rdflib.term import URIRef

from skosprovider.skos import (
    Concept,
    Collection,
    Label,
    Note,
    ConceptScheme)

from skosprovider.exceptions import ProviderUnavailableException

import logging
import sys

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    binary_type = bytes
else:  # pragma: no cover
    binary_type = str

log = logging.getLogger(__name__)

from rdflib.namespace import RDF, SKOS, DC, RDFS

PROV = rdflib.Namespace('http://www.w3.org/ns/prov#')


class heritagedata_to_skos():
    def __init__(self, concept_scheme=None):
        self.graph = None
        self.concept_scheme = concept_scheme

    def conceptscheme_from_uri(self, conceptscheme_uri):
        self.graph = uri_to_graph('%s.rdf' % (conceptscheme_uri))

        # get the conceptscheme
        conceptscheme = ConceptScheme(conceptscheme_uri)
        conceptscheme.notes = []
        conceptscheme.labels = []
        if self.graph is not False:
            for s, p, o in self.graph.triples((URIRef(conceptscheme_uri), RDFS.label, None)):
                label = Label(o.toPython(), "prefLabel", 'en')
                conceptscheme.labels.append(label)
        return conceptscheme

    def things_from_graph(self, graph):
        self.graph = graph
        clist = []
        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Concept)):
            uri = str(sub)
            con = Concept(_split_uri(uri, 1), uri=uri)
            con.broader = self._create_from_subject_predicate(sub, SKOS.broader)
            con.narrower = self._create_from_subject_predicate(sub, SKOS.narrower)
            con.related = self._create_from_subject_predicate(sub, SKOS.related)
            con.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            con.notes = self._create_from_subject_typelist(sub, Note.valid_types)
            con.subordinate_arrays = []
            con.concept_scheme = self.concept_scheme
            clist.append(con)

            # at this moment, Heritagedata does not support SKOS.Collection
        # for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Collection)):
        # uri = str(sub)
        #     col = Collection(_split_uri(uri, 1), uri=uri)
        #     col.members = self._create_from_subject_predicate(sub, SKOS.member)
        #     col.labels = self._create_from_subject_typelist(sub, Label.valid_types)
        #     col.notes = self._create_from_subject_typelist(sub, Note.valid_types)
        #     clist.append(col)

        return clist

    def _create_from_subject_typelist(self, subject, typelist):
        list = []
        for p in typelist:
            term = SKOS.term(p)
            list.extend(self._create_from_subject_predicate(subject, term))
        return list

    def _create_from_subject_predicate(self, subject, predicate):
        list = []
        for s, p, o in self.graph.triples((subject, predicate, None)):
            type = predicate.split('#')[-1]
            if Label.is_valid_type(type):
                o = self._create_label(o, type)
            elif Note.is_valid_type(type):
                o = self._create_note(o, type)
            else:
                o = _split_uri(o, 1)
            if o:
                list.append(o)
        return list

    def _create_label(self, literal, type):
        language = literal.language
        if language is None:
            return 'und'  # return undefined code when no language
        return Label(literal.toPython(), type, language)

    def _create_note(self, literal, type):
        if not Note.is_valid_type(type):
            raise ValueError('Type of Note is not valid.')

        return Note(text_(literal.value, encoding="utf-8"), type, self._get_language_from_literal(literal))

    def _get_language_from_literal(self, data):
        if data.language is None:
            return 'und'  # return undefined code when no language
        return text_(data.language, encoding="utf-8")


def _split_uri(uri, index):
    return uri.strip('/').rsplit('/', 1)[index]


def uri_to_graph(uri):
    graph = rdflib.Graph()
    try:
        graph.parse(uri)
        return graph
    except:
        raise ProviderUnavailableException("URI niet bereikbaar: %s" % uri)




def text_(s, encoding='latin-1', errors='strict'):
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s


