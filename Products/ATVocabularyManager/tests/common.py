from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

import Products.ATVocabularyManager

from Products.ATVocabularyManager.config import *

from Products.Five import zcml
from Products.Five import fiveconfigure

#from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName


@onsetup
def installProducts():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.ATVocabularyManager)
    fiveconfigure.debug_mode = False

PloneTestCase.setupPloneSite(id='plone')
installProducts()
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('PortalTransforms')
# to support tests for translated vocabularies
ZopeTestCase.installProduct('PloneLanguageTool')
ZopeTestCase.installProduct('LinguaPlone')
ZopeTestCase.installProduct(PROJECTNAME)


def installWithinPortal(portal):
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.installProduct(PROJECTNAME)


def getATVM(portal):
    return portal[TOOL_NAME]
