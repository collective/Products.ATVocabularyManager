#
# Skeleton PloneTestCase
#

import common
import doctest
from Products.PloneTestCase import PloneTestCase
from Products.ATVocabularyManager import NamedVocabulary


class TestNamedVocabulary(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        common.installWithinPortal(self.portal)
        self.atvm = common.getATVM(self.portal)
        self.loginAsPortalOwner()

    def setupSimpleVocabularyContainer(self):
        self.vname = 'svtest'
        self.atvm.invokeFactory('SimpleVocabulary', self.vname)
        self.atvm.svtest.setTitle('Test Vocabulary')

    def setupSimpleVocabulary(self):
        self.setupSimpleVocabularyContainer()
        svtest = self.atvm.svtest
        for k, v in [('t%s' % x, 'T %s' % x) for x in range(1,6)]:
            svtest.addTerm(k, v)

    def testNamedVocab(self):
        self.setupSimpleVocabulary()
        svtest = self.atvm.svtest
        nv = NamedVocabulary(self.vname)
        # vocabs are the same
        self.assertEqual(nv.getVocabulary(self.atvm), svtest)
        vocab = svtest.getVocabularyDict()
        # dict vocab are the same
        self.assertEqual(nv.getVocabularyDict(self.atvm), vocab)
        # 5 items in place
        self.assertEqual(len(svtest), len(nv.getVocabulary(self.atvm)), 5)
        # in display list too
        self.assertEqual(len(nv.getDisplayList(self.atvm)), 5)

        # let's test `empty_first_item` option
        nv1 = NamedVocabulary(self.vname, empty_first_item=1)
        # vocab are still the same
        self.assertEqual(nv1.getVocabulary(self.atvm), svtest)
        # 5 items in place
        self.assertEqual(len(nv1.getVocabulary(self.atvm)), 5)
        # but 6 items in display list
        dlist = nv1.getDisplayList(self.atvm)
        self.assertEqual(len(dlist), 6)
        # and we have an empty item on top
        empty_item = (u'', u'--')
        self.failUnless(empty_item in dlist.items())
        self.assertEqual(empty_item, dlist.items()[0])

        # now use a `custom_empty_first_item`
        custom_item = (u'foo', u'Foo')
        nv2 = NamedVocabulary(self.vname,
                              empty_first_item=1,
                              custom_empty_first_item=[custom_item])
        # vocab are still the same
        self.assertEqual(nv2.getVocabulary(self.atvm), svtest)
        # 5 items in place
        self.assertEqual(len(nv2.getVocabulary(self.atvm)), 5)
        # but 6 items in display list
        dlist = nv2.getDisplayList(self.atvm)
        self.assertEqual(len(dlist), 6)
        # and we have an empty item on top
        self.failUnless(custom_item in dlist.items())
        self.assertEqual(custom_item, dlist.items()[0])


def test_suite():
    from unittest import TestSuite, makeSuite
    optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

    suite = TestSuite()
    suite.addTest(makeSuite(TestNamedVocabulary))

    return suite

#EOF
