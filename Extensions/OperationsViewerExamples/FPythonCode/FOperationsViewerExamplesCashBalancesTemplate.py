""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesCashBalancesTemplate.py"
import acm
import Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumnId, AddColumnSetting


openingBalanceTodayColumnId = "8d2afbe1-2cb0-4897-abbb-d8e009466def"
failedToPayColumnId = "397ba95e-59e1-4085-adfa-01370fd061fc"
failedToReceiveColumnId = "52a6d3d9-56cc-42e9-9069-e42c74025028"
paidTodayColumnId = "c9bd2d5f-71d0-4373-8b6e-c3625864281d"
receivedTodayColumnId = "d90a85f2-0651-4bb5-85e7-85d2497da575"

closingBalanceTodayColumnId = "d5cc9f4d-d9bf-4b25-afba-53a14e2ae104"
closingBalance1DColumnId = "f58d985d-6291-46ad-9a38-dbc19d16f8c4"
closingBalance2DColumnId = "6682644b-6a9a-431e-b29c-554e14703acc"
closingBalance3DColumnId = "20f986fe-0c61-40b0-9682-c3e1ebb167ce"
closingBalanceFutureColumnId = "a3577da6-e1b7-4b35-8d0f-c348d73ca875"

toPayTodayColumnId = "24faf0b4-d72f-4f1f-ac4c-bc1db36eed3f"
toPay1DColumnId = "429e2b63-3a5a-4d09-9378-44ffbb5fb9d7"
toPay2DColumnId = "3210ad34-f770-46db-8373-dd7c49c7ceef"
toPay3DColumnId = "50436824-14df-45af-bef0-817953f6c9f0"
toPayFutureColumnId = "b97ec207-f71a-45cd-aa94-475f6d00c84d"

toReceiveTodayColumnId = "b0a7c9b3-30af-44dc-a6a9-279ba4baf226"
toReceive1DColumnId = "1b5e9ad9-9436-4940-9b66-5e9d324343ec"
toReceive2DColumnId = "3256a83e-a91a-4711-ae23-c0c9ae355e89"
toReceive3DColumnId = "0834b7af-595a-4ce6-9254-aef26107211f"
toReceiveFutureColumnId = "482833a9-3c3b-4c97-9959-c77f86336c23"

