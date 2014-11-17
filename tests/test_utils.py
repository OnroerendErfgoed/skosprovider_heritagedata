# -*- coding: utf-8 -*-
import unittest

from skosprovider_heritagedata.utils import text_


class UtilsTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_text(self):
        res = text_(b'test123')
        self.assertEqual(u'test123', res)

    def test_text_unicode(self):
        res = text_(u'test123')
        self.assertEqual(u'test123', res)

    def test_text_utf8(self):
        res = text_(b'LaPe\xc3\xb1a', 'utf-8')
        self.assertEqual(u'LaPe\xf1a', res)