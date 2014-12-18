.. _general:

Introduction
============

This library offers an implementation of the 
:class:`skosprovider.providers.VocabularyProvider` interface based on the 
`Heritagedata Vocabularies <http://www.heritagedata.org>`_. These vocabularies
are used by :term:`EH`, :term:`RCAHMS` and :term:`RCAHMW` in their role as
curators of heritage.

Installation
------------

To be able to use this library you need to have a modern version of Python 
installed. Currently we're supporting versions 2.7, 3.3 and 3.4 of Python.

This easiest way to install this library is through :command:`pip` or 
:command:`easy install`:

.. code-block:: bash    
    
    $ pip install skosprovider_heritagedata

This will download and install :mod:`skosprovider_heritagedata` and a few libraries it 
depends on. 

.. _supported_thesauri:

Supported Heritagedata thesauri
-------------------------------

The webservices provides by `heritagedata.org <http://www.heritagedata.org>`_ 
provide access to multiple vocabularies or conceptschemes. You can select
one of these vocabularies by passing a `scheme_uri` to the constructor of
the :class:`~skosprovider_heritagedata.providers.HeritagedataProvider`.

`Heritagedata Vocabulary schemes <http://heritagedata.org/live/getAllSchemes.php>`_

An overview of all `scheme_uri` can be provided by the following service:

www.heritagedata.org/live/services/getSchemes?pretty

.. code-block:: javascript

    [
        {
            "uri": "http://purl.org/heritagedata/schemes/agl_et",
            "label": "EVENT TYPE (EH)",
            "label lang": "en",
            "description": "Terminology used for recording archaeological and architectural investigative, data collection exercises; from intrusive interventions to non damaging surveys",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/1",
            "label": "Monument Type Thesaurus (Scotland)",
            "label lang": "en",
            "description": "Monument types relating to the archaeological and built heritage of Scotland.",
            "attribution": "RCAHMS"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/2",
            "label": "Archaeological Objects Thesaurus (Scotland)",
            "label lang": "en",
            "description": "Objects made by human activity.",
            "attribution": "RCAHMS"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/3",
            "label": "Maritime Craft Thesaurus (Scotland)",
            "label lang": "en",
            "description": "Types of craft that survive as wrecks, or are documented as losses, in Scottish maritime waters.",
            "attribution": "RCAHMS"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/11",
            "label": "PERIOD (WALES)",
            "label lang": "en",
            "description": "A list of periods for use in Wales.",
            "attribution": "RCAHMW"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/eh_tmt2",
            "label": "MONUMENT TYPE (EH)",
            "label lang": "en",
            "description": "Classification of monument type records by function.",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/560",
            "label": "ARCHAEOLOGICAL SCIENCES (EH)",
            "label lang": "en",
            "description": "Used for recording the techniques, recovery methods and materials associated with archaeological sciences.",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/eh_tbm",
            "label": "BUILDING MATERIALS (EH)",
            "label lang": "en",
            "description": "Thesaurus of main constructional material types (eg. the walls) for indexing of monuments.",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/eh_tmc",
            "label": "MARITIME CRAFT TYPE (EH)",
            "label lang": "en",
            "description": "A thesaurus of craft types which survive as wrecks in English Heritage's maritime record",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/eh_period",
            "label": "PERIOD (EH)",
            "label lang": "en",
            "description": "English Heritage Periods List",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/eh_com",
            "label": "COMPONENTS (EH)",
            "label lang": "en",
            "description": "Terminology covering divisions and structural elements of a building or monument",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/eh_evd",
            "label": "EVIDENCE (EH)",
            "label lang": "en",
            "description": "Terminology covering the existing physical remains of a monument, or the means by which a monument has been identified where no physical remains exist",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/mda_obj",
            "label": "FISH Archaeological Objects Thesaurus",
            "label lang": "en",
            "description": "Originally developed by the Archaeological Objects Working Party and published by the mda. It provides guidance for the recording of archaeological objects in Britain and Ireland covering all historical periods. Now maintained by FISH on behalf of the heritage sector",
            "attribution": "English Heritage"
        },
        {
            "uri": "http://purl.org/heritagedata/schemes/10",
            "label": "MONUMENT TYPE THESAURUS (WALES)",
            "label lang": "en",
            "description": "Classification of monument types in Wales by function",
            "attribution": "RCAHMW"
        }
    ]

Using the providers
===================

Using HeritagedataProvider
--------------------------

The :class:`~skosprovider_heritagedata.providers.HeritagedataProvider` is a 
general provider for the Heritagedata vocabularies. It's use is identical to 
all other SKOSProviders. A scheme_uri is required to indicate the vocabulary
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
