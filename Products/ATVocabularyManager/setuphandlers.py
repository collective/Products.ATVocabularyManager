from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_TITLE


def importVarious(self):

    if self.readDataFile('atvocabularymanager.txt') is None:
        return

    site = self.getSite()
    catalog = getToolByName(site, 'uid_catalog')

    idxName = 'getTermKeyPath'

    if idxName not in catalog.schema():
        catalog.addColumn(idxName)

    if idxName not in catalog.indexes():
        catalog.addIndex(idxName, 'KeywordIndex')

    vtool = getToolByName(site, 'portal_vocabularies')
    vtool.title = TOOL_TITLE
    # remove from portal_catalog
    vtool.unindexObject()
