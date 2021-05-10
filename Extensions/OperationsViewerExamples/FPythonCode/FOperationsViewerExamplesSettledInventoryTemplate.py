""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesSettledInventoryTemplate.py"
import acm
import Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumnId, AddColumnSetting

custodianColumnId = "4008f605-3f7d-4921-8a47-b49ffbbca9e3"
issuerColumnId = "67bfe3c7-0c80-40c5-9253-ce84f7e0edac"
issueDayColumnId = "da684fe1-d432-4aae-867f-9d8d700ca011"
expiryDayColumnId = "b532da3b-dbbc-4a22-8a8f-1dd6f5a02d74"
currencyColumnId = "b2c2d3b6-0066-4502-a4e0-20967464e15a"
custodyPositionColumnId = "0628caf1-b7ab-4755-8a52-47dfab3bd9ae"
securityTransactionTypeColumnId = "b896c56f-e0cc-4a67-aecc-dd2956eedc89"
temporaryInColumnId = "a1d7a37b-ab34-443a-b51c-1286b6e590b9"
temporaryOutColumnId = "d4b62b5b-cd79-4fe5-afa8-2aca3c0f57dd"
adjustedBalanceColumnId = "90c6d338-cbfa-416b-b013-909a7fe11ee7"
settledDayColumnId = "2d23d5b1-9271-49b8-9002-b3ec6c88a77f"
tradeRefColumnId = "3db8672c-0c51-4638-a193-2da2f84e9adf"
totalIssueSizeColumnId = "ce13385b-9757-4ad1-bfe5-7b46b090319f"
vaultPositionColumnId = "3ad16f46-277b-4523-922b-1a4bf089382a"
issueOutstandingColumnId = "bee28a37-75ab-4c8c-8046-9cb69485cbd6"
issueAmortizationColumnId = "345c5172-28cc-4174-9b1e-adac8747601e"
amountColumnId = "2043fa2d-de63-4b23-8798-fc98fccce6a2"


