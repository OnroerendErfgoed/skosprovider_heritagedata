import pytest

from rdflib import Graph
from skosprovider.exceptions import ProviderUnavailableException

from skosprovider_heritagedata.utils import text_
from skosprovider_heritagedata.utils import uri_to_graph
from skosprovider_heritagedata.utils import CONCEPTSCHEMES

class UtilsTests():

    def test_text(self):
        res = text_(b'test123')
        assert 'test123' == res

    def test_text_unicode(self):
        res = text_('test123')
        assert 'test123' == res

    def test_text_utf8(self):
        res = text_(b'LaPe\xc3\xb1a', 'utf-8')
        assert 'LaPe\xf1a' == res

    def test_uri_to_graph(self):
        res = uri_to_graph('http://purl.org/heritagedata/schemes/eh_period.rdf')
        assert isinstance(res, Graph)
        assert len(res)

    def test_uri_to_graph_uri_not_available(self):
        with pytest.raises(ProviderUnavailableException):
            g = uri_to_graph("http://does_not_exist.be/1.rdf")

    def test_uri_to_graph_no_resource(self):
        res = uri_to_graph('http://purl.org/heritagedata/schemes/no_resource.rdf')
        assert not res

class ConceptSchemeTests():

    def test_conceptschemes_key_is_uri():
        for uri, cs in CONCEPTSCHEMES.items():
            assert uri == cs.uri

    def test_conceptschemes_have_labels():
        for cs in CONCEPTSCHEMES:
            assert len(cs.label)

    def test_conceptschemes_have_notes():
        for cs in CONCEPTSCHEMES:
            assert len(cs.notes)

    def test_conceptschemes_have_sources():
        for cs in CONCEPTSCHEMES:
            assert len(cs.sources)
