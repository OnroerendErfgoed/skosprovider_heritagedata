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
