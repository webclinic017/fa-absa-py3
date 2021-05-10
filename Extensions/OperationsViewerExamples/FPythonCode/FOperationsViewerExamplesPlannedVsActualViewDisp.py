""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesPlannedVsActualViewDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumn, AddTree


#-------------------------------------------------------------------------
def CreatePlannedVsActualViewDispMessage(dataDispName):
    newStoredViewDisp = Contracts_Imdr_Messages_ImdrMessages.StoredViewDispositon()

    newStoredViewDisp.dataDispositionName = dataDispName

    newStoredViewDisp.viewDisposition.SetInParent()
    viewDisp = newStoredViewDisp.viewDisposition
    
    # Add Grouping Information

    grandGrandChild = dict()
    grandGrandChild["includeLevelInProjection"] = False
    grandGrandChild["groupBy.type.tableValue.tableValueId"] = "securityUnSettledSettledExtAttr"
    grandGrandChild["groupBy.showLeafs.sort.tableValueId"] = "value_day"
    grandGrandChild["groupBy.showLeafs.sort.ascending"] = False
    grandGrandChild["groupBy.nodeDetails.sort.ascending"] = False

    grandChild = dict()
    grandChild["includeLevelInProjection"] = False
    grandChild["groupBy.type.tableValue.tableValueId"] = "instrumentIsin"
    grandChild["groupBy.partition.tableFormula.namedFormulaId"] = "Activity/NoActivity"
    grandChild["children"] = [grandGrandChild]

    child = dict()
    child["includeLevelInProjection"] = False
    child["groupBy.type.tableValue.tableValueId"] = "acquirer_accname account"
    child["children"] = [grandChild]

    tree = dict()
    tree["uniqueId"] = "e161e708-b974-4997-b783-d48b686e95bc"
    tree["displayInformation.label.formatString"] = "AC/ISIN/UnSettledSettled"
    tree["root.includeLevelInProjection"] = True
    tree["root.children"] = [child]

    AddTree(viewDisp, tree)

    # Add Trade Ref (Trade.Oid) Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "trdnbr trdnbr"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()
    summarizationFormattingOptions["formatterUniqueId"] = "IntDefault"

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    tradeOId = dict()
    tradeOId["uniqueId"] = "2b8aff6e-5781-4dbc-8b9f-728a820b564d"
    tradeOId["displayInformation.icon"] = "DetailsBase"
    tradeOId["displayInformation.label.formatString"] = "Trade Ref"
    tradeOId["displayInformation.description.formatString"] = "Unique internal number identifying this trade, generated \nautomatically."
    tradeOId["root.children"] = [child]

    AddColumn(viewDisp, tradeOId)

    # Add CCY (Currency) Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "curr insid"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    curr = dict()
    curr["uniqueId"] = "14930ff4-5f6c-4555-a75c-078a89acdc49"
    curr["displayInformation.icon"] = "DetailsBase"
    curr["displayInformation.label.formatString"] = "CCY"
    curr["displayInformation.description.formatString"] = "Unique name of instrument. Used to select instrument in \napplications."
    curr["root.children"] = [child]

    AddColumn(viewDisp, curr)

    # Add Settled Position Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Settled Position"

    child = dict()
    child["contribution.formula"] = namedFormula

    settledPosition = dict()
    settledPosition["uniqueId"] = "ec60efd1-054c-4984-9e85-40a9fb68acb4"
    settledPosition["displayInformation.label.formatString"] = "Settled Position"
    settledPosition["root.children"] = [child]

    AddColumn(viewDisp, settledPosition)

    # Add Failed Deliveries Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Failed Deliveries"

    child = dict()
    child["contribution.formula"] = namedFormula

    failedDeliveries = dict()
    failedDeliveries["uniqueId"] = "b379cbd4-0a5b-4109-a555-1aa79d85b733"
    failedDeliveries["displayInformation.label.formatString"] = "Failed Deliveries"
    failedDeliveries["root.children"] = [child]

    AddColumn(viewDisp, failedDeliveries)

    # Add Failed Receipts Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Failed Receipts"

    child = dict()
    child["contribution.formula"] = namedFormula

    failedReceipts = dict()
    failedReceipts["uniqueId"] = "4ddd37b1-eae6-4704-9df7-d47f227b1254"
    failedReceipts["displayInformation.label.formatString"] = "Failed Receipts"
    failedReceipts["root.children"] = [child]

    AddColumn(viewDisp, failedReceipts)
    
    # Add To Be Delivered Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Delivered Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeDeliveredToday = dict()
    toBeDeliveredToday["uniqueId"] = "a4b4b5a4-4f09-4679-a384-fbb0fd70a681"
    toBeDeliveredToday["displayInformation.label.formatString"] = "To Be Delivered Today"
    toBeDeliveredToday["root.children"] = [child]

    AddColumn(viewDisp, toBeDeliveredToday)

    # Add To Be Received Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Received Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeReceivedToday = dict()
    toBeReceivedToday["uniqueId"] = "afa719f4-f73a-49be-952b-2e3613968c1f"
    toBeReceivedToday["displayInformation.label.formatString"] = "To Be Received Today"
    toBeReceivedToday["root.children"] = [child]

    AddColumn(viewDisp, toBeReceivedToday)

    # Add Projected Position Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Projected Position Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    projectedPositionToday = dict()
    projectedPositionToday["uniqueId"] = "6d7a0dfb-53fe-4d0b-945c-8162de4e126c"
    projectedPositionToday["displayInformation.label.formatString"] = "Projected Position Today"
    projectedPositionToday["root.children"] = [child]

    AddColumn(viewDisp, projectedPositionToday)

    # Add To Be Delivered 1D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Delivered 1D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeDelivered1D = dict()
    toBeDelivered1D["uniqueId"] = "0086fa63-df4b-4297-b325-6e14daf30e6f"
    toBeDelivered1D["displayInformation.label.formatString"] = "To Be Delivered 1D"
    toBeDelivered1D["root.children"] = [child]

    AddColumn(viewDisp, toBeDelivered1D)

    # Add To Be Received 1D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Received 1D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeReceived1D = dict()
    toBeReceived1D["uniqueId"] = "ecdcc3d8-8e06-4d21-b342-ab9fdfcdb426"
    toBeReceived1D["displayInformation.label.formatString"] = "To Be Received 1D"
    toBeReceived1D["root.children"] = [child]

    AddColumn(viewDisp, toBeReceived1D)

    # Add Projected Position 1D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Projected Position 1D"

    child = dict()
    child["contribution.formula"] = namedFormula

    projectedPosition1D = dict()
    projectedPosition1D["uniqueId"] = "5a5fe249-1128-415b-9215-e30decf2388c"
    projectedPosition1D["displayInformation.label.formatString"] = "Projected Position 1D"
    projectedPosition1D["root.children"] = [child]

    AddColumn(viewDisp, projectedPosition1D)

    # Add To Be Delivered 2D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Delivered 2D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeDelivered2D = dict()
    toBeDelivered2D["uniqueId"] = "facbe46f-4235-49ae-89a6-52b5a77c5ce1"
    toBeDelivered2D["displayInformation.label.formatString"] = "To Be Delivered 2D"
    toBeDelivered2D["root.children"] = [child]

    AddColumn(viewDisp, toBeDelivered2D)

    # Add To Be Received 2D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Received 2D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeReceived2D = dict()
    toBeReceived2D["uniqueId"] = "2845efd1-15d8-430c-bed7-df711d327a32"
    toBeReceived2D["displayInformation.label.formatString"] = "To Be Received 2D"
    toBeReceived2D["root.children"] = [child]

    AddColumn(viewDisp, toBeReceived2D)

    # Add Projected Position 2D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Projected Position 2D"

    child = dict()
    child["contribution.formula"] = namedFormula

    projectedPosition2D = dict()
    projectedPosition2D["uniqueId"] = "f180ac5f-cde9-4314-be03-299befa1c20a"
    projectedPosition2D["displayInformation.label.formatString"] = "Projected Position 2D"
    projectedPosition2D["root.children"] = [child]

    AddColumn(viewDisp, projectedPosition2D)

    # Add To Be Delivered 3D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Delivered 3D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeDelivered3D = dict()
    toBeDelivered3D["uniqueId"] = "a2d5730a-82f5-4356-bd78-47da889e1cb0"
    toBeDelivered3D["displayInformation.label.formatString"] = "To Be Delivered 3D"
    toBeDelivered3D["root.children"] = [child]

    AddColumn(viewDisp, toBeDelivered3D)

    # Add To Be Received 3D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Received 3D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeReceived3D = dict()
    toBeReceived3D["uniqueId"] = "0e5a2a7a-71fa-4dc6-a071-01baa996b8d3"
    toBeReceived3D["displayInformation.label.formatString"] = "To Be Received 3D"
    toBeReceived3D["root.children"] = [child]

    AddColumn(viewDisp, toBeReceived3D)

    # Add Projected Position 3D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Projected Position 3D"

    child = dict()
    child["contribution.formula"] = namedFormula

    projectedPosition3D = dict()
    projectedPosition3D["uniqueId"] = "79e9a9ac-20ff-4624-9a06-3803c4af92be"
    projectedPosition3D["displayInformation.label.formatString"] = "Projected Position 3D"
    projectedPosition3D["root.children"] = [child]

    AddColumn(viewDisp, projectedPosition3D)

    # Add Value Day Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "value_day"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()
    summarizationFormattingOptions["formatterUniqueId"] = "DateDefault"

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    settledDay = dict()
    settledDay["uniqueId"] = "0764529d-8fb8-434b-9015-d6e50dd1e520"
    settledDay["displayInformation.icon"] = "DetailsBase"
    settledDay["displayInformation.label.formatString"] = "Value Day"
    settledDay["displayInformation.description.formatString"] = "Day when this settlement is to be paid."
    settledDay["root.children"] = [child]

    AddColumn(viewDisp, settledDay)

    # Add Failed Settlements Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Failed Settlements"

    child = dict()
    child["contribution.formula"] = namedFormula

    failedSettlements = dict()
    failedSettlements["uniqueId"] = "1d26e20c-cdf1-45a8-b033-e4e86f4b955f"
    failedSettlements["displayInformation.label.formatString"] = "Failed Settlements"
    failedSettlements["root.children"] = [child]

    AddColumn(viewDisp, failedSettlements)

    # Add Settled Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Settled Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    settledToday = dict()
    settledToday["uniqueId"] = "7490d37a-bfa8-465e-91a5-195706855d4d"
    settledToday["displayInformation.label.formatString"] = "Settled Today"
    settledToday["root.children"] = [child]

    AddColumn(viewDisp, settledToday)
    
    # Add Total UnSettled Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Total UnSettled Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    totalUnSettledToday = dict()
    totalUnSettledToday["uniqueId"] = "9db7e4f4-721c-4a8f-8420-dde5df106136"
    totalUnSettledToday["displayInformation.label.formatString"] = "Total UnSettled Today"
    totalUnSettledToday["root.children"] = [child]

    AddColumn(viewDisp, totalUnSettledToday)
    
    # Add To Be Settled Today Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Settled Today"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeSettledToday = dict()
    toBeSettledToday["uniqueId"] = "526cc335-b05b-44d7-9238-b0520d6b6f7d"
    toBeSettledToday["displayInformation.label.formatString"] = "To Be Settled Today"
    toBeSettledToday["root.children"] = [child]

    AddColumn(viewDisp, toBeSettledToday)
    
    # Add To Be Settled 1D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Settled 1D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeSettled1D = dict()
    toBeSettled1D["uniqueId"] = "16e0683d-85d0-4476-8c6a-5fc3f3a83fc4"
    toBeSettled1D["displayInformation.label.formatString"] = "To Be Settled 1D"
    toBeSettled1D["root.children"] = [child]

    AddColumn(viewDisp, toBeSettled1D)
    
    # Add To Be Settled 2D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Settled 2D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeSettled2D = dict()
    toBeSettled2D["uniqueId"] = "6720d99d-faef-4024-82eb-5576cdddde98"
    toBeSettled2D["displayInformation.label.formatString"] = "To Be Settled 2D"
    toBeSettled2D["root.children"] = [child]

    AddColumn(viewDisp, toBeSettled2D)
    
    # Add To Be Settled 3D Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "To Be Settled 3D"

    child = dict()
    child["contribution.formula"] = namedFormula

    toBeSettled3D = dict()
    toBeSettled3D["uniqueId"] = "36f39d2b-14ea-4f0b-b107-df6ddb892189"
    toBeSettled3D["displayInformation.label.formatString"] = "To Be Settled 3D"
    toBeSettled3D["root.children"] = [child]

    AddColumn(viewDisp, toBeSettled3D)
    
    # Add Counterparty Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "counterparty_ptynbr ptyid"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    issuer = dict()
    issuer["uniqueId"] = "8e987e4c-020c-4563-9409-530f4fe3a3c7"
    issuer["displayInformation.icon"] = "DetailsBase"
    issuer["displayInformation.label.formatString"] = "Counterparty"
    issuer["displayInformation.description.formatString"] = "Unique name of party."
    issuer["root.children"] = [child]

    AddColumn(viewDisp, issuer)
    
    # Add Settled Day Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "settled_day"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()
    summarizationFormattingOptions["formatterUniqueId"] = "DateDefault"

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    settledDay = dict()
    settledDay["uniqueId"] = "d96e22e5-f8fb-4be8-8eec-e08f6561d755"
    settledDay["displayInformation.icon"] = "DetailsBase"
    settledDay["displayInformation.label.formatString"] = "Settled Day"
    settledDay["displayInformation.description.formatString"] = "The settlement day of a security settlement."
    settledDay["root.children"] = [child]

    AddColumn(viewDisp, settledDay)

    return newStoredViewDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreatePlannedVsActualViewDisposition(viewDispositionName, dataDispositionName):
    newViewDisp = acm.FStoredViewDisposition()
    newViewDisp.Name(viewDispositionName)
    newViewDisp.SubType(dataDispositionName)
    newViewDisp.SetViewDisposition(CreatePlannedVsActualViewDispMessage(dataDispositionName))
    newViewDisp.Commit()
