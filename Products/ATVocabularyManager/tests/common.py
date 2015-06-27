from plone.app.testing import bbb
from plone.app.testing import FunctionalTesting, applyProfile
from Products.GenericSetup import EXTENSION, profile_registry
from Products.ATVocabularyManager.config import PROJECTNAME, TOOL_NAME
from plone.testing import z2


class ATTestCaseFixture(bbb.PloneTestCaseFixture):

    defaultBases = (bbb.PTC_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load i18n fallback domain
        import Products.ATVocabularyManager
        self.loadZCML("configure.zcml", package=Products.ATVocabularyManager)
        z2.installProduct(app, 'Products.ATVocabularyManager')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.ATVocabularyManager:default')

AT_FIXTURE = ATTestCaseFixture()
AT_FUNCTIONAL_TESTING = FunctionalTesting(bases=(AT_FIXTURE,),
                                          name='ATVocabularyManager:Functional')

class ATVocTestCase(bbb.PloneTestCase):
    """ Simple ATVocabularyManager test case
    """

    layer = AT_FUNCTIONAL_TESTING

def x_installWithinPortal(portal):
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.installProduct(PROJECTNAME)


def x_getATVM(portal):
    return portal[TOOL_NAME]
