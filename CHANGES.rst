1.2.0 (2023-??-??)
------------------

- This library now requires skosprovider 1.1.0 (#86)
- All current (2023-11-06) conceptschemes defines by heritagedata.org are now included
  as skosprovider_heritagedata.utils.CONCEPTSCHEMES. Reusing them avoids a call to the
  webservice just to get the conceptscheme loaded (#88)
- Add support for Python 3.11

1.1.0 (2022-08-17)
------------------
- Remove python 3.6 and 3.7 support, add support for 3.8, 3.9 and 3.10
- Update RDFLib to 6.2.0 (#77)

1.0.0 (2021-12-17)
------------------
- Drop python 2 support
- Upgrade all requirements (#65)


0.3.1 (2017-09-06)
------------------

- Stop loading the conceptscheme while initialising the provider.
- Add support for Python 3.6

0.3.0 (2016-08-11)
------------------

- Compatibile with `SkosProvider 0.6.0 <http://skosprovider.readthedocs.org/en/0.6.0>`_.
- Allow passing a custom requests Session to a provider. (#14)

0.2.1 (2015-03-10)
------------------

- Fix an issue where calls that include a `language` parameter would fail because
  certain methods were not expecting extra keyword parameters. (#12)
- Some documentation clarifications. (#11)

0.2.0 (2014-12-19)
------------------

- Compatibile with `SkosProvider 0.5.0 <http://skosprovider.readthedocs.org/en/0.5.0>`_.
- Each Concept or Collection now also provides information on the ConceptScheme 
  it's part of.
- Fix some issues with UTF-8 encoding.
- Fixed some issues with Python 2.x/3.x compatibility.
- Provider now throws a ProviderNotAvailableException when the underlying service is down.


0.1.0 (2014-10-08)
------------------

- Initial version
- Compatible with `SkosProvider 0.3.0 <http://skosprovider.readthedocs.org/en/0.3.0>`_.
