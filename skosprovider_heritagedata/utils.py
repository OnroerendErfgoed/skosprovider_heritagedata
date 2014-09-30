#!/usr/bin/python
# -*- coding: utf-8 -*-

import rdflib

from skosprovider.skos import (
    Concept,
    Collection,
    Label,
    Note
)

import logging
log = logging.getLogger(__name__)

from rdflib.namespace import RDF, SKOS, DC
PROV = rdflib.Namespace('http://www.w3.org/ns/prov#')

class heritagedata_to_skos():

    def __init__(self, graph):
        self.graph = graph

    def from_graph(self):
        clist = []
        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Concept)):
            uri = str(sub)
            con = Concept(uri_to_id(uri), uri=uri)
            con.broader = self._create_from_subject_predicate(sub, SKOS.broader)
            con.narrower = self._create_from_subject_predicate(sub, SKOS.narrower)
            con.related = self._create_from_subject_predicate(sub, SKOS.related)
            con.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            con.notes = self._create_from_subject_typelist(sub, Note.valid_types)
            clist.append(con)

        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Collection)):
            uri = str(sub)
            col = Collection(uri_to_id(uri), uri=uri)
            col.members = self._create_from_subject_predicate(sub, SKOS.member)
            col.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            col.notes = self._create_from_subject_typelist(sub, Note.valid_types)
            clist.append(col)

        return clist

    def _create_from_subject_typelist(self, subject, typelist):
        list=[]
        note_uris = []
        for p in typelist:
            term = SKOS.term(p)
            list.extend(self._create_from_subject_predicate(subject, term, note_uris))
        return list

    def _create_from_subject_predicate(self, subject, predicate, note_uris=None):
        list = []
        for s, p, o in self.graph.triples((subject, predicate, None)):
            type = predicate.split('#')[-1]
            if Label.is_valid_type(type):
                o = self._create_label(o, type)
            elif Note.is_valid_type(type):
                if o.toPython() not in note_uris:
                    note_uris.append(o.toPython())
                    o = self._create_note(o, type)
                else:
                    o = None
            else:
                o = uri_to_id(o)
            if o:
                list.append(o)
        return list

    def _create_label(self, literal, type):
        language = literal.language
        if language is None:
            return None
        return Label(literal.toPython(), type, language)

    def _create_note(self, uri, type):
        note = u''
        language = 'en'

        # http://vocab.getty.edu/aat/scopeNote
        for s, p, o in self.graph.triples((uri, RDF.value, None)):
            note += o.toPython()
            language = o.language

        # for http://vocab.getty.edu/aat/rev/
        for s, p, o in self.graph.triples((uri, DC.type, None)):
            note += o.toPython()
        for s, p, o in self.graph.triples((uri, DC.description, None)):
            note += ': %s' % o.toPython()
        for s, p, o in self.graph.triples((uri, PROV.startedAtTime, None)):
            note += ' at %s ' % o.toPython()

        return Note(note, type, language)

def uri_to_id(uri):
    return uri.strip('/').rsplit('/',1)[1]

def uri_to_base_uri(uri):
    return uri.strip('/').rsplit('/',1)[0]