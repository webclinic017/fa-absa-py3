""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesPlannedVsActualDataDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
import Contracts_Tk_Messages_TkEnumerations as TkEnum
from FOperationsViewerExamplesHelperFunctions import AddTableValue, AddTableFormulaAndParameterValues, AddNamedFilter, AddPreFilter, AddQuickFilters

#-------------------------------------------------------------------------
def CreatePlannedVsActualDataDispMessage():
    
    storedDataDisp = Contracts_Imdr_Messages_ImdrMessages.StoredDataDisposition()

    storedDataDisp.serviceName = "FrontArena.DbMaster"

    storedDataDisp.sheetType.SetInParent()

    storedDataDisp.sheetType.name = "ext.Settlement"

    storedDataDisp.dataDisposition.SetInParent()
    
    dataDisp = storedDataDisp.dataDisposition

    storedDataDisp.version = "50a798ff-d211-41a8-b4a5-7700a9fe463e"

    # Add Table Values

    tradeOId = dict()
    tradeOId["uniqueId"] = "trdnbr trdnbr"
    tradeOId["attributeChain.attributeIds"] = ["trdnbr", "trdnbr"]
    tradeOId["displayInformation.icon"] = "DetailsBase"
    tradeOId["displayInformation.label.formatString"] = "Trade Ref"
    tradeOId["displayInformation.description.formatString"] = "Unique internal number identifying this trade, generated \nautomatically."
    tradeOId["formattingOptions.formatterUniqueId"] = "IntDefault"
    AddTableValue(dataDisp, tradeOId)

    currency = dict()
    currency["uniqueId"] = "curr insid"
    currency["attributeChain.attributeIds"] = ["curr", "insid"]
    currency["displayInformation.icon"] = "DetailsBase"
    currency["displayInformation.label.formatString"] = "CCY"
    currency["displayInformation.description.formatString"] = "Unique name of instrument. Used to select instrument in \napplications."
    AddTableValue(dataDisp, currency)

    valueDay = dict()
    valueDay["uniqueId"] = "value_day"
    valueDay["attributeChain.attributeIds"] = ["value_day"]
    valueDay["displayInformation.icon"] = "DetailsBase"
    valueDay["displayInformation.label.formatString"] = "Value Day"
    valueDay["displayInformation.description.formatString"] = "Day when this settlement is to be paid."
    valueDay["formattingOptions.formatterUniqueId"] = "DateDefault"
    AddTableValue(dataDisp, valueDay)

    account = dict()
    account["uniqueId"] = "acquirer_accname account"
    account["attributeChain.attributeIds"] = ["acquirer_accname", "account"]
    account["displayInformation.icon"] = "DetailsBase"
    account["displayInformation.label.formatString"] = "Account"
    account["displayInformation.description.formatString"] = "The account number of the account at the depository."
    AddTableValue(dataDisp, account)

    amount = dict()
    amount["uniqueId"] = "amount"
    amount["attributeChain.attributeIds"] = ["amount"]
    amount["displayInformation.icon"] = "DetailsBase"
    amount["displayInformation.label.formatString"] = "Amount"
    amount["displayInformation.description.formatString"] = "The amount to be paid."
    amount["formattingOptions.formatterUniqueId"] = "NumDefault"
    amount["formattingOptions.overideNumberOfDecimals"] = 0
    AddTableValue(dataDisp, amount)
    
    counterParty = dict()
    counterParty["uniqueId"] = "counterparty_ptynbr ptyid"
    counterParty["attributeChain.attributeIds"] = ["counterparty_ptynbr", "ptyid"]
    counterParty["displayInformation.icon"] = "DetailsBase"
    counterParty["displayInformation.label.formatString"] = "Counterparty"
    counterParty["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, counterParty)
    
    custodian = dict()
    custodian["uniqueId"] = "acquirer_accname correspondent_bank_ptynbr ptyid"
    custodian["attributeChain.attributeIds"] = ["acquirer_accname", "correspondent_bank_ptynbr", "ptyid"]
    custodian["displayInformation.icon"] = "DetailsBase"
    custodian["displayInformation.label.formatString"] = "Custodian"
    custodian["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, custodian)

    expiryDay = dict()
    expiryDay["uniqueId"] = "sec_insaddr exp_day"
    expiryDay["attributeChain.attributeIds"] = ["sec_insaddr", "exp_day"]
    expiryDay["displayInformation.icon"] = "DetailsBase"
    expiryDay["displayInformation.label.formatString"] = "Expiry Day"
    expiryDay["displayInformation.description.formatString"] = "Expiry date for non-generic instruments."
    expiryDay["formattingOptions.formatterUniqueId"] = "DateDefault"
    AddTableValue(dataDisp, expiryDay)

    activeSecurity = dict()
    activeSecurity["uniqueId"] = "activeSecurityExtAttr"
    activeSecurity["attributeChain.attributeIds"] = ["activeSecurityExtAttr"]
    activeSecurity["displayInformation.label.formatString"] = "Active Security"
    AddTableValue(dataDisp, activeSecurity)
    
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

    tradePrimaryIssuance = dict()
    tradePrimaryIssuance["uniqueId"] = "trdnbr primary_issuance"
    tradePrimaryIssuance["attributeChain.attributeIds"] = ["trdnbr", "primary_issuance"]
    tradePrimaryIssuance["displayInformation.icon"] = "DetailsBase"
    tradePrimaryIssuance["displayInformation.label.formatString"] = "Trade.Primary Issuance"
    tradePrimaryIssuance["displayInformation.description.formatString"] = "Used to decide counterparty when generating TradeAccountLinks."
    tradePrimaryIssuance["formattingOptions.formatterUniqueId"] = "BoolDefault"
    AddTableValue(dataDisp, tradePrimaryIssuance)

    unSettledSettledSecurity = dict()
    unSettledSettledSecurity["uniqueId"] = "securityUnSettledSettledExtAttr"
    unSettledSettledSecurity["attributeChain.attributeIds"] = ["securityUnSettledSettledExtAttr"]
    unSettledSettledSecurity["displayInformation.label.formatString"] = "Security UnSettled/Settled"
    AddTableValue(dataDisp, unSettledSettledSecurity)

    # Add Formulas

    settledPosition = dict()
    settledPosition["uniqueId"] = "Settled Position"
    settledPosition["displayInformation.label.formatString"] = "Settled Position"
    settledPosition["formulaWithFormatting.formula.formulaId"] = "Security Settled Position"
    settledPosition["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    settledPosition["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, settledPosition)

    failedDeliveries = dict()
    failedDeliveries["uniqueId"] = "Failed Deliveries"
    failedDeliveries["displayInformation.label.formatString"] = "Failed Deliveries"
    failedDeliveries["formulaWithFormatting.formula.formulaId"] = "Security Failed Deliveries"
    failedDeliveries["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    failedDeliveries["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, failedDeliveries)

    failedReceipts = dict()
    failedReceipts["uniqueId"] = "Failed Receipts"
    failedReceipts["displayInformation.label.formatString"] = "Failed Receipts"
    failedReceipts["formulaWithFormatting.formula.formulaId"] = "Security Failed Receipts"
    failedReceipts["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    failedReceipts["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, failedReceipts)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 0
    
    toBeDeliveredToday = dict()
    toBeDeliveredToday["uniqueId"] = "To Be Delivered Today"
    toBeDeliveredToday["displayInformation.label.formatString"] = "To Be Delivered Today"
    toBeDeliveredToday["formulaWithFormatting.formula.formulaId"] = "Security To Be Delivered XD"
    toBeDeliveredToday["formulaWithFormatting.formula.values"] = [parameter]
    toBeDeliveredToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeDeliveredToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeDeliveredToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 0
    
    toBeReceivedToday = dict()
    toBeReceivedToday["uniqueId"] = "To Be Received Today"
    toBeReceivedToday["displayInformation.label.formatString"] = "To Be Received Today"
    toBeReceivedToday["formulaWithFormatting.formula.formulaId"] = "Security To Be Received XD"
    toBeReceivedToday["formulaWithFormatting.formula.values"] = [parameter]
    toBeReceivedToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeReceivedToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeReceivedToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 0
    
    projectedPositionToday = dict()
    projectedPositionToday["uniqueId"] = "Projected Position Today"
    projectedPositionToday["displayInformation.label.formatString"] = "Projected Position Today"
    projectedPositionToday["formulaWithFormatting.formula.formulaId"] = "Security Projected Position XD"
    projectedPositionToday["formulaWithFormatting.formula.values"] = [parameter]
    projectedPositionToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    projectedPositionToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, projectedPositionToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 1
    
    toBeDelivered1D = dict()
    toBeDelivered1D["uniqueId"] = "To Be Delivered 1D"
    toBeDelivered1D["displayInformation.label.formatString"] = "To Be Delivered 1D"
    toBeDelivered1D["formulaWithFormatting.formula.formulaId"] = "Security To Be Delivered XD"
    toBeDelivered1D["formulaWithFormatting.formula.values"] = [parameter]
    toBeDelivered1D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeDelivered1D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeDelivered1D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 1
    
    toBeReceived1D = dict()
    toBeReceived1D["uniqueId"] = "To Be Received 1D"
    toBeReceived1D["displayInformation.label.formatString"] = "To Be Received 1D"
    toBeReceived1D["formulaWithFormatting.formula.formulaId"] = "Security To Be Received XD"
    toBeReceived1D["formulaWithFormatting.formula.values"] = [parameter]
    toBeReceived1D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeReceived1D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeReceived1D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 1
    
    projectedPosition1D = dict()
    projectedPosition1D["uniqueId"] = "Projected Position 1D"
    projectedPosition1D["displayInformation.label.formatString"] = "Projected Position 1D"
    projectedPosition1D["formulaWithFormatting.formula.formulaId"] = "Security Projected Position XD"
    projectedPosition1D["formulaWithFormatting.formula.values"] = [parameter]
    projectedPosition1D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    projectedPosition1D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, projectedPosition1D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 2
    
    toBeDelivered2D = dict()
    toBeDelivered2D["uniqueId"] = "To Be Delivered 2D"
    toBeDelivered2D["displayInformation.label.formatString"] = "To Be Delivered 2D"
    toBeDelivered2D["formulaWithFormatting.formula.formulaId"] = "Security To Be Delivered XD"
    toBeDelivered2D["formulaWithFormatting.formula.values"] = [parameter]
    toBeDelivered2D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeDelivered2D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeDelivered2D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 2
    
    toBeReceived2D = dict()
    toBeReceived2D["uniqueId"] = "To Be Received 2D"
    toBeReceived2D["displayInformation.label.formatString"] = "To Be Received 2D"
    toBeReceived2D["formulaWithFormatting.formula.formulaId"] = "Security To Be Received XD"
    toBeReceived2D["formulaWithFormatting.formula.values"] = [parameter]
    toBeReceived2D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeReceived2D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeReceived2D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 2
    
    projectedPosition2D = dict()
    projectedPosition2D["uniqueId"] = "Projected Position 2D"
    projectedPosition2D["displayInformation.label.formatString"] = "Projected Position 2D"
    projectedPosition2D["formulaWithFormatting.formula.formulaId"] = "Security Projected Position XD"
    projectedPosition2D["formulaWithFormatting.formula.values"] = [parameter]
    projectedPosition2D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    projectedPosition2D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, projectedPosition2D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 3
    
    toBeDelivered3D = dict()
    toBeDelivered3D["uniqueId"] = "To Be Delivered 3D"
    toBeDelivered3D["displayInformation.label.formatString"] = "To Be Delivered 3D"
    toBeDelivered3D["formulaWithFormatting.formula.formulaId"] = "Security To Be Delivered XD"
    toBeDelivered3D["formulaWithFormatting.formula.values"] = [parameter]
    toBeDelivered3D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeDelivered3D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeDelivered3D)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 3
    
    toBeReceived3D = dict()
    toBeReceived3D["uniqueId"] = "To Be Received 3D"
    toBeReceived3D["displayInformation.label.formatString"] = "To Be Received 3D"
    toBeReceived3D["formulaWithFormatting.formula.formulaId"] = "Security To Be Received XD"
    toBeReceived3D["formulaWithFormatting.formula.values"] = [parameter]
    toBeReceived3D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeReceived3D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeReceived3D)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 3
    
    projectedPosition3D = dict()
    projectedPosition3D["uniqueId"] = "Projected Position 3D"
    projectedPosition3D["displayInformation.label.formatString"] = "Projected Position 3D"
    projectedPosition3D["formulaWithFormatting.formula.formulaId"] = "Security Projected Position XD"
    projectedPosition3D["formulaWithFormatting.formula.values"] = [parameter]
    projectedPosition3D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    projectedPosition3D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, projectedPosition3D)
    
    failedSettlements = dict()
    failedSettlements["uniqueId"] = "Failed Settlements"
    failedSettlements["displayInformation.label.formatString"] = "Failed Settlements"
    failedSettlements["formulaWithFormatting.formula.formulaId"] = "Security Failed Settlements"
    failedSettlements["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    failedSettlements["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, failedSettlements)
    
    settledToday = dict()
    settledToday["uniqueId"] = "Settled Today"
    settledToday["displayInformation.label.formatString"] = "Settled Today"
    settledToday["formulaWithFormatting.formula.formulaId"] = "Security Settled Today"
    settledToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    settledToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, settledToday)
    
    totalUnSettledToday = dict()
    totalUnSettledToday["uniqueId"] = "Total UnSettled Today"
    totalUnSettledToday["displayInformation.label.formatString"] = "Total UnSettled Today"
    totalUnSettledToday["formulaWithFormatting.formula.formulaId"] = "Security Total UnSettled Today"
    totalUnSettledToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    totalUnSettledToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, totalUnSettledToday)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 0
    
    toBeSettledToday = dict()
    toBeSettledToday["uniqueId"] = "To Be Settled Today"
    toBeSettledToday["displayInformation.label.formatString"] = "To Be Settled Today"
    toBeSettledToday["formulaWithFormatting.formula.formulaId"] = "Security To Be Settled XD"
    toBeSettledToday["formulaWithFormatting.formula.values"] = [parameter]
    toBeSettledToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeSettledToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeSettledToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 1
    
    toBeSettled1D = dict()
    toBeSettled1D["uniqueId"] = "To Be Settled 1D"
    toBeSettled1D["displayInformation.label.formatString"] = "To Be Settled 1D"
    toBeSettled1D["formulaWithFormatting.formula.formulaId"] = "Security To Be Settled XD"
    toBeSettled1D["formulaWithFormatting.formula.values"] = [parameter]
    toBeSettled1D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeSettled1D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeSettled1D)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 2
    
    toBeSettled2D = dict()
    toBeSettled2D["uniqueId"] = "To Be Settled 2D"
    toBeSettled2D["displayInformation.label.formatString"] = "To Be Settled 2D"
    toBeSettled2D["formulaWithFormatting.formula.formulaId"] = "Security To Be Settled XD"
    toBeSettled2D["formulaWithFormatting.formula.values"] = [parameter]
    toBeSettled2D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeSettled2D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeSettled2D)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 3
    
    toBeSettled3D = dict()
    toBeSettled3D["uniqueId"] = "To Be Settled 3D"
    toBeSettled3D["displayInformation.label.formatString"] = "To Be Settled 3D"
    toBeSettled3D["formulaWithFormatting.formula.formulaId"] = "Security To Be Settled XD"
    toBeSettled3D["formulaWithFormatting.formula.values"] = [parameter]
    toBeSettled3D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    toBeSettled3D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 0
    AddTableFormulaAndParameterValues(dataDisp, toBeSettled3D)

    activityNoActivity = dict()
    activityNoActivity["uniqueId"] = "Activity/NoActivity"
    activityNoActivity["displayInformation.label.formatString"] = "Activity/NoActivity"
    activityNoActivity["formulaWithFormatting.formula.formulaId"] = "Security Activity/NoActivity"
    AddTableFormulaAndParameterValues(dataDisp, activityNoActivity)

    # Add Filters
    
    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_accname correspondent_bank_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("counterparty_ptynbr ptyid", "string", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("instrumentIsin", "string", dict()))
    descendents.append(("activeSecurityExtAttr", "bool", {"value" : True}))
    descendents.append(("securityExtAttr", "bool", dict()))
    descendents.append(("securityNonParentExtAttr", "bool", {"value" : True}))
    descendents.append(("sec_insaddr exp_day", "date", {"start" : "0d"}))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("settled_day", "date", dict()))
    descendents.append(("trdnbr primary_issuance", "bool", {"isNot" : True, "value" : True}))
    descendents.append(("trdnbr trdnbr", "int", dict()))
    descendents.append(("securityUnSettledSettledExtAttr", "string", dict()))
    descendents.append(("value_day", "date", dict()))

    namedFilter = dict()
    namedFilter["uniqueId"] = "e5ccbc5a-2516-4b66-9a26-caf3e630f83b"
    namedFilter["displayInformation.label.formatString"] = "LiveCustodyDeals"
    namedFilter["filter.op"] = "And"
    namedFilter["filter.descendents"] = descendents
    
    AddNamedFilter(dataDisp, namedFilter)
    
    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_accname correspondent_bank_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("counterparty_ptynbr ptyid", "string", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("instrumentIsin", "string", dict()))
    descendents.append(("activeSecurityExtAttr", "bool", {"value" : True}))
    descendents.append(("securityExtAttr", "bool", dict()))
    descendents.append(("securityNonParentExtAttr", "bool", {"value" : True}))
    descendents.append(("sec_insaddr exp_day", "date", {"start" : "0d"}))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("settled_day", "date", dict()))
    descendents.append(("trdnbr primary_issuance", "bool", {"value" : True}))
    descendents.append(("trdnbr trdnbr", "int", dict()))
    descendents.append(("securityUnSettledSettledExtAttr", "string", dict()))
    descendents.append(("value_day", "date", dict()))

    namedFilter = dict()
    namedFilter["uniqueId"] = "a1e5d2f6-2916-4ae9-b9eb-32eecc501781"
    namedFilter["displayInformation.label.formatString"] = "LiveOwnIssues"
    namedFilter["filter.op"] = "And"
    namedFilter["filter.descendents"] = descendents
    
    AddNamedFilter(dataDisp, namedFilter)

    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_accname correspondent_bank_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("counterparty_ptynbr ptyid", "string", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("instrumentIsin", "string", dict()))
    descendents.append(("activeSecurityExtAttr", "bool", dict()))
    descendents.append(("securityExtAttr", "bool", {"value" : True}))
    descendents.append(("securityNonParentExtAttr", "bool", dict()))
    descendents.append(("sec_insaddr exp_day", "date", dict()))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("settled_day", "date", dict()))
    descendents.append(("trdnbr primary_issuance", "bool", dict()))
    descendents.append(("trdnbr trdnbr", "int", dict()))
    descendents.append(("securityUnSettledSettledExtAttr", "string", dict()))
    descendents.append(("value_day", "date", dict()))
    
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
    ids.append("counterparty_ptynbr ptyid")
    ids.append("curr insid")
    ids.append("amount")

    AddQuickFilters(dataDisp, ids)
    
    return storedDataDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreatePlannedVsActualDataDisposition(dataDispositionName):
    newDataDisp = acm.FStoredDataDisposition()
    newDataDisp.Name(dataDispositionName)
    newDataDisp.SubType("FrontArena.DbMaster")
    newDataDisp.SetDataDisposition(CreatePlannedVsActualDataDispMessage())
    newDataDisp.Commit()
