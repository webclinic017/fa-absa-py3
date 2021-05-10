""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesCustodyInventoryViewDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumn, AddTree


#-------------------------------------------------------------------------
def CreateCustodyInventoryViewDispMessage(dataDispName):
    newStoredViewDisp = Contracts_Imdr_Messages_ImdrMessages.StoredViewDispositon()

    newStoredViewDisp.dataDispositionName = dataDispName

    newStoredViewDisp.viewDisposition.SetInParent()
    viewDisp = newStoredViewDisp.viewDisposition
    
    # Add Grouping Information

    grandGrandChild = dict()
    grandGrandChild["includeLevelInProjection"] = False
    grandGrandChild["groupBy.type.tableValue.tableValueId"] = "securityRecentPastSettledExtAttr"
    grandGrandChild["groupBy.showLeafs.sort.tableValueId"] = "settled_day"
    grandGrandChild["groupBy.showLeafs.sort.ascending"] = False
    grandGrandChild["groupBy.nodeDetails.sort.ascending"] = False

    grandChild = dict()
    grandChild["includeLevelInProjection"] = False
    grandChild["groupBy.type.tableValue.tableValueId"] = "instrumentIsin"
    grandChild["groupBy.partition.tableFormula.namedFormulaId"] = "OpenPositions/ZeroPositions"
    grandChild["children"] = [grandGrandChild]

    child = dict()
    child["includeLevelInProjection"] = False
    child["groupBy.type.tableValue.tableValueId"] = "acquirer_accname account"
    child["children"] = [grandChild]

    tree = dict()
    tree["uniqueId"] = "62c3f6a2-e835-4197-88cd-e87032045eba"
    tree["displayInformation.label.formatString"] = "AC/ISIN/RecentPast"
    tree["root.includeLevelInProjection"] = True
    tree["root.children"] = [child]

    AddTree(viewDisp, tree)

    # Add Issuer Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "sec_insaddr issuer_ptynbr ptyid"

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
    issuer["uniqueId"] = "59b27eb6-b421-466f-b507-11d01fdd7dc9"
    issuer["displayInformation.icon"] = "DetailsBase"
    issuer["displayInformation.label.formatString"] = "Issuer"
    issuer["displayInformation.description.formatString"] = "Unique name of party."
    issuer["root.children"] = [child]

    AddColumn(viewDisp, issuer)

    # Add CCY(Currency) Column

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
    curr["uniqueId"] = "55e17772-e5e2-4f8f-9326-989f15c0cea3"
    curr["displayInformation.icon"] = "DetailsBase"
    curr["displayInformation.label.formatString"] = "CCY"
    curr["displayInformation.description.formatString"] = "Unique name of instrument. Used to select instrument in \napplications."
    curr["root.children"] = [child]

    AddColumn(viewDisp, curr)

    # Add Issue Day Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "sec_insaddr issue_day"

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

    issueDay = dict()
    issueDay["uniqueId"] = "675557a7-40c4-4ef6-b4cc-ad39b1a9b6ac"
    issueDay["displayInformation.icon"] = "DetailsBase"
    issueDay["displayInformation.label.formatString"] = "Issue Day"
    issueDay["displayInformation.description.formatString"] = "Issue day for securities."
    issueDay["root.children"] = [child]

    AddColumn(viewDisp, issueDay)
    
    # Add Expiry Day Column
    
    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "sec_insaddr exp_day"

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
                 
    expiryDay = dict()
    expiryDay["uniqueId"] = "16d691c1-cb3e-48b2-a8ef-274f9ec70aca"
    expiryDay["displayInformation.icon"] = "DetailsBase"
    expiryDay["displayInformation.label.formatString"] = "Expiry Day"
    expiryDay["displayInformation.description.formatString"] = "Expiry date for non-generic instruments."
    expiryDay["root.children"] = [child]

    AddColumn(viewDisp, expiryDay)    
        
    # Add Amount Column
    
    tableFormulaReferenceValue = dict()
    tableFormulaReferenceValue["parameterId"] = "parameter1"
    tableFormulaReferenceValue["tableValueId"] = "amount"

    tableFormulaReferenceFormula = dict()
    tableFormulaReferenceFormula["formulaId"] = "Sum"
    tableFormulaReferenceFormula["values"] = [tableFormulaReferenceValue]

    tableFormulaReferenceFormattingOptions = dict()

    tableFormulaReferenceWithFormattingOptions = dict()
    tableFormulaReferenceWithFormattingOptions["formulaWithFormattingOptions.formula"] = tableFormulaReferenceFormula
    tableFormulaReferenceWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = tableFormulaReferenceFormattingOptions

    backgroundColorFormulaValue = dict()
    backgroundColorFormulaValue["parameterId"] = "parameter1"
    backgroundColorFormulaValue["tableFormulaReference"] = tableFormulaReferenceWithFormattingOptions

    backgroundColorFormula = dict()
    backgroundColorFormula["formulaId"] = "int.colorsNegativePositive"
    backgroundColorFormula["values"] = [backgroundColorFormulaValue]

    backgroundColorFormulaFormattingOptions = dict()

    backgroundColorFormulaWithFormattingOptions = dict()
    backgroundColorFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = backgroundColorFormula
    backgroundColorFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = backgroundColorFormulaFormattingOptions

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "amount"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Sum"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()
    summarizationFormattingOptions["formatterUniqueId"] = "NumDefault"
    summarizationFormattingOptions["overideNumberOfDecimals"] = 0

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions
    child["contribution.backgroundColorFormula"] = backgroundColorFormulaWithFormattingOptions

    amount = dict()
    amount["uniqueId"] = "2aa7e297-f27d-4576-b263-6ffd33f5686b"
    amount["displayInformation.icon"] = "DetailsBase"
    amount["displayInformation.label.formatString"] = "Amount"
    amount["displayInformation.description.formatString"] = "The amount to be paid."
    amount["root.children"] = [child]

    AddColumn(viewDisp, amount)

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
    settledDay["uniqueId"] = "af8efb42-0767-478a-9fdc-190eaa6f886f"
    settledDay["displayInformation.icon"] = "DetailsBase"
    settledDay["displayInformation.label.formatString"] = "Settled Day"
    settledDay["displayInformation.description.formatString"] = "The settlement day of a security settlement."
    settledDay["root.children"] = [child]

    AddColumn(viewDisp, settledDay)

    # Add Settlement Ref (OId) Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "seqnbr"

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

    oId = dict()
    oId["uniqueId"] = "741165a6-faa7-42c0-b069-5aa9beafb6fa"
    oId["displayInformation.icon"] = "DetailsBase"
    oId["displayInformation.label.formatString"] = "Settlement Ref"
    oId["displayInformation.description.formatString"] = "Unique internal number identifying this payment, generated \nautomatically."
    oId["root.children"] = [child]

    AddColumn(viewDisp, oId)

    # Add Account Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "acquirer_accname account"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    account = dict()
    account["uniqueId"] = "e3f65bfd-cbb5-46b3-8e68-ce6d506836ee"
    account["displayInformation.icon"] = "DetailsBase"
    account["displayInformation.label.formatString"] = "Account"
    account["displayInformation.description.formatString"] = "The account number of the account at the depository."
    account["root.children"] = [child]

    AddColumn(viewDisp, account)

    return newStoredViewDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreateCustodyInventoryViewDisposition(viewDispositionName, dataDispositionName):
    newViewDisp = acm.FStoredViewDisposition()
    newViewDisp.Name(viewDispositionName)
    newViewDisp.SubType(dataDispositionName)
    newViewDisp.SetViewDisposition(CreateCustodyInventoryViewDispMessage(dataDispositionName))
    newViewDisp.Commit()
