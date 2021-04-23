""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingTransporter.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FAccountingTransporter

    (c) Copyright 2013 by SunGard Front Arena. All rights reserved.

VERSION
    %R%
DESCRIPTION

MAJOR REVISIONS

    2013-02-19  RL  Initial implementation
-------------------------------------------------------------------------------------------------------"""
import itertools
import FAccountingExporter as Exporter
import FAccountingImporter as Importer
import FAccountingDeleter as Deleter
from FBDPCurrentContext import Logme

class FileExtensionMapKey:
    KEY_BOOK                   = 'book'
    KEY_COMPLETE_EXPORT        = 'completeExport'

class FileExtensionMapValue:
    VALUE_BOOK                   = 'opbook'
    VALUE_COMPLETE_EXPORT        = 'opcompleteacc'

fileExtensionMap = {
                    FileExtensionMapKey.KEY_BOOK:FileExtensionMapValue.VALUE_BOOK,
                    FileExtensionMapKey.KEY_COMPLETE_EXPORT:FileExtensionMapValue.VALUE_COMPLETE_EXPORT
                    }

def ExportBooks(zipFile, books, treatments = [], accountingInstructions = []):
    exporter = Exporter.AccountingExporter.CreateBookExporter(True)
    Export(zipFile, "ExportedBooks.txt", exporter, books)

    listOfBookLinks = list(itertools.chain(*[book.BookLinks() for book in books]))
    treatmentsForBooksSet = set()
    for bookLink in listOfBookLinks:
        treatment = bookLink.Treatment()
        if treatment in treatments:
            treatmentsForBooksSet.add(treatment)

    ExportTreatments(zipFile, books, list(treatmentsForBooksSet), accountingInstructions)

def ExportBooksOnly(zipFile, books):
    exporter = Exporter.AccountingExporter.CreateBookExporter()
    Export(zipFile, "ExportedBooks.txt", exporter, books)

def ExportTreatments(zipFile, books, treatments = [], accountingInstructions = []):
    exporter = Exporter.AccountingExporter.CreateTreatmentExporter(books, True)
    Export(zipFile, "ExportedTreatments.txt", exporter, treatments)

    listOftreatmentLinks = list(itertools.chain(*[treatment.TreatmentLinks() for treatment in treatments]))
    accountingInstructionsForTreatmentsSet = set()
    for treatmentLink in listOftreatmentLinks:
        ai = treatmentLink.AccountingInstruction()
        if ai in accountingInstructions:
            accountingInstructionsForTreatmentsSet.add(ai)

    ExportAccountingInstructions(zipFile, books, treatments, list(accountingInstructionsForTreatmentsSet))

def ExportTreatmentsOnly(zipFile, books, treatments):
    exporter = Exporter.AccountingExporter.CreateTreatmentExporter(books)
    Export(zipFile, "ExportedTreatments.txt", exporter, treatments)

def ExportAccountingInstructions(zipFile, books, treatments, accountingInstructions):
    exporter = Exporter.AccountingExporter.CreateAccountingInstructionExporter(treatments, books, True)
    Export(zipFile, "ExportedAccountingInstructions.txt", exporter, accountingInstructions)

    listOfJVDs = list(itertools.chain(*[accountingInstruction.JournalValueDefinitions() for accountingInstruction in accountingInstructions]))
    taccountAllocationLinks = list(itertools.chain(*[jvd.TAccountAllocationLinks() for jvd in listOfJVDs]))

    if treatments:
        taccountAllocationLinks = list(filter(lambda taal: taal.Treatment() in treatments, taccountAllocationLinks))
    if books:
        chartOfAccounts = list(itertools.chain(*[book.ChartOfAccounts() for book in books]))
        taccountAllocationLinks = list(filter(lambda taal: taal.ChartOfAccount() in chartOfAccounts, taccountAllocationLinks))

    ExportTAccounts(zipFile, taccountAllocationLinks)

def ExportAccountingInstructionsOnly(zipFile, treatments, accountingInstructions, books = None):
    exporter = Exporter.AccountingExporter.CreateAccountingInstructionExporter(treatments, books)
    Export(zipFile, "ExportedAccountingInstructions.txt", exporter, accountingInstructions)

def ExportTAccounts(zipFile, taccountAllocationLinks):
    exporter = Exporter.AccountingExporter.CreateTAccountExporter()
    Export(zipFile, "ExportedTAccounts.txt", exporter, taccountAllocationLinks)

def ImportBooks(zipFile):
    bookImporter = Importer.AccountingImporter.CreateBookImporter()
    bookMemberDeleter = Importer.BookMemberDeleter()
    Import(zipFile, "ExportedBooks.txt", bookImporter, bookMemberDeleter)
    ImportTreatments(zipFile, bookMemberDeleter.GetBooks())

def ImportTreatments(zipFile, books):
    treatmentImporter = Importer.AccountingImporter.CreateTreatmentImporter()
    treatmentMemberDeleter = Importer.TreatmentMemberDeleter(books)
    Import(zipFile, "ExportedTreatments.txt", treatmentImporter, treatmentMemberDeleter)
    ImportAccountingInstructions(zipFile, treatmentMemberDeleter.GetTreatments(), treatmentMemberDeleter.GetBooks())

def ImportAccountingInstructions(zipFile, treatments, books = None):
    accountingInstructionImporter = Importer.AccountingImporter.CreateAccountingInstructionImporter()
    accountingInstructionMemberDeleter = Importer.AccountingInstructionMemberDeleter(treatments, books)
    Import(zipFile, "ExportedAccountingInstructions.txt", accountingInstructionImporter, accountingInstructionMemberDeleter)
    ImportTAccounts(zipFile)

def ImportTAccounts(zipFile):
    taccountImporter = Importer.AccountingImporter.CreateTAccountImporter()
    tAccountMemberDeleter = Importer.TAccountMemberDeleter()
    Import(zipFile, "ExportedTAccounts.txt", taccountImporter, tAccountMemberDeleter)

def DeleteBook(book):
    Deleter.DeleteBook(book)
    Logme()("Deleted Book")

def DeleteTreatment(treatment):
    Deleter.DeleteTreatment(treatment)
    Logme()("Deleted Treatment")

def DeleteAccountingInstruction(accountingInstruction):
    Deleter.DeleteAccountingInstruction(accountingInstruction)
    Logme()("Deleted Accounting Instruction")

def Export(zipFile, exportFile, exporter, objectsToExport):
    try:
        messages = exporter.Export(objectsToExport)
        zipFile.writestr(exportFile, messages)
    except Exception as e:
        Logme()( "\n\n".join(["Export failed", "Cause: " + str(e)]))

def Import(zipFile, importFile, importer, memberDeleter):
    try:
        importFile = zipFile.open(importFile)
        importer.Import(importFile, memberDeleter)
    except Exception as e:
        raise e
    finally:
        importFile.close()

