# File: vdexRelationEndPoint.py
"""\
unknown

RCS-ID $Id: codesnippets.py 3417 2005-01-11 19:29:35Z yenzenz $
"""
# Copyright (c) 2005 by eduplone Open Source Business Network EEIG
# This code was created for the ZUCCARO project.
# ZUCCARO (Zope-based Universally Configurable Classes for Academic Research
# Online) is a database framework for the Humanities developed by the
# Bibliotheca Hertziana, Max-Planck Institute for Art History
# For further information: http://zuccaro.biblhertz.it/
#
# BSD-like licence, see LICENCE.txt
#
__author__  = '''Jens Klein <jens@bluedynamics.com>'''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *


class vdexRelationEndPoint(BaseContent):

    __implements__ = getattr(BaseContent,'__implements__',())

    security = ClassSecurityInfo()
    portal_type = meta_type = 'VdexRelationEndPoint'
    archetype_name = 'VDEX Relation End-Point'   #this name appears in the 'add' box
    allowed_content_types = []

    factory_type_information={
        'allowed_content_types':allowed_content_types,
        'allow_discussion': 0,
        'immediate_view':'base_view',
        'global_allow':0,
        'filter_content_types':1,
        }

    aliases = { 
        '(Default)' : 'base_view', 
        'view' : 'base_view', 
        'edit' : 'base_edit', 
    }
    
    schema=BaseSchema + Schema((
        StringField('TermIdentifier',
            widget=StringWidget(description='Enter a value for TermIdentifier.',
                description_msgid='VDEXVocabulary_help_TermIdentifier',
                i18n_domain='VDEXVocabulary',
                label='Termidentifier',
                label_msgid='VDEXVocabulary_label_TermIdentifier',
            ),
        ),

        StringField('VocabularyIdentifier',
            widget=StringWidget(description='Enter a value for VocabularyIdentifier.',
                description_msgid='VDEXVocabulary_help_VocabularyIdentifier',
                i18n_domain='VDEXVocabulary',
                label='Vocabularyidentifier',
                label_msgid='VDEXVocabulary_label_VocabularyIdentifier',
            ),
        ),

    ),
    )

    #Methods
    def getDOMBindingNode(self,doc):
        """
        returns a dom-element containing its and all it subobjects dom
        representation
        """
        node=doc.createElement('relationship')
        return node

    def SearchableText(self):
        return ''

registerType(vdexRelationEndPoint)