#-------------------------------------------------------------------------
def CreateCashBalancesTemplateMessage(viewDispName, dataDispName, dataDispVersion, insertFilterName, insertFilterId):
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
    
    openingBalanceToday = dict()
    openingBalanceToday["name"] = openingBalanceTodayColumnId
    AddColumnId(newContentsMessage, openingBalanceToday)
    
    failedToReceive = dict()
    failedToReceive["name"] = failedToReceiveColumnId
    AddColumnId(newContentsMessage, failedToReceive)
    
    failedToPay = dict()
    failedToPay["name"] = failedToPayColumnId
    AddColumnId(newContentsMessage, failedToPay)
    
    cashRcvdToday = dict()
    cashRcvdToday["name"] = receivedTodayColumnId
    AddColumnId(newContentsMessage, cashRcvdToday)
    
    cashPaidToday = dict()
    cashPaidToday["name"] = paidTodayColumnId
    AddColumnId(newContentsMessage, cashPaidToday)
    
    toReceiveToday = dict()
    toReceiveToday["name"] = toReceiveTodayColumnId
    AddColumnId(newContentsMessage, toReceiveToday)
    
    toPayToday = dict()
    toPayToday["name"] = toPayTodayColumnId
    AddColumnId(newContentsMessage, toPayToday)
    
    closingBalanceToday = dict()
    closingBalanceToday["name"] = closingBalanceTodayColumnId
    AddColumnId(newContentsMessage, closingBalanceToday)
    
    toReceive1D = dict()
    toReceive1D["name"] = toReceive1DColumnId
    AddColumnId(newContentsMessage, toReceive1D)
    
    toPay1D = dict()
    toPay1D["name"] = toPay1DColumnId
    AddColumnId(newContentsMessage, toPay1D)
    
    closingBalance1D = dict()
    closingBalance1D["name"] = closingBalance1DColumnId
    AddColumnId(newContentsMessage, closingBalance1D)
    
    toReceive2D = dict()
    toReceive2D["name"] = toReceive2DColumnId
    AddColumnId(newContentsMessage, toReceive2D)
    
    toPay2D = dict()
    toPay2D["name"] = toPay2DColumnId
    AddColumnId(newContentsMessage, toPay2D)
    
    closingBalance2D = dict()
    closingBalance2D["name"] = closingBalance2DColumnId
    AddColumnId(newContentsMessage, closingBalance2D)
    
    toReceive3D = dict()
    toReceive3D["name"] = toReceive3DColumnId
    AddColumnId(newContentsMessage, toReceive3D)
    
    toPay3D = dict()
    toPay3D["name"] = toPay3DColumnId
    AddColumnId(newContentsMessage, toPay3D)
    
    closingBalance3D = dict()
    closingBalance3D["name"] = closingBalance3DColumnId
    AddColumnId(newContentsMessage, closingBalance3D)
    
    toReceiveFut = dict()
    toReceiveFut["name"] = toReceiveFutureColumnId
    AddColumnId(newContentsMessage, toReceiveFut)
    
    toPayFut = dict()
    toPayFut["name"] = toPayFutureColumnId
    AddColumnId(newContentsMessage, toPayFut)
    
    closingBalanceFut = dict()
    closingBalanceFut["name"] = closingBalanceFutureColumnId
    AddColumnId(newContentsMessage, closingBalanceFut)
    
    # Add data with grouper

    rowItem = newContentsMessage.rowItems.add()
    rowItem.grouper.SetInParent()
    rowItem.grouper.name = "f124a109-fbe6-448a-ad5e-59e768816b7e"
    rowItem.object.SetInParent()
    rowItem.object.name = insertFilterId

    newTemplateMessage.contents = newContentsMessage.SerializeToString()

    newSettingsMessage = Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages.SheetSettings()

    # Add column settings

    openingBalanceToday = dict()
    openingBalanceToday["columnUniqueId"] = "{}: [].Opening Balance Today [] [] []".format(openingBalanceTodayColumnId)
    openingBalanceToday["columnWidth"] = 135
    openingBalanceToday["configuredColumnAppearance.bold"] = True
    openingBalanceToday["configuredColumnAppearance.fontSize"] = 10
    openingBalanceToday["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, openingBalanceToday)
    
    failedToReceive = dict()
    failedToReceive["columnUniqueId"] = "{}: [].Failed To Receive [] [] []".format(failedToReceiveColumnId)
    failedToReceive["columnWidth"] = 95
    failedToReceive["configuredColumnAppearance.bkgColor"] = "LightRed"
    AddColumnSetting(newSettingsMessage, failedToReceive)
    
    failedToPay = dict()
    failedToPay["columnUniqueId"] = "{}: [].Failed To Pay [] [] []".format(failedToPayColumnId)
    failedToPay["columnWidth"] = 95
    failedToPay["configuredColumnAppearance.bkgColor"] = "LightRed"
    AddColumnSetting(newSettingsMessage, failedToPay)
    
    cashRcvdToday = dict()
    cashRcvdToday["columnUniqueId"] = "{}: [].Received Today [] [] []".format(receivedTodayColumnId)
    cashRcvdToday["columnWidth"] = 90
    AddColumnSetting(newSettingsMessage, cashRcvdToday)
    
    cashPaidToday = dict()
    cashPaidToday["columnUniqueId"] = "{}: [].Paid Today [] [] []".format(paidTodayColumnId)
    cashPaidToday["columnWidth"] = 90
    AddColumnSetting(newSettingsMessage, cashPaidToday)
    
    toReceiveToday = dict()
    toReceiveToday["columnUniqueId"] = "{}: [].To Receive Today [] [] []".format(toReceiveTodayColumnId)
    toReceiveToday["columnWidth"] = 98
    toReceiveToday["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toReceiveToday)
    
    toPayToday = dict()
    toPayToday["columnUniqueId"] = "{}: [].To Pay Today [] [] []".format(toPayTodayColumnId)
    toPayToday["columnWidth"] = 98
    toPayToday["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toPayToday)
    
    closingBalanceToday = dict()
    closingBalanceToday["columnUniqueId"] = "{}: [].Closing Balance Today [] [] []".format(closingBalanceTodayColumnId)
    closingBalanceToday["columnWidth"] = 135
    closingBalanceToday["configuredColumnAppearance.bold"] = True
    closingBalanceToday["configuredColumnAppearance.fontSize"] = 10
    closingBalanceToday["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, closingBalanceToday)
    
    toReceive1D = dict()
    toReceive1D["columnUniqueId"] = "{}: [].To Receive 1D [] [] []".format(toReceive1DColumnId)
    toReceive1D["columnWidth"] = 98
    toReceive1D["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toReceive1D)
    
    toPay1D = dict()
    toPay1D["columnUniqueId"] = "{}: [].To Pay 1D [] [] []".format(toPay1DColumnId)
    toPay1D["columnWidth"] = 98
    toPay1D["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toPay1D)
    
    closingBalance1D = dict()
    closingBalance1D["columnUniqueId"] = "{}: [].Closing Balance 1D [] [] []".format(closingBalance1DColumnId)
    closingBalance1D["columnWidth"] = 135
    closingBalance1D["configuredColumnAppearance.bold"] = True
    closingBalance1D["configuredColumnAppearance.fontSize"] = 10
    closingBalance1D["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, closingBalance1D)
    
    toReceive2D = dict()
    toReceive2D["columnUniqueId"] = "{}: [].To Receive 2D [] [] []".format(toReceive2DColumnId)
    toReceive2D["columnWidth"] = 98
    toReceive2D["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toReceive2D)
    
    toPay2D = dict()
    toPay2D["columnUniqueId"] = "{}: [].To Pay 2D [] [] []".format(toPay2DColumnId)
    toPay2D["columnWidth"] = 98
    toPay2D["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toPay2D)
    
    closingBalance2D = dict()
    closingBalance2D["columnUniqueId"] = "{}: [].Closing Balance 2D [] [] []".format(closingBalance2DColumnId)
    closingBalance2D["columnWidth"] = 135
    closingBalance2D["configuredColumnAppearance.bold"] = True
    closingBalance2D["configuredColumnAppearance.fontSize"] = 10
    closingBalance2D["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, closingBalance2D)
    
    toReceive3D = dict()
    toReceive3D["columnUniqueId"] = "{}: [].To Receive 3D [] [] []".format(toReceive3DColumnId)
    toReceive3D["columnWidth"] = 98
    toReceive3D["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toReceive3D)
    
    toPay3D = dict()
    toPay3D["columnUniqueId"] = "{}: [].To Pay 3D [] [] []".format(toPay3DColumnId)
    toPay3D["columnWidth"] = 98
    toPay3D["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toPay3D)
    
    closingBalance3D = dict()
    closingBalance3D["columnUniqueId"] = "{}: [].Closing Balance 3D [] [] []".format(closingBalance3DColumnId)
    closingBalance3D["columnWidth"] = 135
    closingBalance3D["configuredColumnAppearance.bold"] = True
    closingBalance3D["configuredColumnAppearance.fontSize"] = 10
    closingBalance3D["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, closingBalance3D)
    
    toReceiveFuture = dict()
    toReceiveFuture["columnUniqueId"] = "{}: [].To Receive Future [] [] []".format(toReceiveFutureColumnId)
    toReceiveFuture["columnWidth"] = 98
    toReceiveFuture["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toReceiveFuture)
    
    toPayFuture = dict()
    toPayFuture["columnUniqueId"] = "{}: [].To Pay Future [] [] []".format(toPayFutureColumnId)
    toPayFuture["columnWidth"] = 98
    toPayFuture["configuredColumnAppearance.bkgColor"] = "LightOrange"
    AddColumnSetting(newSettingsMessage, toPayFuture)
    
    closingBalanceFuture = dict()
    closingBalanceFuture["columnUniqueId"] = "{}: [].Closing Balance Future [] [] []".format(closingBalanceFutureColumnId)
    closingBalanceFuture["columnWidth"] = 135
    closingBalanceFuture["configuredColumnAppearance.bold"] = True
    closingBalanceFuture["configuredColumnAppearance.fontSize"] = 10
    closingBalanceFuture["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, closingBalanceFuture)

    # Add info about expanded nodes

    expandedNode = newSettingsMessage.expandedNodes.add()
    expandedNode.nodeDisplayName = insertFilterName + " (CCY/AC/UnSettledSettled)"

    newSettingsMessage.rowHeaderWidth = 154
    newSettingsMessage.showGroupLabels = True

    newTemplateMessage.userSettings = newSettingsMessage.SerializeToString()

    newTemplateMessage.commonSettings.SetInParent()
    
    return newTemplateMessage.SerializeToString()

#-------------------------------------------------------------------------
def CreateCashBalancesAllCCYTemplate(templateName, viewDispositionName, dataDispositionName):
    newTemplate = acm.FHgcStoredViewTemplate()
    newTemplate.AutoUser(False)
    newTemplate.User(None)
    newTemplate.Name(templateName)
    newTemplate.SetTemplate(CreateCashBalancesTemplateMessage(viewDispositionName, dataDispositionName, "292a019e-47ab-45f4-a254-e91933232a5c", "All CCY", "cc89f7d7-81b4-4faf-b44d-7142dcde3a52"), "FrontArena.DbMaster")
    newTemplate.Commit()

#-------------------------------------------------------------------------
def CreateCashBalancesMajorCCYTemplate(templateName, viewDispositionName, dataDispositionName):
    newTemplate = acm.FHgcStoredViewTemplate()
    newTemplate.AutoUser(False)
    newTemplate.User(None)
    newTemplate.Name(templateName)
    newTemplate.SetTemplate(CreateCashBalancesTemplateMessage(viewDispositionName, dataDispositionName, "292a019e-47ab-45f4-a254-e91933232a5c", "Major CCY", "f45f10da-c010-4ce3-994f-29aa93de6a88"), "FrontArena.DbMaster")
    newTemplate.Commit()

#-------------------------------------------------------------------------
def CreateCashBalancesMinorCCYTemplate(templateName, viewDispositionName, dataDispositionName):
    newTemplate = acm.FHgcStoredViewTemplate()
    newTemplate.AutoUser(False)
    newTemplate.User(None)
    newTemplate.Name(templateName)
    newTemplate.SetTemplate(CreateCashBalancesTemplateMessage(viewDispositionName, dataDispositionName, "292a019e-47ab-45f4-a254-e91933232a5c", "Minor CCY", "a6798d5c-e72f-4504-ab09-e5825211c89f"), "FrontArena.DbMaster")
    newTemplate.Commit()
