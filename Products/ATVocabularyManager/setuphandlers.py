from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple
from plone import api


# handy profile importer taken from plone.app.mosaic
def import_profile(portal, profile_name):
    setup_tool = api.portal.get_tool('portal_setup')
    if not setup_tool.getProfileImportDate(profile_name):
        setup_tool.runAllImportStepsFromProfile(profile_name)

def importVarious(self):
    if self.readDataFile('atvocabularymanager.txt') is None:
        return

    site = self.getSite()
    if getFSVersionTuple()[0] >= 5:   # Plone 5
        import_profile(site, 'profile-Products.ATContentTypes:base')

    catalog = getToolByName(site, 'uid_catalog')

    idxName = 'getTermKeyPath'

    if idxName not in catalog.schema():
        catalog.addColumn(idxName)

    if idxName not in catalog.indexes():
        catalog.addIndex(idxName, 'KeywordIndex')

