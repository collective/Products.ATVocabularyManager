# File: vocabulary.py
"""\
A vocabulary is a container for key/value pairs. This AliasVocabulary can points
to any other registered vocabulary-type.

RCS-ID $Id: SimpleVocabulary.py 3219 2004-10-29 00:49:03Z zworkb $
"""
# Copyright (c) 2004-2006 by BlueDynamics Alliance - Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'

#import csv
#from StringIO import StringIO
from zope.interface import implements
from Products.ATVocabularyManager.config import *
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import *
else:
    from Products.Archetypes.atapi import *

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IVocabulary
from Products.ATVocabularyManager.tools import registerVocabularyContainer
from Products.ATVocabularyManager.config import TOOL_NAME as VOCABTOOL_NAME
from Products.ATVocabularyManager.config import PROJECTNAME


class AliasVocabulary(BaseContent):

    implements(IVocabulary)

    security = ClassSecurityInfo()
    meta_type = 'AliasVocabulary'

    schema = BaseFolderSchema + Schema((
        StringField('id',
            required=1, ## Still actually required, but
                        ## the widget will supply the missing value
                        ## on non-submits
            mode="rw",
            accessor="getId",
            mutator="setId",
            default='',
            widget=StringWidget(
                label="Vocabulary Name",
                label_msgid="label_vocab_name",
                description="Should not contain spaces, underscores or mixed case.",
                description_msgid="help_vocab_name",
                i18n_domain="atvocabularymanager"
            ),
        ),

        TextField('description',
            default='',
            required=0,
            searchable=0,
            accessor="Description",
            storage=MetadataStorage(),
            widget = TextAreaWidget(description = "Enter a brief description",
              description_msgid = "help_description",
              label = "Description",
              label_msgid = "label_description",
              rows = 5,
              i18n_domain = "plone"
            ),
        ),
        ReferenceField('target',
            relationship = 'vocabulary_alias',
            allowed_types_method = 'getPossibleTargets',
            vocabulary_display_path_bound = -1,
            required = True,
            widget=ReferenceWidget(
                label='Target',
                label_msgid='label_target',
                description='Select target vocabulary.',
                description_msgid='help_target',
                i18n_domain='atvocabularymanager',
            ),
        )
    ))

    def getPossibleTargets(self, instance):
        """ fetch a list of vocabularie w/o AliasVocabulary """
        vlib = getToolByName(instance, VOCABTOOL_NAME)
        allowed = vlib.allowedContentTypes()
        allowed = [a.id for a in allowed if a.id != self.portal_type]
        return allowed


    # Methods from Interface IVocabulary

    def getDisplayList(self, instance):
        """ returns a object of class DisplayList as defined in
            Products.Archetypes.utils

            The instance of the content class is given as parameter.
        """
        target = self.getTarget()
        return target.getDisplayList(instance)

    def getVocabularyLines(self, instance=None):
        """ returns a List of Key-Value tuples """
        target = self.getTarget()
        return target.getVocabularyLines(instance)

    def getVocabularyDict(self, instance=None):
        """ returns a vocabulary dictionary as defined in the interface"""
        target = self.getTarget()
        return target.getVocabularyDict(instance)

    def isFlat(self):
        """ returns true for a flat vocabulary """
        target = self.getTarget()
        return target.isFlat()

    def showLeafsOnly(self):
        """ indicates if only leafs should be shown """
        target = self.getTarget()
        return target.showLeafsOnly()

registerType(AliasVocabulary, PROJECTNAME)
registerVocabularyContainer(AliasVocabulary)
# end of class AliasVocabulary
