""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/operations_viewer/etc/FOperationsViewerExamplesSettledInventoryViewDisp.py"
import acm
import Contracts_Imdr_Messages_ImdrMessages
from FOperationsViewerExamplesHelperFunctions import AddColumn, AddTree

#-------------------------------------------------------------------------
def CreateSettledInventoryViewDispMessage(dataDispName):
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
    tree["uniqueId"] = "f5b41933-0e42-4de2-b193-d29911703d6f"
    tree["displayInformation.label.formatString"] = "AC/ISIN/RecentPast"
    tree["root.includeLevelInProjection"] = True
    tree["root.children"] = [child]

    AddTree(viewDisp, tree)
    
    # Add Custodian Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "acquirer_accname correspondent_bank_ptynbr ptyid"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    custodian = dict()
    custodian["uniqueId"] = "4008f605-3f7d-4921-8a47-b49ffbbca9e3"
    custodian["displayInformation.icon"] = "DetailsBase"
    custodian["displayInformation.label.formatString"] = "Custodian"
    custodian["displayInformation.description.formatString"] = "Unique name of party."
    custodian["root.children"] = [child]

    AddColumn(viewDisp, custodian)
    
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
    issuer["uniqueId"] = "67bfe3c7-0c80-40c5-9253-ce84f7e0edac"
    issuer["displayInformation.icon"] = "DetailsBase"
    issuer["displayInformation.label.formatString"] = "Issuer"
    issuer["displayInformation.description.formatString"] = "Unique name of party."
    issuer["root.children"] = [child]

    AddColumn(viewDisp, issuer)

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
    issueDay["uniqueId"] = "da684fe1-d432-4aae-867f-9d8d700ca011"
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
    expiryDay["uniqueId"] = "b532da3b-dbbc-4a22-8a8f-1dd6f5a02d74"
    expiryDay["displayInformation.icon"] = "DetailsBase"
    expiryDay["displayInformation.label.formatString"] = "Expiry Day"
    expiryDay["displayInformation.description.formatString"] = "Expiry date for non-generic instruments."
    expiryDay["root.children"] = [child]

    AddColumn(viewDisp, expiryDay)

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
    curr["uniqueId"] = "b2c2d3b6-0066-4502-a4e0-20967464e15a"
    curr["displayInformation.icon"] = "DetailsBase"
    curr["displayInformation.label.formatString"] = "CCY"
    curr["displayInformation.description.formatString"] = "Unique name of instrument. Used to select instrument in \napplications."
    curr["root.children"] = [child]

    AddColumn(viewDisp, curr)
    
    # Add Custody Position Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Custody Position"

    child = dict()
    child["contribution.formula"] = namedFormula

    custodyPosition = dict()
    custodyPosition["uniqueId"] = "0628caf1-b7ab-4755-8a52-47dfab3bd9ae"
    custodyPosition["displayInformation.label.formatString"] = "Custody Position"
    custodyPosition["root.children"] = [child]

    AddColumn(viewDisp, custodyPosition)
    
    # Add Security Transaction Type Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "securityTransactionTypeExtAttr"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    securityTransactionType = dict()
    securityTransactionType["uniqueId"] = "b896c56f-e0cc-4a67-aecc-dd2956eedc89"
    securityTransactionType["displayInformation.label.formatString"] = "Security Transaction Type"
    securityTransactionType["root.children"] = [child]

    AddColumn(viewDisp, securityTransactionType)
    
    # Add Temporary In Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Temporary In"

    child = dict()
    child["contribution.formula"] = namedFormula

    temporaryIn = dict()
    temporaryIn["uniqueId"] = "a1d7a37b-ab34-443a-b51c-1286b6e590b9"
    temporaryIn["displayInformation.label.formatString"] = "Temporary In"
    temporaryIn["root.children"] = [child]

    AddColumn(viewDisp, temporaryIn)
    
    # Add Temporary Out Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Temporary Out"

    child = dict()
    child["contribution.formula"] = namedFormula

    temporaryOut = dict()
    temporaryOut["uniqueId"] = "d4b62b5b-cd79-4fe5-afa8-2aca3c0f57dd"
    temporaryOut["displayInformation.label.formatString"] = "Temporary Out"
    temporaryOut["root.children"] = [child]
    
    AddColumn(viewDisp, temporaryOut)
    
    # Add Adjusted Balance Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Adjusted Balance"

    child = dict()
    child["contribution.formula"] = namedFormula

    adjustedBalance = dict()
    adjustedBalance["uniqueId"] = "90c6d338-cbfa-416b-b013-909a7fe11ee7"
    adjustedBalance["displayInformation.label.formatString"] = "Adjusted Balance"
    adjustedBalance["root.children"] = [child]

    AddColumn(viewDisp, adjustedBalance)
    
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
    settledDay["uniqueId"] = "2d23d5b1-9271-49b8-9002-b3ec6c88a77f"
    settledDay["displayInformation.icon"] = "DetailsBase"
    settledDay["displayInformation.label.formatString"] = "Settled Day"
    settledDay["displayInformation.description.formatString"] = "The settlement day of a security settlement."
    settledDay["root.children"] = [child]

    AddColumn(viewDisp, settledDay)
    
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
    tradeOId["uniqueId"] = "3db8672c-0c51-4638-a193-2da2f84e9adf"
    tradeOId["displayInformation.icon"] = "DetailsBase"
    tradeOId["displayInformation.label.formatString"] = "Trade Ref"
    tradeOId["displayInformation.description.formatString"] = "Unique internal number identifying this trade, generated \nautomatically."
    tradeOId["root.children"] = [child]

    AddColumn(viewDisp, tradeOId)
    
    # Add Total Issue Size Column

    summarizationValue = dict()
    summarizationValue["parameterId"] = "parameter1"
    summarizationValue["tableValueId"] = "sec_insaddr total_issued"

    summarizationFormula = dict()
    summarizationFormula["formulaId"] = "Unique"
    summarizationFormula["values"] = [summarizationValue]

    summarizationFormattingOptions = dict()
    summarizationFormattingOptions["formatterUniqueId"] = "NumDefault"
    summarizationFormattingOptions["overideNumberOfDecimals"] = 0

    summarizationFormulaWithFormattingOptions = dict()
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formula"] = summarizationFormula
    summarizationFormulaWithFormattingOptions["formulaWithFormattingOptions.formattingOptions"] = summarizationFormattingOptions

    child = dict()
    child["contribution.formula"] = summarizationFormulaWithFormattingOptions

    totalIssueSize = dict()
    totalIssueSize["uniqueId"] = "ce13385b-9757-4ad1-bfe5-7b46b090319f"
    totalIssueSize["displayInformation.icon"] = "DetailsBase"
    totalIssueSize["displayInformation.label.formatString"] = "Total Issue Size"
    totalIssueSize["displayInformation.description.formatString"] = "Total issue size for a security."
    totalIssueSize["root.children"] = [child]

    AddColumn(viewDisp, totalIssueSize)
    
    # Add Vault Position Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Vault Position"

    child = dict()
    child["contribution.formula"] = namedFormula

    vaultPosition = dict()
    vaultPosition["uniqueId"] = "3ad16f46-277b-4523-922b-1a4bf089382a"
    vaultPosition["displayInformation.label.formatString"] = "Vault Position"
    vaultPosition["root.children"] = [child]

    AddColumn(viewDisp, vaultPosition)

    # Add Issue Outstanding Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Issue Outstanding"

    child = dict()
    child["contribution.formula"] = namedFormula

    issueOutstanding = dict()
    issueOutstanding["uniqueId"] = "bee28a37-75ab-4c8c-8046-9cb69485cbd6"
    issueOutstanding["displayInformation.label.formatString"] = "Issue Outstanding"
    issueOutstanding["root.children"] = [child]
    
    AddColumn(viewDisp, issueOutstanding)
    
    # Add Issue Amortization Column
    
    namedFormula = dict()
    namedFormula["namedFormulaId"] = "Issue Amortization"

    child = dict()
    child["contribution.formula"] = namedFormula

    issueAmortization = dict()
    issueAmortization["uniqueId"] = "345c5172-28cc-4174-9b1e-adac8747601e"
    issueAmortization["displayInformation.label.formatString"] = "Issue Amortization"
    issueAmortization["root.children"] = [child]

    AddColumn(viewDisp, issueAmortization)
        
    # Add Amount Column

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

    amount = dict()
    amount["uniqueId"] = "2043fa2d-de63-4b23-8798-fc98fccce6a2"
    amount["displayInformation.icon"] = "DetailsBase"
    amount["displayInformation.label.formatString"] = "Amount"
    amount["displayInformation.description.formatString"] = "The amount to be paid."
    amount["root.children"] = [child]

    AddColumn(viewDisp, amount)

    return newStoredViewDisp.SerializeToString()

#-------------------------------------------------------------------------
def CreateSettledInventoryViewDisposition(viewDispositionName, dataDispositionName):
    newViewDisp = acm.FStoredViewDisposition()
    newViewDisp.Name(viewDispositionName)
    newViewDisp.SubType(dataDispositionName)
    newViewDisp.SetViewDisposition(CreateSettledInventoryViewDispMessage(dataDispositionName))
    newViewDisp.Commit()
