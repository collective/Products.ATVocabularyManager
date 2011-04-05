# File: TreeVocabulary.py
"""
A Tree Vocabulary is a container for hierachical key/value pairs.
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
#from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.Archetypes.utils import OrderedDict
try:
    from Products.Archetypes.lib.vocabulary import DisplayList
except ImportError:
    from Products.Archetypes.utils import DisplayList

from Products.ATVocabularyManager.tools import registerVocabularyContainer
from Products.ATVocabularyManager.types.simple import SimpleVocabulary
from Products.ATVocabularyManager.config import PROJECTNAME


schema = SimpleVocabulary.schema + Schema((
    BooleanField('ShowLeavesOnly',
        widget = BooleanWidget(
            label = "Show leaves only",
            label_msgid = "label_show_leaves_only",
            description = "Check to show only leaves in this vocabulary.",
            description_msgid = "help_show_leaves_only",
            i18n_domain = "atvocabularymanager",
        ),
    ),
))


class TreeVocabulary(SimpleVocabulary):
    security = ClassSecurityInfo()

    schema = schema

    meta_type = 'TreeVocabulary'

    def getDisplayList(self, instance, display_parents='tree'):
        """ returns an object of class DisplayList as defined in
            Products.Archetypes.utils

            The instance of the content class is given as parameter.
        """
        dl = DisplayList()
        self._appendToDisplayList(dl, self.getVocabularyDict(instance), None,
                                  display_parents=display_parents)
        return dl

    def _appendToDisplayList(self, displaylist, vdict, valueparent,
                             display_parents='tree'):
        """ append subtree to flat display list
        """
        for key in vdict.keys():
            if type(vdict[key]) == type((1, 2)):
                value = vdict[key][0]
                subdict = vdict[key][1] or None
            else:
                value = vdict[key]
                subdict = None
            if valueparent and display_parents == 'tree':
                value = '%s - %s' % (valueparent, value)
            if valueparent and display_parents == 'marker':
                # Extract any leading -'s from the parent
                markers = 0
                for char in valueparent:
                    if char == '-':
                        markers += 1
                    else:
                        break
                value = '%s-- %s' % ('-'*markers, value)

            if (not self.showLeafsOnly()) or (not subdict):
                displaylist.add(key, value)

            if subdict:
                self._appendToDisplayList(displaylist, subdict, value,
                                          display_parents=display_parents)

    def getVocabularyDict(self, instance=None):
        """returns a vocabulary dictionary as defined in the interface
        """

        # see if we simply can return all objects and their
        # subtree, or if we have to use the correct translations

        if self.isLinguaPloneInstalled():
            # find out the currently used Language
            try:
                lang = instance.getLanguage()
            except AttributeError:
                # we try to retrieve the current language
                langtool = getToolByName(self, 'portal_languages')
                lang = langtool.getPreferredLanguage()

            return self._getTranslatedVocabularyDict(lang)
        else:
            # we don't need to care about languages, and can simply
            # return all contentObjects
            return self._getUntranslatedVocabularyDict()

    def _getTranslatedVocabularyDict(self, lang):
        """returns a vocabulary dict using the titles of the
        translations for language ``lang``

        Only canonical objects are used to build up this
        dictionary. If available, the translation's titles
        are used.
        """
        vdict = OrderedDict()

        for obj in self.contentValues():
            if obj.isCanonical():
                # we only add the canonical objects to this dict
                key = obj.getTermKey()
                # but use the title of the appropriate translation
                # if it is available (getTermValue is LP aware)
                vsubdict = obj._getTranslatedVocabularyDict(lang)
                vdict[key] = (obj.getTermValue(lang=lang), vsubdict)
        return vdict

    def _getUntranslatedVocabularyDict(self):
        """returns a vocabulary dictionary as defined in the interface
        """
        vdict = OrderedDict()

        for obj in self.contentValues():
            vsubdict = obj._getUntranslatedVocabularyDict()
            vdict[obj.getVocabularyKey()] = ( \
                obj.getVocabularyValue(), vsubdict)
        return vdict

    def showLeafsOnly(self):
        """ indicates if only leaves should be shown """
        if base_hasattr(self, 'getShowLeavesOnly'):
            return self.getShowLeavesOnly()
        return None

    def isFlat(self):
        """ indicates if tree or flat """
        return 0


registerType(TreeVocabulary, PROJECTNAME)
registerVocabularyContainer(TreeVocabulary)
# end of class TreeVocabulary
