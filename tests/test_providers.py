#!/usr/bin/python
# -*- coding: utf-8 -*-

from skosprovider_heritagedata.providers import (
    HeritagedataProvider
)
import unittest

class HeritagedataProviderTests(unittest.TestCase):

    def test_get_by_id_concept(self):
        concept = HeritagedataProvider({'id': 'period'}).get_by_id('PM')
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['type'], 'concept')
        self.assertIsInstance(concept['labels'], list)

        preflabels = [{'en': 'POST MEDIEVAL'}]
        preflabels_conc = [{label['language']: label['label']} for label in concept['labels']
                           if label['type'] == 'prefLabel']
        self.assertGreater(len(preflabels_conc), 0)
        for label in preflabels:
            self.assertIn(label, preflabels_conc)

        self.assertGreater(len(concept['notes']), 0)

        self.assertEqual(concept['id'], 'PM')
        self.assertEqual(len(concept['broader']), 0)
        self.assertEqual(len(concept['related']), 0)
        self.assertIn('STU', concept['narrower'])

    def test_get_by_id_nonexistant_id(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}).get_by_id('123')
        self.assertIsNone(concept)

    def test_get_by_uri(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}).get_by_uri('http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['id'], 'PM')

    def test_get_all(self):
        self.assertFalse(HeritagedataProvider({'id': 'Heritagedata'}).get_all())

    def test_get_top_display(self):
        top_heritagedata_display = HeritagedataProvider({'id': 'Heritagedata'}).get_top_display()
        self.assertIsInstance(top_heritagedata_display, list)
        self.assertGreater(len(top_heritagedata_display), 0)
        keys_first_display = top_heritagedata_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn('POST MEDIEVAL', [label['label'] for label in top_heritagedata_display])

    def test_get_top_concepts(self):
        top_heritagedata_concepts = HeritagedataProvider({'id': 'Heritagedata'}).get_top_concepts()
        self.assertIsInstance(top_heritagedata_concepts, list)
        self.assertGreater(len(top_heritagedata_concepts), 0)

    def test_get_childeren_display(self):
        childeren_Heritagedata_pm = HeritagedataProvider({'id': 'Heritagedata'}).get_children_display('PM')
        self.assertIsInstance(childeren_Heritagedata_pm, list)
        self.assertGreater(len(childeren_Heritagedata_pm), 0)
        keys_first_display = childeren_Heritagedata_pm[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("VICTORIAN", [label['label'] for label in childeren_Heritagedata_pm])

    def test_expand(self):
        all_childeren_churches = HeritagedataProvider({'id': 'Heritagedata'}).expand('300007466')
        self.assertIsInstance(all_childeren_churches, list)
        self.assertGreater(len(all_childeren_churches), 0)
        self.assertIn('300007466', all_childeren_churches)

    def test_expand_invalid(self):
        all_childeren_invalid = HeritagedataProvider({'id': 'Heritagedata'}).expand('invalid')
        self.assertFalse(all_childeren_invalid)

    def test_find_without_label(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}).find({'type': 'concept', 'collection': {'id': '300007466', 'depth': 'all'}})
        self.assertIsInstance(r, list)

    def test_find_wrong_type(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}).find, {'type': 'collectie', 'collection': {'id': '300007466', 'depth': 'all'}})

    def test_find_no_collection_id(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}).find, {'type': 'collection', 'collection': {'depth': 'all'}})

    def test_find_wrong_collection_depth(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}).find, {'type': 'concept', 'collection': {'id': '300007466', 'depth': 'allemaal'}})

    def test_find_concepts_in_collection(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}).find({'label': 'church', 'type': 'concept', 'collection': {'id': '300007466', 'depth': 'all'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'Concept')

    def test_find_multiple_keywords(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}).find({'label': 'church abbey', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'Concept')

    def test_find_member_concepts_in_collection(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}).find({'label': 'church', 'type': 'concept', 'collection': {'id': '300007494', 'depth': 'members'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'Concept')

    def test_find_collections_in_collection(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}).find({'label': 'church', 'type': 'collection', 'collection': {'id': '300007466', 'depth': 'all'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'Collection')

    def test_find_concepts(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}).find({'label': 'church', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'Concept')

    def test_find_concepts_kerk(self):
        r1 = HeritagedataProvider({'id': 'Heritagedata'}).find({'label': 'kerk', 'type': 'concept'})
        r2 = HeritagedataProvider({'id': 'Heritagedata', 'default_language': 'en'}).find({'label': 'kirche', 'type': 'concept'})
        r3 = HeritagedataProvider({'id': 'Heritagedata', 'default_language': 'nl'}).find({'label': 'kerk', 'type': 'concept'})

        self.assertIsInstance(r1, list)
        self.assertIsInstance(r2, list)
        self.assertIsInstance(r3, list)
        self.assertGreater(len(r1), 0)
        self.assertGreater(len(r2), 0)
        self.assertGreater(len(r3), 0)
        for res in r1:
            self.assertIn('church', res['label'].lower())
            self.assertEqual(res['type'], 'Concept')
        for res in r2:
            self.assertIn('church', res['label'].lower())
            self.assertEqual(res['type'], 'Concept')
        for res in r3:
            self.assertIn('kerk', res['label'].lower())
            self.assertEqual(res['type'], 'Concept')



    def test_find_member_collections_in_collection(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}).find({'label': 'church', 'type': 'collection', 'collection': {'id': '300007466', 'depth': 'members'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'Collection')

    def test_answer_wrong_query(self):
        self.assertFalse(HeritagedataProvider({'id': 'test'}, vocab_id='Heritagedata', url='http://vocab.Heritagedata.edu/Heritagedata')._get_answer("Wrong SPARQL query"))


