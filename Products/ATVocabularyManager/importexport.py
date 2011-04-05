# Copyright (c) 2008 by BlueDynamics Alliance - Klein & Partner KEG, Austria
#
# BSD-like licence, see LICENCE.txt
#
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'
import os
from imsvdex.vdex import VDEXManager
from imsvdex.vdex import VDEXError
from zope.component import adapts
from zExceptions import BadRequest
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.CMFPlone.utils import normalizeString
from interfaces import IATVocabularyLibrary


class ATVMXMLAdapter(XMLAdapterBase):
    adapts(IATVocabularyLibrary, ISetupEnviron)

    name = 'vocabularies'

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeVocabs()
        self._initVocabs(node)
        self._logger.info('ATVocabularyManager library imported.')

    def _purgeVocabs(self):
        ids = self.context.contentIds()
        self.context.manage_delObjects(ids)

    def _initVocabs(self, node):
        for objnode in node.getElementsByTagName('object'):
            filename = objnode.getAttribute('name')
            filepath = os.path.join(self.name, filename)
            data = self.environ.readDataFile(filepath)
            if filename.endswith('.vdex') or filename.endswith('.xml'):
                # VDEX file
                try:
                    vdex = VDEXManager(data)
                except VDEXError, e:
                    self._logger.error('Problem with vdex-file: %s' % filepath)
                    raise
                vocabid = vdex.getVocabIdentifier()
                if not vocabid:
                    vocabid = filename[:filename.rfind('.')]
                vocabname = vocabid
                if vocabname in self.context.objectIds():
                    self.context.manage_delObjects([vocabname])
                try:
                    self._logger.info(
                        'Import VDEX file %s with identifier %s' % \
                        (filename, vocabname))
                    self.context.invokeFactory('VdexFileVocabulary', vocabname)
                except BadRequest, e:
                    self._logger.warning(
                        'Import VDEX file %s with identifier %s renamed as %s' % \
                        (filename, vocabid, vocabname))
                    vocabname = normalizeString(vocabid, context=self.context)
                    if vocabname in self.context.objectIds():
                        self.context.manage_delObjects([vocabname])
                    self.context.invokeFactory('VdexFileVocabulary', vocabname)
                self.context[vocabname].importXMLBinding(data)
            elif filename.endswith('.csv') or filename.endswith('.txt'):
                # CSV file
                self._logger.info('CSV import not yet implemented.')
            else:
                self._logger.info('Unknown File Format.')


def importVocabularies(context):
    """Import vocabularies from an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_vocabularies')
    importObjects(tool, '', context)


def exportVocabularies(context):
    """Export vocabularies as an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_vocabularies')
    if tool is None:
        logger = context.getLogger('atvm')
        logger.info('Nothing to export.')
        return
    exportObjects(tool, '', context)
