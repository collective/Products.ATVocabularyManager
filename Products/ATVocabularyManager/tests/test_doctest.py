# -*- coding: utf-8 -*-

__author__ = """Harald Friessnegger <harald at webmeisterei(dot) com>"""
__docformat__ = 'plaintext'

import doctest
from Products.ATVocabularyManager.tests.common import AT_FUNCTIONAL_TESTING
from Products.ATVocabularyManager.tests.common import createTestVocabulary
from plone.testing import layered


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS
    suites = []

    scriptTests = [
        'search_treevocabulary.txt',
        'simplevocabulary.txt',
    ]

    for test in scriptTests:
        suites.append(layered(doctest.DocFileSuite(
            test,
            optionflags=optionflags,
            globs={'createTestVocabulary': createTestVocabulary},
            package='Products.ATVocabularyManager.doc',
        ), layer=AT_FUNCTIONAL_TESTING))
    return TestSuite(suites)

#EOF
