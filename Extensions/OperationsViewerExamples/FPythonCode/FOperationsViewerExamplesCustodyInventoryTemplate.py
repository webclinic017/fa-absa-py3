""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesCustodyInventoryTemplate.py"
import acm
import Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumnId, AddColumnSetting

issuerColumnId = "59b27eb6-b421-466f-b507-11d01fdd7dc9"
currencyColumnId = "55e17772-e5e2-4f8f-9326-989f15c0cea3"
issueDayColumnId = "675557a7-40c4-4ef6-b4cc-ad39b1a9b6ac"
expiryDayColumnId = "16d691c1-cb3e-48b2-a8ef-274f9ec70aca"
amountColumnId = "2aa7e297-f27d-4576-b263-6ffd33f5686b"
settledDayColumnId = "af8efb42-0767-478a-9fdc-190eaa6f886f"
seqNbrColumnId = "741165a6-faa7-42c0-b069-5aa9beafb6fa"


#-------------------------------------------------------------------------
def CreateCustodyInventoryTemplateMessage(viewDispName, dataDispName, dataDispVersion):
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

    issuer = dict()
    issuer["name"] = issuerColumnId
    AddColumnId(newContentsMessage, issuer)

    currency = dict()
    currency["name"] = currencyColumnId
    AddColumnId(newContentsMessage, currency)

    issueDay = dict()
    issueDay["name"] = issueDayColumnId
    AddColumnId(newContentsMessage, issueDay)

    expiryDay = dict()
    expiryDay["name"] = expiryDayColumnId
    AddColumnId(newContentsMessage, expiryDay)

    amount = dict()
    amount["name"] = amountColumnId
    AddColumnId(newContentsMessage, amount)

    settledDay = dict()
    settledDay["name"] = settledDayColumnId
    AddColumnId(newContentsMessage, settledDay)

    seqNbr = dict()
    seqNbr["name"] = seqNbrColumnId
    AddColumnId(newContentsMessage, seqNbr)

    # Add data with grouper

    rowItem = newContentsMessage.rowItems.add()
    rowItem.grouper.SetInParent()
    rowItem.grouper.name = "62c3f6a2-e835-4197-88cd-e87032045eba"
    rowItem.object.SetInParent()
    rowItem.object.name = "032bb5dc-441b-4307-9b95-d83e75393ad0"

    newTemplateMessage.contents = newContentsMessage.SerializeToString()

    newSettingsMessage = Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages.SheetSettings()

    # Add column settings

    issuer = dict()
    issuer["columnUniqueId"] = "{}: [].Unique[parameter1=sec_insaddr issuer_ptynbr ptyid] [] [] []".format(issuerColumnId)
    issuer["columnWidth"] = 222
    AddColumnSetting(newSettingsMessage, issuer)

    currency = dict()
    currency["columnUniqueId"] = "{}: [].Unique[parameter1=curr insid] [] [] []".format(currencyColumnId)
    currency["columnWidth"] = 36
    AddColumnSetting(newSettingsMessage, currency)

    issueDay = dict()
    issueDay["columnUniqueId"] = "{}: [].Unique[parameter1=sec_insaddr issue_day] [] [] []".format(issueDayColumnId)
    issueDay["columnWidth"] = 75
    AddColumnSetting(newSettingsMessage, issueDay)

    expiryDay = dict()
    expiryDay["columnUniqueId"] = "{}: [].Unique[parameter1=sec_insaddr exp_day] [] [] []".format(expiryDayColumnId)
    expiryDay["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, expiryDay)

    amount = dict()
    amount["columnUniqueId"] = "{}: [].Sum[parameter1=amount] [] [] []".format(amountColumnId)
    amount["columnWidth"] = 86
    amount["customLabel"] = "SecurityAmount"
    AddColumnSetting(newSettingsMessage, amount)

    settledDay = dict()
    settledDay["columnUniqueId"] = "{}: [].Unique[parameter1=settled_day] [] [] []".format(settledDayColumnId)
    settledDay["columnWidth"] = 85
    AddColumnSetting(newSettingsMessage, settledDay)

    seqNbr = dict()
    seqNbr["columnUniqueId"] = "{}: [].Unique[parameter1=seqnbr] [] [] []".format(seqNbrColumnId)
    seqNbr["columnWidth"] = 88
    AddColumnSetting(newSettingsMessage, seqNbr)

    # Add info about expanded nodes

    expandedNode = newSettingsMessage.expandedNodes.add()
    expandedNode.nodeDisplayName = "Non-expired securities (AC/ISIN/RecentPast)"

    newSettingsMessage.rowHeaderWidth = 168
    newSettingsMessage.showGroupLabels = True

    newTemplateMessage.userSettings = newSettingsMessage.SerializeToString()

    newTemplateMessage.commonSettings.SetInParent()
    
    return newTemplateMessage.SerializeToString()

#-------------------------------------------------------------------------
def CreateCustodyInventoryTemplate(templateName, viewDispositionName, dataDispositionName):
    newTemplate = acm.FHgcStoredViewTemplate()
    newTemplate.AutoUser(False)
    newTemplate.User(None)
    newTemplate.Name(templateName)
    newTemplate.SetTemplate(CreateCustodyInventoryTemplateMessage(viewDispositionName, dataDispositionName, "50a798ff-d211-41a8-b4a5-7700a9fe463e"), "FrontArena.DbMaster")
    newTemplate.Commit()
