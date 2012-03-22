import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.6.2'

long_description = (
    read('README.txt')
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


setup(name='Products.ATVocabularyManager',
      version=version,
      description="Vocabulary library Plone. Central, Pluggable, TTW, with IMS VDEX Support",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Framework :: Zope2",
          #"License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
      ],
      keywords='Plone Vocabulary Manager Zope IMS VDEX Tree Taxonomy Onthology',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url='https://svn.plone.org/svn/archetypes/Products.ATVocabularyManager/',
      #license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require = dict(
          test = ['interlude', 'Products.LinguaPlone',],
          plone4 = ['Plone', 'Pillow'],
      ),
      install_requires=[
        'setuptools',
        'imsvdex',
        'zope.i18nmessageid'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
