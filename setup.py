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
    'skosprovider>=0.5.0',
    'requests',
    'rdflib'
]

setup(
    name='skosprovider_heritagedata',
    version='0.2.0',
    description='Skosprovider implementation of the heritagedata.org Vocabularies',
    long_description=README,
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    url='https://github.com/OnroerendErfgoed/skosprovider_heritagedata',
    keywords='heritagedata.org skos skosprovider',
    test_suite='nose.collector'
)
