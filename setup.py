import os
from xml.dom.minidom import parse
from setuptools import setup, find_packages

CLASSIFIERS = [
    'Programming Language :: Python',
    'Framework :: Zope2',
    'Framework :: Plone',
]

mdfile = os.path.join(os.path.dirname(__file__), 'Products',
                      'ATVocabularyManager', 'profiles', 'default',
                      'metadata.xml')
metadata = parse(mdfile)
assert metadata.documentElement.tagName == "metadata"
version =  metadata.getElementsByTagName("version")[0].childNodes[0].data
shortdesc = metadata.getElementsByTagName("description")[0].childNodes[0].data
readme = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()
changes = open(os.path.join(os.path.dirname(__file__),
                            'HISTORY.txt')).read().strip()
long_description = readme + '\n\nCHANGES\n=======\n\n' +  changes

setup(name='Products.ATVocabularyManager',
      version=version,
      author='Jens Klein',
      author_email='jens@bluedynamics.com',
      maintainer='Jens Klein',
      maintainer_email='jens@bluedynamics.com',
      classifiers=CLASSIFIERS,
      keywords='Plone Vocabulary Manager Zope',
      url='http://plone.org/products/atvocabularymanager',
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
