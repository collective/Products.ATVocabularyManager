from plone.app.testing import bbb
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.testing import FunctionalTesting, applyProfile
from Products.GenericSetup import EXTENSION, profile_registry
from Products.ATVocabularyManager.config import PROJECTNAME, TOOL_NAME
from plone.testing import z2
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
from plone import api


try:
    import Products.LinguaPlone
    HAS_LP = True
except ImportError:
    HAS_LP = False

class ATTestCaseFixture(bbb.PloneTestCaseFixture):

    defaultBases = (bbb.PTC_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load i18n fallback domain
        import Products.ATVocabularyManager
        self.loadZCML("configure.zcml", package=Products.ATVocabularyManager)
        z2.installProduct(app, 'Products.ATVocabularyManager')
        if HAS_LP:
	    import Products.LinguaPlone
            self.loadZCML("configure.zcml", package=Products.LinguaPlone)
            z2.installProduct(app, 'Products.LinguaPlone')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.ATVocabularyManager:default')
        if HAS_LP:
            applyProfile(portal, 'Products.LinguaPlone:LinguaPlone')

AT_FIXTURE = ATTestCaseFixture()
AT_FUNCTIONAL_TESTING = FunctionalTesting(bases=(AT_FIXTURE,),
                                          name='ATVocabularyManager:Functional')


def createTestVocabulary(atvm, testvocabs=None):
    """creates a simplevocabulary for testing purposes
    using the utlity methods provided by atvocabularymanager
    """

    portal = api.portal.get()
    setRoles(portal, TEST_USER_ID, ['Manager'])
    testvocabs = {'teststates': (
	('aut', u'Austria'),
	('ger', u'Germany'),
	('nor', u'Norway'),
	('fin', u'Finland'))}

    createSimpleVocabs(atvm, testvocabs)

class ATVocTestCase(bbb.PloneTestCase):
    """ Simple ATVocabularyManager test case
    """

    layer = AT_FUNCTIONAL_TESTING

    def _createTestVocabulary(self):
        createTestVocabulary(self.atvm)
