# File: sortedvocabulary.py
#
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__ = '''gotcha'''
__docformat__ = 'plaintext'


from Products.ATVocabularyManager.config import *
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import *
else:
    from Products.Archetypes.atapi import *

from AccessControl import ClassSecurityInfo

from Products.Archetypes.interfaces.vocabulary import IVocabulary

from Products.ATVocabularyManager.tools import registerVocabularyContainer
from Products.ATVocabularyManager.config import PROJECTNAME
from Products.ATVocabularyManager.types.simple.vocabulary import SimpleVocabulary


class SortedSimpleVocabulary(SimpleVocabulary):
    security = ClassSecurityInfo()

    __implements__ = getattr(OrderedBaseFolder, '__implements__', ()) + (IVocabulary, )


    # This name appears in the 'add' box
    archetype_name = 'Sorted Simple Vocabulary'

    meta_type = 'SortedSimpleVocabulary'
    portal_type = 'SortedSimpleVocabulary'
    allowed_content_types = list(getattr(SimpleVocabulary, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    allow_discussion = 0
    #content_icon = 'SortedSimpleVocabulary.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "SortedSimpleVocabulary"
    typeDescMsgId = 'description_edit_sortedsimplevocabulary'

    def getDisplayList(self, instance):
        """ returns a object of class DisplayList as defined in
            Products.Archetypes.utils

            The instance of the content class is given as parameter.
        """
        vdict = self.getVocabularyDict(instance)
        key_values = []
        for key in vdict.keys():
            key_values.append((key, vdict[key]))

        def cmp_second_term(item1, item2):
            return cmp(item1[1].upper(), item2[1].upper())

        key_values.sort(cmp_second_term)

        dl = DisplayList(key_values)
        return dl


registerType(SortedSimpleVocabulary, PROJECTNAME)
registerVocabularyContainer(SortedSimpleVocabulary)
