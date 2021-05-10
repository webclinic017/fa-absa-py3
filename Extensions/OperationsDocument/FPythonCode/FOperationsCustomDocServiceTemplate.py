""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/templates/FOperationsCustomDocServiceTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FDocumentationCustomDocServiceTemplate

DESCRIPTION
    Changes to any of these settings require a restart of the
    documentation ATS for the changes to take affect.
----------------------------------------------------------------------------"""

class CustomDocumentServiceTemplate:
    
    def __init__(self, parameters):
        self.parameters = parameters
    
    def IsConnected(self):
        return True
    
    def GetDocument(self, documentId, documentFormat):
        return None
    
    def GetDocumentInfo(self, documentId):
        info = {}
        info["TreatmentEvent"] = "LongForm"
        return info
    
    def SendDocumentByRouterName(self, documentId, transportType):
        pass
    
    def CreateDocument(self, xml):
        return [1]
        
    def GetXML(self, xml):        
        return xml
    
    def Disconnect(self):
        pass