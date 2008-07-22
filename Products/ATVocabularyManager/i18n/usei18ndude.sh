#!/bin/sh

i18ndude rebuild-pot --pot atvocabularymanager.pot --create atvocabularymanager --merge manual.pot ../
i18ndude sync --pot  atvocabularymanager.pot atvocabularymanager-??.po
i18ndude sync --pot  atvocabularymanager.pot atvocabularymanager-??-??.po

# atvocabularymanager-plone.pot is manually created
i18ndude sync --pot  atvocabularymanager-plone.pot atvocabularymanager-plone-??.po
i18ndude sync --pot  atvocabularymanager-plone.pot atvocabularymanager-plone-??-??.po

