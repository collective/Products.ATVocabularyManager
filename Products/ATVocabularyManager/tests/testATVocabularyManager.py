#
# Test for TreeVocabulary
#
from time import sleep

from Products.ATVocabularyManager.config import PROJECTNAME
from Products.ATVocabularyManager.tests.common import ATVocTestCase
from Products.CMFCore.utils import getToolByName
from plone import api


class TestATVocabularyManager(ATVocTestCase):

    def afterSetUp(self):
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')

    def test_install(self):
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME))

    def test_vocabulariesDeletedAtUninstall(self):
        """the tool and all the vocabularies get deleted
        at product uninstall.
        """

        self.loginAsPortalOwner()

        #create some vocabulary
        atvm = api.portal.get_tool(name='portal_vocabularies')
        atvm.invokeFactory('SimpleVocabulary', 'foo')
        vocab = atvm.getVocabularyByName('foo')
        vocab.invokeFactory('SimpleVocabularyTerm', 'bar', title='Some test')

        #uninstall the product
        self.qi.uninstallProducts([PROJECTNAME, ])
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))

        #see if tool hidden
        # XXX CMFQuickInstallerTool 3.0.3 does not delete the portal items any
        # any longer if Folderish. Asked eleddy and jens what they think about
        # the implications here(feature/bug) [do3cc]
        #self.assertRaises(AttributeError, getToolByName,
        #                  self.portal, 'portal_vocabularies')

        #install the product again
        sleep(1)
        self.qi.installProduct(PROJECTNAME)
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME))

        #all vocabs are gone!
        atvm = getToolByName(self.portal, 'portal_vocabularies')
        foo = atvm.getVocabularyByName('foo')
        # see the XXX about CMFQuickInstallerTool above
        #self.failUnless(foo is None)

    def test_zexpOfVocabulariesAtUninstall(self):
        """vocabulariees get deleted together with the tool at product
        uninstallation.

        as a kind of safetybelt a zexp of all vocabularies gets created
        when atvm gets uninstalled (in case this was done by accident)
        """

        #XXX add a test for this here and patch Extensions/Install.py

    def test_vocabulariesPreservedAtReinstall(self):
        """the tool and all the vocabularies are preserved when
        reinstalling the product.
        """

        self.loginAsPortalOwner()

        #create some vocabulary
        atvm = getToolByName(self.portal, 'portal_vocabularies')
        atvm.invokeFactory('SimpleVocabulary', 'foo')
        vocab = atvm.getVocabularyByName('foo')
        vocab.invokeFactory('SimpleVocabularyTerm', 'bar', title='Some test')

        #reinstall the product
        sleep(1)
        self.qi.reinstallProducts([PROJECTNAME, ])

        #the tool and the vocabularies are still there
        atvm = getToolByName(self.portal, 'portal_vocabularies')

        foo = atvm.getVocabularyByName('foo')
        self.failIf(foo is None)
        self.failIf(foo.bar is None)
        self.assertEqual(foo.bar.Title(), 'Some test')

#EOF
