
import acm
from ChoicesExprCommon import allEnumValuesExcludeNone, listChoices, listChoicesWithEmpty

def getAccountingInstructionCategories():
    return listChoices('AccountingInstruction Category')
    
def getChartOfAccounts(journal):
    assert(journal)

    chartOfAccounts = list()
    book = journal.Book()
    
    if book:
        for coa in book.ChartOfAccounts():
            tAccount = coa.Account()
            if tAccount and tAccount.ReportingClass() == 'TAccount':
                chartOfAccounts.append(coa)
    return chartOfAccounts

def getSuspenseAccounts(book):
    assert(book)
    suspenseAccounts = list()
    for chartOfAccount in book.ChartOfAccounts():
        tAccount = chartOfAccount.Account()
        if (tAccount and tAccount.ReportingClass() == 'Suspense'):
            suspenseAccounts.append(tAccount)
    return suspenseAccounts

def getTAccountCategories():
    return listChoices('TAccount Category')

def getLedgerKeys():
    context = acm.GetDefaultContext()
    keys = [""]
    keys.extend(context.MemberNames('FExtensionValue', 'accounting ledger keys', ''))
    return keys
    
def getJournalTypes():
    return ['Live', 'Simulated']
    
def getDebitOrCreditExcludeNone():
    return allEnumValuesExcludeNone( acm.FEnumeration['enum(DebitOrCredit)'] )
    
def getDateChoices(accountingInstruction, field):
    return acm.Accounting.GetDateColumnsForField(accountingInstruction, field)
    
def getFxRateChoices(accountingInstruction, field):
    return acm.Accounting.GetRateColumnsForField(accountingInstruction, field)
    
def getJournalAggregationLevelChoices(object):
    choices = allEnumValuesExcludeNone(acm.FEnumeration['enum(JournalAggregationLevel)'])
    if object.Type() != 'Trade':
        for choice in choices:
            if choice == 'Tax Lot Closing' or choice == 'Instrument and Portfolio':
                choices.remove(choice)
    return choices
