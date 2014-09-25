skosprovider_heritagedata
=========================

A skosprovider for the services at `heritagedata.org <http://heritagedata.org>`_.

.. image:: https://travis-ci.org/OnroerendErfgoed/skosprovider_heritagedata.png?branch=master
        :target: https://travis-ci.org/OnroerendErfgoed/skosprovider_heritagedata
.. image:: https://coveralls.io/repos/OnroerendErfgoed/skosprovider_heritagedata/badge.png?branch=master
        :target: https://coveralls.io/r/OnroerendErfgoed/skosprovider_heritagedata
.. image:: https://readthedocs.org/projects/skosprovider-heritagedata/badge/?version=latest
        :target: https://readthedocs.org/projects/skosprovider-heritagedata/?badge=latest
.. image:: https://badge.fury.io/py/skosprovider_heritagedata.png
        :target: http://badge.fury.io/py/skosprovider_heritagedata

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
