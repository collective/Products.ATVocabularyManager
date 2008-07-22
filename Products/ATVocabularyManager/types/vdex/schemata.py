"""\
schemata definition for the vdex types

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

from Products.Archetypes.atapi import *
from Products.ATVocabularyManager.types.vdex.marshaller import VDEXMarshaller

# reusable fields
OrderSignificantField = BooleanField('OrderSignificant',
        searchable=0,
        default=False,
        languageIndependent = True,
        widget=BooleanWidget(description='Enter a value for OrderSignificant.',
            description_msgid='VDEXVocabulary_help_OrderSignificant',
            i18n_domain='VDEXVocabulary',
            label='Ordersignificant',
            label_msgid='VDEXVocabulary_label_OrderSignificant',
        ),
    )

# the schemata
vocabulary_schema=OrderedBaseFolderSchema + Schema((
    StringField('VocabularyIdentifier',
        searchable=False,
        languageIndependent = True,
        widget=StringWidget(description='Enter a value for the VDEX Identifier.',
            description_msgid='VDEXVocabulary_help_VocabularyIdentifier',
            i18n_domain='VDEXVocabulary',
            label='VDEX Identifier',
            label_msgid='VDEXVocabulary_label_VocabularyIdentifier',
        ),
    ),

    StringField('title',
        searchable=False,
        accessor="Title",
        required=1,
        default='',
        mode='r',
        widget=StringWidget(description='The Vocabulary Name is entered using langstrings.',
            description_msgid='VDEXVocabulary_help_VocabularyName',
            i18n_domain='VDEXVocabulary',
            label='Vocabulary Name',
            label_msgid='VDEXVocabulary_label_VocabularyName',
        ),
    ),

    OrderSignificantField,

    StringField('ProfileType',
        searchable=False,
        languageIndependent = True,
        default='lax',
        vocabulary=['lax','thesaurus','hierachicalTokenTerms','glossaryOrDictionary','flatTokenTerms'],
        widget=StringWidget(description='Enter a value for ProfileType.',
            description_msgid='VDEXVocabulary_help_ProfileType',
            i18n_domain='VDEXVocabulary',
            label='Profile Type',
            label_msgid='VDEXVocabulary_label_ProfileType',
        ),
    ),

    BooleanField('RegistrationStatus',
        searchable=False,
        languageIndependent = True,
        default=False,
        widget=BooleanWidget(description='Enter a value for RegistrationStatus.',
            description_msgid='VDEXVocabulary_help_RegistrationStatus',
            i18n_domain='VDEXVocabulary',
            label='Registration Status',
            label_msgid='VDEXVocabulary_label_RegistrationStatus',
        ),
    ),

    StringField('DefaultLanguage',
        searchable=False,
        languageIndependent = True,
        widget=StringWidget(description='Enter a value for DefaultLanguage.',
            description_msgid='VDEXVocabulary_help_DefaultLanguage',
            i18n_domain='VDEXVocabulary',
            label='Default Language',
            label_msgid='VDEXVocabulary_label_DefaultLanguage',
        ),
    ),

),
marshall=VDEXMarshaller()
)

term_schema=BaseFolderSchema + Schema((
    StringField('Identifier',
        searchable=0,
        languageIndependent = True,
        widget=StringWidget(description='Enter a value for VDEX Identifier.',
            description_msgid='VDEXVocabulary_help_Identifier',
            i18n_domain='VDEXVocabulary',
            label='VDEX Identifier',
            label_msgid='VDEXVocabulary_label_Identifier',
        ),
    ),

    StringField('title',
        searchable=0,
        accessor="Title",
        storage=MetadataStorage(),
        widget=StringWidget(description='Enter a value for Caption.',
            description_msgid='VDEXVocabulary_help_Caption',
            i18n_domain='VDEXVocabulary',
            label='Caption',
            label_msgid='VDEXVocabulary_label_Caption',
        ),
    ),

    StringField('description',
        searchable=0,
        accessor="Description",
        storage=MetadataStorage(),
        widget=StringWidget(description='Enter a value for Description.',
            description_msgid='VDEXVocabulary_help_Description',
            i18n_domain='VDEXVocabulary',
            label='Description',
            label_msgid='VDEXVocabulary_label_Description',
        ),
    ),

    OrderSignificantField,

    BooleanField('ValidForIndexing',
        searchable=0,
        languageIndependent = True,
        widget=BooleanWidget(description='Enter a value for ValidForIndexing.',
            description_msgid='VDEXVocabulary_help_ValidForIndexing',
            i18n_domain='VDEXVocabulary',
            label='Validforindexing',
            label_msgid='VDEXVocabulary_label_ValidForIndexing',
        ),
    ),


    ReferenceField('vdexRelation',
        searchable=0,
        allowed_types=('VdexTerm','vdexRelationEndPoint',),
        multiValued=1,
        relationship='vdexRelation',
        languageIndependent = True,
        widget=ReferenceWidget(description='Enter a value for vdexRelation.',
            description_msgid='VDEXVocabulary_help_vdexRelation',
            i18n_domain='VDEXVocabulary',
            label='Vdexrelation',
            label_msgid='VDEXVocabulary_label_vdexRelation',
        ),
    ),

),
)

mediadescriptor_schema=BaseSchema + Schema((
    StringField('title',
        required=1,
        searchable=0,
        default='',
        mode='r',
        accessor='Title',
    ),

    StringField('MediaLocation',
        required=True,
        languageIndependent = True,
        widget=StringWidget(description='Enter a URL for Media Location.',
            description_msgid='VDEXVocabulary_help_MediaLocation',
            i18n_domain='VDEXVocabulary',
            label='Media Location',
            label_msgid='VDEXVocabulary_label_MediaLocation',
        ),
    ),

),
)
