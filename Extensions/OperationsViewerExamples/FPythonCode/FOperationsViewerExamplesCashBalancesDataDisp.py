""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesCashBalancesDataDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
import Contracts_Tk_Messages_TkEnumerations as TkEnum
from FOperationsViewerExamplesHelperFunctions import AddTableValue, AddTableFormulaAndParameterValues, AddNamedFilter, AddPreFilter, AddQuickFilters

#-------------------------------------------------------------------------
def CreateCashBalancesDataDispMessage():
    
    storedDataDisp = Contracts_Imdr_Messages_ImdrMessages.StoredDataDisposition()

    storedDataDisp.serviceName = "FrontArena.DbMaster"

    storedDataDisp.sheetType.SetInParent()

    storedDataDisp.sheetType.name = "ext.Settlement"

    storedDataDisp.dataDisposition.SetInParent()
    
    dataDisp = storedDataDisp.dataDisposition

    storedDataDisp.version = "292a019e-47ab-45f4-a254-e91933232a5c"

    # Add Table Values

    account = dict()
    account["uniqueId"] = "acquirer_accname account"
    account["attributeChain.attributeIds"] = ["acquirer_accname", "account"]
    account["displayInformation.icon"] = "DetailsBase"
    account["displayInformation.label.formatString"] = "Account"
    account["displayInformation.description.formatString"] = "The account number of the account at the depository."
    AddTableValue(dataDisp, account)
    
    acquirer = dict()
    acquirer["uniqueId"] = "acquirer_ptynbr ptyid"
    acquirer["attributeChain.attributeIds"] = ["acquirer_ptynbr", "ptyid"]
    acquirer["displayInformation.icon"] = "DetailsBase"
    acquirer["displayInformation.label.formatString"] = "Acquirer"
    acquirer["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, acquirer)

    amount = dict()
    amount["uniqueId"] = "amount"
    amount["attributeChain.attributeIds"] = ["amount"]
    amount["displayInformation.icon"] = "DetailsBase"
    amount["displayInformation.label.formatString"] = "Amount"
    amount["displayInformation.description.formatString"] = "The amount to be paid."
    amount["formattingOptions.formatterUniqueId"] = "NumDefault"
    amount["formattingOptions.overideNumberOfDecimals"] = 2
    AddTableValue(dataDisp, amount)

    currency = dict()
    currency["uniqueId"] = "curr insid"
    currency["attributeChain.attributeIds"] = ["curr", "insid"]
    currency["displayInformation.icon"] = "DetailsBase"
    currency["displayInformation.label.formatString"] = "CCY"
    currency["displayInformation.description.formatString"] = "Unique name of instrument. Used to select instrument in \napplications."
    AddTableValue(dataDisp, currency)
    
    counterparty = dict()
    counterparty["uniqueId"] = "counterparty_ptynbr ptyid"
    counterparty["attributeChain.attributeIds"] = ["counterparty_ptynbr", "ptyid"]
    counterparty["displayInformation.icon"] = "DetailsBase"
    counterparty["displayInformation.label.formatString"] = "Counterparty"
    counterparty["displayInformation.description.formatString"] = "Unique name of party."
    AddTableValue(dataDisp, counterparty)

    activeCash = dict()
    activeCash["uniqueId"] = "activeCashExtAttr"
    activeCash["attributeChain.attributeIds"] = ["activeCashExtAttr"]
    activeCash["displayInformation.label.formatString"] = "Active Cash"
    AddTableValue(dataDisp, activeCash)

    cash = dict()
    cash["uniqueId"] = "cashExtAttr"
    cash["attributeChain.attributeIds"] = ["cashExtAttr"]
    cash["displayInformation.label.formatString"] = "Cash"
    AddTableValue(dataDisp, cash)

    oId = dict()
    oId["uniqueId"] = "seqnbr"
    oId["attributeChain.attributeIds"] = ["seqnbr"]
    oId["displayInformation.icon"] = "DetailsBase"
    oId["displayInformation.label.formatString"] = "Settlement Ref"
    oId["displayInformation.description.formatString"] = "Unique internal number identifying this payment, generated \nautomatically."
    oId["formattingOptions.formatterUniqueId"] = "IntDefault"
    AddTableValue(dataDisp, oId)
    
    cashUnSettledSettled = dict()
    cashUnSettledSettled["uniqueId"] = "cashUnSettledSettledExtAttr"
    cashUnSettledSettled["attributeChain.attributeIds"] = ["cashUnSettledSettledExtAttr"]
    cashUnSettledSettled["displayInformation.label.formatString"] = "Cash UnSettled/Settled"
    AddTableValue(dataDisp, cashUnSettledSettled)

    valueDay = dict()
    valueDay["uniqueId"] = "value_day"
    valueDay["attributeChain.attributeIds"] = ["value_day"]
    valueDay["displayInformation.icon"] = "DetailsBase"
    valueDay["displayInformation.label.formatString"] = "Value Day"
    valueDay["displayInformation.description.formatString"] = "Day when this settlement is to be paid."
    valueDay["formattingOptions.formatterUniqueId"] = "DateDefault"
    AddTableValue(dataDisp, valueDay)
    
    # Add Formulas
    
    cashOpeningBalanceToday = dict()
    cashOpeningBalanceToday["uniqueId"] = "Opening Balance Today"
    cashOpeningBalanceToday["displayInformation.label.formatString"] = "Opening Balance Today"
    cashOpeningBalanceToday["formulaWithFormatting.formula.formulaId"] = "Cash Opening Balance Today"
    cashOpeningBalanceToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashOpeningBalanceToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashOpeningBalanceToday)

    cashFailedToReceive = dict()
    cashFailedToReceive["uniqueId"] = "Failed To Receive"
    cashFailedToReceive["displayInformation.label.formatString"] = "Failed To Receive"
    cashFailedToReceive["formulaWithFormatting.formula.formulaId"] = "Cash Failed To Receive"
    cashFailedToReceive["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashFailedToReceive["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashFailedToReceive)
    
    cashFailedToPay = dict()
    cashFailedToPay["uniqueId"] = "Failed To Pay"
    cashFailedToPay["displayInformation.label.formatString"] = "Failed To Pay"
    cashFailedToPay["formulaWithFormatting.formula.formulaId"] = "Cash Failed To Pay"
    cashFailedToPay["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashFailedToPay["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashFailedToPay)
    
    cashReceivedToday = dict()
    cashReceivedToday["uniqueId"] = "Received Today"
    cashReceivedToday["displayInformation.label.formatString"] = "Received Today"
    cashReceivedToday["formulaWithFormatting.formula.formulaId"] = "Cash Received Today"
    cashReceivedToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashReceivedToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashReceivedToday)
    
    cashPaidToday = dict()
    cashPaidToday["uniqueId"] = "Paid Today"
    cashPaidToday["displayInformation.label.formatString"] = "Paid Today"
    cashPaidToday["formulaWithFormatting.formula.formulaId"] = "Cash Paid Today"
    cashPaidToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashPaidToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashPaidToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 0
    
    cashToReceiveToday = dict()
    cashToReceiveToday["uniqueId"] = "To Receive Today"
    cashToReceiveToday["displayInformation.label.formatString"] = "To Receive Today"
    cashToReceiveToday["formulaWithFormatting.formula.formulaId"] = "Cash To Receive XD"
    cashToReceiveToday["formulaWithFormatting.formula.values"] = [parameter]
    cashToReceiveToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToReceiveToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToReceiveToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 0
    
    cashToPayToday = dict()
    cashToPayToday["uniqueId"] = "To Pay Today"
    cashToPayToday["displayInformation.label.formatString"] = "To Pay Today"
    cashToPayToday["formulaWithFormatting.formula.formulaId"] = "Cash To Pay XD"
    cashToPayToday["formulaWithFormatting.formula.values"] = [parameter]
    cashToPayToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToPayToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToPayToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 0
    
    cashClosingBalanceToday = dict()
    cashClosingBalanceToday["uniqueId"] = "Closing Balance Today"
    cashClosingBalanceToday["displayInformation.label.formatString"] = "Closing Balance Today"
    cashClosingBalanceToday["formulaWithFormatting.formula.formulaId"] = "Cash Closing Balance XD"
    cashClosingBalanceToday["formulaWithFormatting.formula.values"] = [parameter]
    cashClosingBalanceToday["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashClosingBalanceToday["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashClosingBalanceToday)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 1
    
    cashToReceive1D = dict()
    cashToReceive1D["uniqueId"] = "To Receive 1D"
    cashToReceive1D["displayInformation.label.formatString"] = "To Receive 1D"
    cashToReceive1D["formulaWithFormatting.formula.formulaId"] = "Cash To Receive XD"
    cashToReceive1D["formulaWithFormatting.formula.values"] = [parameter]
    cashToReceive1D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToReceive1D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToReceive1D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 1
    
    cashToPay1D = dict()
    cashToPay1D["uniqueId"] = "To Pay 1D"
    cashToPay1D["displayInformation.label.formatString"] = "To Pay 1D"
    cashToPay1D["formulaWithFormatting.formula.formulaId"] = "Cash To Pay XD"
    cashToPay1D["formulaWithFormatting.formula.values"] = [parameter]
    cashToPay1D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToPay1D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToPay1D)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 1
    
    cashClosingBalance1D = dict()
    cashClosingBalance1D["uniqueId"] = "Closing Balance 1D"
    cashClosingBalance1D["displayInformation.label.formatString"] = "Closing Balance 1D"
    cashClosingBalance1D["formulaWithFormatting.formula.formulaId"] = "Cash Closing Balance XD"
    cashClosingBalance1D["formulaWithFormatting.formula.values"] = [parameter]
    cashClosingBalance1D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashClosingBalance1D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashClosingBalance1D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 2
    
    cashToReceive2D = dict()
    cashToReceive2D["uniqueId"] = "To Receive 2D"
    cashToReceive2D["displayInformation.label.formatString"] = "To Receive 2D"
    cashToReceive2D["formulaWithFormatting.formula.formulaId"] = "Cash To Receive XD"
    cashToReceive2D["formulaWithFormatting.formula.values"] = [parameter]
    cashToReceive2D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToReceive2D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToReceive2D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 2
    
    cashToPay2D = dict()
    cashToPay2D["uniqueId"] = "To Pay 2D"
    cashToPay2D["displayInformation.label.formatString"] = "To Pay 2D"
    cashToPay2D["formulaWithFormatting.formula.formulaId"] = "Cash To Pay XD"
    cashToPay2D["formulaWithFormatting.formula.values"] = [parameter]
    cashToPay2D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToPay2D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToPay2D)
    
    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 2
    
    cashClosingBalance2D = dict()
    cashClosingBalance2D["uniqueId"] = "Closing Balance 2D"
    cashClosingBalance2D["displayInformation.label.formatString"] = "Closing Balance 2D"
    cashClosingBalance2D["formulaWithFormatting.formula.formulaId"] = "Cash Closing Balance XD"
    cashClosingBalance2D["formulaWithFormatting.formula.values"] = [parameter]
    cashClosingBalance2D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashClosingBalance2D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashClosingBalance2D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 3
    
    cashToReceive3D = dict()
    cashToReceive3D["uniqueId"] = "To Receive 3D"
    cashToReceive3D["displayInformation.label.formatString"] = "To Receive 3D"
    cashToReceive3D["formulaWithFormatting.formula.formulaId"] = "Cash To Receive XD"
    cashToReceive3D["formulaWithFormatting.formula.values"] = [parameter]
    cashToReceive3D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToReceive3D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToReceive3D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 3
    
    cashToPay3D = dict()
    cashToPay3D["uniqueId"] = "To Pay 3D"
    cashToPay3D["displayInformation.label.formatString"] = "To Pay 3D"
    cashToPay3D["formulaWithFormatting.formula.formulaId"] = "Cash To Pay XD"
    cashToPay3D["formulaWithFormatting.formula.values"] = [parameter]
    cashToPay3D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToPay3D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToPay3D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 3
    
    cashClosingBalance3D = dict()
    cashClosingBalance3D["uniqueId"] = "Closing Balance 3D"
    cashClosingBalance3D["displayInformation.label.formatString"] = "Closing Balance 3D"
    cashClosingBalance3D["formulaWithFormatting.formula.formulaId"] = "Cash Closing Balance XD"
    cashClosingBalance3D["formulaWithFormatting.formula.values"] = [parameter]
    cashClosingBalance3D["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashClosingBalance3D["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashClosingBalance3D)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 4
    
    cashToReceiveFuture = dict()
    cashToReceiveFuture["uniqueId"] = "To Receive Future"
    cashToReceiveFuture["displayInformation.label.formatString"] = "To Receive Future"
    cashToReceiveFuture["formulaWithFormatting.formula.formulaId"] = "Cash To Receive Future"
    cashToReceiveFuture["formulaWithFormatting.formula.values"] = [parameter]
    cashToReceiveFuture["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToReceiveFuture["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToReceiveFuture)

    parameter = dict()
    parameter["parameterId"] = "X"
    parameter["value.type"] = TkEnum.PVT_INT32
    parameter["value.int32Value"] = 4
    
    cashToPayFuture = dict()
    cashToPayFuture["uniqueId"] = "To Pay Future"
    cashToPayFuture["displayInformation.label.formatString"] = "To Pay Future"
    cashToPayFuture["formulaWithFormatting.formula.formulaId"] = "Cash To Pay Future"
    cashToPayFuture["formulaWithFormatting.formula.values"] = [parameter]
    cashToPayFuture["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashToPayFuture["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashToPayFuture)
    
    cashClosingBalanceFuture = dict()
    cashClosingBalanceFuture["uniqueId"] = "Closing Balance Future"
    cashClosingBalanceFuture["displayInformation.label.formatString"] = "Closing Balance Future"
    cashClosingBalanceFuture["formulaWithFormatting.formula.formulaId"] = "Cash Closing Balance Future"
    cashClosingBalanceFuture["formulaWithFormatting.formattingOptions.formatterUniqueId"] = "NumDefault"
    cashClosingBalanceFuture["formulaWithFormatting.formattingOptions.overideNumberOfDecimals"] = 2
    AddTableFormulaAndParameterValues(dataDisp, cashClosingBalanceFuture)

    activeNotActiveCash = dict()
    activeNotActiveCash["uniqueId"] = "Active/NotActive"
    activeNotActiveCash["displayInformation.label.formatString"] = "Active/NotActive"
    activeNotActiveCash["formulaWithFormatting.formula.formulaId"] = "Cash Active/NotActive"
    AddTableFormulaAndParameterValues(dataDisp, activeNotActiveCash)
    
    # Add Filters
    
    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("counterparty_ptynbr ptyid", "string", dict()))
    descendents.append(("cashExtAttr", "bool", dict()))
    descendents.append(("activeCashExtAttr", "bool", {"value" : True}))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("value_day", "date", dict()))
    descendents.append(("cashUnSettledSettledExtAttr", "string", dict()))

    namedFilter = dict()
    namedFilter["uniqueId"] = "cc89f7d7-81b4-4faf-b44d-7142dcde3a52"  
    namedFilter["displayInformation.label.formatString"] = "All CCY"
    namedFilter["filter.op"] = "And"
    namedFilter["filter.descendents"] = descendents
    
    AddNamedFilter(dataDisp, namedFilter)
    
    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("curr insid", "string", {"values" : ["USD", "EUR"], "textMatchMode" : TkEnum.TMM_EXACT}))
    descendents.append(("counterparty_ptynbr ptyid", "string", dict()))
    descendents.append(("cashExtAttr", "bool", dict()))
    descendents.append(("activeCashExtAttr", "bool", {"value" : True}))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("value_day", "date", dict()))
    descendents.append(("cashUnSettledSettledExtAttr", "string", dict()))

    namedFilter = dict()
    namedFilter["uniqueId"] = "f45f10da-c010-4ce3-994f-29aa93de6a88"  
    namedFilter["displayInformation.label.formatString"] = "Major CCY"
    namedFilter["filter.op"] = "And"
    namedFilter["filter.descendents"] = descendents
    
    AddNamedFilter(dataDisp, namedFilter)
    
    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("curr insid", "string", {"values" : ["USD", "EUR"], "isNot" : True, "textMatchMode" : TkEnum.TMM_EXACT}))
    descendents.append(("counterparty_ptynbr ptyid", "string", dict()))
    descendents.append(("cashExtAttr", "bool", dict()))
    descendents.append(("activeCashExtAttr", "bool", {"value" : True}))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("value_day", "date", dict()))
    descendents.append(("cashUnSettledSettledExtAttr", "string", dict()))

    namedFilter = dict()
    namedFilter["uniqueId"] = "a6798d5c-e72f-4504-ab09-e5825211c89f"  
    namedFilter["displayInformation.label.formatString"] = "Minor CCY"
    namedFilter["filter.op"] = "And"
    namedFilter["filter.descendents"] = descendents
    
    AddNamedFilter(dataDisp, namedFilter)

    descendents = list()
    descendents.append(("acquirer_accname account", "string", dict()))
    descendents.append(("acquirer_ptynbr ptyid", "string", dict()))
    descendents.append(("amount", "double", dict()))
    descendents.append(("curr insid", "string", dict()))
    descendents.append(("counterparty_ptynbr ptyid", "string", dict()))
    descendents.append(("cashExtAttr", "bool", {"value" : True}))
    descendents.append(("activeCashExtAttr", "bool", dict()))
    descendents.append(("seqnbr", "int", dict()))
    descendents.append(("value_day", "date", dict()))
    descendents.append(("cashUnSettledSettledExtAttr", "string", dict()))
    
    preFilter = dict()
    preFilter["filter.op"] = "And"
    preFilter["filter.descendents"] = descendents

    AddPreFilter(dataDisp, preFilter)

    ids = list()
    ids.append("curr insid")
    ids.append("value_day")
    ids.append("amount")
    ids.append("seqnbr")
    ids.append("acquirer_accname account")
    ids.append("counterparty_ptynbr ptyid")

    AddQuickFilters(dataDisp, ids)
    
    return storedDataDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreateCashBalancesDataDisposition(dataDispositionName):
    newDataDisp = acm.FStoredDataDisposition()
    newDataDisp.Name(dataDispositionName)
    newDataDisp.SubType("FrontArena.DbMaster")
    newDataDisp.SetDataDisposition(CreateCashBalancesDataDispMessage())
    newDataDisp.Commit()
