""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingDeleter.py"
import acm

def GetPythonList(entities):
    aList = list()
    aList.extend(entities)
    return aList

def DeleteBook(book):
    try:
        DeleteItems(book.AccountingPeriods())
        DeleteMappingsInBook(book)
        DeleteTAccountAllocationLinksInBook(book)
        DeleteLinksInBook(book)
        book.Delete()
    except Exception as e:
        raise e

def DeleteTreatment(treatment):
    try:
        DeleteMappingsInTreatment(treatment)
        DeleteTAccountAllocationLinksInTreatment(treatment)
        DeleteLinksInTreatment(treatment)
        treatment.Delete()
    except Exception as e:
        raise e

def DeleteAccountingInstruction(accountingInstruction):
    try:
        DeleteMappingsInAccountingInstruction(accountingInstruction)
        DeleteTAccountAllocationLinksInAccountingInstruction(accountingInstruction)
        DeleteItems(accountingInstruction.JournalValueDefinitions())
        DeleteItems(accountingInstruction.TreatmentLinks())
        accountingInstruction.Delete()
    except Exception as e:
        raise e

#used by the importer
def DeleteChartOfAccounts(book):
    for chartOfAccount in GetPythonList(book.ChartOfAccounts()):
        for child in GetPythonList(chartOfAccount.Children()):
            DeleteChartOfAccountsChildren(child)
        chartOfAccount.Delete()

def DeleteChartOfAccountsChildren(chartOfAccount):
    for child in GetPythonList(chartOfAccount.Children()):
        DeleteChartOfAccountsChildren(child)
        child.Delete()
    chartOfAccount.Delete()

#used by the importer
def DeleteItems(items):
    for item in GetPythonList(items):
        item.Delete()

#used by the importer
def DeleteMappings(mappings):
    for mapping in GetPythonList(mappings):
        if mapping.IsSimulated():
            mapping.Unsimulate()
        for child in mapping.Children():
            __RemoveChildren(child)
        __RemoveReferencesFromMapping(mapping)
        mapping.Delete()

def DeleteTAccountAllocationLinksInBook(book):
    taccountLinks = list()
    for chartOfAccount in book.ChartOfAccounts():
        taccountLinks.extend(chartOfAccount.TAccountAllocationLinks())
    DeleteItems(taccountLinks)

def DeleteTAccountAllocationLinksInTreatment(treatment):
    taccountLinks = acm.FTAccountAllocationLink.Select("treatment = %d" % treatment.Oid())
    DeleteItems(taccountLinks)

def DeleteTAccountAllocationLinksInAccountingInstruction(accountingInstruction):
    taccountLinks = list()
    for jvd in accountingInstruction.JournalValueDefinitions():
        taccountLinks.extend(jvd.TAccountAllocationLinks())
    DeleteItems(taccountLinks)

#used by the importer
def DeleteTAccountAllocationLinks(taccountAllocationLinks):
    for taccountAllocationLink in GetPythonList(taccountAllocationLinks):
        DeleteMappings(taccountAllocationLink.TAccountMappings())
        taccountAllocationLink.Delete()

def DeleteTAccountMappings(treatmentLinks):
    taccountMappings = list()
    for treatmentLink in treatmentLinks:
        mappings = acm.FTAccountMapping.Select("treatmentLink = %d" % treatmentLink.Oid())
        taccountMappings.extend(mappings)
    DeleteMappings(taccountMappings)

def DeleteAIMappings(bookLinks):
    aiMappings = list()
    for bookLink in bookLinks:
        mappings = acm.FAccountingInstructionMapping.Select("bookLink = %d" % bookLink.Oid()).AsArray()
        aiMappings.extend(mappings)
    DeleteMappings(aiMappings)

def __RemoveChildren(mapping):
    if mapping.IsSimulated():
        mapping.Unsimulate()
    for childMapping in mapping.Class().Select("parentId = {}".format(mapping.Id())):
        __RemoveChildren(childMapping)
    __RemoveReferencesFromMapping(mapping)
    mapping.Delete()

def __RemoveReferencesFromMapping(mapping):
    nextMappingId = mapping.NextId()
    previousMappingId = mapping.PreviousId()

    if nextMappingId:
        nextMapping = mapping.Class().Select01("id = {}".format(nextMappingId), None)
        nextMapping.PreviousId(previousMappingId)
        nextMapping.Commit()

    if previousMappingId:
        previousMapping = mapping.Class().Select01("id = {}".format(previousMappingId), None)
        previousMapping.NextId(nextMappingId)
        previousMapping.Commit()

def DeleteMappingsInBook(book):
    bookMappings = book.BookMappings()
    treatmentMappings = acm.FTreatmentMapping.Select("book = %d" % book.Oid())
    treatmentLinks = acm.FTreatmentLink.Select("book = %d" % book.Oid())

    DeleteMappings(bookMappings)
    DeleteMappings(treatmentMappings)
    DeleteAIMappings(book.BookLinks())
    DeleteTAccountMappings(treatmentLinks)

def DeleteMappingsInTreatment(treatment):
    treatmentMappings = list()
    for bookLink in treatment.BookLinks():
        treatmentMappings.extend(bookLink.TreatmentMappings())

    DeleteMappings(treatmentMappings)
    DeleteAIMappings(treatment.BookLinks())
    DeleteTAccountMappings(treatment.TreatmentLinks())

def DeleteMappingsInAccountingInstruction(accountingInstruction):
    treatmentLinks = accountingInstruction.TreatmentLinks()
    aiMappings = list()
    for treatmentLink in treatmentLinks:
        aiMappings.extend(treatmentLink.AccountingInstructionMappings())

    DeleteMappings(aiMappings)
    DeleteTAccountMappings(treatmentLinks)

def DeleteLinksInBook(book):
    treatmentLinks = acm.FTreatmentLink.Select("book = %d" % book.Oid())
    DeleteItems(book.BookLinks())
    DeleteItems(treatmentLinks)

def DeleteLinksInTreatment(treatment):
    DeleteItems(treatment.TreatmentLinks())
    DeleteItems(treatment.BookLinks())

