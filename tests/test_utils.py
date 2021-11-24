import unittest

from rdflib import Graph
from skosprovider.exceptions import ProviderUnavailableException

from skosprovider_heritagedata.utils import text_
from skosprovider_heritagedata.utils import uri_to_graph


class UtilsTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_text(self):
        res = text_(b'test123')
        self.assertEqual('test123', res)

    def test_text_unicode(self):
        res = text_('test123')
        self.assertEqual('test123', res)

    def test_text_utf8(self):
        res = text_(b'LaPe\xc3\xb1a', 'utf-8')
        self.assertEqual('LaPe\xf1a', res)

    def test_uri_to_graph(self):
        res = uri_to_graph('http://purl.org/heritagedata/schemes/eh_period.rdf')
        self.assertIsInstance(res, Graph)
        self.assertGreater(len(res), 0)

    def test_uri_to_graph_uri_not_available(self):
        self.assertRaises(ProviderUnavailableException, uri_to_graph, "http://does_not_exist.be/1.rdf")

    def test_uri_to_graph_no_resource(self):
        res = uri_to_graph('http://purl.org/heritagedata/schemes/no_resource.rdf')
        self.assertFalse(res)
