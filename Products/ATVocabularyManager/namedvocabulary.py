# File: NamedVocabulary.py
"""\
This is a small 'wrapper' to access a named vocabulary from
portal_vocabularytool and to fetch its DisplayList

"""
# Copyright (c) 2004-2008 by BlueDynamics Alliance, Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'

import Missing
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IVocabulary
from Products.ATVocabularyManager.types.tree.vocabulary import TreeVocabulary
from config import TOOL_NAME


class NamedVocabulary(object):

    implements(IVocabulary)

    vocab_name= None

    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')
    # Add a class variable to avoid migration issues
    display_parents = 'tree'

    def __init__(self, vocabname=None, display_parents='tree'):
        self.vocab_name = vocabname
        self.display_parents = display_parents

    security.declarePublic('getDisplayList')
    def getDisplayList(self, instance):
        """ returns a object of class DisplayList as defined in
            Products.Archetypes.utils.

            The instance of the content class is given as parameter.
        """
        vocab = self.getVocabulary(instance)
        if isinstance(vocab, TreeVocabulary):
            return vocab.getDisplayList(instance,
                                    display_parents=self.display_parents)
        return vocab.getDisplayList(instance)

    security.declarePublic('getVocabularyDict')
    def getVocabularyDict(self, instance):
        """ returns the vocabulary as a dictionary with a string key and a
            string value. If it is not a flat vocabulary, the value is a
            tuple with a string and a sub-dictionary with the same format
            (or None if its a leave).

            The instance of the content is given as parameter.
        """
        vocab = self.getVocabulary(instance)
        return vocab.getVocabularyDict(instance)

    security.declarePublic('isFlat')
    def isFlat(self, instance):
        """ indicates if it is a flat or hierachical vocabulary """

        vocab = self.getVocabulary(instance)
        return vocab.isFlat(instance)

    security.declarePublic('showLeafsOnly')
    def showLeafsOnly(self, instance):
        """ indicates if only leaves or also nots should be shown
        """

        vocab = self.getVocabulary(instance)
        return vocab.showLeafsOnly(instance)


    security.declarePrivate('getVocabulary')
    def getVocabulary(self, instance):
        """ return the vocabulary by name from atvocabularymanager
        """
        vt = getToolByName(instance, TOOL_NAME)
        vocab = vt.getVocabularyByName(self.vocab_name)
        if vocab is None:
            raise KeyError('Vocabulary id not found in '+ \
                'portal_vocabularies : %s' % self.vocab_name)        
        assert(IVocabulary.providedBy(vocab))
        return vocab

    def getKeyPathForTerms(self, instance, terms=()):
        """Returns a list containing all keypaths for the
        given terms.

        Terms can be given as objects or their keys.

        The instance of the content is given as parameter.
        """

        # XXX testcase: provide None, an empty list, treeterms, keys
        # maybe even wrong keys (of (non)existing objects, but no terms)


        # keywordindex is satisfied with an empty list
        keypath = []

        # if terms is none or an empty list we can't do a lot
        if terms is None or terms == ():
            return keypath

        # we can get a list, or just a value
        if not isinstance(terms, (tuple, list)):
            terms=[terms, ]

        uc = getToolByName(instance, 'uid_catalog')

        # obtain the keypath for every term given in ``terms``
        for term in terms:
            if isinstance(term, str):
                # term is given as termkey/uid
                key = term
            else:
                key = term.getTermKey()

            result = uc(UID=key)

            # if we found a term, we can add it's keypath to our list
            if result:
                uids = result[0].getTermKeyPath
                if uids != Missing.Value:
                    keypath.extend(uids)

        return keypath

# end of class NamedVocabulary
