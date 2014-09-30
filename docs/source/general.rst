.. _general:

Introduction
============

This library offers an implementation of the 
:class:`skosprovider.providers.VocabularyProvider` interface based on the 
`Heritagedata Vocabularies <http://www.heritagedata.org>`_. These vocabularies
are used by :term:`EH`, :term:`RCAHMS` and :term:`RCAHMW` in their role as
curators of heritage.


.. _supported_thesauri:

Supported Heritagedata thesauri
-------------------------------

The webservices provides by `heritagedata.org <http://www.heritagedata.org>`_ 
provide access to multiple vocabularies or conceptschemes. You can select
one of these vocabularies by passing a `scheme_id` to the constructor of
the :class:`~skosprovider_heritagedata.providers.HeritagedataProvider`.

`Heritagedata Vocabulary schemes <http://heritagedata.org/live/getAllSchemes.php>`_


Using the providers
===================

Using HeritagedataProvider
--------------------------

The :class:`~skosprovider_heritagedata.providers.HeritagedataProvider` is a 
general provider for the Heritagedata vocabularies. It's use is identical to 
all other SKOSProviders. A scheme_id is required to indicate the vocabulary
to be used. Please consult :ref:`supported_thesauri` for a complete list.

.. literalinclude:: ../../examples/period.py
   :language: python


Finding concepts
----------------

See the :meth:`skosprovider_heritagedata.providers.HeritagedataProvider.find` 
method for a detailed description of how this works.

.. literalinclude:: ../../examples/find.py
   :language: python

Using expand()
--------------

The expand methods return the id's of all the concepts that are narrower 
concepts of a certain concept or collection.

See the :meth:`skosprovider_heritagedata.providers.HeritagedataProvider.expand` method for
a detailed description of how this works.

.. literalinclude:: ../../examples/expand.py
   :language: python
