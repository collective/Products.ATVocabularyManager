# File: term.py
"""
VDEX compliant vocabulary term
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
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
try:
    from Products.Archetypes.interfaces.vocabulary import IVocabularyTerm
except ImportError:
    from Products.ATVocabularyManager.backports import IVocabularyTerm    
from Products.ATVocabularyManager.types.vdex.schemata import term_schema as schema
from Products.ATVocabularyManager.types.vdex.vocabulary import VdexTermHandlerMixin
from Products.ATVocabularyManager.utils import xml
from Products.ATVocabularyManager.utils import text

class VdexTerm(OrderedBaseFolder,VdexTermHandlerMixin):
    """ content type representing a VDEX compliant term """

    __implements__ = getattr(OrderedBaseFolder,'__implements__',()) + (IVocabularyTerm,)

    security = ClassSecurityInfo()
    portal_type = meta_type = 'VdexTerm'
    archetype_name          = 'VdexTerm'   #this name appears in the 'add' box
    global_allow            = False
    allowed_content_types   = ['VdexTerm', 'VdexMediaDescriptor','VdexLangstring']
    filter_content_types    = True
    allow_discussion        = False
    #content_icon            = 'VdexTerm.gif'

    schema=schema
    
    aliases = { 
        '(Default)' : 'base_view', 
        'view' : 'base_view', 
        'edit' : 'base_edit', 
    }

    def getCaption(self):
        """
        return language dependend Title
        """
        return self.Title()

    def Title(self, lang='default'):
        """ returns langstring of default language or first available """
        return self._getLangstring('caption', lang)

    def setTitle(self, title, lang='default'):
        """ set title using langstring """
        self._setLangstring(title, 'caption', lang)

    def Description(self, lang='default'):
        """ returns langstring of default language or first available """
        return self._getLangstring('description',lang)

    def setDescription(self, title, lang='default'):
        """ set Description using a langstring """
        self._setLangstring(title, 'description', lang)
        

    def _getLangstring(self, group, lang):
        """ returns langstring of default language or first available """            
        oids = self.objectIds()
        plt = getToolByName(self, 'portal_languages', None)
        # language fallback using plt info
        if plt is not None:
            pref = plt.getPreferredLanguage()
            for lcode in [pref]+plt.getSupportedLanguages():
                id = '%s.%s' % (group, lcode)
                if id in oids:
                    return self[id].Title()
        
        id = '%s.%s' % (group, lang or 'default')
        if id in oids:
            return self[id].Title()
        else:
            objs=self._getLangstrings(group)
            if len(objs) < 1:
                return '(Caption for %s not available)' % self.getTermKey()
            return objs[0].Title()
    

    def _setLangstring(self, s, group, lang='default'):
        if not s:
            return
        id = '%s.%s' % (group,lang)
        if not id in self.contentIds():
            self.invokeFactory('VdexLangstring', id)
        self[id].setTitle(s)
        self[id].reindexObject()

    def _getLangstrings(self, group):
        """ returns langstrings by group """
        res=[]
        for obj in self.objectValues():
            if obj.meta_type=='VdexLangstring':
                s = obj.getId().split('.')
                target = s[0]
                if target == group:
                    res.append(obj)
        return res

    def getTermKey(self):
        """
        returns the Key / Identifier of the term
        """
        return self.getIdentifier()

    def getTermValue(self):
        """
        returns the language dependent value of the term
        """        
        return self.getCaption()

    def getDOMBindingNode(self, doc):
        """
        returns a dom-element containing its and all it subobjects dom
        representation
        """
        node=doc.createElement('term')
        if self.getOrderSignificant():
            xml.setAttr(doc,node,'orderSignificant',self.getOrderSignificant())
        xml.appendText(doc,node,'termIdentifier',self.getTermKey())

        # caption
        langstrings=self._getLangstrings('caption')
        if langstrings:
            captionnode=xml.appendNode(doc,node,'caption')
            for langstring in langstrings:
                langnode=langstring.getDOMBindingNode(doc)
                captionnode.appendChild(langnode)

        # description
        langstrings=self._getLangstrings('description')
        if langstrings:
            descrnode=xml.appendNode(doc,node,'description')
            for langstring in langstrings:
                langnode=langstring.getDOMBindingNode(doc)
                descrnode.appendChild(langnode)

        # all media descriptor nodes
        for media in self.contentValues():
            if media.meta_type == "VdexMediaDescriptor":
                medianode=media.getDOMBindingNode(doc)
                node.appendChild(medianode)

        # all sub term nodes
        for term in self.contentValues():
            if term.meta_type == "VdexTerm":
                termnode=term.getDOMBindingNode(doc)
                node.appendChild(termnode)

        return node

    def setDOMBindingNode(self, doc, node):
        """ sets data on term given by node """
        # set name(s)
        captionnodes=xml.getChildrenByTagName(node,'caption')
        if captionnodes:
            for langstringnode in xml.getChildrenByTagName(captionnodes[0],'langstring'):
                lang=langstringnode.getAttribute('language') or 'default'
                value=xml.getData(langstringnode)
                self.setTitle(value,lang=lang)

        descrnodes=xml.getChildrenByTagName(node,'description')
        if descrnodes:
            for langstringnode in xml.getChildrenByTagName(descrnodes[0],'langstring'):
                lang=langstringnode.getAttribute('language') or 'default'
                value=xml.getData(langstringnode)
                self.setDescription(value,lang=lang)

        # add mediadescriptors
        for medianode in xml.getChildrenByTagName(node,'mediaDescriptor'):
            loc = xml.getData(xml.getChildrenByTagName(medianode,'mediaLocator')[0])
            id="media.%s" % text.text.convertStringToId(loc)
            self.invokeFactory('VdexMediaDescriptor',id)
            self[id].setDOMBindingNode(doc,medianode)

        # add terms
        for termnode in xml.getChildrenByTagName(node,'term'):
            key = xml.getData(xml.getChildrenByTagName(termnode,'termIdentifier')[0])
            term=self.createTerm(key)
            term.setDOMBindingNode(doc,termnode)


registerType(VdexTerm)
