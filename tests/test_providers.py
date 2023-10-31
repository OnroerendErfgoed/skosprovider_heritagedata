#!/usr/bin/python

import unittest

from skosprovider.exceptions import ProviderUnavailableException

from skosprovider_heritagedata.providers import HeritagedataProvider


class HeritagedataProviderTests(unittest.TestCase):

    def _get_provider(self):
        return HeritagedataProvider(
            {'id': 'Heritagedata'},
            service_scheme_uri='http://heritagedata.org/live/services/'
        )

    def test_set_custom_session(self):
        import requests
        sess = requests.Session()
        provider = HeritagedataProvider(
            {'id': 'Heritagedata'},
            service_scheme_uri='http://heritagedata.org/live/services/',
            session=sess
        )
        self.assertEqual(sess, provider.session)

    def test_get_default_vocabulary_uri(self):
        provider = self._get_provider()
        assert 'http://purl.org/heritagedata/schemes/eh_period' == provider.get_vocabulary_uri()

    def test_get_custom_vocabulary_uri(self):
        provider = HeritagedataProvider(
            {'id': 'ScAPA'},
            service_scheme_uri='http://heritagedata.org/live/services/',
            scheme_uri= 'http://purl.org/heritagedata/schemes/scapa'
        )
        assert 'http://purl.org/heritagedata/schemes/scapa' == provider.get_vocabulary_uri()

    def test_get_vocabulary_uri_does_not_load_cs(self):
        provider = HeritagedataProvider(
            {'id': 'ScAPA'},
            service_scheme_uri='http://heritagedata.org/live/services/',
            scheme_uri= 'http://purl.org/heritagedata/schemes/scapa'
        )
        assert provider._conceptscheme is None
        assert 'http://purl.org/heritagedata/schemes/scapa' == provider.get_vocabulary_uri()
        assert provider._conceptscheme is None

    def test_default_provider(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'},service_scheme_uri='http://heritagedata.org/live/services/')
        self.assertEqual(provider.base_scheme_uri, 'http://purl.org/heritagedata/schemes')
        self.assertEqual(provider.scheme_id, 'eh_period')
        self.assertEqual(provider.service_scheme_uri, 'http://heritagedata.org/live/services')

    def test_scheme_uri_not_available(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'}, service_scheme_uri='http://heritagedata.org/live/services_not_available/')
        self.assertEqual(provider.base_scheme_uri, 'http://purl.org/heritagedata/schemes')
        self.assertEqual(provider.scheme_id, 'eh_period')
        self.assertEqual(provider.service_scheme_uri, 'http://heritagedata.org/live/services_not_available')
        self.assertRaises(ProviderUnavailableException, provider.find, {'label': 'LOCH', 'type': 'concept'})

    def test_get_top_concepts_provider(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period')
        self.assertEqual(len(provider.get_top_concepts()), 8)

    def test_default_language_scottish_gaelic(self):
        provider_gd = HeritagedataProvider({'id': 'Heritagedata', 'default_language': 'gd'}, scheme_uri='http://purl.org/heritagedata/schemes/1')
        concept = provider_gd.get_by_id('500614')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/1/concepts/500614')

        result = provider_gd.find({'label': 'LOCH', 'type': 'concept'})
        for r in result:
            self.assertIn("LOCH", r['label'])
            self.assertTrue(r['lang'] in ('en', 'gd'))

        provider_en = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/1')
        concept = provider_en.get_by_id('500614')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/1/concepts/500614')

        result = provider_en.find({'label': 'LOCH', 'type': 'concept'})
        for r in result:
            self.assertIn("LOCH", r['label'])
            self.assertTrue(r['lang'] in ('en', 'gd'))


    def test_get_by_id_concept(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').get_by_id('PM')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['type'], 'concept')
        self.assertIsInstance(concept['labels'], list)

        preflabels = [{'en': 'POST MEDIEVAL'}]
        preflabels_conc = [{label.language: label.label} for label in concept['labels']
                           if label.type == 'prefLabel']
        self.assertGreater(len(preflabels_conc), 0)
        for label in preflabels:
            self.assertIn(label, preflabels_conc)

        self.assertGreater(len(concept['notes']), 0)
        self.assertIsNotNone(concept['notes'][0])
        self.assertEqual(concept['notes'][0].language, 'en')
        self.assertEqual(concept['notes'][0].note, 'Begins with the dissolution of the monasteries and'
                                                   ' ends with the death of Queen Victoria. '
                                                   'Use more specific period where known.')
        self.assertEqual(concept['notes'][0].type, 'scopeNote')

        self.assertEqual(concept['id'], 'PM')
        self.assertEqual(len(concept['broader']), 0)
        self.assertEqual(len(concept['related']), 0)
        self.assertIn('STU', concept['narrower'])

    def test_get_by_id_nonexistant_id(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').get_by_id('123')
        self.assertFalse(concept)

    def test_get_by_uri(self):
        concept = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').get_by_uri('http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'http://purl.org/heritagedata/schemes/eh_period/concepts/PM')
        self.assertEqual(concept['id'], 'PM')

    def test_get_all(self):
        kwargs = {'language': 'nl'}
        self.assertFalse(HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').get_all(**kwargs))

    def test_get_top_display(self):
        kwargs = {'language': 'nl'}
        top_heritagedata_display = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').get_top_display(**kwargs)
        self.assertIsInstance(top_heritagedata_display, list)
        self.assertGreater(len(top_heritagedata_display), 0)
        keys_first_display = top_heritagedata_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn('POST MEDIEVAL', [label['label'] for label in top_heritagedata_display])

    def test_get_top_display_sort_sort(self):
        prov = HeritagedataProvider(
            {'id': 'Heritagedata'},
            scheme_uri='http://purl.org/heritagedata/schemes/eh_period'
        )
        sorted_by_id = prov.get_top_display(sort='id')
        sorted_by_uri = prov.get_top_display(sort='uri', sort_order='desc')
        assert len(sorted_by_id) > 1
        assert len(sorted_by_id) == len(sorted_by_uri)
        assert [c['id'] for c in sorted_by_id] != [c['id'] for c in sorted_by_uri]

    def test_get_top_concepts(self):
        kwargs = {'language': 'nl'}
        top_heritagedata_concepts = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').get_top_concepts(**kwargs)
        self.assertIsInstance(top_heritagedata_concepts, list)
        self.assertGreater(len(top_heritagedata_concepts), 0)

    def test_get_top_concepts_sort(self):
        prov = HeritagedataProvider(
            {'id': 'Heritagedata'},
            scheme_uri='http://purl.org/heritagedata/schemes/eh_period'
        )
        not_sorted = prov.get_top_concepts()
        sorted_by_id = prov.get_top_concepts(sort='id')
        assert [c['id'] for c in not_sorted] == [c['id'] for c in sorted_by_id]
        sorted_by_uri = prov.get_top_concepts(sort='uri')
        assert len(sorted_by_id) == 8
        assert len(sorted_by_id) == len(sorted_by_uri)
        assert [c['id'] for c in sorted_by_id] == [c['id'] for c in sorted_by_uri]
        sorted_by_label = prov.get_top_concepts(sort='label')
        assert len(sorted_by_id) == len(sorted_by_label)
        assert [c['id'] for c in sorted_by_id] == [c['id'] for c in sorted_by_label]

    def test_get_childeren_display(self):
        kwargs = {'language': 'nl'}
        childeren_Heritagedata_pm = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').get_children_display('PM', **kwargs)
        self.assertIsInstance(childeren_Heritagedata_pm, list)
        self.assertGreater(len(childeren_Heritagedata_pm), 0)
        keys_first_display = childeren_Heritagedata_pm[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("TUDOR", [label['label'] for label in childeren_Heritagedata_pm])

    def test_get_children_display_sort(self):
        prov = HeritagedataProvider(
            {'id': 'Heritagedata'},
            scheme_uri='http://purl.org/heritagedata/schemes/eh_period'
        )
        not_sorted = prov.get_children_display('PM')
        sorted_by_id = prov.get_children_display('PM', sort='id')
        assert [c['id'] for c in not_sorted] == [c['id'] for c in sorted_by_id]
        assert len(sorted_by_id) == len(not_sorted)
        sorted_by_label = prov.get_children_display('PM', sort='label')
        assert len(sorted_by_id) == len(sorted_by_label)
        assert [c['id'] for c in sorted_by_id] == [c['id'] for c in sorted_by_label]
        sorted_by_label_desc = prov.get_children_display('PM', sort='label', sort_order='desc')
        assert [c['id'] for c in sorted_by_label] != [c['id'] for c in sorted_by_label_desc]

    def test_expand(self):
        all_childeren_pm = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').expand('PM')
        self.assertIsInstance(all_childeren_pm, list)
        self.assertGreater(len(all_childeren_pm), 0)
        self.assertIn('PM', all_childeren_pm)

        # all_childeren_monumentsbyform = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_tmt2').expand('102872')
        # self.assertIsInstance(all_childeren_monumentsbyform, list)
        # self.assertGreater(len(all_childeren_monumentsbyform), 0)
        # self.assertIn('102872', all_childeren_monumentsbyform)



    def test_expand_invalid(self):
        all_childeren_invalid = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').expand('invalid')
        self.assertFalse(all_childeren_invalid)

    def test_find_with_collection(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').find, {'type': 'concept', 'collection': {'id': '300007466', 'depth': 'all'}})

    def test_find_collections(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').find({'type': 'collection'})
        self.assertEqual(r, [])

    def test_find_wrong_type(self):
        self.assertRaises(ValueError, HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').find, {'type': 'collectie'})

    def test_find_multiple_keywords(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').find({'label': 'iron Age', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_find_one_keyword(self):
        r = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').find({'label': 'VICTORIAN', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_find_one_keyword_language(self):
        kwargs = {'language': 'nl'}
        r = HeritagedataProvider({'id': 'Heritagedata'}, scheme_uri='http://purl.org/heritagedata/schemes/eh_period').find({'label': 'VICTORIAN', 'type': 'concept'}, **kwargs)
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_find_kwargs_language(self):
        kwargs = {'language': 'gd'}
        provider_gd = HeritagedataProvider({'id': 'Heritagedata', 'default_language': 'en'}, scheme_uri='http://purl.org/heritagedata/schemes/1')
        result = provider_gd.find({'label': 'LOCH', 'type': 'concept'}, **kwargs)
        for r in result:
            self.assertIn("LOCH", r['label'])
            self.assertTrue(r['lang'] in ('en', 'gd'))

    def test_find_sort(self):
        prov = HeritagedataProvider(
            {'id': 'Heritagedata'},
            scheme_uri='http://purl.org/heritagedata/schemes/eh_period'
        )
        sorted_by_id = prov.find({'label': 'century', 'sort': 'id'})
        sorted_by_uri = prov.find({'label': 'century', 'sort': 'uri'})
        assert len(sorted_by_id) > 1
        assert len(sorted_by_id) == len(sorted_by_uri)
        assert [c for c in sorted_by_id] == [c for c in sorted_by_uri]
        sorted_by_label = prov.find({'label': 'century', 'sort': 'label'})
        assert len(sorted_by_id) == len(sorted_by_label)
        assert [c for c in sorted_by_id] == [c for c in sorted_by_label]
        sorted_by_sortlabel = prov.find({'label': 'century', 'sort': 'sortlabel'})
        assert sorted_by_sortlabel == sorted_by_label

    def test_get_items(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'},service_scheme_uri='http://heritagedata.org/live/services/')
        res = provider._get_items("getConceptLabelMatch", {'contains': 'VICTORIAN', 'schemeURI': 'http://purl.org/heritagedata/schemes/eh_period'})
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['label'], 'VICTORIAN')
        self.assertEqual(res[0]['id'], 'VIC')
        self.assertEqual(res[0]['lang'], 'en')
        self.assertEqual(res[0]['type'], 'concept')
        self.assertEqual(res[0]['uri'], 'http://purl.org/heritagedata/schemes/eh_period/concepts/VIC')

    def test_get_items_non_exist_service(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'},service_scheme_uri='http://heritagedata.org/live/services2/')
        self.assertRaises(ProviderUnavailableException, provider._get_items, "getConceptLabelMatch",{'contains': 'VICTORIAN', 'schemeURI': 'http://purl.org/heritagedata/schemes/eh_period'})

    def test_get_items_non_exist_service2(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'},service_scheme_uri='http://heritagedata.org/live/services/')
        self.assertRaises(ProviderUnavailableException, provider._get_items, "invalid", {})

    def test_get_items_wrong_params(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'},service_scheme_uri='http://heritagedata.org/live/services/')
        self.assertRaises(ValueError, provider._get_items, "getConceptLabelMatch", {"fhgfhg"})

    def test_get_items_non_exist_provider(self):
        provider = HeritagedataProvider({'id': 'Heritagedata'},service_scheme_uri='http://not_existent.org/live/services/')
        self.assertRaises(ProviderUnavailableException, provider._get_items,"getConceptLabelMatch",{'contains': 'VICTORIAN', 'schemeURI': 'http://purl.org/heritagedata/schemes/eh_period'})
