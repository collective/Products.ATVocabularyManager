# File: TreeVocabularyTerm.py
"""
A Tree-aware Key-Value term, where Value may be i18nized using LinguaPlone.
"""
# Copyright (c) 2004-2006 by BlueDynamics Alliance - Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'

from Products.ATVocabularyManager.config import *
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import *
else:
    from Products.Archetypes.atapi import *

from AccessControl import ClassSecurityInfo

#from zope.interface import noLongerProvides
from Products.Archetypes.debug import deprecated
#from Products.Archetypes.interfaces.vocabulary import IVocabulary
from Products.ATVocabularyManager.types.simple import SimpleVocabularyTerm
from Products.ATVocabularyManager.types.tree import TreeVocabulary
from Products.ATVocabularyManager.config import PROJECTNAME
from Products.ATVocabularyManager import messageFactory as _ 


class TreeVocabularyTerm(TreeVocabulary, SimpleVocabularyTerm):
    """ Term inside of a TreeVocabulary or as an subterm
    """

    security = ClassSecurityInfo()
    meta_type = 'TreeVocabularyTerm'

    schema = BaseSchema + Schema((
        StringField('id',
            required = 0, ## Still actually required, but
                        ## the widget will supply the missing value
                        ## on non-submits
            mode = "rw",
            accessor = "getId",
            mutator = "setId",
            default = '',
            size=50,
            widget = IdWidget(
                label=_("label_key", default=u"Key"),
                description=_("help_vocab_name",
                              default="Should not contain spaces, underscores or mixed case."),
                ),
            ),

        StringField('title',
            required = 1,
            searchable = 0,
            default = '',
            accessor = 'Title',
            widget = StringWidget(
                label=_("label_value", default=u"Value"),
            ),
        )),
    )


    # Methods
    # methods from Interface IVocabularyTerm

    def getTermKey(self):
        """
        """
        if not HAS_LINGUA_PLONE or self.isCanonical():
            return self.UID()
        else:
            return self.getCanonical().UID()

    def getTermValue(self, lang=None):
        """
        """
        if (not HAS_LINGUA_PLONE) or (lang is None):
            return self.Title()
        else:
            trans = self.getTranslation(lang)
            return trans and trans.Title() or self.Title()

    def getTermKeyPath(self):
        path = [self.getTermKey(), ]
        actTerm = self
        while actTerm.aq_parent.portal_type != 'TreeVocabulary' \
                  and hasattr(actTerm.aq_parent, 'getTermKey'):
            path.append(actTerm.aq_parent.getTermKey())
            actTerm = actTerm.aq_parent

        path.reverse()
        return path

    def getVocabularyKey(self):
        ''' returns the key of the field '''
        deprecated("please use the IVocabularyTerm compatible method 'getTermKey'")
        return self.getTermKey()

    def getVocabularyValue(self, lang=None, **kwargs):
        ''' returns the value of the field. The value is a processed value '''
        deprecated("please use the IVocabularyTerm compatible method 'getTermValue'")
        return self.getTermValue(lang=lang, **kwargs)

    # these should be inherited from SimpleVocabularyTerm
    processForm = SimpleVocabularyTerm.processForm
    edit = SimpleVocabularyTerm.edit
    update = SimpleVocabularyTerm.update


registerType(TreeVocabularyTerm, PROJECTNAME)
# end of class TreeVocabularyTerm
