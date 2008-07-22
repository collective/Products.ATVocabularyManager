# File: marshaller.py
"""\
VDEX compliant marshaller

RCS-ID $Id: codesnippets.py 3417 2005-01-11 19:29:35Z yenzenz $
"""
# Copyright (c) 2005 by eduplone Open Source Business Network EEIG
# This code was created for the ZUCCARO project.
# ZUCCARO (Zope-based Universally Configurable Classes for Academic Research
# Online) is a database framework for the Humanities developed by
# Bibliotheca Hertziana, Max-Planck Institute for Art History
# For further information: http://zuccaro.biblhertz.it/
#
# BSD-like licence, see LICENCE.txt
#
__author__  = '''Jens Klein <jens@bluedynamics.com>'''
__docformat__ = 'plaintext'

try:
    from Products.Archetypes.marshallers import Marshaller
except ImportError:
    from Products.Archetypes.Marshall import Marshaller
    
class VDEXMarshaller(Marshaller):

    def marshall(self, instance, **kwargs):
        sio=instance.exportXMLBinding()
        xml=sio.getvalue()
        return ('text/xml', len(xml), xml)

    def demarshall(self, instance, data, **kwargs):
        instance.importXMLBinding(data)
