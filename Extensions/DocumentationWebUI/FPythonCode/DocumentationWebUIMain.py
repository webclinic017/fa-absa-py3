

import acm, ael
import FUxCore
import webbrowser
try:
    import FDocumentationParameters as DocParams
except ImportError:
    import FDocumentationParametersTemplate as DocParams

import FOperationsDocumentXMLCreator as XmlCreator
import FSettlementSwiftXMLSpecifier
import FOperationsDocumentService

global __docService
__docService = None

associatedViewerConfirmationStr      = 'Show Associated Viewer - Confirmation'
associatedViewerSettlementStr        = 'Show Associated Viewer - Settlement'
messageAdminConfirmationStr          = 'Show Message Admin - Confirmation'
messageAdminSettlementStr            = 'Show Message Admin - Settlement'
editDocumentConfirmationStr          = 'Show Edit Document - Confirmation'
templateEditorStr                    = 'Show Template Editor'
templateTagDefinitionStr             = 'Show Template Tag Definition'
heightAndWidth                       = '&height=700&width=700'

associatedViewerURL      = 'Launch=Adaptiv%2FDocumentation%2FAssociated%20Viewer'
messageAdminURL          = 'Launch=Adaptiv%2FDocumentation%2FMessageAdmin'
editDocumentURL          = 'Launch=Adaptiv%2FDocumentation%2FDocument%20Repair'
templateEditorURL        = 'Launch=Adaptiv%2fDocumentation%2fSet-up%2fTemplateEditor'
templateTagDefinitionURL = 'Launch=Adaptiv%2fDocumentation%2fSet-up%2fTemplateTagDef'

MODE_SWIFT                = 1
MODE_LONGFORM             = 2
MODE_SWIFT_LONGFORM       = 3

ID_POSITIVE               = 1
ID_NEGATIVE               = 2
ID_POSITIVE_NEGATIVE      = 3
ID_POSITIVE_OR_AUTHORISED = 4

# User profile permission
def GetOperationComponentType():
    componentTypes = acm.FEnumeration['enum(ComponentType)']
    return componentTypes.Enumeration('Operation')

def UserHasOperationPermission(user, operation):
    if OperationExists(operation):
        return user.IsAllowed(operation, GetOperationComponentType())
    return False

def OperationExists(operation):
    compType = 'Operation'
    queryString = 'name=\'%s\' and type=\'%s\'' % (operation, compType)
    op = acm.FComponent.Select01(queryString, '')
    if op == None:
        return False
    return True

# Web UI calls
def GetAdaptivURL():
    return DocParams.adaptivWebUIAddress+'AppStyle=FA&'

def ViewInAssociatedViewerSettlement(eii):
    '''Authorised settlements can be previewed in assoc viewer '''
    s = GetSourceObject(eii)
    if IsAuthSettlementForSWIFT(s):
        docIDs = GetPreviewDocumentIDs(s)
    else:
        docIDs = GetDocumentIds(s, ID_POSITIVE, MODE_SWIFT)

    for docID in docIDs:
        webbrowser.open_new(GetAdaptivURL()+associatedViewerURL+'&DocID='+str(docID)+heightAndWidth)

def ViewInMessageAdminSettlement(eii):
    webbrowser.open_new(GetAdaptivURL()+messageAdminURL)

def ViewInAssociatedViewerConfirmation(eii):
    for docID in GetDocumentIds(eii, ID_POSITIVE, MODE_SWIFT):
        webbrowser.open_new(GetAdaptivURL()+associatedViewerURL+'&DocID='+str(docID)+heightAndWidth)

def ViewInMessageAdminConfirmation(eii):
    webbrowser.open_new(GetAdaptivURL()+messageAdminURL)

def TemplateTagDefinition(eii):
    webbrowser.open_new(GetAdaptivURL()+templateTagDefinitionURL)

def TemplateEditor(eii):
    webbrowser.open_new(GetAdaptivURL()+templateEditorURL)

def EditDocumentConfirmation(eii):
    for docID in GetDocumentIds(eii, ID_POSITIVE, MODE_LONGFORM):
        webbrowser.open_new(GetAdaptivURL() + editDocumentURL + '&ResultID=' + str(docID))

# Utils
def GetSourceObject(obj):
    srcObj = None
    if (obj and
       (obj.IsKindOf(acm.FSettlement) or (obj.IsKindOf(acm.FConfirmation)))):
        srcObj = obj
    elif obj and obj.IsKindOf(acm.FArray):
        if len(obj) >= 1:
            srcObj = obj[0]
    else:
        extensionObject = obj.ExtensionObject()
        if extensionObject.IsKindOf(acm.FBackOfficeManagerFrame):
            cell = obj.ExtensionObject().ActiveSheet().Selection().SelectedCell()
            srcObj = cell.RowObject()
        elif extensionObject.IsKindOf(acm.FArray):
            if len(extensionObject) >= 1:
                srcObj = extensionObject[0]
    return srcObj

