"""
provides VDEX compliant vocabulary - using imsvdex python package
"""
# Copyright (c) 2007 by BlueDynamics Alliance, Klein & Partner KEG, Austria
# This code was created for the ZUCCARO project.
# ZUCCARO (Zope-based Universally Configurable Classes for Academic Research
# Online) is a database framework for the Humanities developed by the
# Bibliotheca Hertziana, Max-Planck Institute for Art History
# For further information: http://zuccaro.biblhertz.it/
#
# BSD-like licence, see LICENCE.txt
#
__author__ = '''Jens Klein <jens@bluedynamics.com>'''
__docformat__ = 'plaintext'

from zope.interface import implements
from StringIO import StringIO
from types import StringTypes
from AccessControl import ClassSecurityInfo
from Products.PlacelessTranslationService.Negotiator import getLangPrefs
from Products.CMFCore  import permissions
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces import IVocabulary
from Products.ATVocabularyManager.tools.vocabularylib import registerVocabularyContainer
from Products.ATVocabularyManager.config import *
from Products.ATVocabularyManager.config import PROJECTNAME
from zope.interface import implements
from imsvdex.vdex import VDEXManager, VDEXError

from Products.ATContentTypes import ATCTMessageFactory as _

IMSVDEXVocabularySchema = Schema((

    StringField(
        name = 'title',
        required = 1,
        searchable = 1,
        default = '',
        accessor = 'Title',
        widget = StringWidget(
            label=_(u'label_title', default=u'Title'),
            visible = {'view': 'invisible', 'edit': 'invisible'},
            i18n_domain = 'plone',
        ),
    ),
    TextField(
        'description',
        default = '',
        searchable = 1,
        accessor = "Description",
        schemata = 'default',
        widget = TextAreaWidget(
            visible = {'view': 'visible', 'edit': 'invisible'},
            label=_(u'label_description', default=u'Description'),
            description=_(u'help_description', default=u'A short summary of the content'),
            i18n_domain = "plone"),
    ),

    FileField(
        name = 'vdex',
        allowable_content_types = ["text/xml"],
        widget = FileWidget(
            label=_(u'IMSVDEXVocabulary_label_vdex', default=u'VDEX-XML-Data'),
            description=_(u'IMSVDEXVocabulary_description_vdex', 
                            default=u'upload the IMS Vocabulary Definition Format '
                            'compliant XML file into this text field.'),
            allow_file_upload = True,
        ),
        default_output_type = "text/plain",
        default_content_type = "text/xml"
    ),
    BooleanField(
        name = 'showTermPath',
        default = True,
        widget = BooleanWidget(
            label=_(u'label_showTermPath', default=u'Show Term Path'),
            visible = {'view': 'visible', 'edit': 'visible'},
        ),
    ),
    BooleanField(
        name = 'showLeafsOnly',
        default = True,
        widget = BooleanWidget(
            label=_(u'label_showLeafsOnly', default=u'Show Leafs Only'),
            visible = {'view': 'visible', 'edit': 'visible'},
        ),
    ),
))

