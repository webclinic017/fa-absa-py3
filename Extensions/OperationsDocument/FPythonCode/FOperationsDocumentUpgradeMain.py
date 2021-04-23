""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/upgrade/FOperationsDocumentUpgradeMain.py"

import acm
from FOperationsExceptions import WrapperException
import FOperationsUtils as Utils
import FSwiftMessageTypeExtractor as MTExtractor
import FOperationsDocumentService as DocumentMod
from FSettlementEnums import SettlementStatus
from FOperationsDocumentEnums import OperationsDocumentStatus, OperationsDocumentType
from FConfirmationEnums import ConfirmationStatus

class UpgradeCollocator():

    def __init__(self, providerClass, numberOfCreatedDocuments, exceptionInfos):
        self.__providerClass = providerClass
        self.__numberOfCreatedDocuments = numberOfCreatedDocuments
        self.__exceptionInfos = exceptionInfos

    def PrintUpgradeCollocation(self):
        print("Upgrade result for record type %s:" % self.__providerClass.GetRecordType())
        print("%d OperationsDocument records created." % self.__numberOfCreatedDocuments)
        print("Number of errors: %d" % len(self.__exceptionInfos))
        if len(self.__exceptionInfos) > 0:
            print("Errors:")
            for exceptionInfo in self.__exceptionInfos:
                print(exceptionInfo)
        print("")

class ExceptionInfo():
    def __init__(self, provider, exception):
        self.__provider = provider
        self.__exception = exception

    def __str__(self):
        return 'No OperationsDocument record created for %s %d. Cause: %s' % (self.__provider.GetRecordType(), self.__provider.GetRecordOid(), self.__exception)

class SettlementDocumentProvider():
    def __init__(self, settlement):
        self.__settlement = settlement

    @staticmethod
    def GetResultSet():
        query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        query.AddAttrNode('Document', 'NOT_EQUAL', '')
        return query.Select()

    def IsSWIFT(self):
        return True

    @staticmethod
    def GetRecordType():
        return "settlement"

    def GetRecordOid(self):
        return self.__settlement.Oid()

    def SetRecord(self, operationsDoc):
        operationsDoc.Settlement(self.__settlement)

    def GetDocumentType(self):
        return OperationsDocumentType.SWIFT

    def GetStatus(self, operationsDoc):
        status = OperationsDocumentStatus.SENT_SUCCESSFULLY
        if operationsDoc.DocumentId() == -1:
            status = OperationsDocumentStatus.EXCEPTION
        elif self.__settlement.Status() == SettlementStatus.NOT_ACKNOWLEDGED:
            status = OperationsDocumentStatus.SEND_FAILED
        return status

    def GetStatusExplanation(self):
        statusExpl = ''
        if self.__settlement.Status() == SettlementStatus.NOT_ACKNOWLEDGED:
            statusExpl = 'Settlement was in status Not Acknowledged during upgrade'
        return statusExpl

class ConfirmationDocumentProvider():
    def __init__(self, confirmation):
        self.__confirmation = confirmation

    @staticmethod
    def GetResultSet():
        query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
        query.AddAttrNode('Document', 'NOT_EQUAL', '')
        return query.Select()

    def IsSWIFT(self):
        return (self.__confirmation.Transport() == 'Network') and \
               (self.__confirmation.ConfTemplateChlItem()) and \
               (self.__confirmation.ConfTemplateChlItem().Name() == 'SWIFT')

    @staticmethod
    def GetRecordType():
        return "confirmation"

    def GetRecordOid(self):
        return self.__confirmation.Oid()

    def SetRecord(self, operationsDoc):
        operationsDoc.Confirmation(self.__confirmation)

    def GetDocumentType(self):
        documentType = OperationsDocumentType.LONGFORM
        if self.IsSWIFT():
            documentType = OperationsDocumentType.SWIFT
        return documentType

    def GetStatus(self, operationsDoc):
        status = OperationsDocumentStatus.GENERATED
        if operationsDoc.DocumentId() == -1:
            status = OperationsDocumentStatus.EXCEPTION
        elif self.__confirmation.IsPostRelease():
            if self.__confirmation.Status() != ConfirmationStatus.NOT_ACKNOWLEDGED:
                status = OperationsDocumentStatus.SENT_SUCCESSFULLY
            else:
                status = OperationsDocumentStatus.SEND_FAILED
        return status

    def GetStatusExplanation(self):
        statusExpl = ''
        if self.__confirmation.Status() == ConfirmationStatus.NOT_ACKNOWLEDGED:
            statusExpl = 'Confirmation was in status Not Acknowledged during upgrade'
        return statusExpl

