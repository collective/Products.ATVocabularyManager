"""
    CMFPlone functional doctests.  This module collects all *.txt
    files in the tests directory and runs them.

    See also ``test_doctests.py``.

"""

import glob
import os
import sys
import unittest

from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
from Products.PloneTestCase import PloneTestCase
from Products.ATVocabularyManager.tests import PACKAGE_HOME

REQUIRE_TESTBROWSER = []

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

# FIXME: the following two import lines were causing lots of tests to fail.
# Installation of atvm is now done in class TestFunctional (like in
# test_searchTreeVocabulary).
#PloneTestCase.installProduct('ATVocabularyManager')
#PloneTestCase.setupPloneSite(products=['ATVocabularyManager'])

# Using module common to install products and create plone site
import common


class TestFunctional(PloneTestCase.PloneTestCase):
    """
    """
    # class to be used as `test_class` in Suite initialization.

    def afterSetUp(self):
        """installs dependencies and defines atvm
        """
        common.installWithinPortal(self.portal)
        self.atvm = common.getATVM(self.portal)
        self.loginAsPortalOwner()


def list_doctests():
    return [filename for filename in
            glob.glob(os.path.sep.join([PACKAGE_HOME, '*.txt']))]


def list_nontestbrowser_tests():
    return [filename for filename in list_doctests()
            if os.path.basename(filename) not in REQUIRE_TESTBROWSER]


def test_suite():
    # BBB: We can obviously remove this when testbrowser is Plone
    #      mainstream, read: with Five 1.4.
    try:
        import Products.Five.testbrowser
    except ImportError:
        print >> sys.stderr, ("testbrowser not found; "
                              "testbrowser tests skipped")
        filenames = list_nontestbrowser_tests()
    else:
        filenames = list_doctests()

    suites = [Suite(os.path.basename(filename),
               optionflags=OPTIONFLAGS,
               package='Products.ATVocabularyManager.tests',
               test_class=TestFunctional)
              for filename in filenames]

    # BBB: Fix for http://zope.org/Collectors/Zope/2178
    from Products.PloneTestCase import layer
    from Products.PloneTestCase import setup

    if setup.USELAYER:
        for s in suites:
            if not hasattr(s, 'layer'):
                s.layer = layer.PloneSite

    return unittest.TestSuite(suites)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
