""" Compiled: NONE NONE """

'''
FConfirmation:GetDocument =
  DisplayName=Get Document
  Function=GetDocument.ShowDocument
  MenuType=Object
'''

import amb
import acm
import os
from tempfile import gettempdir

try:
    import FDocumentationParameters as Params
except ImportError:
    import FDocumentationParametersTemplate as Params
import FOperationsUtils as Utils

def event_cb(channel, event_p, *arg_p):
    Utils.LogTrace()
    pass


def GenerateFilepath(document, extension):
    filename = '%s.%s' % (document, extension)
    return os.path.join(gettempdir(), filename)


def ShowDocument(eii):
    shell = eii.Parameter('shell')
    'ExtensionObject returns a FArray containing the real object'
    ob = eii.ExtensionObject()[0]

    fileName = GenerateFilepath('BARML', 'XML')
    f = open(fileName, 'w')
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    query.AddAttrNode('Confirmation.Oid', 'EQUAL', ob.Oid())
    documents = query.Select()
    import os
    if not documents.IsEmpty():
        document = documents.First()
        if document.Data() !='':
            f.write(document.Data().decode("hex").decode("zlib"))
            f.close()
            os.startfile(fileName)

def start(dict ):
    import FOperationsDocumentHandler as DocumentHandler
    import FDocumentationParameters as Params
    confirmationToReleases = dict['confirmationToReleases']




"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
        import sys, getopt

    import acm, time, ael
    import FOperationsUtils as Utils

    ael_variables = [('confirmationToReleases', 'Confirmation document to review:',
                       'int', None, 0, 0)]

    def ael_main(dict):
        start(dict )

except Exception, e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    Utils.Log(True, str(e))