class IMSVDEXVocabulary(BaseContent):
    """Content type for handling of VDEX compliant vocabulary.
    """
    implements(IVocabulary)
    security = ClassSecurityInfo()
    meta_type = 'VdexFileVocabulary'
    schema = BaseSchema.copy() + IMSVDEXVocabularySchema.copy()

    security.declareProtected(permissions.View, 'Title')
    def Title(self):
        """return the title of the given vdex file"""
        manager = self._getManager()
        if manager is None:
            return 'No or corrupt file uploaded.'
        return manager.getVocabName()

    security.declareProtected(permissions.View, 'Title')
    def Description(self):
        """the description gives information about the state of the vdex"""
        manager = self._getManager(reset=True, returnerror=True)
        if type(manager) in StringTypes:
            return manager
        return manager.getVocabName()

    security.declareProtected(permissions.View, 'getDisplayList')
    def getDisplayList(self, instance):
        """ returns an object of class DisplayList as defined in
            Products.Archetypes.utils

            The instance of the content class is given as parameter.
        """
        dl = DisplayList()
        tree = self.getVocabularyDict(instance)
                        
        def build_display_list(current, valueparent):
            for key in current:
                value, part = current[key]
                if valueparent and self.getShowTermPath():
                    value = '%s &rarr; %s' % (valueparent, value)
                leafs_only = self.getShowLeafsOnly()
                is_leaf = part is None
                if (is_leaf and leafs_only) or (not leafs_only):
                    dl.add(key, value)
                build_display_list(part or {}, value)

        build_display_list(tree, None)
        return dl

    def getVocabularyDict(self, instance):
        """ returns the vocabulary as a dictionary with a string key and a
            string value. If it is not a flat vocabulary, the value is a
            tuple with a string and a sub-dictionary with the same format
            (or None if its a leave).

            Example for a flat vocabulary-dictionary:
            {'key1':'Value 1', 'key2':'Value 2'}

            Example for a hierachical:
            {'key1':('Value 1',{'key1.1':('Value 1.1',None)}), 'key2':('Value 2',None)}

            The instance of the content is given as parameter.
        """
        vtool = getToolByName(self, 'portal_vocabularies')
        vdict = vtool.cachedVocabularyDict(self)
        if vdict is not None:
            return vdict
        manager = self._getManager()
        if manager is None:
            return {self.getId(): 'no or corrupt vocabulary with name %s' % \
                                    self.getId()}
        vdict = manager.getVocabularyDict(lang=self._getLanguage())
        vtool.cacheVocabularyDict(self, vdict)
        return vdict

    def getTermByKey(self, key):
        """ returns a term object implementing IVocabularyTerm
            The instance of the content is given as parameter.
        """
        manager = self._getManager()
        if manager is None:
            return ''
        return manager.getTermCaptionById(key, lang=self._getLanguage())

    security.declareProtected(permissions.View, 'isFlat')
    def isFlat(self):
        """ returns true if the underlying vocabulary is flat, otherwise
            if its hierachical (tree-like) it returns false.
        """
        manager = self._getManager()
        if manager is None:
            return -1
        return manager.isFlat()

    security.declareProtected(permissions.View, 'showLeafsOnly')
    def showLeafsOnly(self):
        """ returns true for flat vocabularies. In hierachical (tree-like)
            vocabularies it defines if only leafs should be displayed/selectable,
            or knots and leafs.
        """
        # not provided by vdex - or better: depends on type
        return False

    security.declarePrivate('_getManager')
    def _getManager(self, reset=False, returnerror=False):
        """takes the given file and returns an initialized VDEXManager."""
        if reset and hasattr(self, '_v_vdexmanager'):
            del self._v_vdexmanager
        manager = getattr(self, '_v_vdexmanager', None)
        if manager is not None:
            return manager
        field = self.getField('vdex')
        data = field.getRaw(self)
        lang = self._getLanguage()
        try:
            manager = VDEXManager(str(data), lang='en', fallback=True)
        except VDEXError, e:
            if not returnerror:
                return None
            return str(e)
        self._v_manager = manager
        return manager

    security.declarePrivate('_getLanguage')
    def _getLanguage(self):
        """determine language"""
        plt = getToolByName(self, 'portal_languages', None)
        if plt is not None:
            # if we have PLT take it to vary the language
            lang = plt.getPreferredLanguage()
        else:
            # try to get it from PTS
            accepted = getLangPrefs(self.REQUEST)
            if len(accepted) > 0:
                lang = accepted[0]
            else:
                # bummer, it cant determine a language
                lang = 'neutral'
        return lang and lang[:2] or None

    def SearchableText(self):
        """dont find in live-search"""
        return ''

    security.declareProtected(permissions.ModifyPortalContent,
                              'importXMLBinding')
    def importXMLBinding(self, data):
        """
        imports IMS VDEX compliant XML (BBB)
        """
        self.setVdex(data)
        self.reindexObject()

registerType(IMSVDEXVocabulary, PROJECTNAME)
registerVocabularyContainer(IMSVDEXVocabulary)
