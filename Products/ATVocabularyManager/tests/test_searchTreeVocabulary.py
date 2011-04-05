# -*- coding: utf-8 -*-

__author__ = """Harald Friessnegger <harald at webmeisterei(dot) com>"""
__docformat__ = 'plaintext'


import unittest

from zope.testing import doctest
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

#from Products.CMFCore.utils import getToolByName

import common

from Products.ATVocabularyManager import doc


class TestSearchTreeVocabulary(PloneTestCase.PloneTestCase):
    """
    """

    def afterSetUp(self):
        """installs dependencies and defines atvm
        """
        common.installWithinPortal(self.portal)
        self.atvm = common.getATVM(self.portal)
        self.loginAsPortalOwner()


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS
    suites = []

    scriptTests = ['search_treevocabulary.txt',
                   ]


    for test in scriptTests:
        suites.append(ZopeDocFileSuite(test,
                                         optionflags=optionflags,
                                         package='Products.ATVocabularyManager.doc',
                                         test_class=TestSearchTreeVocabulary,
                                         ))
    return TestSuite(suites)


##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
