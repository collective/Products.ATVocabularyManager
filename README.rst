Introduction
============

ATVocabularyManager: a vocabulary managing portal tool for Plone

.. contents::

Overview
========

- ATVocabularyManager offers central through the Plone management of
  dynamic vocabularies.

- This product is based on Archetypes and made to work with Archetypes as well
  as with other Products. It is intended use is within Archetypes Fields.
  Using it as a vocabulary provider for CMFMetadata worked out fine too. 
  Integration with different other products will work as well.

- to use a managed vocabulary simply add the term
  ``vocabulary = NamedVocabulary("myvocabulary")`` to the fields of your
  Archetypes Schema, import NamedVocabulary from this Product and create
  your vocabulary with id myvocabulary in 'portal_vocabularies' tool
  (available through Plone Site-Setup).

- ATVocabularyManager supports:

  simple flat key 
     value vocabularies

  tree like 
     hierachical vocabularies (see Limitations)

  IMS Vocabulary Definition Exchange Format (VDEX) aware vocabularies
     with XML Import and Export. VDEX is i18n-aware by its nature and does 
     not need LinguaPlone!

  Vocabularies are pluggable types. 
     ATVocabularyManager is prepared for extension with your special 
     vocabulary type. ArchGenXML will help you here.
     Each vocabulary term needs to be an CMF aware content type. Reuse normal
     rich content as a vocabularies.

ArchGenXML 1.4+ code-generator does full integration of ATVocabularyManager:
via tagged value defined named vocabularies are registered transparently,
VDEX-XML files are imported at install-time, stub vocabularies are created
at install time and custom types are registered by just providing appropriate
stereotypes.

ATVM is Linguaplone compatible (only tested with SimpleVocabulary, and 
TreeVocabulary). Add a simple vocabulary with some items, install and configure 
Linguaplone, translate the vocabulary to the language(s) of your choice, 
translate every item to the language(s) of your choice. NamedVocabulary() will 
return the vocabulary as usual, the keys will stay the same disregarding 
language settings, the values will show in the currently selected language.
VDEX vocabularies are not using LinguaPlone, but are i18n-aware (imo much 
better than  everything else).

You can do hierachy-aware searches on treevocabularies (for more information on 
this see doc/search_treevocabulary.txt) attention: curently certain changes in 
the term hierachy require a catalog rebuild (see Limitations).


Installation
============

This addon can be installed has any other addons. please follow official
documentation_

.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to

To speed up ATVocabularyManager you might want to associate it with a
Cache-Manager.


Dependencies
------------

- Products.Archetypes
- imsvdex
- [Products.Linguaplone] optional


Limitations
===========

TreeVocabulary catalog updates
    If you are using the hierachy-aware catalog search support of 
    tree-vocabularies you need to rebuild the uid_catalog and portal_catalog 
    if you move a vocabularyterm that has other terms below it.

Creation/Edit of VDEX TTW is difficult. 
    Take an editor of your choice, create the vocab and upload it or help 
    writing an UI.


Known Bugs
==========

- Check the issue-tracker: https://github.com/collective/Products.ATVocabularyManager/issues
  Feel free to add bugs in here!


Support
=======
Usally the authors are offering professional support. The classical well-working 
community support is found at the mailing-lists and IRC-channels announced at
plone.org:http://plone.org

