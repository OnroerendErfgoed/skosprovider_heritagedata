'''
This module implements a :class:`skosprovider.providers.VocabularyProvider`
for http://www.heritagedata.org.
'''

import logging
import warnings

import requests
from language_tags import tags
from rdflib.namespace import SKOS
from requests.exceptions import ConnectionError
from skosprovider.exceptions import ProviderUnavailableException
from skosprovider.providers import VocabularyProvider

from skosprovider_heritagedata.utils import _split_uri
from skosprovider_heritagedata.utils import conceptscheme_from_uri
from skosprovider_heritagedata.utils import things_from_graph
from skosprovider_heritagedata.utils import uri_to_graph

log = logging.getLogger(__name__)


class HeritagedataProvider(VocabularyProvider):
    """A provider that can work with the Heritagedata services of
    http://www.heritagedata.org/blog/services/

    """

    def __init__(self, metadata, **kwargs):
        """ Constructor of the :class:`skosprovider_heritagedata.providers.HeritagedataProvider`

        :param (dict) metadata: metadata of the provider
        :param kwargs: arguments defining the provider.
            * Typical argument is `scheme_uri`.
                The `scheme_uri` is a composition of the `base_scheme_uri` and `scheme_id`
            * session: a custom requests Sesssion
            * concept_scheme: the scheme all concepts belong to, avoids a call to the webservice
        """
        if not 'default_language' in metadata:
            metadata['default_language'] = 'en'
        if not 'subject' in metadata:
            metadata['subject'] = []
        self.metadata = metadata
        if 'scheme_uri' in kwargs:
            self.base_scheme_uri = _split_uri(kwargs['scheme_uri'], 0)
            self.scheme_id = _split_uri(kwargs['scheme_uri'], 1)
        else:
            self.base_scheme_uri = 'http://purl.org/heritagedata/schemes'
            self.scheme_id = 'eh_period'
        self.scheme_uri = self.base_scheme_uri + "/" + self.scheme_id
        if not 'uri' in self.metadata:
            self.metadata['uri'] = self.scheme_uri

        if 'service_scheme_uri' in kwargs:
            self.service_scheme_uri = kwargs['service_scheme_uri'].strip('/')
        else:
            self.service_scheme_uri = "http://heritagedata.org/live/services"
        self.session = kwargs.get('session', requests.Session())
        
        if 'concept_scheme' in kwargs:
            self._conceptscheme = kwargs.get('concept_scheme')
        else:
            self._conceptscheme = None

    @property
    def concept_scheme(self):
        if self._conceptscheme is None:
            self._conceptscheme = self._get_concept_scheme()
        return self._conceptscheme
    
    def _get_concept_scheme(self):
        return conceptscheme_from_uri(
            self.scheme_uri,
            session=self.session
        )

    def _get_language(self, **kwargs):
        if 'language' in kwargs:
            return kwargs['language']
        return self.metadata['default_language']

    def get_by_id(self, id):
        """ Get a :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Collection` by id

        :param (str) id: integer id of the :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`
        :return: corresponding :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`.
            Returns False if non-existing id
        """
        graph = uri_to_graph(
            '{}/{}/{}.rdf'.format(self.scheme_uri, "concepts", id),
            session=self.session
        )
        if graph is False:
            return False
        # get the concept
        things = things_from_graph(graph, self.concept_scheme)
        if len(things) == 0:
            return False
        c = things[0]
        return c

    def get_by_uri(self, uri):
        """ Get a :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Collection` by uri

        :param (str) uri: string uri of the :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`
        :return: corresponding :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`.
            Returns False if non-existing id
        """
        id = _split_uri(uri, 1)
        return self.get_by_id(id)

    def find(self, query, **kwargs):
        '''Find concepts that match a certain query.

        Currently query is expected to be a dict, so that complex queries can
        be passed. You can use this dict to search for concepts or collections
        with a certain label, with a certain type and for concepts that belong
        to a certain collection.

        .. warning::

            The underlying service returns labels without specifying if they are
            prefLabels or altLabels. For a certain concept several labels are
            returned. This method does not return labels, but returns concepts.
            When multiple labels are detected for a single concept, only one
            label is attached to this concept. Since no information is present
            about the type of this label, this can be an altLabel for a concept
            where a prefLabel exists.

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
        if type_c == 'collection':
            warnings.warn("This provider doesn't support collections at the moment of implementation because Heritagedata doesn't use SKOS:Collection.", UserWarning)
            return []
        if type_c not in ('all', 'concept', 'collection'):
            raise ValueError("type: only the following values are allowed: 'all', 'concept', 'collection'")
        #collection
        if 'collection' in query:
            warnings.warn("This provider doesn't support collections at the moment of implementation because Heritagedata doesn't use SKOS:Collection.", UserWarning)
            raise ValueError('You are searching for items in an unexisting collection.')
        params = {'schemeURI': self.scheme_uri, 'contains': label}
        ret = self._get_items("getConceptLabelMatch", params, **kwargs)
        language = self._get_language(**kwargs)
        sort = self._get_sort(**kwargs)
        sort_order = self._get_sort_order(**kwargs)
        return self._sort(ret, sort, language, sort_order == 'desc')

    def get_all(self, **kwargs):
        """
        Not supported: This provider does not support this. The amount of results is too large
        """
        warnings.warn(
            'This provider does not support this. The amount of results is too large',
            UserWarning
        )
        return False

    def get_top_concepts(self, **kwargs):
        """  Returns all concepts that form the top-level of a display hierarchy.

        :return: A :class:`lst` of concepts.
        """
        #Collections are not used in Heritagedata so get_top_concepts() equals get_top_display()
        return self.get_top_display(**kwargs)

    def get_top_display(self, **kwargs):
        """  Returns all concepts or collections that form the top-level of a display hierarchy.
        :return: A :class:`lst` of concepts and collections.
        """
        params = {'schemeURI': self.scheme_uri, 'alias': True}
        ret = self._get_items("getTopConceptsForScheme", params, **kwargs)
        language = self._get_language(**kwargs)
        sort = self._get_sort(**kwargs)
        sort_order = self._get_sort_order(**kwargs)
        return self._sort(ret, sort, language, sort_order == 'desc')

    def get_children_display(self, id, **kwargs):
        """ Return a list of concepts or collections that should be displayed under this concept or collection.

        :param str id: A concept or collection id.
        :returns: A :class:`lst` of concepts and collections.
        """
        params = {'conceptURI': self.scheme_uri + "/concepts/" + id, 'alias': True}
        ret = self._get_items("getConceptRelations", params, **kwargs)
        language = self._get_language(**kwargs)
        sort = self._get_sort(**kwargs)
        sort_order = self._get_sort_order(**kwargs)
        return self._sort(ret, sort, language, sort_order == 'desc')

    def expand(self, id):
        """ Expand a concept or collection to all it's narrower concepts.
            If the id passed belongs to a :class:`skosprovider.skos.Concept`,
            the id of the concept itself should be include in the return value.

        :param str id: A concept or collection id.
        :returns: A :class:`lst` of id's. Returns false if the input id does not exists
        """
        expanded = []
        expanded.append(id)
        expanded.extend(self._get_children(id, all=True))
        if len(expanded) == 1:
            if self.get_by_id(id) is False:
                return False
        return expanded

    def _get_children(self, id, all=False):
        #If all=True this method works recursive
        request = self.service_scheme_uri + "/getConceptRelations"
        res = self.session.get(request, params={'conceptURI': self.scheme_uri + "/concepts/" + id})
        res.encoding = 'utf-8'
        result = res.json()
        answer = []
        for r in result:
            if r['property'] == str(SKOS.narrower):
                child_id = _split_uri(r["uri"], 1)
                answer.append(child_id)
                if all is True:
                    child_list = self._get_children(child_id, all=True)
                    if child_list is not False:
                        answer.extend(child_list)
        return answer

    def _get_items(self, service, params, **kwargs):
        # send request to Heritagedata
        """ Returns the results of a service method to a :class:`lst` of concepts (and collections).
            The return :class:`lst`  can be empty.

        :param service (str): service method
        :returns: A :class:`lst` of concepts (and collections). Each of these
            is a dict with the following keys:
            * id: id within the conceptscheme
            * uri: :term:`uri` of the concept or collection
            * type: concept or collection
            * label: A label to represent the concept or collection.
        """

        request = self.service_scheme_uri + "/" + service
        try:
            res = self.session.get(request, params=params)
        except ConnectionError as e:
            raise ProviderUnavailableException(f"Request could not be executed - Request: {request} - Params: {params}")
        if res.status_code == 404:
            raise ProviderUnavailableException(f"Service not found (status_code 404) - Request: {request} - Params: {params}")
        res.encoding = 'utf-8'
        result = res.json()
        d = {}
        for r in result:
            uri = r['uri']
            label = None
            if 'label' in r.keys():
                label = r['label']
            language = None
            if 'label lang' in r.keys():
                language = r['label lang']
            property = None
            if 'property' in r.keys():
                property = r['property']
            if not service == 'getConceptRelations' or property == "skos:narrower":
                item = {
                    'id': _split_uri(uri, 1),
                    'uri': uri,
                    'type': 'concept',
                    'label': label,
                    'lang': language
                }
                if uri not in d:
                    d[uri] = item
                if tags.tag(d[uri]['lang']).format == tags.tag(self._get_language(**kwargs)).format:
                    pass
                elif tags.tag(item['lang']).format == tags.tag(self._get_language(**kwargs)).format:
                    d[uri] = item
                elif tags.tag(item['lang']).language and (tags.tag(item['lang']).language.format == tags.tag(self._get_language(**kwargs)).language.format):
                    d[uri] = item
                elif tags.tag(item['lang']).format == 'en':
                    d[uri] = item
        return list(d.values())

    def _sort(self, items, sort, language='en', reverse=False):
        if sort is None:
            sort = 'id'
        if sort == 'sortlabel':
            sort='label'
        items.sort(key=lambda item: item[sort], reverse=reverse)
        return items

