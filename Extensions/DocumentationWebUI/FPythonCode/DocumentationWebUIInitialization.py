

import acm
import DocumentationWebUIMain as DocWebUI


def AddWebUIOperation(operationName):
    if not DocWebUI.OperationExists(operationName):
        componentTypes = acm.FEnumeration['enum(ComponentType)']
        operation = componentTypes.Enumeration('Operation')
        component = acm.FComponent();
        component.Name(operationName)
        component.Type(operation)
        component.Commit()
        print ('Operation added: \'%s\'' % (operationName))
    else:
        print ('Operation already exists: \'%s\'' % (operationName))

def WebUIPermissionsInitialization():
    AddWebUIOperation(DocWebUI.messageAdminConfirmationStr)
    AddWebUIOperation(DocWebUI.messageAdminSettlementStr)
    AddWebUIOperation(DocWebUI.associatedViewerConfirmationStr)
    AddWebUIOperation(DocWebUI.associatedViewerSettlementStr)
    AddWebUIOperation(DocWebUI.editDocumentConfirmationStr)
    AddWebUIOperation(DocWebUI.templateTagDefinitionStr)
    AddWebUIOperation(DocWebUI.templateEditorStr)
