import os
from setuptools import setup, find_packages


CLASSIFIERS = [
    'Programming Language :: Python',
    'Framework :: Zope2',
    'Framework :: Plone',
]

version_file = os.path.join('Products', 'ATVocabularyManager', 'version.txt')
version = open(version_file).read().strip()

readme_file= os.path.join('Products', 'ATVocabularyManager', 'README.txt')
desc = open(readme_file).read().strip()
changes_file = os.path.join('Products', 'ATVocabularyManager', 'HISTORY.txt')
changes = open(changes_file).read().strip()

long_description = desc + '\n\nCHANGES\n=======\n\n' +  changes 

setup(name='Products.ATVocabularyManager',
      version=version,
      author='Jens Klein',
      author_email='jens.klein@bluedynamics.com',
      maintainer='Jens Klein',
      maintainer_email='jens.klein@bluedynamics.com',
      classifiers=CLASSIFIERS,
      keywords='Plone Vocabulary Manager Zope',
      url='http://plone.org/products/atvocabularymanager',
      description='A central pluggable vocabulary library for use with Archetypes based products',
      long_description=long_description,
      packages=['Products', 'Products.ATVocabularyManager'],
      include_package_data = True,
      zip_safe=False,
      install_requires=['setuptools', 'imsvdex'],
      namespace_packages=['Products'],

      )
