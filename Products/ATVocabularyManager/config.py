# Copyright (c) 2004-2006 by BlueDynamics Tyrol - Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#

from Products.Archetypes.utils import DisplayList

# package configuration

PROJECTNAME = 'ATVocabularyManager'
SKINS_DIR = 'skins'

DEPENDENCIES = ['Archetypes', ]

TOOL_NAME = 'portal_vocabularies'
TOOL_TITLE = 'Vocabulary Library'
TOOL_META = 'VocabularyLibrary'

ADD_CONTENT_PERMISSION = 'Add ATVocabularyManager content'

DEFAULT_VOCABULARY_CONTAINER = 'SimpleVocabulary'
DEFAULT_VOCABULARY_ITEM = 'SimpleVocabularyTerm'

VDEX_EXPORT_NEWL = '\n'
VDEX_EXPORT_INDENT = '\t'

# encoding of files in flat-file csv import
IMPORT_ENCODING = 'latin-1'


SORT_METHOD_FOLDER_ORDER = "getObjPositionInParent"
SORT_METHOD_LEXICO_VALUES = "lexicographic_values"
SORT_METHOD_LEXICO_KEYS = "lexicographic_keys"

VOCABULARY_SORT_ORDERS = DisplayList((
    ('getObjPositionInParent', 'Vocabulary Folder Order', 'sort_method_folder_order'),
    ('lexicographic_values', 'Lexicographic sort by values', 'sort_method_lexi_value'),
    ('lexicographic_keys', 'Lexicographic sort by keys', 'sort_method_lexi_keys'),
    ))

# LinguaPlone addon?
try:
    import Products.LinguaPlone
except ImportError:
    HAS_LINGUA_PLONE = False
else:
    HAS_LINGUA_PLONE = True

GLOBALS = globals()
