""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesCustodyInventoryDataDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
import Contracts_Tk_Messages_TkEnumerations as TkEnum
from FOperationsViewerExamplesHelperFunctions import AddTableValue, AddTableFormulaAndParameterValues, AddNamedFilter, AddPreFilter, AddQuickFilters

#-------------------------------------------------------------------------
def CreateCustodyInventoryDataDispMessage():
    
    storedDataDisp = Contracts_Imdr_Messages_ImdrMessages.StoredDataDisposition()

    storedDataDisp.serviceName = "FrontArena.DbMaster"

    storedDataDisp.sheetType.SetInParent()

    storedDataDisp.sheetType.name = "ext.Settlement"

    storedDataDisp.dataDisposition.SetInParent()
    
    dataDisp = storedDataDisp.dataDisposition

    storedDataDisp.version = "b5cfe6a0-94c6-4c16-bdcc-6668d60f2483"

    # Add Table Values

    issuer = dict()
    issuer["uniqueId"] = "sec_insaddr issuer_ptynbr ptyid"
    issuer["attributeChain.attributeIds"] = ["sec_insaddr", "issuer_ptynbr", "ptyid"]
    issuer["displayInformation.icon"] = "DetailsBase"
    issuer["displayInformation.label.formatString"] = "Issuer"
    issuer["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, issuer)

    curr = dict()
    curr["uniqueId"] = "curr insid"
    curr["attributeChain.attributeIds"] = ["curr", "insid"]
    curr["displayInformation.icon"] = "DetailsBase"
    curr["displayInformation.label.formatString"] = "CCY"
    curr["displayInformation.description.formatString"] = "Unique name of instrument. Used to select instrument in \napplications."
    AddTableValue(dataDisp, curr)

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

    amount = dict()
    amount["uniqueId"] = "amount"
    amount["attributeChain.attributeIds"] = ["amount"]
    amount["displayInformation.icon"] = "DetailsBase"
    amount["displayInformation.label.formatString"] = "Amount"
    amount["displayInformation.description.formatString"] = "The amount to be paid."
    amount["formattingOptions.formatterUniqueId"] = "NumDefault"
    amount["formattingOptions.overideNumberOfDecimals"] = 0
    AddTableValue(dataDisp, amount)

    settledDay = dict()
    settledDay["uniqueId"] = "settled_day"
    settledDay["attributeChain.attributeIds"] = ["settled_day"]
    settledDay["displayInformation.icon"] = "DetailsBase"
    settledDay["displayInformation.label.formatString"] = "Settled Day"
    settledDay["displayInformation.description.formatString"] = "The settlement day of a security settlement."
    settledDay["formattingOptions.formatterUniqueId"] = "DateDefault"
    AddTableValue(dataDisp, settledDay)

    oId = dict()
    oId["uniqueId"] = "seqnbr"
    oId["attributeChain.attributeIds"] = ["seqnbr"]
    oId["displayInformation.icon"] = "DetailsBase"
    oId["displayInformation.label.formatString"] = "Settlement Ref"
    oId["displayInformation.description.formatString"] = "Unique internal number identifying this payment, generated \nautomatically."
    oId["formattingOptions.formatterUniqueId"] = "IntDefault"
    AddTableValue(dataDisp, oId)

    account = dict()
    account["uniqueId"] = "acquirer_accname account"
    account["attributeChain.attributeIds"] = ["acquirer_accname", "account"]
    account["displayInformation.icon"] = "DetailsBase"
    account["displayInformation.label.formatString"] = "Account"
    account["displayInformation.description.formatString"] = "The account number of the account at the depository."
    AddTableValue(dataDisp, account)
    
    custodian = dict()
    custodian["uniqueId"] = "acquirer_accname correspondent_bank_ptynbr ptyid"
    custodian["attributeChain.attributeIds"] = ["acquirer_accname", "correspondent_bank_ptynbr", "ptyid"]
    custodian["displayInformation.icon"] = "DetailsBase"
    custodian["displayInformation.label.formatString"] = "Custodian"
    custodian["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, custodian)

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

    securityRecentPastSettled = dict()
    securityRecentPastSettled["uniqueId"] = "securityRecentPastSettledExtAttr"
    securityRecentPastSettled["attributeChain.attributeIds"] = ["securityRecentPastSettledExtAttr"]
    securityRecentPastSettled["displayInformation.label.formatString"] = "Security Recent/Past Settled"
    AddTableValue(dataDisp, securityRecentPastSettled)

    status = dict()
    status["uniqueId"] = "status"
    status["attributeChain.attributeIds"] = ["status"]
    status["displayInformation.icon"] = "DetailsBase"
    status["displayInformation.label.formatString"] = "Status"
    status["displayInformation.description.formatString"] = "The status of this settlement."
    AddTableValue(dataDisp, status)

    primaryIssuance = dict()
    primaryIssuance["uniqueId"] = "trdnbr primary_issuance"
    primaryIssuance["attributeChain.attributeIds"] = ["trdnbr", "primary_issuance"]
    primaryIssuance["displayInformation.icon"] = "DetailsBase"
    primaryIssuance["displayInformation.label.formatString"] = "Trade.Primary Issuance"
    primaryIssuance["displayInformation.description.formatString"] = "Used to decide counterparty when generating TradeAccountLinks."
    primaryIssuance["formattingOptions.formatterUniqueId"] = "BoolDefault"
    AddTableValue(dataDisp, primaryIssuance)

    # Add Formulas

    openZero = dict()
    openZero["uniqueId"] = "OpenPositions/ZeroPositions"
    openZero["displayInformation.label.formatString"] = "OpenPositions/ZeroPositions"
    openZero["formulaWithFormatting.formula.formulaId"] = "Security OpenPositions/ZeroPositions"
    AddTableFormulaAndParameterValues(dataDisp, openZero)
    
    # Add Filters
    
    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_accname correspondent_bank_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("instrumentIsin", "string", dict()))
    descendents.append(("securityExtAttr", "bool", dict()))
    descendents.append(("securityRecentPastSettledExtAttr", "string", dict()))
    descendents.append(("sec_insaddr exp_day", "date", {"start" : "0d"}))
    descendents.append(("sec_insaddr issue_day", "date", dict()))
    descendents.append(("sec_insaddr issuer_ptynbr ptyid", "string", dict()))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("settled_day", "date", dict()))
    descendents.append(("status", "string", dict()))
    descendents.append(("trdnbr primary_issuance", "bool", dict()))

    namedFilter = dict()
    namedFilter["uniqueId"] = "032bb5dc-441b-4307-9b95-d83e75393ad0"
    namedFilter["displayInformation.label.formatString"] = "Non-expired securities"
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
    descendents.append(("securityRecentPastSettledExtAttr", "string", dict()))
    descendents.append(("sec_insaddr exp_day", "date", dict()))
    descendents.append(("sec_insaddr issue_day", "date", dict()))
    descendents.append(("sec_insaddr issuer_ptynbr ptyid", "string", dict()))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("settled_day", "date", dict()))
    descendents.append(("status", "string", {"values" : ["Settled"], "textMatchMode" : TkEnum.TMM_EXACT}))
    descendents.append(("trdnbr primary_issuance", "bool", {"value" : False}))
    
    preFilter = dict()
    preFilter["filter.op"] = "And"
    preFilter["filter.descendents"] = descendents

    AddPreFilter(dataDisp, preFilter)

    ids = list()
    ids.append("acquirer_accname account")
    ids.append("instrumentIsin")
    ids.append("sec_insaddr exp_day")
    ids.append("seqnbr")
    ids.append("acquirer_accname correspondent_bank_ptynbr ptyid")
    ids.append("sec_insaddr issuer_ptynbr ptyid")
    ids.append("curr insid")
    ids.append("amount")

    AddQuickFilters(dataDisp, ids)
    
    return storedDataDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreateCustodyInventoryDataDisposition(dataDispositionName):
    newDataDisp = acm.FStoredDataDisposition()
    newDataDisp.Name(dataDispositionName)
    newDataDisp.SubType("FrontArena.DbMaster")
    newDataDisp.SetDataDisposition(CreateCustodyInventoryDataDispMessage())
    newDataDisp.Commit()
