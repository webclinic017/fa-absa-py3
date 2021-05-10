""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesPlannedVsActualTemplate.py"
import acm
import Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumnId, AddColumnSetting

toBeSettledTodayColumnId = "526cc335-b05b-44d7-9238-b0520d6b6f7d"
toBeSettled1DColumnId = "16e0683d-85d0-4476-8c6a-5fc3f3a83fc4"
toBeSettled2DColumnId = "6720d99d-faef-4024-82eb-5576cdddde98"
toBeSettled3DColumnId = "36f39d2b-14ea-4f0b-b107-df6ddb892189"

toBeDeliveredTodayColumnId = "a4b4b5a4-4f09-4679-a384-fbb0fd70a681"
toBeDelivered1DColumnId = "0086fa63-df4b-4297-b325-6e14daf30e6f"
toBeDelivered2DColumnId = "facbe46f-4235-49ae-89a6-52b5a77c5ce1"
toBeDelivered3DColumnId = "a2d5730a-82f5-4356-bd78-47da889e1cb0"

toBeReceivedTodayColumnId = "afa719f4-f73a-49be-952b-2e3613968c1f"
toBeReceived1DColumnId = "ecdcc3d8-8e06-4d21-b342-ab9fdfcdb426"
toBeReceived2DColumnId = "2845efd1-15d8-430c-bed7-df711d327a32"
toBeReceived3DColumnId = "0e5a2a7a-71fa-4dc6-a071-01baa996b8d3"

projectedPositionTodayColumnId = "6d7a0dfb-53fe-4d0b-945c-8162de4e126c"
projectedPosition1DColumnId = "5a5fe249-1128-415b-9215-e30decf2388c"
projectedPosition2DColumnId = "f180ac5f-cde9-4314-be03-299befa1c20a"
projectedPosition3DColumnId = "79e9a9ac-20ff-4624-9a06-3803c4af92be"

failedSettlementsColumnId = "1d26e20c-cdf1-45a8-b033-e4e86f4b955f"
failedReceiptsColumnId = "4ddd37b1-eae6-4704-9df7-d47f227b1254"
failedDeliveriesColumnId = "b379cbd4-0a5b-4109-a555-1aa79d85b733"

settledTodayColumnId = "1d26e20c-cdf1-45a8-b033-e4e86f4b955f"
totUnSettledTodayColumnId = "9db7e4f4-721c-4a8f-8420-dde5df106136"
settledPositionColumnId = "ec60efd1-054c-4984-9e85-40a9fb68acb4"

valueDayColumnId = "0764529d-8fb8-434b-9015-d6e50dd1e520"
currencyColumnId = "14930ff4-5f6c-4555-a75c-078a89acdc49"
tradeRefColumnId = "2b8aff6e-5781-4dbc-8b9f-728a820b564d"
counterpartyColumnId = "8e987e4c-020c-4563-9409-530f4fe3a3c7"
settledDayColumnId = "d96e22e5-f8fb-4be8-8eec-e08f6561d755"


