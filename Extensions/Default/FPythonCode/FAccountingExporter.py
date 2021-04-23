""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingExporter.py"
import acm
import FAccountingExportImportStrategy as ExportImport
from FBDPCurrentContext import Logme

class AccountingExporter:

    @staticmethod
    def CreateBookExporter(partialExport = False):
        return AccountingExporter(ExportImport.ExportImportStrategy.BookExportImportStrategy(partialExport))

    @staticmethod
    def CreateTreatmentExporter(filteredBooks, partialExport = False):
        return AccountingExporter(ExportImport.ExportImportStrategy.TreatmentExportImportStrategy(filteredBooks, partialExport))

    @staticmethod
    def CreateAccountingInstructionExporter(filteredTreatments, filteredBooks = None, partialExport = False):
        return AccountingExporter(ExportImport.ExportImportStrategy.AccountingInstructionExportImportStrategy(filteredTreatments, filteredBooks, partialExport))

    @staticmethod
    def CreateTAccountExporter(partialExport = False):
        return AccountingExporter(ExportImport.ExportImportStrategy.TAccountExportImportStrategy(partialExport))


    def __init__(self, instanceExportStrategy):
        self.__instanceExportStrategy = instanceExportStrategy

    def __ExportMemberObjects(self, messageList, messageGenerator, objectsToExport):
        Logme()("Exporting member objects...")
        for objectToExport in self.__instanceExportStrategy.GetObjectsToExport(objectsToExport):
            self.__ExportObject(messageList, objectToExport, messageGenerator)
        Logme()("Member objects exported")

    def __ExportMappingObjects(self, messageList, messageGenerator, objectsToExport):
        Logme()("Exporting mapping objects...")
        for objectToExport in self.__instanceExportStrategy.GetMappingsAndQueriesToExport(objectsToExport):
            self.__ExportObject(messageList, objectToExport, messageGenerator)
        Logme()("Mapping objects exported")

    def __ExportAllObjects(self, messageList, messageGenerator, objectsToExport):
        self.__ExportMemberObjects(messageList, messageGenerator, objectsToExport)
        self.__ExportMappingObjects(messageList, messageGenerator, objectsToExport)

    @staticmethod
    def __ExportObject(messageList, o, messageGenerator):
        Logme()("Exporting %s %s" % (o.Class().Name(), o.StringKey()))
        try:
            ambaMessage = messageGenerator.Generate(o)
            messageList.append(ambaMessage.AsString())
        except Exception as e:
            raise Exception("Could not export object: %s", str(e))

    def CreateExportMessages(self, objectsToExport, showAll = True):
        messageList = []
        self.__instanceExportStrategy.CustomizeMessageGenerator(showAll)
        self.__ExportAllObjects(messageList, self.__instanceExportStrategy.GetMessageGenerator(), objectsToExport)
        return ("").join(messageList)

    def Export(self, objectsToExport):
        try:
            messages = self.CreateExportMessages(objectsToExport)
        except Exception as e:
            raise Exception("Export failed: %s" % str(e))
        return messages

