""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingImporter.py"
import acm
import FAccountingExportImportStrategy as ExportImport
import FAccountingUpdater as UpdateHandler
import FAccountingMember
import FAccountingDeleter
from FBDPCurrentContext import Logme

class ObjectType:
    BOOK                   = 'BOOK'
    BOOK_MAPPING           = 'BOOKMAPPING'
    TREATMENT              = 'TREATMENT'
    TREATMENT_MAPPING      = 'TREATMENTMAPPING'
    ACCOUNTING_INSTRUCTION = 'ACCOUNTINGINSTRUCTION'

class AccountingImporter:

    messageBeginTag = "[MESSAGE]"
    messageEndTag = "[/MESSAGE]"
    typeEqualsString = "TYPE="

    @staticmethod
    def CreateBookImporter():
        return AccountingImporter(ExportImport.ExportImportStrategy.BookExportImportStrategy())

    @staticmethod
    def CreateTreatmentImporter():
        return AccountingImporter(ExportImport.ExportImportStrategy.TreatmentExportImportStrategy([]))

    @staticmethod
    def CreateAccountingInstructionImporter():
        return AccountingImporter(ExportImport.ExportImportStrategy.AccountingInstructionExportImportStrategy([], []))

    @staticmethod
    def CreateTAccountImporter():
        return AccountingImporter(ExportImport.ExportImportStrategy.TAccountExportImportStrategy())

    @staticmethod
    def IsObjectOfType(objectType, messageAsString):
        return (-1 != messageAsString.find(AccountingImporter.typeEqualsString + objectType))

    @staticmethod
    def GetNameFromMessage(message):
        startIndex = message.find('NAME=')
        if startIndex != -1:
            endIndex = message.find('\n', startIndex)
            return message[startIndex + 5:endIndex]
        return ''

    def __init__(self, instanceExportStrategy):
        self.__instanceExportStrategy = instanceExportStrategy
        self.__objectFinder = FAccountingMember.ObjectFinder()

    def __GetMessagesFromFile(self, aFile):
        messageString = self.__ReadMessageString(aFile)
        while messageString:
            yield messageString
            messageString = self.__ReadMessageString(aFile)

    def __ReadMessageString(self, aFile):
        messageComplete = False
        messageLines = []
        line = aFile.readline()
        if line.strip() == AccountingImporter.messageBeginTag:
            messageLines.append(line)
            while line.strip() and line.strip() != AccountingImporter.messageEndTag:
                line = aFile.readline()
                messageLines.append(line)

        if len(messageLines) and line.strip() == AccountingImporter.messageEndTag:
            messageComplete = True
        return messageComplete and "".join(messageLines) or None

    def Import(self, aFile, memberDeleter):
        self.ImportObjects(aFile, memberDeleter)

    def ImportObjects(self, aFile, memberDeleter):
        try:
            for message in self.__GetMessagesFromFile(aFile):
                memberDeleter.DeleteEntities(message)
                acmObject = UpdateHandler.GetAcmObjectFromMessage(self.IsObjectOfType, message)
                self.PostSimulation(acmObject, message)

                if acmObject.IsKindOf(acm.FBookMapping):
                    self.ConnectToMappingTree(acmObject)

                Logme()("Importing %s %s" % (acmObject.Class().Name(), acmObject.StringKey()))
        except Exception as e:
            Logme()("Import failed, Cause: %s" % str(e))
            raise e
        finally:
            aFile.close()

    def PostSimulation(self, acmObject, message):
        objectPostSimulationHandler = UpdateHandler.GetPostSimulationHandlerForObject(acmObject, message, self.__instanceExportStrategy)
        objectPostSimulationHandler.Commit()

    def ConnectToMappingTree(self, mapping):
        lastMapping = acm.FBookMapping.Select01("parentId = '' and nextId = '' and oid <> {} and type = {}".format(mapping.Oid(), mapping.Type()), None)
        if lastMapping:
            mapping.PreviousId(lastMapping.Id())
            lastMapping.NextId(mapping.Id())
            mapping.Commit()
            lastMapping.Commit()

class AccountingMemberDeleter:

    def __init__(self):
        pass

    def DeleteEntities(self, messages):
        pass

    @staticmethod
    def GetOriginalEntities(entities, originalEntities):
        for entity in entities:
            if entity.Oid() > 0:
                originalEntities.Add(entity)

class BookMemberDeleter(AccountingMemberDeleter):

    def __init__(self):
        AccountingMemberDeleter.__init__(self)
        self.__books = list()

    def __GetBookFromBookName(self, message):
        bookName = AccountingImporter.GetNameFromMessage(message)
        if '' != bookName:
            return acm.FBook[bookName]
        return None

    def GetBooks(self):
        return self.__books

    def DeleteEntities(self, message):
        if (AccountingImporter.IsObjectOfType(ObjectType.BOOK, message) and
            not AccountingImporter.IsObjectOfType(ObjectType.BOOK_MAPPING, message)):
            book = self.__GetBookFromBookName(message)

            if None != book:
                FAccountingDeleter.DeleteItems(book.AccountingPeriods())
                FAccountingDeleter.DeleteMappingsInBook(book)
                FAccountingDeleter.DeleteTAccountAllocationLinksInBook(book)
                FAccountingDeleter.DeleteChartOfAccounts(book)
                FAccountingDeleter.DeleteItems(book.BookLinks())
                self.__books.append(book)

