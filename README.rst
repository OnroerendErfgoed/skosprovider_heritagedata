skosprovider_heritagedata
=========================

.. image:: https://img.shields.io/pypi/v/skosprovider_heritagedata.svg
        :target: https://pypi.python.org/pypi/skosprovider_heritagedata
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.10086289.svg
        :target: https://doi.org/10.5281/zenodo.10086289
.. image:: https://app.travis-ci.com/OnroerendErfgoed/skosprovider_heritagedata.svg?branch=develop
        :target: https://app.travis-ci.com/OnroerendErfgoed/skosprovider_heritagedata
.. image:: https://coveralls.io/repos/github/OnroerendErfgoed/skosprovider_heritagedata/badge.svg?branch=develop
        :target: https://coveralls.io/github/OnroerendErfgoed/skosprovider_heritagedata?branch=develop

----

.. image:: https://readthedocs.org/projects/skosprovider_heritagedata/badge/?version=latest
        :target: http://skosprovider-heritagedata.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. image:: https://joss.theoj.org/papers/10.21105/joss.05040/status.svg
        :target: https://doi.org/10.21105/joss.05040

`Skosprovider <http://skosprovider.readthedocs.org>`_ implementation of the 
`Heritagedata Vocabularies <http://heritagedata.org>`_ (Historic England,
Historic Environment Scotland, Royal Commission on the Ancient and 
Historical Monuments of Wales, ...), can be used in conjunction with the 
`Atramhasis SKOS editor <https://github.com/OnroerendErfgoed/atramhasis>`_ to allow 
linking your own vocabularies to the Heritagedata thesauri and importing from them.

Building the docs
-----------------

More information about this library can be found in `docs`. The docs can be
built using `Sphinx <http://sphinx-doc.org>`_.

Please make sure you have installed Sphinx in the same environment where
skosprovider_heritagedata is present.

.. code-block:: bash

    # activate your virtual env
    $ pip install sphinx
    $ python setup.py develop
    $ cd docs
    $ make html
