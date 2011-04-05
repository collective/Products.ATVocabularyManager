from zope import event
from zope import interface
from Products.ATVocabularyManager import interfaces
from Products.ATVocabularyManager.tools import vocabularylib
#from Products.CMFCore import utils as cmfutils


class TermRenamedEvent(object):
    interface.implements(interfaces.ITermRenamedEvent)

    def __init__(self, keyword, new_keyword, term, vocabulary):
        self.keyword = keyword
        self.new_keyword = new_keyword
        self.term = term
        self.vocabulary = vocabulary


class TermDeletedEvent(object):
    interface.implements(interfaces.ITermDeletedEvent)

    def __init__(self, keyword, term, vocabulary):
        self.keyword = keyword
        self.term = term
        self.vocabulary = vocabulary


def find_toplevel_vocab(obj):
    result = obj
    while hasattr(result, 'aq_parent'):
        if isinstance(result.aq_parent.aq_base,
                      vocabularylib.VocabularyLibrary):
            return result
        result = result.aq_parent

    return None


def term_removed_handler(obj, evt):
    vocab = find_toplevel_vocab(obj)
    event.notify(TermDeletedEvent(obj.Title(), obj, vocab))
