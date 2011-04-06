# Copyright (c) 2004-2006 by BlueDynamics Alliance - Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#
import os

try:
    from App.Common import package_home
except ImportError:
    # not sure that we still need to support this
    from Globals import package_home


from Products.CMFCore import utils as cmfutils
from Products.CMFCore import DirectoryView

from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.ATVocabularyManager.config import *
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary

DirectoryView.registerDirectory(SKINS_DIR, GLOBALS)
DirectoryView.registerDirectory(os.path.join(SKINS_DIR, 'ATVocabularyManager'),
                                GLOBALS)


def initialize(context):
    ##Import Types here to register them
    import types
    import tools
    import utils

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME),
                                                      PROJECTNAME)

    cmfutils.ToolInit( PROJECTNAME+' Tools',
                tools = [tools.VocabularyLibrary],
                icon='tool.gif'
                ).initialize( context )

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