class OperationsDocumentUpgrader():

    def __init__(self):
        self.__settlementUpgradeCollocator = None
        self.__confirmationUpgradeCollocator = None

    def UpgradeOperationsDocuments(self):
        self.__UpgradeOperationsDocuments(SettlementDocumentProvider)
        self.__UpgradeOperationsDocuments(ConfirmationDocumentProvider)
        self.__PrintUpgradeCollocations()
        print('\nUpgrade script finished.')

    def __SetUpgradeCollocator(self, providerClass, numberOfCreatedDocuments, exceptionInfos):
        if providerClass.GetRecordType() == 'settlement':
            self.__settlementUpgradeCollocator = UpgradeCollocator(providerClass, numberOfCreatedDocuments, exceptionInfos)
        else:
            self.__confirmationUpgradeCollocator = UpgradeCollocator(providerClass, numberOfCreatedDocuments, exceptionInfos)

    def __PrintUpgradeCollocations(self):
        if self.__settlementUpgradeCollocator:
            self.__settlementUpgradeCollocator.PrintUpgradeCollocation()
        else:
            print('No upgrade collocation available for settlements.')
        if self.__confirmationUpgradeCollocator:
            self.__confirmationUpgradeCollocator.PrintUpgradeCollocation()
        else:
            print('No upgrade collocation available for confirmations.')

    @staticmethod
    def GetDocumentServiceHandle():
        import FDocumentationParameters as Params

        try:
            docService = DocumentMod.CreateDocumentService(Params)
        except WrapperException as e:
            Utils.Log(True, 'Could not create connect to AMB %s' % e)
            docService = None
        return docService

    def __UpgradeOperationsDocuments(self, providerClass):
        exceptionInfos = []
        numberOfCreatedDocuments = 0
        print("Upgrade started for record type %s" % providerClass.GetRecordType())
        docService = OperationsDocumentUpgrader.GetDocumentServiceHandle()
        if docService:
            resultSet = providerClass.GetResultSet()
            print("Table operations_document will be upgraded from %d %s records." % (resultSet.Size(), providerClass.GetRecordType()))
            for record in resultSet:
                print("Upgrading table operations_document from %s %d" % (providerClass.GetRecordType(), record.Oid()))
                provider = providerClass(record)
                if len(record.Documents()) == 0:
                    documents = record.Document()
                    if documents != "":
                        acm.BeginTransaction()
                        try:
                            numberOfCreatedDocumentsForRecord = 0
                            for document_id in documents.split(","):
                                try:
                                    docId = int(document_id.strip())
                                except ValueError as e:
                                    docId = -1
                                mt = 0
                                if (docId != -1) and (provider.IsSWIFT()):
                                    extractor = MTExtractor.FSwiftMessageTypeExtractor(docService)
                                    mt = extractor.Extract(docId)
                                operationsDoc = acm.FOperationsDocument()
                                operationsDoc.DocumentId(docId)
                                provider.SetRecord(operationsDoc)
                                operationsDoc.Type(provider.GetDocumentType())
                                operationsDoc.Status(provider.GetStatus(operationsDoc))
                                operationsDoc.SwiftMessageType(mt)
                                operationsDoc.StatusExplanation(provider.GetStatusExplanation())
                                operationsDoc.Data('')
                                operationsDoc.Size(len(''))
                                operationsDoc.Commit()
                                numberOfCreatedDocumentsForRecord += 1
                            acm.CommitTransaction()
                            numberOfCreatedDocuments += numberOfCreatedDocumentsForRecord
                        except Exception as e:
                            acm.AbortTransaction()
                            exceptionInfos.append(ExceptionInfo(provider, e))

        self.__SetUpgradeCollocator(providerClass, numberOfCreatedDocuments, exceptionInfos)


operationsDocumentUpgrader = OperationsDocumentUpgrader()
operationsDocumentUpgrader.UpgradeOperationsDocuments()