class TreatmentMemberDeleter(AccountingMemberDeleter):

    def __init__(self, books):
        AccountingMemberDeleter.__init__(self)
        self.__books = books
        self.__treatments = list()

    def __GetTreatmentFromTreatmentName(self, message):
        treatmentName = AccountingImporter.GetNameFromMessage(message)
        if '' != treatmentName:
            return acm.FTreatment[treatmentName]
        return None

    def GetTreatments(self):
        return self.__treatments

    def GetBooks(self):
        return self.__books

    def __DeleteBookLinks(self, treatment):
        bookLinksToDelete = acm.FArray()
        bookLinks = treatment.BookLinks()
        for book in self.__books:
            for bookLink in bookLinks:
                if book.Name() == bookLink.Book().Name():
                    bookLinksToDelete.Add(bookLink)
        FAccountingDeleter.DeleteItems(bookLinksToDelete)

    def __DeleteTreatmentMappings(self, treatment):
        treatmentMappings = list()
        treatmentMappingsToDelete = list()
        for bookLink in treatment.BookLinks():
            treatmentMappings.extend(bookLink.TreatmentMappings())
        treatmentMappingsToDelete = [treatmentMapping for treatmentMapping in treatmentMappings if treatmentMapping.Book() in self.__books]
        FAccountingDeleter.DeleteMappings(treatmentMappingsToDelete)

    def DeleteEntities(self, message):
        if (AccountingImporter.IsObjectOfType(ObjectType.TREATMENT, message) and
            not AccountingImporter.IsObjectOfType(ObjectType.TREATMENT_MAPPING, message)):

            treatment = self.__GetTreatmentFromTreatmentName(message)
            if None != treatment:
                self.__DeleteTreatmentMappings(treatment)
                self.__DeleteBookLinks(treatment)

                entities = acm.FArray()
                AccountingMemberDeleter.GetOriginalEntities(treatment.TAccountAllocationLinks(), entities)
                filteredTAccAllocLinks = [taal for taal in entities if taal.ChartOfAccount().Book() in self.__books]
                FAccountingDeleter.DeleteTAccountAllocationLinks(filteredTAccAllocLinks)

                self.__treatments.append(treatment)


class AccountingInstructionMemberDeleter(AccountingMemberDeleter):

    def __init__(self, treatments, books):
        AccountingMemberDeleter.__init__(self)
        self.__treatments = treatments
        self.__books = books

    def __GetAIFromAIName(self, message):
        aiName = AccountingImporter.GetNameFromMessage(message)
        if '' != aiName:
            return acm.FAccountingInstruction[aiName]
        return None

    def __DeleteTreatmentLinks(self, accountingInstruction):
        treatmentLinksToDelete = acm.FArray()
        treatmentLinks = accountingInstruction.TreatmentLinks()

        for treatment in self.__treatments:
            for treatmentLink in treatmentLinks:
                if treatment.Name() == treatmentLink.Treatment().Name() and treatmentLink.Book() in self.__books:
                    treatmentLinksToDelete.Add(treatmentLink)
            bookLinks = []
        FAccountingDeleter.DeleteTAccountMappings(treatmentLinksToDelete)
        FAccountingDeleter.DeleteItems(treatmentLinksToDelete)

    def __DeleteAIMappings(self, accountingInstruction):
        treatmentLinks = accountingInstruction.TreatmentLinks()
        aiMappings = list()
        bookLinks = list()
        aiMappingsToDelete = list()
        for treatmentLink in treatmentLinks:
            aiMappings.extend(treatmentLink.AccountingInstructionMappings())

        for aiMapping in aiMappings:
            if aiMapping.BookLink().Book() in self.__books:
                aiMappingsToDelete.extend(aiMapping)
        FAccountingDeleter.DeleteMappings(aiMappingsToDelete)

    def DeleteEntities(self, message):
        if (AccountingImporter.IsObjectOfType(ObjectType.ACCOUNTING_INSTRUCTION, message)):
            ai = self.__GetAIFromAIName(message)
            if None != ai:
                self.__DeleteAIMappings(ai)

                entities = acm.FArray()
                for jvd in ai.JournalValueDefinitions():
                    AccountingMemberDeleter.GetOriginalEntities(jvd.TAccountAllocationLinks(), entities)
                    FAccountingDeleter.DeleteTAccountAllocationLinks(entities)
                    entities.Clear()
                FAccountingDeleter.DeleteItems(ai.JournalValueDefinitions())
                self.__DeleteTreatmentLinks(ai)


class TAccountMemberDeleter(AccountingMemberDeleter):

    def __init__(self):
        AccountingMemberDeleter.__init__(self)
