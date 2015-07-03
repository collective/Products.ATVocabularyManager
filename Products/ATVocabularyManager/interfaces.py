from zope import interface
from zope import schema

from Products.Archetypes.interfaces import IVocabulary

# Vocabulary types

class IAliasVocabulary(IVocabulary):
    """ An alias vocabulary
    """

class ISimpleVocabulary(IVocabulary):
    """ A simple vocabulary
    """

class ISortedSimpleVocabulary(IVocabulary):
    """ A sorted simple vocabulary
    """

class ITreeVocabulary(IVocabulary):
    """ A tree vocabulary
    """

class ISimpleVocabularyTerm(interface.Interface):
    """ A term of a simple vocabulary
    """

class ITreeVocabularyTerm(interface.Interface):
    """ A term of a tree vocabulary
    """

class IMSVDEXVocabulary(IVocabulary):
    """ A VDEX vocabulary
    """

#

class IATVocabularyLibrary(interface.Interface):
    """ Interface for the tool """

class IKeywordEvent(interface.Interface):
    """An event concerning keywords.
    """

    keyword = schema.TextLine(title=u'Keyword',
                              readonly=False,
                              required=True)

class IKeywordDeletedEvent(IKeywordEvent):
    """Keyword deleted event.
    """

class IKeywordRenamedEvent(IKeywordEvent):
    """Keyword renamed event.
    """

    new_keyword = schema.TextLine(title=u'New Keyword',
                                  readonly=False,
                                  required=True)

class ITermDeletedEvent(IKeywordDeletedEvent):
    """An event signifying that a term has been deleted.
    """

    vocabulary = interface.Attribute('Parent vocabulary')
    term = interface.Attribute('A term')

class ITermRenamedEvent(IKeywordRenamedEvent):
    """An event signifying that a term has been renamed.
    """

    vocabulary = interface.Attribute('Parent vocabulary')
    term = interface.Attribute('A term')
