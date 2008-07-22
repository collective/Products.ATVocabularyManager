import unittest
import os

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

from Products.ATVocabularyManager.tests import PACKAGE_HOME

import common

VOCABTITLE = 'Test Vdex Vocabulary'

class TestVdexVocabulary(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        common.installWithinPortal(self.portal)
        self.atvm = common.getATVM(self.portal)

    def setupVdexVocabularyContainer(self):
        self.loginAsPortalOwner()
        self.atvm.invokeFactory('VdexVocabulary','vdextest')
        self.atvm.vdextest.setTitle(VOCABTITLE)


    def setupVdexVocabulary(self):
        self.setupVdexVocabularyContainer()
        self.atvm.vdextest.invokeFactory('VdexTerm', 'key1')
        self.atvm.vdextest.key1.setTitle('Value 1')
        self.logout()

    def testGetVocabularyByName(self):
        # Test if vocab can be fetched
        self.setupVdexVocabulary()
        vdextest = self.atvm.getVocabularyByName('vdextest')
        self.failUnlessEqual(vdextest.Title(),VOCABTITLE)

    def testAddTerm(self):
        self.setupVdexVocabularyContainer()
        vdextest = self.atvm.vdextest
        vdextest.createTerm('foo',title='bar')
        self.failUnlessEqual(vdextest.getTermByKey('foo').getTermValue(), 'bar')

    def testGetVocabularyDict(self):
        pass

    def testGetDisplayList(self):
        pass

    def testIsFlat(self):
        pass

    def testShowLeafsOnly(self):
        pass

    def testGetXMLBinding(self):
        self.setupVdexVocabularyContainer()
        vdextest = self.atvm.vdextest
        vdextest.createTerm('foo',title='bar')
        vdextest.createTerm('abc',title='123')

        sio = vdextest.exportXMLBinding()
        # XXX: untested dump
        #print sio.getvalue()

    def testSetXMLBinding(self):
        xmlfilepath = os.path.join(PACKAGE_HOME, "data", "farben.xml")
        xmlfile = open(xmlfilepath, 'r')
        data = xmlfile.read()
        self.setupVdexVocabularyContainer()
        vdextest = self.atvm.vdextest
        vdextest.importXMLBinding(data)
        sio = vdextest.exportXMLBinding()
        # XXX: untested dump
        #print sio.getvalue()



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestVdexVocabulary))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
