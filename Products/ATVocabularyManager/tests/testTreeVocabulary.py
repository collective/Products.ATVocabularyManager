#
# Test for TreeVocabulary
#
import unittest

from Products.ATVocabularyManager.tests.common import ATVocTestCase
from Products.ATVocabularyManager.tests.common import HAS_LP
from Products.ATVocabularyManager.utils.vocabs import createHierarchicalVocabs
from Products.CMFCore.utils import getToolByName
from plone import api


class TestTreeVocabulary(ATVocTestCase):

    def afterSetUp(self):
        self.atvm = api.portal.get_tool(name='portal_vocabularies')
        self.setRoles(['Manager',])
        self.setupExampleTreeVocabulary()

    def setupExampleTreeVocabulary(self):
        hierarchicalVocabs = {}

        hierarchicalVocabs[('regions', 'Some regions in europe')] = {
            ('aut', 'Austria'): {
                ('tyr', 'Tyrol'): {
                    ('auss', 'Ausserfern'): {},
                }
            },
            ('ger', 'Germany'): {
                ('bav', 'Bavaria'): {}
            },
        }

        createHierarchicalVocabs(self.atvm, hierarchicalVocabs)

    def test_getTermKeyPath(self):
        """Test for the method term.getTermKeyPath.

        We need not test this for translated content
        because getTermKey is tested with translations
        elsewhere.
        """

        vocab = self.atvm.getVocabularyByName('regions')

        autUID = vocab.aut.UID()
        tyrUID = vocab.aut.tyr.UID()
        aussUID = vocab.aut.tyr.auss.UID()

        correctPath = [autUID, tyrUID, aussUID]
        path = vocab.aut.tyr.auss.getTermKeyPath()
        self.assertEqual(correctPath, path,
                         "getTermKeyPath does not return the correct path")

    @unittest.skipUnless(HAS_LP, 'requires LinguaPlone')
    def testTranslations(self):
        """tests if treevocabulary works fine with linguaplone
        """
        # translates the vocabulary 'regions'
        # created in ``setupExampleTreeVocabulary``
        # we do not completely translate the vocabulary, to see if canonical
        # titles are correctly used as fallbacks
        regions = self.atvm.getVocabularyByName('regions')
        regions.aut.setLanguage('en')
        regions.aut.addTranslation('de', title='Oesterreich')
        regions.aut.tyr.setLanguage('en')
        regions.aut.tyr.addTranslation('de', title='Tirol')

        # a term and it's translation have to provide the same keys
        vocab = self.atvm.getVocabularyByName('regions')
        aut = vocab.aut
        autDe = vocab['aut-de']

        self.assertEqual(aut.getTermKey(), autDe.getTermKey())

        # check if displaylist are translated correctly
        langtool = getToolByName(self.portal, 'portal_languages')

        # set available portal languages
        langtool.supported_langs = ['en', 'de']

        # per default english is the preferred language
        self.assertEqual('en', langtool.getPreferredLanguage())
        enDict = vocab.getVocabularyDict()

        autUID = vocab.aut.UID()
        # title for austria in english
        self.assertEqual('Austria', enDict[autUID][0])

        # switch to german
        vocab.REQUEST['set_language'] = 'de'
        langtool.setLanguageBindings()
        self.assertEqual('de', langtool.getPreferredLanguage())
        deDict = vocab.getVocabularyDict()
        self.assertEqual(
            'Oesterreich', deDict[autUID][0],
            "Vocab Title is not translated")
        # for not translated content, the canonicals title is used
        germanyUID = vocab.ger.UID()
        self.assertEqual(
            'Germany', deDict[germanyUID][0],
            "Canonical's is not used for unstranslated vocabularies")

#EOF