#-------------------------------------------------------------------------
def CreateSettledInventoryTemplateMessage(viewDispName, dataDispName, dataDispVersion):
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

    custodian = dict()
    custodian["name"] = custodianColumnId
    AddColumnId(newContentsMessage, custodian)

    issuer = dict()
    issuer["name"] = issuerColumnId
    AddColumnId(newContentsMessage, issuer)

    issueDay = dict()
    issueDay["name"] = issueDayColumnId
    AddColumnId(newContentsMessage, issueDay)

    expiryDay = dict()
    expiryDay["name"] = expiryDayColumnId
    AddColumnId(newContentsMessage, expiryDay)
    
    currency = dict()
    currency["name"] = currencyColumnId
    AddColumnId(newContentsMessage, currency)

    custodyPosition = dict()
    custodyPosition["name"] = custodyPositionColumnId
    AddColumnId(newContentsMessage, custodyPosition)

    securityTransactionType = dict()
    securityTransactionType["name"] = securityTransactionTypeColumnId
    AddColumnId(newContentsMessage, securityTransactionType)

    temporaryIn = dict()
    temporaryIn["name"] = temporaryInColumnId
    AddColumnId(newContentsMessage, temporaryIn)
    
    temporaryOut = dict()
    temporaryOut["name"] = temporaryOutColumnId
    AddColumnId(newContentsMessage, temporaryOut)
    
    adjustedBalance = dict()
    adjustedBalance["name"] = adjustedBalanceColumnId
    AddColumnId(newContentsMessage, adjustedBalance)
    
    settledDay = dict()
    settledDay["name"] = settledDayColumnId
    AddColumnId(newContentsMessage, settledDay)
    
    tradeRef = dict()
    tradeRef["name"] = tradeRefColumnId
    AddColumnId(newContentsMessage, tradeRef)
    
    totalIssueSize = dict()
    totalIssueSize["name"] = totalIssueSizeColumnId
    AddColumnId(newContentsMessage, totalIssueSize)
    
    vaultPosition = dict()
    vaultPosition["name"] = vaultPositionColumnId
    AddColumnId(newContentsMessage, vaultPosition)
    
    issueOutstanding = dict()
    issueOutstanding["name"] = issueOutstandingColumnId
    AddColumnId(newContentsMessage, issueOutstanding)
    
    issueAmortization = dict()
    issueAmortization["name"] = issueAmortizationColumnId
    AddColumnId(newContentsMessage, issueAmortization)
    
    amount = dict()
    amount["name"] = amountColumnId
    AddColumnId(newContentsMessage, amount)

    # Add data with grouper

    rowItem = newContentsMessage.rowItems.add()
    rowItem.grouper.SetInParent()
    rowItem.grouper.name = "f5b41933-0e42-4de2-b193-d29911703d6f"
    rowItem.object.SetInParent()
    rowItem.object.name = "e39eac6b-bd8c-4bce-907b-ed8c3428b1e3"

    newTemplateMessage.contents = newContentsMessage.SerializeToString()

    newSettingsMessage = Contracts_HierarchicalGrid_Messages_HierarchicalGridStorageMessages.SheetSettings()

    # Add column settings

    adjustedBalance = dict()
    adjustedBalance["columnUniqueId"] = "{}: [].Adjusted Balance [] [] []".format(adjustedBalanceColumnId)
    adjustedBalance["columnWidth"] = 97
    adjustedBalance["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, adjustedBalance)

    temporaryOut = dict()
    temporaryOut["columnUniqueId"] = "{}: [].Temporary Out [] [] []".format(temporaryOutColumnId)
    temporaryOut["columnWidth"] = 84
    AddColumnSetting(newSettingsMessage, temporaryOut)
    
    amount = dict()
    amount["columnUniqueId"] = "{}: [].Sum[parameter1=amount] [] [] []".format(amountColumnId)
    amount["columnWidth"] = 95
    amount["customLabel"] = "SecurityAmount"
    AddColumnSetting(newSettingsMessage, amount)

    tradeRef = dict()
    tradeRef["columnUniqueId"] = "{}: [].Unique[parameter1=trdnbr trdnbr] [] [] []".format(tradeRefColumnId)
    tradeRef["columnWidth"] = 99
    AddColumnSetting(newSettingsMessage, tradeRef)

    totalIssueSize = dict()
    totalIssueSize["columnUniqueId"] = "{}: [].Sum[parameter1=sec_insaddr total_issued] [] [] []".format(totalIssueSizeColumnId)
    totalIssueSize["columnWidth"] = 100
    totalIssueSize["configuredColumnAppearance.bkgColor"] = "LightCyan"
    AddColumnSetting(newSettingsMessage, totalIssueSize)

    expiryDay = dict()
    expiryDay["columnUniqueId"] = "{}: [].Unique[parameter1=sec_insaddr exp_day] [] [] []".format(expiryDayColumnId)
    expiryDay["columnWidth"] = 65
    AddColumnSetting(newSettingsMessage, expiryDay)
    
    temporaryIn = dict()
    temporaryIn["columnUniqueId"] = "{}: [].Temporary In [] [] []".format(temporaryInColumnId)
    temporaryIn["columnWidth"] = 84
    AddColumnSetting(newSettingsMessage, temporaryIn)
    
    issuer = dict()
    issuer["columnUniqueId"] = "{}: [].Unique[parameter1=sec_insaddr issuer_ptynbr ptyid] [] [] []".format(issuerColumnId)
    issuer["columnWidth"] = 243
    AddColumnSetting(newSettingsMessage, issuer)
    
    issueDay = dict()
    issueDay["columnUniqueId"] = "{}: [].Unique[parameter1=sec_insaddr issue_day] [] [] []".format(issueDayColumnId)
    issueDay["columnWidth"] = 65
    AddColumnSetting(newSettingsMessage, issueDay)
    
    issueAmortization = dict()
    issueAmortization["columnUniqueId"] = "{}: [].Issue Amortization [] [] []".format(issueAmortizationColumnId)
    issueAmortization["columnWidth"] = 100
    issueAmortization["configuredColumnAppearance.bkgColor"] = "LightCyan"
    AddColumnSetting(newSettingsMessage, issueAmortization)
    
    securityTransactionType = dict()
    securityTransactionType["columnUniqueId"] = "{}: [].Unique[parameter1=securityTransactionTypeExtAttr] [] [] []".format(securityTransactionTypeColumnId)
    securityTransactionType["columnWidth"] = 136
    AddColumnSetting(newSettingsMessage, securityTransactionType)
    
    currency = dict()
    currency["columnUniqueId"] = "{}: [].Unique[parameter1=curr insid] [] [] []".format(currencyColumnId)
    currency["columnWidth"] = 34
    AddColumnSetting(newSettingsMessage, currency)
    
    issueOutstanding = dict()
    issueOutstanding["columnUniqueId"] = "{}: [].Issue Outstanding [] [] []".format(issueOutstandingColumnId)
    issueOutstanding["columnWidth"] = 100
    issueOutstanding["configuredColumnAppearance.bkgColor"] = "LightCyan"
    AddColumnSetting(newSettingsMessage, issueOutstanding)
    
    vaultPosition = dict()
    vaultPosition["columnUniqueId"] = "{}: [].Vault Position [] [] []".format(vaultPositionColumnId)
    vaultPosition["columnWidth"] = 100
    vaultPosition["configuredColumnAppearance.bkgColor"] = "LightCyan"
    AddColumnSetting(newSettingsMessage, vaultPosition)
    
    settledDay = dict()
    settledDay["columnUniqueId"] = "{}: [].Unique[parameter1=settled_day] [] [] []".format(settledDayColumnId)
    settledDay["columnWidth"] = 72
    AddColumnSetting(newSettingsMessage, settledDay)
    
    custodyPosition = dict()
    custodyPosition["columnUniqueId"] = "{}: [].Custody Position [] [] []".format(custodyPositionColumnId)
    custodyPosition["columnWidth"] = 112
    custodyPosition["configuredColumnAppearance.bkgColor"] = "LightGreen"
    AddColumnSetting(newSettingsMessage, custodyPosition)
    
    custodian = dict()
    custodian["columnUniqueId"] = "{}: [].Unique[parameter1=acquirer_accname correspondent_bank_ptynbr ptyid] [] [] []".format(custodianColumnId)
    custodian["columnWidth"] = 139
    AddColumnSetting(newSettingsMessage, custodian)

    # Add info about expanded nodes

    expandedNode = newSettingsMessage.expandedNodes.add()
    expandedNode.nodeDisplayName = "LiveIssues (AC/ISIN/RecentPast)"

    newSettingsMessage.rowHeaderWidth = 166
    newSettingsMessage.showGroupLabels = True

    newTemplateMessage.userSettings = newSettingsMessage.SerializeToString()

    newTemplateMessage.commonSettings.SetInParent()
    
    return newTemplateMessage.SerializeToString()

#-------------------------------------------------------------------------
def CreateSettledInventoryTemplate(templateName, viewDispositionName, dataDispositionName):
    newTemplate = acm.FHgcStoredViewTemplate()
    newTemplate.AutoUser(False)
    newTemplate.User(None)
    newTemplate.Name(templateName)
    newTemplate.SetTemplate(CreateSettledInventoryTemplateMessage(viewDispositionName, dataDispositionName, "ef2646ca-8280-4735-8421-dcc5931add25"), "FrontArena.DbMaster")
    newTemplate.Commit()
