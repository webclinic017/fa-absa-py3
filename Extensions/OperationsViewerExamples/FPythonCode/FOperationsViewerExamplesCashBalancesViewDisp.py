""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesCashBalancesViewDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumn, AddTree

#-------------------------------------------------------------------------
def CreateCashBalancesViewDispMessage(dataDispName):
    newStoredViewDisp = Contracts_Imdr_Messages_ImdrMessages.StoredViewDispositon()

    newStoredViewDisp.dataDispositionName = dataDispName

    newStoredViewDisp.viewDisposition.SetInParent()
    viewDisp = newStoredViewDisp.viewDisposition
    
    # Add Grouping Information

    grandGrandChild = dict()
    grandGrandChild["includeLevelInProjection"] = False
    grandGrandChild["groupBy.type.tableValue.tableValueId"] = "cashUnSettledSettledExtAttr"
    grandGrandChild["groupBy.showLeafs.sort.tableValueId"] = "value_day"
    grandGrandChild["groupBy.showLeafs.sort.ascending"] = False
    grandGrandChild["groupBy.nodeDetails.sort.ascending"] = False

    grandChild = dict()
    grandChild["includeLevelInProjection"] = False
    grandChild["groupBy.type.tableValue.tableValueId"] = "acquirer_accname account"
    grandChild["groupBy.partition.tableFormula.namedFormulaId"] = "Active/NotActive"
    grandChild["children"] = [grandGrandChild]

    child = dict()
    child["includeLevelInProjection"] = False
    child["groupBy.type.tableValue.tableValueId"] = "curr insid"
    child["children"] = [grandChild]

    tree = dict()
    tree["uniqueId"] = "f124a109-fbe6-448a-ad5e-59e768816b7e"
    tree["displayInformation.label.formatString"] = "CCY/AC/UnSettledSettled"
    tree["root.includeLevelInProjection"] = True
    tree["root.children"] = [child]

    AddTree(viewDisp, tree)
    
    # Add Opening Balance Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Opening Balance Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    openingBalanceToday = dict()
    openingBalanceToday["uniqueId"] = "8d2afbe1-2cb0-4897-abbb-d8e009466def"
    openingBalanceToday["displayInformation.label.formatString"] = "Opening Balance Today"
    openingBalanceToday["root.children"] = [child]

    AddColumn(viewDisp, openingBalanceToday)
    
    # Add Failed To Receive Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Failed To Receive"

    child = dict()
    child["contribution.formula"] = namedFormula

    failedToReceive = dict()
    failedToReceive["uniqueId"] = "52a6d3d9-56cc-42e9-9069-e42c74025028"
    failedToReceive["displayInformation.label.formatString"] = "Failed To Receive"
    failedToReceive["root.children"] = [child]

    AddColumn(viewDisp, failedToReceive)
    
    # Add Failed To Pay Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Failed To Pay"

    child = dict()
    child["contribution.formula"] = namedFormula

    failedToPay = dict()
    failedToPay["uniqueId"] = "397ba95e-59e1-4085-adfa-01370fd061fc"
    failedToPay["displayInformation.label.formatString"] = "Failed To Pay"
    failedToPay["root.children"] = [child]

    AddColumn(viewDisp, failedToPay)
        
    # Add Received Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Received Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    receivedToday = dict()
    receivedToday["uniqueId"] = "d90a85f2-0651-4bb5-85e7-85d2497da575"
    receivedToday["displayInformation.label.formatString"] = "Received Today"
    receivedToday["root.children"] = [child]

    AddColumn(viewDisp, receivedToday)
        
    # Add Paid Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Paid Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    paidToday = dict()
    paidToday["uniqueId"] = "c9bd2d5f-71d0-4373-8b6e-c3625864281d"
    paidToday["displayInformation.label.formatString"] = "Paid Today"
    paidToday["root.children"] = [child]

    AddColumn(viewDisp, paidToday)

    # Add To Receive Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Receive Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    toReceiveToday = dict()
    toReceiveToday["uniqueId"] = "b0a7c9b3-30af-44dc-a6a9-279ba4baf226"
    toReceiveToday["displayInformation.label.formatString"] = "To Receive Today"
    toReceiveToday["root.children"] = [child]

    AddColumn(viewDisp, toReceiveToday)
    
    # Add To Pay Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Pay Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    toPayToday = dict()
    toPayToday["uniqueId"] = "24faf0b4-d72f-4f1f-ac4c-bc1db36eed3f"
    toPayToday["displayInformation.label.formatString"] = "To Pay Today"
    toPayToday["root.children"] = [child]

    AddColumn(viewDisp, toPayToday)
        
    # Add Closing Balance Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Closing Balance Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    closingBalanceToday = dict()
    closingBalanceToday["uniqueId"] = "d5cc9f4d-d9bf-4b25-afba-53a14e2ae104"
    closingBalanceToday["displayInformation.label.formatString"] = "Closing Balance Today"
    closingBalanceToday["root.children"] = [child]

    AddColumn(viewDisp, closingBalanceToday)
    
    # Add To Receive 1D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Receive 1D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toReceive1D = dict()
    toReceive1D["uniqueId"] = "1b5e9ad9-9436-4940-9b66-5e9d324343ec"
    toReceive1D["displayInformation.label.formatString"] = "To Receive 1D"
    toReceive1D["root.children"] = [child]

    AddColumn(viewDisp, toReceive1D)
        
    # Add To Pay 1D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Pay 1D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toPay1D = dict()
    toPay1D["uniqueId"] = "429e2b63-3a5a-4d09-9378-44ffbb5fb9d7"
    toPay1D["displayInformation.label.formatString"] = "To Pay 1D"
    toPay1D["root.children"] = [child]

    AddColumn(viewDisp, toPay1D)
        
    # Add Closing Balance 1D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Closing Balance 1D"

    child = dict()
    child["contribution.formula"] = namedFormula

    closingBalance1D = dict()
    closingBalance1D["uniqueId"] = "f58d985d-6291-46ad-9a38-dbc19d16f8c4"
    closingBalance1D["displayInformation.label.formatString"] = "Closing Balance 1D"
    closingBalance1D["root.children"] = [child]

    AddColumn(viewDisp, closingBalance1D)
    
    # Add To Receive 2D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Receive 2D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toReceive2D = dict()
    toReceive2D["uniqueId"] = "3256a83e-a91a-4711-ae23-c0c9ae355e89"
    toReceive2D["displayInformation.label.formatString"] = "To Receive 2D"
    toReceive2D["root.children"] = [child]

    AddColumn(viewDisp, toReceive2D)
    
    # Add To Pay 2D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Pay 2D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toPay2D = dict()
    toPay2D["uniqueId"] = "3210ad34-f770-46db-8373-dd7c49c7ceef"
    toPay2D["displayInformation.label.formatString"] = "To Pay 2D"
    toPay2D["root.children"] = [child]

    AddColumn(viewDisp, toPay2D)
        
    # Add Closing Balance 2D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Closing Balance 2D"

    child = dict()
    child["contribution.formula"] = namedFormula

    closingBalance2D = dict()
    closingBalance2D["uniqueId"] = "6682644b-6a9a-431e-b29c-554e14703acc"
    closingBalance2D["displayInformation.label.formatString"] = "Closing Balance 2D"
    closingBalance2D["root.children"] = [child]

    AddColumn(viewDisp, closingBalance2D)
    
    # Add To Receive 3D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Receive 3D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toReceive3D = dict()
    toReceive3D["uniqueId"] = "0834b7af-595a-4ce6-9254-aef26107211f"
    toReceive3D["displayInformation.label.formatString"] = "To Receive 3D"
    toReceive3D["root.children"] = [child]

    AddColumn(viewDisp, toReceive3D)
    
    # Add To Pay 3D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Pay 3D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toPay3D = dict()
    toPay3D["uniqueId"] = "50436824-14df-45af-bef0-817953f6c9f0"
    toPay3D["displayInformation.label.formatString"] = "To Pay 3D"
    toPay3D["root.children"] = [child]

    AddColumn(viewDisp, toPay3D)
        
    # Add Closing Balance 3D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Closing Balance 3D"

    child = dict()
    child["contribution.formula"] = namedFormula

    closingBalance3D = dict()
    closingBalance3D["uniqueId"] = "20f986fe-0c61-40b0-9682-c3e1ebb167ce"
    closingBalance3D["displayInformation.label.formatString"] = "Closing Balance 3D"
    closingBalance3D["root.children"] = [child]

    AddColumn(viewDisp, closingBalance3D)
    
    # Add To Receive Future Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Receive Future"

    child = dict()
    child["contribution.formula"] = namedFormula

    toReceiveFuture = dict()
    toReceiveFuture["uniqueId"] = "482833a9-3c3b-4c97-9959-c77f86336c23"
    toReceiveFuture["displayInformation.label.formatString"] = "To Receive Future"
    toReceiveFuture["root.children"] = [child]

    AddColumn(viewDisp, toReceiveFuture)
    
    # Add To Pay Future Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Pay Future"

    child = dict()
    child["contribution.formula"] = namedFormula

    toPayFuture = dict()
    toPayFuture["uniqueId"] = "b97ec207-f71a-45cd-aa94-475f6d00c84d"
    toPayFuture["displayInformation.label.formatString"] = "To Pay Future"
    toPayFuture["root.children"] = [child]

    AddColumn(viewDisp, toPayFuture)
        
    # Add Closing Balance Future Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Closing Balance Future"

    child = dict()
    child["contribution.formula"] = namedFormula

    closingBalanceFuture = dict()
    closingBalanceFuture["uniqueId"] = "a3577da6-e1b7-4b35-8d0f-c348d73ca875"
    closingBalanceFuture["displayInformation.label.formatString"] = "Closing Balance Future"
    closingBalanceFuture["root.children"] = [child]

    AddColumn(viewDisp, closingBalanceFuture)
    

    return newStoredViewDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreateCashBalancesViewDisposition(viewDispositionName, dataDispositionName):
    newViewDisp = acm.FStoredViewDisposition()
    newViewDisp.Name(viewDispositionName)
    newViewDisp.SubType(dataDispositionName)
    newViewDisp.SetViewDisposition(CreateCashBalancesViewDispMessage(dataDispositionName))
    newViewDisp.Commit()
