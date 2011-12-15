import os
import types
from Products.CMFCore.utils import getToolByName
from imsvdex.vdex import VDEXManager


def fetchValueByKeyFromVocabularyDict(searchedkey, vdict):
    """recursive find of a key in the vocabulary dictionary tree."""
    for key in vdict.keys():
        if key == searchedkey:
            if vdict[key] in types.StringTypes:
                return vdict[key]
            else:
                return vdict[key][0]
    for key in vdict.keys():
        if vdict[key] not in types.StringTypes:
            if not vdict[key][1]:
                continue
            res = fetchValueByKeyFromVocabularyDict(searchedkey, vdict[key][1])
            if res is not None:
                return res
    return None


def createSimpleVocabs(atvm, simpleVocabDictionary):
    """
    creates simple ATVM vocabularies out of tuples stored in the dictionary
    simpleVocabDictionary.
    code taken from http://plone.org/documentation/tutorial/archgenxml-getting-started/vocabulary-manager

    example:
    simpleVocabs['examplestates'] = (
            ('aut', u'Austria'),
            ('ger', u'Germany'),
            ('nor', u'Norway'),
            ('fin', u'Finland'),
    )
    """
    for vkey in simpleVocabDictionary.keys():
        if isinstance(vkey, (list, tuple)):
            title = vkey[1]
            vocabname = vkey[0]
        else:
            title = None
            vocabname = vkey

        # create vocabulary if it doesn't exist:
        if not hasattr(atvm, vocabname):
            if title is not None:
                atvm.invokeFactory('SimpleVocabulary', vocabname, title=title)
            else:
                atvm.invokeFactory('SimpleVocabulary', vocabname)

        vocab = atvm[vocabname]
        for (ikey, value) in simpleVocabDictionary[vkey]:
            if not hasattr(vocab, ikey):
                vocab.invokeFactory('SimpleVocabularyTerm', ikey)
                vocab[ikey].setTitle(value)
                vocab[ikey].reindexObject()
        vocab.reindexObject()


def createHierarchicalVocabs(atvm, hierarchicalVocabDictionary):
    """
    creates TreeVocabularyTerms out of dictionaries of the following format:

    hierarchicalVocabs[('exampleregions', 'Regions used in ATVocabExample')] =
        ('aut', 'Austria'): {
            ('tyr', 'Tyrol'): {
                ('auss', 'Ausserfern'): {},
            }
        },
        ('ger', 'Germany'): {
            ('bav', 'Bavaria'):{}
        },
    }
    """

    def createVocabularyTerms(vocabulary, id, title, subDictionary):
        """
        vocabulary    the TreeVocabulary(Term) to operate on
        id,title      the new terms title and id
        subDictionary a (maybe empty) dictionary containing (termId, termTitle) keys with dictionaries again.

        creates a new term within vocabulary and recursively
        checks whether there are subvocabularies to create
        """
        if not hasattr(vocabulary, id):
            vocabulary.invokeFactory('TreeVocabularyTerm', id, title=title)

        newTerm = vocabulary[id]


        for key, value in subDictionary.iteritems():
            createVocabularyTerms(newTerm, key[0], key[1], value)

        newTerm.reindexObject()


    for vkey in hierarchicalVocabDictionary.keys():
        # create vocabulary if it doesn't exist:
        vocabname = vkey

        if not hasattr(atvm, vocabname[0]):
            # just to be sure, normally vocabulary is created in Install.py
            atvm.invokeFactory('TreeVocabulary', vocabname[0], title=vocabname[1])

        # new terms will be created, title changes in dictionary won't affect
        # existing terms
        vocab = atvm[vocabname[0]]


        for (id, title), value in hierarchicalVocabDictionary[vkey].iteritems():
            if not hasattr(vocab, id):
                createVocabularyTerms(vocab, id, title, value)
        vocab.reindexObject()


def loadVdexVocabs(site, directory, files, remove=True):
    atvm = getToolByName(site, 'portal_vocabularies')
    for filename in files:
        # load file
        vdexpath = os.path.join(directory, filename)
        if not (os.path.exists(vdexpath) and os.path.isfile(vdexpath)):
            raise ValueError, \
                  'No valid VDEX import file provided at %s.' % vdexpath
        try:
            data = open(vdexpath, 'r').read()
        except Exception, e:
            raise ValueError, 'Problems while reading VDEX import file ' +\
                              'provided at %s\n%s\n.' % (vdexpath, str(e))
        vdex = VDEXManager(data)
        vocabname = vdex.getVocabIdentifier()
        if vocabname in atvm.contentIds():
            if remove:
                atvm.manage_delObjects([vocabname])
            else:
                # logging here?
                continue
        atvm.invokeFactory('VdexFileVocabulary', vocabname)
        atvm[vocabname].importXMLBinding(data)
