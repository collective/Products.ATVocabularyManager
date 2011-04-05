#
# Skeleton PloneTestCase
#

import unittest


#from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

import common
common.installProducts()


class TestSomeProduct(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        pass

    def testSomething(self):
        # Test something
        self.failUnless(1==1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSomeProduct))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
