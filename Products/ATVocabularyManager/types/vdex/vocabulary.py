# File: vocabulary.py
"""
provide a VDEX compliant vocabulary
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

from StringIO import StringIO
from types import StringTypes
from xml.dom import minidom
from xml.dom.domreg import getDOMImplementation
import transaction
from AccessControl import ClassSecurityInfo
from Products.CMFCore  import permissions
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces.vocabulary import IVocabulary
from Products.Archetypes.utils import OrderedDict
from Products.ATVocabularyManager.tools.vocabularylib import registerVocabularyContainer
from Products.ATVocabularyManager.types.vdex.schemata import vocabulary_schema as schema
from Products.ATVocabularyManager.utils import xml
from Products.ATVocabularyManager.utils import text
from Products.ATVocabularyManager.config import *


class VdexTermHandlerMixin:
    """ abstract mixin class provides methods to handle terms on parent class.
    """

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
        vdict = OrderedDict()
        # phew, ugly, anyway, its gets cached.
        for obj in self.contentValues():
            if obj.meta_type == "VdexTerm":
                vsubdict=obj.getVocabularyDict(instance)
                vdict[obj.getTermKey()] = ( \
                    obj.getTermValue(),
                    vsubdict
                )
        vtool.cacheVocabularyDict(self, vdict)
        return vdict

    def createTerm(self, key, **kwargs):
        """ creates a new empty term obj, append it to the vocabulary and
            returns the object.
            a argument 'title' might be given
        """
        id = "term.%s" % text.convertStringToId(key)
        print "create vdex term %s" % id
        self.invokeFactory('VdexTerm',id)
        term=self[id]
        term.setIdentifier(key)
        if 'title' in kwargs.keys():
            term.setTitle(kwargs['title'])
        return term

    def getTermByKey(self, key):
        """ returns a term object implementing IVocabularyTerm
            The instance of the content is given as parameter.
        """
        #XXX: Dont use this one please.
        # suboptimal, needs a catalog query here -> future task
        for term in self.contentValues():
            if term.meta_type=='VdexTerm' and term.getTermKey() == key:
                return term
        return None

    def SearchableText(self):
        return ''


class VdexVocabulary(OrderedBaseFolder,BaseContent,VdexTermHandlerMixin):
    """ content type providing a VDEX compliant vocabulary """

    __implements__ = getattr(OrderedBaseFolder,'__implements__',()) + (IVocabulary,)

    security = ClassSecurityInfo()
    portal_type = meta_type = 'VdexVocabulary'
    archetype_name          = 'IMS VDEX Vocabulary'
    allowed_content_types   = ['VdexTerm', 'VdexRelationEndPoint','VdexLangstring']
    allow_discussion        = False
    immediate_view          = 'base_edit'
    global_allow            = False
    filter_content_type     = True

    # magic to make FTP/WebDAV regognize this as a XML-Document, not a folder.
    PUT = BaseContent.PUT
    manage_FTPget = BaseContentMixin.manage_FTPget
    manage_FTPstat= BaseContentMixin.manage_FTPstat

    schema = schema

    actions                 =  (
           {'action':      'string:$object_url/download',
            'category':    'object',
            'id':          'download',
            'name':        'Download',
            'permissions': ('Manage Portal',),
            'condition'  : 'python:True'},
     )

    aliases = { 
        '(Default)' : 'base_view', 
        'view' : 'base_view', 
        'edit' : 'base_edit', 
    }
    
    security.declareProtected(permissions.View, 'getDisplayList')
    def getDisplayList(self, instance):
        """ returns an object of class DisplayList as defined in
            Products.Archetypes.utils

            The instance of the content class is given as parameter.
        """
        dl = DisplayList()
        self._appendToDisplayList(dl, self.getVocabularyDict(instance), None)
        return dl

    security.declarePrivate('_appendToDisplayList')
    def _appendToDisplayList(self, displaylist, vdict, valueparent):
        """ append subtree to flat display list
        """
        for key in vdict.keys():
            if type(vdict[key]) == type((1,2)):
                value  = vdict[key][0]
                subdict= vdict[key][1] or None
            else:
                value  = vdict[key]
                subdict= None
            if valueparent:
                value = '%s - %s' % (valueparent, value)
            if (not self.showLeafsOnly()) or (not subdict):
                displaylist.add(key,value)
            if subdict:
                self._appendToDisplayList(displaylist,subdict,value)


    security.declareProtected(permissions.View, 'isFlat')
    def isFlat(self):
        """ returns true if the underlying vocabulary is flat, otherwise
            if its hierachical (tree-like) it returns false.
        """
        if self.getProfileType() in ['flatTokenTerms',]:
            return True
        # suboptimal, needs something more intelligent ...
        for obj in self.contentValues(filter={'meta_type':'VdexTerm'}):
            if len(obj.contentIds(filter={'meta_type':'VdexTerm'}))>0:
                return False
        return True


    security.declareProtected(permissions.View, 'showLeafsOnly')
    def showLeafsOnly(self):
        """ returns true for flat vocabularies. In hierachical (tree-like)
            vocabularies it defines if only leafs should be displayed/selectable,
            or knots and leafs.
        """

        pass

    security.declareProtected(permissions.View, 'Title')
    def Title(self):
        """ returns langstring of default language or first available """
        lang = self.getDefaultLanguage()
        langstring=None
        if lang:
            try:
                langstring=self[lang].Title()
            except:
                pass
        if not langstring:
            langstringids=self.objectIds()
            if langstringids:
                langstring=self[langstringids[0]].Title()
            else:
                langstring='(not available)'

        return langstring

    security.declareProtected(permissions.ModifyPortalContent, 'setTitle')
    def setTitle(self,title,lang=None):
        """ set title as langstring """
        lang = lang or 'default'
        self.invokeFactory('VdexLangstring', lang)
        self[lang].setTitle(title)
        self[lang].reindexObject()


    security.declareProtected(permissions.View, 'exportXMLBinding')
    def exportXMLBinding(self, sio=StringIO(), newl=VDEX_EXPORT_NEWL, addindent=VDEX_EXPORT_INDENT):
        """
        exports whole vocabulary as IMS VDEX compliant XML
        """

        # prepare minidom
        minidom =getDOMImplementation('minidom')
        doc=minidom.createDocument('', 'vdex', '')

        # build vdex base
        elroot = xml.getChildrenByTagName(doc,'vdex')[0]

        # attributes on base
        xml.setAttr(doc,elroot,'profileType',self.getProfileType())
        xml.setAttr(doc,elroot,'xmlns',
                    'http://www.imsglobal.org/xsd/imsvdex_v1p0')
        if self.getOrderSignificant():
            xml.setAttr(doc,elroot,'orderSignificant',self.getOrderSignificant())
        if self.getRegistrationStatus():
            xml.setAttr(doc,elroot,'isRegistered',self.getRegistrationStatus())
        if self.getDefaultLanguage():
            xml.setAttr(doc,elroot,'language',self.getDefaultLanguage())

        # node id
        xml.appendText(doc,elroot,'vocabIdentifier',self.getVocabularyIdentifier() or self.absolute_url())

        # node name with langstring
        elname=xml.appendNode(doc,elroot,'vocabName')
        for langstring in self.contentValues():
            if langstring.meta_type == "VdexLangstring":
                langnode=langstring.getDOMBindingNode(doc)
                elname.appendChild(langnode)

        # all term node
        for term in self.contentValues():
            if term.meta_type == "VdexTerm":
                node=term.getDOMBindingNode(doc)
                elroot.appendChild(node)

        # all realtionship nodes
        for rel in self.contentValues():
            if rel.meta_type == "VdexRelationship":
                node=rel.getDOMBindingNode(doc)
                elroot.appendChild(node)

        doc.writexml(sio, newl='\n', addindent='\t')
        return sio


    security.declareProtected(permissions.ModifyPortalContent,
                              'importXMLBinding')
    def importXMLBinding(self, data):
        """
        imports IMS VDEX compliant XML
        """

        # clean the house
        #self.manage_delObjects(self.objectIds())

        # build a minidom from data
        #data=data.decode('latin-1')
        doc=minidom.parseString(data)
        elroot = xml.getChildrenByTagName(doc,'vdex')[0]

        # set values from attributes
        self.setProfileType(elroot.getAttribute('profileType'))
        value=elroot.getAttribute('orderSignificant')
        if value is not None:
            self.setOrderSignificant(value)
        value=elroot.getAttribute('language')
        if value:
            self.setDefaultLanguage(value)
        value=elroot.getAttribute('isRegistered')
        if value:
            self.setRegistrationStatus(value)

        # set identifier
        idnodes=xml.getChildrenByTagName(elroot,'vocabIdentifier')
        if idnodes:
            self.setVocabularyIdentifier(xml.getData(idnodes[0]))

        # set name(s)
        namenodes=xml.getChildrenByTagName(elroot,'vocabName')
        if namenodes:
            for langstringnode in xml.getChildrenByTagName(namenodes[0],'langstring'):
                lang=langstringnode.getAttribute('language') or None
                value=xml.getData(langstringnode)
                self.setTitle(value,lang=lang)

        # update portal_catalog indexes with the full vocabulary information
        self.reindexObject()

        # add terms
        reindexqueue = []
        for termnode in xml.getChildrenByTagName(elroot,'term'):
            key = xml.getData(xml.getChildrenByTagName(termnode,'termIdentifier')[0])
            term=self.createTerm(key)
            term.setDOMBindingNode(doc,termnode)
            reindexqueue.append(term.getId())
        print "reindex new terms"
        for key in reindexqueue:            
            self[key].reindexObject()
        print "set savepoint"
        sp = transaction.savepoint(optimistic=True)


    security.declareProtected(permissions.View, 'download')
    def download(self, REQUEST, RESPONSE):
        """ response with the xml-file """
        filename = self.getId()
        if filename:
            if not filename.endswith('.xml'):
                filename+='.xml'
            RESPONSE.setHeader('Content-Disposition',
                               'attachment; filename=%s' % filename)
        xmldata = StringIO()
        newl  = self.REQUEST.get('newline', VDEX_EXPORT_NEWL)
        indent= self.REQUEST.get('indent', VDEX_EXPORT_INDENT)

        xmldata = self.exportXMLBinding(xmldata,newl,indent)
        RESPONSE.setHeader('Content-Type', 'text/xml')
        RESPONSE.setHeader('Content-Length', len(xmldata.getvalue()))
        RESPONSE.write(xmldata.getvalue())
        return ''


registerType(VdexVocabulary)
registerVocabularyContainer(VdexVocabulary)
