# Copyright (c) 2004-2006 by BlueDynamics Alliance - Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#
from zope.interface import Interface


class IVocabularyTerm(Interface):
    """A VocabularyTerm has a value (which is used to
    display the term) and a key that is used to identify
    the term.
    """

    def getTermKey(self):
        """Returns the key of this term inside the vocabulary.
        All translations of a term have the same key.
        """

    def getTermValue(self, lang=None):
        """Returns the string-value of the vocabulary.

        This might be language sensitive.
        """

    def getTermKeyPath(self):
        """Returns the Keypath of this term.
        For the term "A - B - C" this method retuns a
        list containing the Keys of A, B, and C forming
        a path.
        eg: [keyA, keyB, keyC]
        """
