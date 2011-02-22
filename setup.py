import os
from xml.dom.minidom import parse
from setuptools import setup, find_packages

CLASSIFIERS = [
    'Programming Language :: Python',
    'Framework :: Zope2',
    'Framework :: Plone',
]

version = '1.6'
shortdesc = 'Vocabulary library Plone. Central, Pluggable, TTW, with IMS VDEX Support'
readme = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()
changes = open(os.path.join(os.path.dirname(__file__),
                            'HISTORY.txt')).read().strip()
long_description = readme + '\n\nCHANGES\n=======\n\n' +  changes

setup(name='Products.ATVocabularyManager',
      version=version,
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      classifiers=CLASSIFIERS,
      keywords='Plone Vocabulary Manager Zope IMS VDEX Tree Taxonomie Onthology',
      url='https://svn.plone.org/svn/archetypes/Products.ATVocabularyManager/',
      description=shortdesc,
      long_description=long_description,
      packages=['Products', 'Products.ATVocabularyManager'],
      include_package_data = True,
      zip_safe=False,
      install_requires=['setuptools', 'imsvdex', 'zope.i18nmessageid'],
      namespace_packages=['Products'],
      extras_require = dict(
          test = ['interlude', 'Products.LinguaPlone',],
          plone4 = ['Plone', 'Pillow'],
      ),

      )
