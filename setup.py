import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.6.8.dev0'

long_description = (
    read('README.rst')
    + '\n' +
    read('docs', 'LICENSE.txt')
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    read('TODO.txt')
    + '\n' +
    read('Products', 'ATVocabularyManager', 'doc', 'simplevocabulary.txt')
    + '\n' +
    read('Products', 'ATVocabularyManager', 'doc', 'search_treevocabulary.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n'
    )

install_requires = [
    'imsvdex',
    'plone.api',
    'setuptools',
    'Products.Archetypes',
    'Products.CMFPlone',
]


setup(name='Products.ATVocabularyManager',
      version=version,
      description="Vocabulary library Plone. Central, Pluggable, "
                  "TTW, with IMS VDEX Support",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Framework :: Zope2",
          "Programming Language :: Python",
          #"License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='Plone Vocabulary Manager Zope IMS VDEX Tree '
               'Taxonomy Onthology',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url='https://github.com/collective/Products.ATVocabularyManager',
      #license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=['interlude', 'Products.LinguaPlone', 'plone.app.testing'],
          test5=['interlude', 'plone.app.testing', 'archetypes.multilingual'],
          plone4=['Plone', 'Pillow'],
      ),
      install_requires=install_requires,
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """)