# -*- coding: utf-8 -*-

__author__ = """Harald Friessnegger <harald at webmeisterei(dot) com>"""
__docformat__ = 'plaintext'

import doctest
from Products.PloneTestCase import PloneTestCase
import common


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

    scriptTests = [
        'tool.txt',
        'search_treevocabulary.txt',
    ]

    for test in scriptTests:
        suites.append(ZopeDocFileSuite(
            test,
            optionflags=optionflags,
            package='Products.ATVocabularyManager.doc',
            test_class=TestSearchTreeVocabulary,
        ))
    return TestSuite(suites)

#EOF