#-------------------------------------------------------------------------
def CreatePlannedVsActualTemplateMessage(viewDispName, dataDispName, dataDispVersion):
    newTemplateMessage = Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages.StoredView()
    newTemplateMessage.serviceName = "FrontArena.DbMaster"
    newTemplateMessage.type.SetInParent()
    
    uniqueIdAndVersion = Contracts_Imdr_Messages_ImdrMessages.UniqueIdAndVersion()
    uniqueIdAndVersion.uniqueId = dataDispName
    uniqueIdAndVersion.version = dataDispVersion
    
    newTemplateMessage.type.data = uniqueIdAndVersion.SerializeToString()

    newTemplateMessage.disposition.SetInParent()
    newTemplateMessage.disposition.name = viewDispName

    newTemplateMessage.viewType = "sheet"

    newContentsMessage = Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages.SheetContent()

    # Add column order

    tradeRef = dict()
    tradeRef["name"] = tradeRefColumnId
    AddColumnId(newContentsMessage, tradeRef)

    currency = dict()
    currency["name"] = currencyColumnId
    AddColumnId(newContentsMessage, currency)

    settledPosition = dict()
    settledPosition["name"] = settledPositionColumnId
    AddColumnId(newContentsMessage, settledPosition)

    failedDeliveries = dict()
    failedDeliveries["name"] = failedDeliveriesColumnId
    AddColumnId(newContentsMessage, failedDeliveries)
    
    failedReceipts = dict()
    failedReceipts["name"] = failedReceiptsColumnId
    AddColumnId(newContentsMessage, failedReceipts)
    
    toBeDeliveredToday = dict()
    toBeDeliveredToday["name"] = toBeDeliveredTodayColumnId
    AddColumnId(newContentsMessage, toBeDeliveredToday)
    
    toBeReceivedToday = dict()
    toBeReceivedToday["name"] = toBeReceivedTodayColumnId
    AddColumnId(newContentsMessage, toBeReceivedToday)
    
    projectedPositionToday = dict()
    projectedPositionToday["name"] = projectedPositionTodayColumnId
    AddColumnId(newContentsMessage, projectedPositionToday)
    
    toBeDelivered1D = dict()
    toBeDelivered1D["name"] = toBeDelivered1DColumnId
    AddColumnId(newContentsMessage, toBeDelivered1D)
    
    toBeReceived1D = dict()
    toBeReceived1D["name"] = toBeReceived1DColumnId
    AddColumnId(newContentsMessage, toBeReceived1D)
    
    projectedPosition1D = dict()
    projectedPosition1D["name"] = projectedPosition1DColumnId
    AddColumnId(newContentsMessage, projectedPosition1D)
    
    toBeDelivered2D = dict()
    toBeDelivered2D["name"] = toBeDelivered2DColumnId
    AddColumnId(newContentsMessage, toBeDelivered2D)
    
    toBeReceived2D = dict()
    toBeReceived2D["name"] = toBeReceived2DColumnId
    AddColumnId(newContentsMessage, toBeReceived2D)
    
    projectedPosition2D = dict()
    projectedPosition2D["name"] = projectedPosition2DColumnId
    AddColumnId(newContentsMessage, projectedPosition2D)
    
    toBeDelivered3D = dict()
    toBeDelivered3D["name"] = toBeDelivered3DColumnId
    AddColumnId(newContentsMessage, toBeDelivered3D)
    
    toBeReceived3D = dict()
    toBeReceived3D["name"] = toBeReceived3DColumnId
    AddColumnId(newContentsMessage, toBeReceived3D)
    
    projectedPosition3D = dict()
    projectedPosition3D["name"] = projectedPosition3DColumnId
    AddColumnId(newContentsMessage, projectedPosition3D)
    
    valueDay = dict()
    valueDay["name"] = valueDayColumnId
    AddColumnId(newContentsMessage, valueDay)
    
    # Add data with grouper
    
    rowItem = newContentsMessage.rowItems.add()
    rowItem.grouper.SetInParent()
    rowItem.grouper.name = "e161e708-b974-4997-b783-d48b686e95bc"
    rowItem.object.SetInParent()
    rowItem.object.name = "e5ccbc5a-2516-4b66-9a26-caf3e630f83b"
    
    rowItem = newContentsMessage.rowItems.add()
    rowItem.grouper.SetInParent()
    rowItem.grouper.name = "e161e708-b974-4997-b783-d48b686e95bc"
    rowItem.object.SetInParent()
    rowItem.object.name = "a1e5d2f6-2916-4ae9-b9eb-32eecc501781"

    newTemplateMessage.contents = newContentsMessage.SerializeToString()

    newSettingsMessage = Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages.SheetSettings()

    # Add column settings
    
    tradeRef = dict()
    tradeRef["columnUniqueId"] = "{}: [].Unique[parameter1=trdnbr trdnbr] [] [] []".format(tradeRefColumnId)
    tradeRef["columnWidth"] = 62
    AddColumnSetting(newSettingsMessage, tradeRef)
    
    currency = dict()
    currency["columnUniqueId"] = "{}: [].Unique[parameter1=curr insid] [] [] []".format(currencyColumnId)
    currency["columnWidth"] = 34
    AddColumnSetting(newSettingsMessage, currency)
    
    settledPosition = dict()
    settledPosition["columnUniqueId"] = "{}: [].Settled Position [] [] []".format(settledPositionColumnId)
    settledPosition["columnWidth"] = 100
    settledPosition["configuredColumnAppearance.bold"] = True
    settledPosition["configuredColumnAppearance.fontSize"] = 10
    settledPosition["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, settledPosition)
    
    failedDeliveries = dict()
    failedDeliveries["columnUniqueId"] = "{}: [].Failed Deliveries [] [] []".format(failedDeliveriesColumnId)
    failedDeliveries["columnWidth"] = 100
    failedDeliveries["configuredColumnAppearance.bold"] = False
    failedDeliveries["configuredColumnAppearance.bkgColor"] = "LightRed"
    AddColumnSetting(newSettingsMessage, failedDeliveries)
    
    failedReceipts = dict()
    failedReceipts["columnUniqueId"] = "{}: [].Failed Receipts [] [] []".format(failedReceiptsColumnId)
    failedReceipts["columnWidth"] = 100
    failedReceipts["configuredColumnAppearance.bold"] = False
    failedReceipts["configuredColumnAppearance.bkgColor"] = "LightRed"
    AddColumnSetting(newSettingsMessage, failedReceipts)
    
    toBeDeliveredToday = dict()
    toBeDeliveredToday["columnUniqueId"] = "{}: [].To Be Delivered Today [] [] []".format(toBeDeliveredTodayColumnId)
    toBeDeliveredToday["columnWidth"] = 85
    toBeDeliveredToday["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toBeDeliveredToday)
    
    toBeReceivedToday = dict()
    toBeReceivedToday["columnUniqueId"] = "{}: [].To Be Received Today [] [] []".format(toBeReceivedTodayColumnId)
    toBeReceivedToday["columnWidth"] = 85
    toBeReceivedToday["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toBeReceivedToday)
    
    projectedPositionToday = dict()
    projectedPositionToday["columnUniqueId"] = "{}: [].Projected Position Today [] [] []".format(projectedPositionTodayColumnId)
    projectedPositionToday["columnWidth"] = 145
    projectedPositionToday["configuredColumnAppearance.bold"] = True
    projectedPositionToday["configuredColumnAppearance.fontSize"] = 10
    projectedPositionToday["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, projectedPositionToday)
    
    toBeDelivered1D = dict()
    toBeDelivered1D["columnUniqueId"] = "{}: [].To Be Delivered 1D [] [] []".format(toBeDelivered1DColumnId)
    toBeDelivered1D["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, toBeDelivered1D)
    
    toBeReceived1D = dict()
    toBeReceived1D["columnUniqueId"] = "{}: [].To Be Received 1D [] [] []".format(toBeReceived1DColumnId)
    toBeReceived1D["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, toBeReceived1D)
    
    projectedPosition1D = dict()
    projectedPosition1D["columnUniqueId"] = "{}: [].Projected Position 1D [] [] []".format(projectedPosition1DColumnId)
    projectedPosition1D["columnWidth"] = 145
    projectedPosition1D["configuredColumnAppearance.bold"] = True
    projectedPosition1D["configuredColumnAppearance.fontSize"] = 10
    projectedPosition1D["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, projectedPosition1D)
    
    toBeDelivered2D = dict()
    toBeDelivered2D["columnUniqueId"] = "{}: [].To Be Delivered 2D [] [] []".format(toBeDelivered2DColumnId)
    toBeDelivered2D["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, toBeDelivered2D)
    
    toBeReceived2D = dict()
    toBeReceived2D["columnUniqueId"] = "{}: [].To Be Received 2D [] [] []".format(toBeReceived2DColumnId)
    toBeReceived2D["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, toBeReceived2D)
    
    projectedPosition2D = dict()
    projectedPosition2D["columnUniqueId"] = "{}: [].Projected Position 2D [] [] []".format(projectedPosition2DColumnId)
    projectedPosition2D["columnWidth"] = 145
    projectedPosition2D["configuredColumnAppearance.bold"] = True
    projectedPosition2D["configuredColumnAppearance.fontSize"] = 10
    projectedPosition2D["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, projectedPosition2D)

    toBeDelivered3D = dict()
    toBeDelivered3D["columnUniqueId"] = "{}: [].To Be Delivered 3D [] [] []".format(toBeDelivered3DColumnId)
    toBeDelivered3D["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, toBeDelivered3D)
    
    toBeReceived3D = dict()
    toBeReceived3D["columnUniqueId"] = "{}: [].To Be Received 3D [] [] []".format(toBeReceived3DColumnId)
    toBeReceived3D["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, toBeReceived3D)
    
    projectedPosition3D = dict()
    projectedPosition3D["columnUniqueId"] = "{}: [].Projected Position 3D [] [] []".format(projectedPosition3DColumnId)
    projectedPosition3D["columnWidth"] = 145
    projectedPosition3D["configuredColumnAppearance.bold"] = True
    projectedPosition3D["configuredColumnAppearance.fontSize"] = 10
    projectedPosition3D["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, projectedPosition3D)

    valueDay = dict()
    valueDay["columnUniqueId"] = "{}: [].Unique[parameter1=value_day] [] [] []".format(valueDayColumnId)
    valueDay["columnWidth"] = 64
    AddColumnSetting(newSettingsMessage, valueDay)

    # Add info about expanded nodes

    expandedNode = newSettingsMessage.expandedNodes.add()
    expandedNode.nodeDisplayName = "LiveCustodyDeals (AC/ISIN/UnSettledSettled)"
    
    expandedNode = newSettingsMessage.expandedNodes.add()
    expandedNode.nodeDisplayName = "LiveOwnIssues (AC/ISIN/UnSettledSettled)"

    newSettingsMessage.rowHeaderWidth = 159
    newSettingsMessage.showGroupLabels = True

    newTemplateMessage.userSettings = newSettingsMessage.SerializeToString()

    newTemplateMessage.commonSettings.SetInParent()
    
    return newTemplateMessage.SerializeToString()

#-------------------------------------------------------------------------
def CreatePlannedVsActualTemplate(templateName, viewDispositionName, dataDispositionName):
    newTemplate = acm.FHgcStoredViewTemplate()
    newTemplate.AutoUser(False)
    newTemplate.User(None)
    newTemplate.Name(templateName)
    newTemplate.SetTemplate(CreatePlannedVsActualTemplateMessage(viewDispositionName, dataDispositionName, "50a798ff-d211-41a8-b4a5-7700a9fe463e"), "FrontArena.DbMaster")
    newTemplate.Commit()
