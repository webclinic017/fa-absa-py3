""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/upgrade/FConfirmationPreUpgradeReport.py"
import acm
from FOperationsUtils import Log

ael_variables = []

upgradableQuery = acm.CreateFASQLQuery(acm.FConfInstruction, 'AND')
upgradableQuery.AddAttrNode('InsType', 'EQUAL', 'None')
upgradableQuery.AddAttrNode('DocumentTypeChlItem', 'EQUAL', None)
upgradableQuery.AddAttrNode('ProductTypeChlItem', 'EQUAL', None)
upgradableQuery.AddAttrNode('OtcInstr', 'EQUAL', 'None')
upgradableQuery.AddAttrNode('UndInsType', 'EQUAL', 'None')
upgradableQuery.AddAttrNode('InternalDepartment', 'EQUAL', None)


def GetRACCConfirmationInstructions():
    query = acm.CreateFASQLQuery(acm.FConfInstruction, 'OR')
    query.AddAttrNode('EventChlItem.Name', 'EQUAL', 'Resend')
    query.AddAttrNode('EventChlItem.Name', 'EQUAL', 'Amendment')
    query.AddAttrNode('EventChlItem.Name', 'EQUAL', 'Cancellation')
    query.AddAttrNode('EventChlItem.Name', 'EQUAL', 'Chaser')
    return query.Select()

def SortByPartyOid(confirmationInstruction1, confirmationInstruction2):
    sortResult = 0
    oid1 = confirmationInstruction1.Counterparty().Oid()
    oid2 = confirmationInstruction2.Counterparty().Oid()
    
    if oid1 < oid2:
        sortResult = -1
    elif oid1 > oid2:
        sortResult = 1
    return sortResult

def IsUpgradableConfirmationInstruction(confirmationInstruction):
    return upgradableQuery.IsSatisfiedBy(confirmationInstruction)

def GetNonUpgradableConfirmationInstructions():
    confirmationInstructionList = list()
    raccConfirmationInstructions = GetRACCConfirmationInstructions()
    for confirmationInstruction in raccConfirmationInstructions:
        if (IsUpgradableConfirmationInstruction(confirmationInstruction) == False):
            confirmationInstructionList.append(confirmationInstruction)
    return confirmationInstructionList

def PerformPreUpgradeReporting():
    Log(True, 'Finding non-upgradable confirmation instructions ...')
    nonUpgradableConfirmationInstructions = GetNonUpgradableConfirmationInstructions()
    count = len(nonUpgradableConfirmationInstructions)
    if count > 0:
        Log(True, '%d confirmation instructions are not possible to convert to confirmation instruction rules.' % count)
        Log(True, '')
        nonUpgradableConfirmationInstructions.sort(SortByPartyOid)
    for nonUpgradableConfirmationInstruction in nonUpgradableConfirmationInstructions:
        name = nonUpgradableConfirmationInstruction.Name()
        party = nonUpgradableConfirmationInstruction.Counterparty()
        oid = nonUpgradableConfirmationInstruction.Oid()
        template = nonUpgradableConfirmationInstruction.ConfTemplateChlItem().Name()
        Log(True, 'Confirmation instruction %d: %s | Template: %s | Party: %s' % (oid, name, template, party.Name()))
    if count == 0:
        Log(True, 'All confirmation instructions are possible to convert to confirmation instruction rules')
    Log(True, '\n')
    Log(True, 'Upgrade report finished.')

def ael_main(parameterDictionary):
    PerformPreUpgradeReporting()