#!/usr/bin/python
# -*- coding: utf-8 -*-
import rdflib
from rdflib.namespace import SKOS
import requests
import warnings
import logging
from skosprovider.providers import VocabularyProvider
from skosprovider_heritagedata.utils import (
    uri_to_id,
    heritagedata_to_skos)

log = logging.getLogger(__name__)

class HeritagedataProvider(VocabularyProvider):
    """A provider that can work with the Heritagedata services of
    http://www.heritagedata.org/blog/services/

    """

    def __init__(self, metadata, **kwargs):
        """ Constructor of the :class:`skosprovider_heritagedata.providers.HeritagedataProvider`

        :param (dict) metadata: metadata of the provider
        :param kwargs: arguments defining the provider.
            * Typical arguments are  `base_url`, `vocab_id` and `url`.
                The `url` is a composition of the `base_url` and `vocab_id`
            * The :class:`skosprovider_Heritagedata.providers.AATProvider`
                is the default :class:`skosprovider_Heritagedata.providers.HeritagedataProvider`
        """
        if not 'default_language' in metadata:
            metadata['default_language'] = 'en'
        if 'base_url' in kwargs:
            self.base_url = kwargs['base_url']
        else:
            self.base_url = 'http://purl.org/heritagedata/'# http://heritagedata.org/live/schemes/560/concepts/445424845454.json
        if 'vocab_id' in kwargs:
            self.vocab_id = kwargs['vocab_id']
        else:
            self.vocab_id = 'eh_period'
        if not 'url' in kwargs:
            self.url = self.base_url + "schemes/" + self.vocab_id
        else:
            self.url = kwargs['url']
        self.service_url = "http://heritagedata.org/live/services"

        super(HeritagedataProvider, self).__init__(metadata, **kwargs)

    def _get_language(self, **kwargs):
        return self.metadata['default_language']

    def get_by_id(self, id, change_notes=False):
        """ Get a :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Collection` by id

        :param (str) id: integer id of the :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`
        :return: corresponding :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`.
            Returns None if non-existing id
        """
        graph = rdflib.Graph()
        try:
            graph.parse('%s/%s/%s.rdf' % (self.url, "concepts", id))
            # get the concept
            graph_to_skos = heritagedata_to_skos(graph).from_graph()
            if len(graph_to_skos) == 0:
                return None
            concept = graph_to_skos[0]
            return concept

        # for python2.7 this is urllib2.HTTPError
        # for python3 this is urllib.error.HTTPError
        except Exception as err:
            if hasattr(err, 'code'):
                if err.code == 404:
                    return None
            else:
                raise

    def get_by_uri(self, uri, change_notes=False):
        """ Get a :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Collection` by uri

        :param (str) uri: string uri of the :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`
        :return: corresponding :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`.
            Returns None if non-existing id
        """
        id = uri_to_id(uri)
        return self.get_by_id(id, change_notes)


    def find(self, query):
        '''Find concepts that match a certain query.

        Currently query is expected to be a dict, so that complex queries can
        be passed. You can use this dict to search for concepts or collections
        with a certain label, with a certain type and for concepts that belong
        to a certain collection.

        .. code-block:: python

            # Find anything that has a label of church.
            provider.find({'label': 'church'}

            # Find all concepts that are a part of collection 5.
            provider.find({'type': 'concept', 'collection': {'id': 5})

            # Find all concepts, collections or children of these
            # that belong to collection 5.
            provider.find({'collection': {'id': 5, 'depth': 'all'})

        :param query: A dict that can be used to express a query. The following
            keys are permitted:

            * `label`: Search for something with this label value. An empty \
                label is equal to searching for all concepts.
            * `type`: Limit the search to certain SKOS elements. If not \
                present `all` is assumed:

                * `concept`: Only return :class:`skosprovider.skos.Concept` \
                    instances.
                * `collection`: Only return \
                    :class:`skosprovider.skos.Collection` instances.
                * `all`: Return both :class:`skosprovider.skos.Concept` and \
                    :class:`skosprovider.skos.Collection` instances.
            * `collection`: Search only for concepts belonging to a certain \
                collection. This argument should be a dict with two keys:

                * `id`: The id of a collection. Required.
                * `depth`: Can be `members` or `all`. Optional. If not \
                    present, `members` is assumed, meaning only concepts or \
                    collections that are a direct member of the collection \
                    should be considered. When set to `all`, this method \
                    should return concepts and collections that are a member \
                    of the collection or are a narrower concept of a member \
                    of the collection.

        :returns: A :class:`lst` of concepts and collections. Each of these
            is a dict with the following keys:

            * id: id within the conceptscheme
            * uri: :term:`uri` of the concept or collection
            * type: concept or collection
            * label: A label to represent the concept or collection. It is \
                determined by looking at the `**kwargs` parameter, the default \
                language of the provider and finally falls back to `en`.
        '''
        # #  interprete and validate query parameters (label, type and collection)
        # Label
        label = None
        if 'label' in query:
            label = query['label']
        # Type: 'collection','concept' or 'all'
        type_c = 'all'
        if 'type' in query:
            type_c = query['type']
        if type_c not in ('all', 'concept', 'collection'):
            raise ValueError("type: only the following values are allowed: 'all', 'concept', 'collection'")
        #Collection to search in (optional)
        coll_id = None
        coll_depth = None
        if 'collection' in query:
            coll = query['collection']
            if not 'id' in coll:
                raise ValueError("collection: 'id' is required key if a collection-dictionary is given")
            coll_id = coll['id']
            coll_depth = 'members'
            if 'depth' in coll:
                coll_depth = coll['depth']
            if coll_depth not in ('members', 'all'):
                raise ValueError(
                    "collection - 'depth': only the following values are allowed: 'members', 'all'")

        return False


    def get_all(self):
        """
        Not supported: This provider does not support this. The amount of results is too large
        """
        warnings.warn(
            'This provider does not support this. The amount of results is too large',
            UserWarning
        )
        return False

    def _get_answer(self, service, params):
        # send request to Heritagedata
        """ Returns the results of the Sparql query to a :class:`lst` of concepts and collections.
            The return :class:`lst`  can be empty.

        :param query (str): Sparql query
        :returns: A :class:`lst` of concepts and collections. Each of these
            is a dict with the following keys:
            * id: id within the conceptscheme
            * uri: :term:`uri` of the concept or collection
            * type: concept or collection
            * label: A label to represent the concept or collection.
        """

        try:
            request = self.service_url + "/" + service
            res = requests.get(request, params=params)
            res.encoding = 'utf-8'
            result = res.json()
            answer = []
            for r in result:
                if 'property' not in r.keys() or r['property'] == str(SKOS.narrower):
                    item = {
                    'id': uri_to_id(r["uri"]),
                    'uri': r["uri"],
                    'type': 'concept',
                    'label': r["label"]
                    }
                    answer.append(item)
            return answer
        except:
            return False

    def get_top_concepts(self):
        """  Returns all concepts that form the top-level of a display hierarchy.

        :return: A :class:`lst` of concepts.
        """
        #Collections are not used in Heritagedata so get_top_concepts() equals get_top_display()
        return self.get_top_display()

    def get_top_display(self):
        """  Returns all concepts or collections that form the top-level of a display hierarchy.
        :return: A :class:`lst` of concepts and collections.
        """
        params = {'schemeURI': self.url}
        return self._get_answer("getTopConceptsForScheme", params)

    def get_children_display(self, id):
        """ Return a list of concepts or collections that should be displayed under this concept or collection.

        :param str id: A concept or collection id.
        :returns: A :class:`lst` of concepts and collections.
        """
        params = {'conceptURI': self.url + "/concepts/" + id}
        return self._get_answer("getConceptRelations", params)

    def expand(self, id):
        """ Expand a concept or collection to all it's narrower concepts.
            If the id passed belongs to a :class:`skosprovider.skos.Concept`,
            the id of the concept itself should be include in the return value.

        :param str id: A concept or collection id.
        :returns: A :class:`lst` of id's. Returns false if the input id does not exists
        """

        return False

class EHPeriodProvider(HeritagedataProvider):
    """
    """

    def __init__(self, metadata):
        """
        """
        HeritagedataProvider.__init__(self, metadata, base_url='http://heritagedata.org/live/schemes/', vocab_id='eh_period')

