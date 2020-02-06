# File: vocabularylib.py
"""\
This tool contains dynamic vocabularies to be used by Archetypes fields. It has
methods to register special/custom vocabulary types
"""
# Copyright (c) 2004-2007 by BlueDynamics Alliance,  Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'


from zope.interface import implements
from AccessControl import ClassSecurityInfo
from OFS.Cache import Cacheable
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from Products.Archetypes.atapi import *

from Products.ATVocabularyManager.config import TOOL_NAME
from Products.ATVocabularyManager.config import TOOL_TITLE
from Products.ATVocabularyManager.config import PROJECTNAME
from Products.ATVocabularyManager.interfaces import IATVocabularyLibrary
from Products.Archetypes.utils import shasattr

try:
    from Products.PlacelessTranslationService.Negotiator import getLangPrefs
except:
    from plone.i18n.negotiate.ptsnegotiator import getLangPrefs


### note: derive somewhere in future from BaseTool
class VocabularyLibrary(UniqueObject, OrderedBaseFolder, Cacheable):
    '''
    This tool contains dynamic vocabularies to be used by Archetypes
    fields. It has methods to register special/custom vocabulary
    types
    '''
    implements(IATVocabularyLibrary)

    security = ClassSecurityInfo()
    meta_type = 'VocabularyLibrary'

    id_field = OrderedBaseFolderSchema['id'].copy()
    id_field.mode = 'r'
    title_field = OrderedBaseFolderSchema['title'].copy()
    title_field.mode = 'r'

    manage_options = OrderedBaseFolder.manage_options + Cacheable.manage_options

    schema = OrderedBaseFolderSchema + Schema((
        # a tool doesnt need an idwidget and title for edit
        id_field,
        title_field,
    ),
    )

    def __init__(self, id='ignored'):
        OrderedBaseFolder.__init__(self, TOOL_NAME)
        self.setTitle(TOOL_TITLE)

    # caches
    security.declarePrivate('cachedVocabularyDict')
    def cachedVocabularyDict(self, vocab):
        """fetches vocabulary form cache if present, else return None."""
        view_name = self.getId() + '-vocabdicts'
        keywords = self._makeCacheKeywords(vocab)
        cached = self.ZCacheable_get(view_name=view_name,
                                     keywords=keywords,
                                     default=None)
        return cached

    security.declarePrivate('cacheVocabularyDict')
    def cacheVocabularyDict(self, vocab, vdict):
        """fetches vocabulary form cache if present, else return None."""
        view_name = self.getId() + '-vocabdicts'
        keywords = self._makeCacheKeywords(vocab)
        self.ZCacheable_set(vdict, view_name=view_name, keywords=keywords)

    def _makeCacheKeywords(self, vocab):
        """returns a key for use in the cache."""
        key = {}
        key['uid'] = vocab.UID()

        plt = getToolByName(self, 'portal_languages', None)
        if plt is not None:
            # if we have PLT take it to vary the language
            lang = plt.getPreferredLanguage()
            key['lang'] = lang
        else:
            # try to get it from PTS
            accepted = getLangPrefs(self.REQUEST)
            if len(accepted) > 0:
                key['lang'] = accepted[0]
            else:
                # bummer, it cant determine a language
                key['lang'] = 'neutral'
        return key


    #Methods
    def getVocabularyByName(self, vocabname):
        """ returns a vocabulary or None if no vocab with this name found """
        if shasattr(self, vocabname):
            return self[vocabname]
        #print "no vocabulary named %s" % vocabname
        return None

    security.declareProtected(ModifyPortalContent, 'PUT')
    def PUT(self, ids=[], REQUEST=None):
        print "PUT in basefolder.py"
        OrderedBaseFolder.PUT(self, ids, REQUEST)

    security.declarePrivate('PUT_factory')
    def PUT_factory(self, name, typ, body):
        """ Dispatcher for PUT requests to non-existent IDs.
            Should always use VDEX. Copied from CMFPhotoAlbum.
        """
        import md5
        md5name = md5.md5(name).hexdigest()
        self.invokeFactory('VdexVocabulary', md5name)

        return self[md5name]

    security.declareProtected(View, 'listVocabularies')
    def listVocabularies(self):
        res = {}
        for id in self.contentIds():
            res[id] = self[id].Title()
        return res

    # Tool should not be indexed

    security.declareProtected(ModifyPortalContent, 'indexObject')
    def indexObject(self):
        pass

    security.declareProtected(ModifyPortalContent, 'reindexObjectSecurity')
    def reindexObjectSecurity(self, skip_self=False):
        pass


registerType(VocabularyLibrary, PROJECTNAME)
