from zope import interface
from zope import schema


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
