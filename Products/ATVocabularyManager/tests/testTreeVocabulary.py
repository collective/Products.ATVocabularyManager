#
# Test for TreeVocabulary
#

from Products.PloneTestCase import PloneTestCase
from Products.ATVocabularyManager.utils.vocabs import createHierarchicalVocabs
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
from Products.CMFCore.utils import getToolByName

import common


class TestTreeVocabulary(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        common.installWithinPortal(self.portal)
        self.atvm = common.getATVM(self.portal)
        self.loginAsPortalOwner()

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

        self.setupExampleTreeVocabulary()
        vocab = self.atvm.getVocabularyByName('regions')

        autUID = vocab.aut.UID()
        tyrUID = vocab.aut.tyr.UID()
        aussUID = vocab.aut.tyr.auss.UID()

        correctPath = [autUID, tyrUID, aussUID]
        path = vocab.aut.tyr.auss.getTermKeyPath()
        self.assertEqual(correctPath, path,
                         "getTermKeyPath does not return the correct path")

    def testSimpleTranslation(self):
        """test if simplevocabulary works fine with linguaplone
        """
        simpleVocabs = dict(
            states=(
                ('aut', u'Austria'),
                ('ger', u'Germany'),
                ('nor', u'Norway'),
                ('fin', u'Finland'),
            ))
        createSimpleVocabs(self.atvm, simpleVocabs)

        self._translateSimpleVocabulary()
        vocab = self.atvm.getVocabularyByName('states')

        langtool = getToolByName(self.portal, 'portal_languages')
        langtool.supported_langs = ['en', 'de']

        # per default english is the preferred language
        self.assertEqual('en', langtool.getPreferredLanguage())
        enDict = vocab.getVocabularyDict()

        # title for austria in english
        self.assertEqual('Austria', enDict.get('aut'))

        # switch to german
        vocab.REQUEST['set_language'] = 'de'
        langtool.setLanguageBindings()
        self.assertEqual('de', langtool.getPreferredLanguage())
        deDict = vocab.getVocabularyDict()
        self.assertEqual('Oesterreich', deDict.get('aut'))

        # create additional states but NOT in english
        simpleVocabs = dict(
            states=(
                ('nld', u'Niederlanden'),
            ))
        createSimpleVocabs(self.atvm, simpleVocabs)
        vocab.nld.setLanguage('de')
        vocab.nld.addTranslation('en', title='Netherlands')
        deDict = vocab.getVocabularyDict()
        self.assertEqual('Niederlanden', deDict.get('nld'))

        vocab.REQUEST['set_language'] = 'en'
        langtool.setLanguageBindings()
        enDict = vocab.getVocabularyDict()
        self.assertEqual('Netherlands', enDict.get('nld'))

    def _translateSimpleVocabulary(self):
        # we need to install 'Linguaplone' to translate
        # vocabularies
        qi = getToolByName(self.portal, 'portal_quickinstaller')

        lpAvailable = qi.isProductAvailable('LinguaPlone')
        self.failUnless(
            lpAvailable,
            "Product LinguaPlone has to be available in INSTANCE_HOME")

        if not qi.isProductInstalled('LinguaPlone'):
            qi.installProduct('LinguaPlone')

        states = self.atvm.getVocabularyByName('states')
        states.aut.setLanguage('en')
        states.aut.addTranslation('de', title='Oesterreich')
        states.ger.setLanguage('en')
        states.ger.addTranslation('de', title='Deutschland')

    def testTreeTranslation(self):
        """tests if treevocabulary works fine with linguaplone
        """
        self.setupExampleTreeVocabulary()
        self._translateTreeVocabulary()

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

    def _translateTreeVocabulary(self):
        """translates the vocabulary 'regions'
        created in ``setupExampleTreeVocabulary``
        """
        # we need to install 'Linguaplone' to translate
        # vocabularies
        qi = getToolByName(self.portal, 'portal_quickinstaller')

        lpAvailable = qi.isProductAvailable('LinguaPlone')
        self.failUnless(
            lpAvailable,
            "Product LinguaPlone has to be available in INSTANCE_HOME")

        if not qi.isProductInstalled('LinguaPlone'):
            qi.installProduct('LinguaPlone')

        regions = self.atvm.getVocabularyByName('regions')
        regions.aut.setLanguage('en')
        regions.aut.addTranslation('de', title='Oesterreich')
        regions.aut.tyr.setLanguage('en')
        regions.aut.tyr.addTranslation('de', title='Tirol')

        # we do not completely translate the vocabulary, to see if canonical
        # titles are correctly used as fallbacks

#EOF
