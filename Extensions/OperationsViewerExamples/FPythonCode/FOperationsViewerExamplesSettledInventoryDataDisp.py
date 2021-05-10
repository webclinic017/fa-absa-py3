""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesSettledInventoryDataDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddTableValue, AddTableFormulaAndParameterValues, AddNamedFilter, AddPreFilter, AddQuickFilters

#-------------------------------------------------------------------------
def CreateSettledInventoryDataDispMessage():
    
    storedDataDisp = Contracts_Imdr_Messages_ImdrMessages.StoredDataDisposition()

    storedDataDisp.serviceName = "FrontArena.DbMaster"

    storedDataDisp.sheetType.SetInParent()

    storedDataDisp.sheetType.name = "ext.Settlement"

    storedDataDisp.dataDisposition.SetInParent()
    
    dataDisp = storedDataDisp.dataDisposition

    storedDataDisp.version = "ef2646ca-8280-4735-8421-dcc5931add25"

    # Add Table Values

    custodian = dict()
    custodian["uniqueId"] = "acquirer_accname correspondent_bank_ptynbr ptyid"
    custodian["attributeChain.attributeIds"] = ["acquirer_accname", "correspondent_bank_ptynbr", "ptyid"]
    custodian["displayInformation.icon"] = "DetailsBase"
    custodian["displayInformation.label.formatString"] = "Custodian"
    custodian["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, custodian)

    issuer = dict()
    issuer["uniqueId"] = "sec_insaddr issuer_ptynbr ptyid"
    issuer["attributeChain.attributeIds"] = ["sec_insaddr", "issuer_ptynbr", "ptyid"]
    issuer["displayInformation.icon"] = "DetailsBase"
    issuer["displayInformation.label.formatString"] = "Issuer"
    issuer["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, issuer)

    issueDay = dict()
    issueDay["uniqueId"] = "sec_insaddr issue_day"
    issueDay["attributeChain.attributeIds"] = ["sec_insaddr", "issue_day"]
    issueDay["displayInformation.icon"] = "DetailsBase"
    issueDay["displayInformation.label.formatString"] = "Issue Day"
    issueDay["displayInformation.description.formatString"] = "Issue day for securities."
    issueDay["formattingOptions.formatterUniqueId"] = "DateDefault"
    AddTableValue(dataDisp, issueDay)

    expiryDay = dict()
    expiryDay["uniqueId"] = "sec_insaddr exp_day"
    expiryDay["attributeChain.attributeIds"] = ["sec_insaddr", "exp_day"]
    expiryDay["displayInformation.icon"] = "DetailsBase"
    expiryDay["displayInformation.label.formatString"] = "Expiry Day"
    expiryDay["displayInformation.description.formatString"] = "Expiry date for non-generic instruments."
    expiryDay["formattingOptions.formatterUniqueId"] = "DateDefault"
    AddTableValue(dataDisp, expiryDay)

    currency = dict()
    currency["uniqueId"] = "curr insid"
    currency["attributeChain.attributeIds"] = ["curr", "insid"]
    currency["displayInformation.icon"] = "DetailsBase"
    currency["displayInformation.label.formatString"] = "CCY"
    currency["displayInformation.description.formatString"] = "Unique name of instrument. Used to select instrument in \napplications."
    AddTableValue(dataDisp, currency)

    securityTransactionType = dict()
    securityTransactionType["uniqueId"] = "securityTransactionTypeExtAttr"
    securityTransactionType["attributeChain.attributeIds"] = ["securityTransactionTypeExtAttr"]
    securityTransactionType["displayInformation.label.formatString"] = "Security Transaction Type"
    AddTableValue(dataDisp, securityTransactionType)

    settledDay = dict()
    settledDay["uniqueId"] = "settled_day"
    settledDay["attributeChain.attributeIds"] = ["settled_day"]
    settledDay["displayInformation.icon"] = "DetailsBase"
    settledDay["displayInformation.label.formatString"] = "Settled Day"
    settledDay["displayInformation.description.formatString"] = "The settlement day of a security settlement."
    settledDay["formattingOptions.formatterUniqueId"] = "DateDefault"
    AddTableValue(dataDisp, settledDay)

    tradeOId = dict()
    tradeOId["uniqueId"] = "trdnbr trdnbr"
    tradeOId["attributeChain.attributeIds"] = ["trdnbr", "trdnbr"]
    tradeOId["displayInformation.icon"] = "DetailsBase"
    tradeOId["displayInformation.label.formatString"] = "Trade Ref"
    tradeOId["displayInformation.description.formatString"] = "Unique internal number identifying this trade, generated \nautomatically."
    tradeOId["formattingOptions.formatterUniqueId"] = "IntDefault"
    AddTableValue(dataDisp, tradeOId)
    
    totalIssueSize = dict()
    totalIssueSize["uniqueId"] = "sec_insaddr total_issued"
    totalIssueSize["attributeChain.attributeIds"] = ["sec_insaddr", "total_issued"]
    totalIssueSize["displayInformation.icon"] = "DetailsBase"
    totalIssueSize["displayInformation.label.formatString"] = "Total Issue Size"
    totalIssueSize["displayInformation.description.formatString"] = "Total issue size for a security."
    totalIssueSize["formattingOptions.formatterUniqueId"] = "NumDefault"
    totalIssueSize["formattingOptions.overideNumberOfDecimals"] = 0
    AddTableValue(dataDisp, totalIssueSize)

    amount = dict()
    amount["uniqueId"] = "amount"
    amount["attributeChain.attributeIds"] = ["amount"]
    amount["displayInformation.icon"] = "DetailsBase"
    amount["displayInformation.label.formatString"] = "Amount"
    amount["displayInformation.description.formatString"] = "The amount to be paid."
    amount["formattingOptions.formatterUniqueId"] = "NumDefault"
    amount["formattingOptions.overideNumberOfDecimals"] = 0
    AddTableValue(dataDisp, amount)

    account = dict()
    account["uniqueId"] = "acquirer_accname account"
    account["attributeChain.attributeIds"] = ["acquirer_accname", "account"]
    account["displayInformation.icon"] = "DetailsBase"
    account["displayInformation.label.formatString"] = "Account"
    account["displayInformation.description.formatString"] = "The account number of the account at the depository."
    AddTableValue(dataDisp, account)

    isin = dict()
    isin["uniqueId"] = "instrumentIsin"
    isin["attributeChain.attributeIds"] = ["instrumentIsin"]
    isin["displayInformation.label.formatString"] = "ISIN"
    AddTableValue(dataDisp, isin)

    security = dict()
    security["uniqueId"] = "securityExtAttr"
    security["attributeChain.attributeIds"] = ["securityExtAttr"]
    security["displayInformation.label.formatString"] = "Security"
    AddTableValue(dataDisp, security)
    
    securityNonParent = dict()
    securityNonParent["uniqueId"] = "securityNonParentExtAttr"
    securityNonParent["attributeChain.attributeIds"] = ["securityNonParentExtAttr"]
    securityNonParent["displayInformation.label.formatString"] = "Security Non Parent"
    AddTableValue(dataDisp, securityNonParent)
    
    settledSecurity = dict()
    settledSecurity["uniqueId"] = "settledSecurityExtAttr"
    settledSecurity["attributeChain.attributeIds"] = ["settledSecurityExtAttr"]
    settledSecurity["displayInformation.label.formatString"] = "Settled Security"
    AddTableValue(dataDisp, settledSecurity)

    securityRecentPastSettled = dict()
    securityRecentPastSettled["uniqueId"] = "securityRecentPastSettledExtAttr"
    securityRecentPastSettled["attributeChain.attributeIds"] = ["securityRecentPastSettledExtAttr"]
    securityRecentPastSettled["displayInformation.label.formatString"] = "Security Recent/Past Settled"
    AddTableValue(dataDisp, securityRecentPastSettled)

    oId = dict()
    oId["uniqueId"] = "seqnbr"
    oId["attributeChain.attributeIds"] = ["seqnbr"]
    oId["displayInformation.icon"] = "DetailsBase"
    oId["displayInformation.label.formatString"] = "Settlement Ref"
    oId["displayInformation.description.formatString"] = "Unique internal number identifying this payment, generated \nautomatically."
    oId["formattingOptions.formatterUniqueId"] = "IntDefault"
    AddTableValue(dataDisp, oId)

    # Add Formulas

    custodyPosition = dict()
    custodyPosition["uniqueId"] = "Custody Position"
    custodyPosition["displayInformation.label.formatString"] = "Custody Position"
    custodyPosition["formulaWithFormatting.formula.formulaId"] = "Security Custody Position"
    custodyPosition["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    custodyPosition["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, custodyPosition)

    temporaryIn = dict()
    temporaryIn["uniqueId"] = "Temporary In"
    temporaryIn["displayInformation.label.formatString"] = "Temporary In"
    temporaryIn["formulaWithFormatting.formula.formulaId"] = "Security Temporary In"
    temporaryIn["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    temporaryIn["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, temporaryIn)
    
    temporaryOut = dict()
    temporaryOut["uniqueId"] = "Temporary Out"
    temporaryOut["displayInformation.label.formatString"] = "Temporary Out"
    temporaryOut["formulaWithFormatting.formula.formulaId"] = "Security Temporary Out"
    temporaryOut["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    temporaryOut["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, temporaryOut)

    adjustedBalance = dict()
    adjustedBalance["uniqueId"] = "Adjusted Balance"
    adjustedBalance["displayInformation.label.formatString"] = "Adjusted Balance"
    adjustedBalance["formulaWithFormatting.formula.formulaId"] = "Security Adjusted Balance"
    adjustedBalance["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    adjustedBalance["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, adjustedBalance)

    vaultPosition = dict()
    vaultPosition["uniqueId"] = "Vault Position"
    vaultPosition["displayInformation.label.formatString"] = "Vault Position"
    vaultPosition["formulaWithFormatting.formula.formulaId"] = "Security Vault Position"
    vaultPosition["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    vaultPosition["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, vaultPosition)

    issueOutstanding = dict()
    issueOutstanding["uniqueId"] = "Issue Outstanding"
    issueOutstanding["displayInformation.label.formatString"] = "Issue Outstanding"
    issueOutstanding["formulaWithFormatting.formula.formulaId"] = "Security Issue Outstanding"
    issueOutstanding["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    issueOutstanding["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, issueOutstanding)

    issueAmortization = dict()
    issueAmortization["uniqueId"] = "Issue Amortization"
    issueAmortization["displayInformation.label.formatString"] = "Issue Amortization"
    issueAmortization["formulaWithFormatting.formula.formulaId"] = "Security Issue Amortization"
    issueAmortization["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    issueAmortization["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, issueAmortization)
    
    openPositionsZeroPositions = dict()
    openPositionsZeroPositions["uniqueId"] = "OpenPositions/ZeroPositions"
    openPositionsZeroPositions["displayInformation.label.formatString"] = "OpenPositions/ZeroPositions"
    openPositionsZeroPositions["formulaWithFormatting.formula.formulaId"] = "Security OpenPositions/ZeroPositions"
    AddTableFormulaAndParameterValues(dataDisp, openPositionsZeroPositions)

    # Add Filters
    
    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_accname correspondent_bank_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("instrumentIsin", "string", dict()))
    descendents.append(("securityExtAttr", "bool", dict()))
    descendents.append(("securityNonParentExtAttr", "bool", {"value" : True}))
    descendents.append(("settledSecurityExtAttr", "bool", {"value" : True}))
    descendents.append(("securityRecentPastSettledExtAttr", "string", dict()))
    descendents.append(("sec_insaddr exp_day", "date", {"start" : "0d"}))
    descendents.append(("sec_insaddr issue_day", "date", dict()))
    descendents.append(("sec_insaddr issuer_ptynbr ptyid", "string", dict()))
    descendents.append(("sec_insaddr total_issued", "double", dict()))
    descendents.append(("securityTransactionTypeExtAttr", "string", dict()))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("settled_day", "date", dict()))
    descendents.append(("trdnbr trdnbr", "int", dict()))

    namedFilter = dict()
    namedFilter["uniqueId"] = "e39eac6b-bd8c-4bce-907b-ed8c3428b1e3"
    namedFilter["displayInformation.label.formatString"] = "LiveIssues"
    namedFilter["filter.op"] = "And"
    namedFilter["filter.descendents"] = descendents
    
    AddNamedFilter(dataDisp, namedFilter)

    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_accname correspondent_bank_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("instrumentIsin", "string", dict()))
    descendents.append(("securityExtAttr", "bool", {"value" : True}))
    descendents.append(("securityNonParentExtAttr", "bool", dict()))
    descendents.append(("settledSecurityExtAttr", "bool", dict()))
    descendents.append(("securityRecentPastSettledExtAttr", "string", dict()))
    descendents.append(("sec_insaddr exp_day", "date", dict()))
    descendents.append(("sec_insaddr issue_day", "date", dict()))
    descendents.append(("sec_insaddr issuer_ptynbr ptyid", "string", dict()))
    descendents.append(("sec_insaddr total_issued", "double", dict()))
    descendents.append(("securityTransactionTypeExtAttr", "string", dict()))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("settled_day", "date", dict()))
    descendents.append(("trdnbr trdnbr", "int", dict()))
    
    preFilter = dict()
    preFilter["filter.op"] = "And"
    preFilter["filter.descendents"] = descendents

    AddPreFilter(dataDisp, preFilter)

    ids = list()
    ids.append("acquirer_accname account")
    ids.append("instrumentIsin")
    ids.append("sec_insaddr exp_day")
    ids.append("trdnbr trdnbr")
    ids.append("acquirer_accname correspondent_bank_ptynbr ptyid")
    ids.append("sec_insaddr issuer_ptynbr ptyid")
    ids.append("curr insid")
    ids.append("amount")

    AddQuickFilters(dataDisp, ids)
    
    return storedDataDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreateSettledInventoryDataDisposition(dataDispositionName):
    newDataDisp = acm.FStoredDataDisposition()
    newDataDisp.Name(dataDispositionName)
    newDataDisp.SubType("FrontArena.DbMaster")
    newDataDisp.SetDataDisposition(CreateSettledInventoryDataDispMessage())
    newDataDisp.Commit()
