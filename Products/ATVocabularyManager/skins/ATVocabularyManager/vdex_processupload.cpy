## Controller Python Script "vdex_processupload"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=vdex=None, REQUEST=None
##title=VDEX File Import

if (vdex and vdex.filename):
    filename = vdex.filename
    data = vdex.read()
else:
    print "No upload"
    return printed

vocabname = filename
# need to normalize the filename using IUserPreferredFileNameNormalizer
# move this into a view class and get rid of CMFFormController in here
# meanwhile a quick fix for Windows:
if '\\' in vocabname:
    vocabname = vocabname[vocabname.rfind('\\'):]
if vocabname.endswith('.vdex'):
    vocabname = vocabname[:-5]

context.invokeFactory('VdexFileVocabulary', vocabname)
context[vocabname].importXMLBinding(data)

message = "imported %s" % filename

return state.set(portal_status_message=message)
