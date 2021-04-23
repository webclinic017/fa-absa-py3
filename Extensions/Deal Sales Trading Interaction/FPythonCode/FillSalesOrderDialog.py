import acm
from DealPackageUtil import DealPackageException
from DealPackageAsDialog import OpenDealPackageDialogWithNoButtons

def StartFillSalesOrderDialog(shell, content):
    try:
        gui = acm.FBusinessLogicGUIShell()
        gui.SetFUxShell(shell)
        dealPackage = acm.DealPackage().NewAsDecorator('Fill Sales Order', gui, [content])
        OpenDealPackageDialogWithNoButtons(shell, dealPackage, 'Fill Sales Order', False)
    except Exception as e:
        errorStr = 'Failed to Start Fill Sales Order Dialog, ' + str(e)
        print(errorStr)
        raise DealPackageException(errorStr)

def ButtonCreate(eii):
    doCreate = False
    try:
        cell = eii.Parameter("Cell")
        order = cell.RowObject()
        if order and order.IsKindOf(acm.FSalesOrder):
            doCreate = True    
    except Exception as e:
        errorStr = 'Failed to Create Button to Fill Sales Order, ' + str(e)
        print(errorStr) 
    return doCreate

def FillSalesOrder(order, shell):
    try:
        StartFillSalesOrderDialog(shell, order)
    except Exception as e:
        errorStr = 'Failed to Create Fill Sales Order Dialog, ' + str(e)
        print(errorStr)
        raise DealPackageException(errorStr)        


def AcceptSalesRequestButtonAction(eii):
    try:
        eii.ExtensionObject().InvokeCommand('cmdAcceptSalesRequest')
    except Exception as e:
        print(('Failed to Accept Sales Request', e))


acceptButtonStatuses = ['Pending', 'Req Modify']

def ButtonAction(eii):
    eo          = eii.ExtensionObject()
    activeSheet = eii.Parameter("sheet")
    cell        = activeSheet.Selection().SelectedCell()
    order       = cell.RowObject()
    shell       = eo.Shell()

    if order and order.IsKindOf(acm.FSalesOrder):
        if order.SalesState() in acceptButtonStatuses:
            AcceptSalesRequestButtonAction(eii)
        else:
            FillSalesOrder(order, shell)
            


def SalesOrderFillOrAcceptLabel(object):
    label = ''
    if object.SalesState() in acceptButtonStatuses:
        label = 'Accept'
    elif object.SalesState() == 'In Exec':
        label = 'Fill'
    else:
        label = 'Open'
    return label
    
