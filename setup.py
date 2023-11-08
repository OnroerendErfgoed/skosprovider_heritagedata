import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

packages = [
    'skosprovider_heritagedata'
]

requires = [
    'skosprovider>=1.1.0',
    'requests',
    'rdflib'
]

setup(
    name='skosprovider_heritagedata',
    version='1.2.1',
    description='Skosprovider implementation of the heritagedata.org Vocabularies',
    long_description=README,
    long_description_content_type='text/x-rst',
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    url='https://github.com/OnroerendErfgoed/skosprovider_heritagedata',
    keywords='heritagedata.org skos skosprovider thesauri vocabularies',
)