def GetDocumentIds(obj, includeNegativeIDs, docMode):
    '''docMode: 1 = Swift, 2 = Longform, 3 = Swift and Longform'''
    srcObj = GetSourceObject(obj)
    docIDs = []

    if includeNegativeIDs == ID_POSITIVE_OR_AUTHORISED and IsAuthSettlementForSWIFT(srcObj):
        return [ID_POSITIVE_OR_AUTHORISED] # non empty list returned

    opDocs = srcObj.Documents()

    for opDoc in opDocs:
        if ShouldDocumentBeIncluded(opDoc, includeNegativeIDs, docMode):
            docIDs.append(opDoc.DocumentId())

    return docIDs

def GetPreviewDocumentIDs(srcObj):
    '''Returns docids that are created via settlement preview '''
    __docService = FOperationsDocumentService.CreateDocumentService(DocParams)
    if not __docService.IsConnected():
        print ("Not connected to Adaptiv Documentation")
        return []
    try:
        xmlSpecifier = FSettlementSwiftXMLSpecifier.SettlementSwiftXMLSpecifier("", ael.Settlement[srcObj.Oid()])
        return __docService.CreateDocument(XmlCreator.to_xml(xmlSpecifier))
    except:
        return []

def IsAuthSettlementForSWIFT(srcObj):
    return srcObj.Status() == "Authorised" and srcObj.MTMessages()

def ShouldDocumentBeIncluded(opDoc, idType, docMode):
    includeDoc = False
    messageType = opDoc.SwiftMessageType()
    docID = opDoc.DocumentId()
    if CheckDocumentID(docID, idType):
        if CheckDocType(messageType, docMode):
            includeDoc = True

    return includeDoc

def CheckDocumentID(docID, idType):
    validID = False
    if idType in [ID_POSITIVE, ID_POSITIVE_OR_AUTHORISED]:
        if docID > 0:
            validID = True
    elif idType == ID_NEGATIVE:
        if docID <= 0:
            validID = True
    elif idType == ID_POSITIVE_NEGATIVE:
        validID = True

    return validID

def CheckDocType(messageType, docMode):
    validType = False
    if docMode == MODE_SWIFT:
        if messageType != 0:
            validType = True
    elif docMode == MODE_LONGFORM:
        if messageType == 0:
            validType = True
    elif docMode == MODE_SWIFT_LONGFORM:
        validType = True

    return validType

def DocumentsExist(eii, includeNegativeIDs, docMode):
    if len(GetDocumentIds(eii, includeNegativeIDs, docMode)):
        return True
    else:
        return False

def EnableEditDocument(eii):
    return DocumentsExist(eii, ID_POSITIVE, MODE_LONGFORM)

def EnableAssociatedViewerForSettlement(eii):
    return DocumentsExist(eii, ID_POSITIVE_OR_AUTHORISED, MODE_SWIFT)

def EnableAssociatedViwerForConfirmation(eii):
    return DocumentsExist(eii, ID_POSITIVE, MODE_SWIFT)


# Common class for dynamic activaion of the menu

class Menu(FUxCore.MenuItem):
    def __init__(self, extObj, operation, invoke, precheck):
        self.m_extObj    = extObj     # array with the object
        self.m_operation = operation  # operation for the menu
        self.m_precheck  = precheck   # extra checks before activating menu
        self.m_invoke    = invoke     # action of the menu

    def Invoke(self, eii):
        '''Call menu function with parameter eii (FExtensionInvokationInfo)'''
        globals()[self.m_invoke](eii)

    def Applicable(self):
        if self.m_extObj:
            objClass = self.m_extObj.Class()
            if objClass == acm.FArray:
                if len(self.m_extObj):
                    return True
                else:
                    return False
            elif objClass == acm.CPartyDefinitionFrame:
                return True
            else:
                return False
        else:
            return False

    def Enabled(self):
        ret = UserHasOperationPermission(acm.User(), self.m_operation)
        if ret and self.m_precheck:
            ret = globals()[self.m_precheck](self.m_extObj)
        return ret

    def Checked(self):
        return False

# Entry points for every menu (refer to corresponding FMenuExtension)

def CreateMenuViewInAssociatedViewerSettlement(extObj):
    return Menu(extObj, associatedViewerSettlementStr, "ViewInAssociatedViewerSettlement", "EnableAssociatedViewerForSettlement")

def CreateMenuViewInMessageAdminSettlement(extObj):
    return Menu(extObj, messageAdminSettlementStr, "ViewInMessageAdminSettlement", "")

def CreateMenuViewInAssociatedViewerConfirmation(extObj):
    return Menu(extObj, associatedViewerConfirmationStr, "ViewInAssociatedViewerConfirmation", "EnableAssociatedViwerForConfirmation")

def CreateMenuViewInMessageAdminConfirmation(extObj):
    return Menu(extObj, messageAdminConfirmationStr, "ViewInMessageAdminConfirmation", "")

def CreateMenuEditDocumentConfirmation(extObj):
    return Menu(extObj, editDocumentConfirmationStr, "EditDocumentConfirmation", "EnableEditDocument")

def CreateMenuTemplateEditorConfirmation(extObj):
    return Menu(extObj, templateEditorStr, "TemplateEditor", "")

def CreateMenuTemplateTagDefinitionConfirmation(extObj):
    return Menu(extObj, templateTagDefinitionStr, "TemplateTagDefinition", "")
