'''
Utility functions for :mod:`skosprovider_heritagedata`.
'''

import logging

import rdflib
import requests
from rdflib.namespace import DCTERMS
from rdflib.namespace import RDF
from rdflib.namespace import RDFS
from rdflib.namespace import SKOS
from rdflib.term import URIRef
from skosprovider.exceptions import ProviderUnavailableException
from skosprovider.skos import Concept
from skosprovider.skos import ConceptScheme
from skosprovider.skos import Label
from skosprovider.skos import Note

log = logging.getLogger(__name__)
PROV = rdflib.Namespace('http://www.w3.org/ns/prov#')

def conceptscheme_from_uri(conceptscheme_uri, **kwargs):
    '''
    Read a SKOS Conceptscheme from a :term:`URI`

    :param string conceptscheme_uri: URI of the conceptscheme.
    :rtype: skosprovider.skos.ConceptScheme
    '''
    s = kwargs.get('session', requests.Session())
    graph = uri_to_graph('%s.rdf' % (conceptscheme_uri), session=s)

    notes = []
    labels = []

    if graph is not False:
        for s, p, o in graph.triples((URIRef(conceptscheme_uri), RDFS.label, None)):
            label = Label(o.toPython(), "prefLabel", 'en')
            labels.append(label)
        for s, p, o in graph.triples((URIRef(conceptscheme_uri), DCTERMS.description, None)):
            note = Note(o.toPython(), "scopeNote", 'en')
            notes.append(note)

    # get the conceptscheme
    conceptscheme = ConceptScheme(
        conceptscheme_uri,
        labels=labels,
        notes=notes
    )
    return conceptscheme


def things_from_graph(graph, concept_scheme):
    '''
    Read concepts and collections from a graph.

    :param rdflib.Graph graph: Graph to read from.
    :param skosprovider.skos.ConceptScheme concept_scheme: Conceptscheme the
        concepts and collections belong to.
    :rtype: :class:`list`
    '''
    clist = []
    for sub, pred, obj in graph.triples((None, RDF.type, SKOS.Concept)):
        uri = str(sub)
        con = Concept(
            id=_split_uri(uri, 1),
            uri=uri,
            concept_scheme = concept_scheme,
            labels = _create_from_subject_typelist(graph, sub, Label.valid_types),
            notes = _create_from_subject_typelist(graph, sub, Note.valid_types),
            broader = _create_from_subject_predicate(graph, sub, SKOS.broader),
            narrower = _create_from_subject_predicate(graph, sub, SKOS.narrower),
            related = _create_from_subject_predicate(graph, sub, SKOS.related),
            subordinate_arrays = []
        )
        clist.append(con)

        # at this moment, Heritagedata does not support SKOS.Collection
    # for sub, pred, obj in graph.triples((None, RDF.type, SKOS.Collection)):
    # uri = str(sub)
    #     col = Collection(_split_uri(uri, 1), uri=uri)
    #     col.members = _create_from_subject_predicate(sub, SKOS.member)
    #     col.labels = _create_from_subject_typelist(sub, Label.valid_types)
    #     col.notes = _create_from_subject_typelist(sub, Note.valid_types)
    #     clist.append(col)

    return clist


def _create_from_subject_typelist(graph, subject, typelist):
    list = []
    for p in typelist:
        term = SKOS.term(p)
        list.extend(_create_from_subject_predicate(graph, subject, term))
    return list


def _create_from_subject_predicate(graph, subject, predicate):
    list = []
    for s, p, o in graph.triples((subject, predicate, None)):
        type = predicate.split('#')[-1]
        if Label.is_valid_type(type):
            o = _create_label(o, type)
        elif Note.is_valid_type(type):
            o = _create_note(o, type)
        else:
            o = _split_uri(o, 1)
        if o:
            list.append(o)
    return list


def _create_label(literal, type):
    language = literal.language
    if language is None:
        return 'und'  # return undefined code when no language
    return Label(literal.toPython(), type, language)


def _create_note(literal, type):
    if not Note.is_valid_type(type):
        raise ValueError('Type of Note is not valid.')

    return Note(text_(literal.value, encoding="utf-8"), type, _get_language_from_literal(literal))


def _get_language_from_literal(data):
    if data.language is None:
        return 'und'  # return undefined code when no language
    return text_(data.language, encoding="utf-8")


def _split_uri(uri, index):
    return uri.strip('/').rsplit('/', 1)[index]


def uri_to_graph(uri, **kwargs):
    '''
    :param string uri: :term:`URI` where the RDF data can be found.
    :rtype: rdflib.Graph
    :raises skosprovider.exceptions.ProviderUnavailableException: if the 
        heritagedata.org services are down
    '''
    s = kwargs.get('session', requests.Session())
    graph = rdflib.Graph()
    try:
        res = s.get(uri)
    except requests.ConnectionError as e:
        raise ProviderUnavailableException("URI not available: %s" % uri)
    if res.status_code == 404:
        return False
    graph.parse(data=res.content)
    #heritagedata.org returns a empy page/graph when a resource does not exists (statsu_code 200). For this reason we return False if the graph is empty
    if len(graph) == 0:
        return False
    return graph


def text_(s, encoding='latin-1', errors='strict'):
    """ If ``s`` is an instance of ``bytes``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, bytes):
        return s.decode(encoding, errors)
    return s
