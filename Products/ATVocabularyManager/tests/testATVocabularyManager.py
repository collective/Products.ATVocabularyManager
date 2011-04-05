#
# Test for TreeVocabulary
#
import unittest
from time import sleep

#from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
#from Products.Five import zcml

import Products.ATVocabularyManager
from Products.ATVocabularyManager.config import *

from Products.CMFCore.utils import getToolByName


import common


class TestATVocabularyManager(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.qi = getToolByName(self.portal, 'portal_quickinstaller')

    def test_install(self):
        # atvm is not installed
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))

        # installing atvm
        self.qi.installProduct(PROJECTNAME)
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME))

    def test_uninstall(self):
        # installing atvm
        self.qi.installProduct(PROJECTNAME)
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME))

        #now uninstall it
        self.qi.uninstallProducts([PROJECTNAME, ])
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))

    def test_reinstall(self):
        # installing atvm
        self.qi.installProduct(PROJECTNAME)
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME))

        sleep(1) # Else the ids are too similar and reinstall will fail. Oh well
        #reinstallProducts
        self.qi.reinstallProducts([PROJECTNAME, ])
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME))

    def test_vocabulariesDeletedAtUninstall(self):
        """the tool and all the vocabularies get deleted
        at product uninstall.
        """

        self.loginAsPortalOwner()

        #install the product
        self.qi.installProduct(PROJECTNAME)

        #create some vocabulary
        atvm = getToolByName(self.portal, 'portal_vocabularies')
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
        #self.assertRaises(AttributeError, getToolByName, self.portal, 'portal_vocabularies')


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
        """vocabulariees get deleted together with the tool at product uninstallation.

        as a kind of safetybelt a zexp of all vocabularies gets created
        when atvm gets uninstalled (in case this was done by accident)
        """

        #XXX add a test for this here and patch Extensions/Install.py

    def test_vocabulariesPreservedAtReinstall(self):
        """the tool and all the vocabularies are preserved when
        reinstalling the product.
        """

        self.loginAsPortalOwner()


        #install the product
        self.qi.installProduct(PROJECTNAME)

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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestATVocabularyManager))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
