""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementCommitter.py"
import acm

from FSettlementEnums import RelationType

import FOperationsUtils as Utils
from FOperationsDocumentEnums import OperationsDocumentStatus
import FSettlementValidations as Validations


class CommitAction(object):
    DELETE = 0
    RECALL = 1
    INSERT = 2
    UPDATE = 3
    NONE   = 4

class SettlementCommitter(object):

    def __init__(self, settlement, commitAction, updateProcess = False):
        self.settlement = settlement
        self.commitAction = commitAction
        self.netParent = None
        self.nettingRule = None
        self.updateProcess = updateProcess

    def GetCommitAction(self):
        return self.commitAction

    def GetSettlement(self):
        return self.settlement

    def SetNetParent(self, netParent):
        self.netParent = netParent

    def GetNetParent(self):
        return self.netParent

    def GetNettingRule(self):
        return self.nettingRule

    def SetNettingRule(self, nettingRule):
        self.nettingRule = nettingRule

    def SetUpdateProcess(self, updateProcess):
        self.updateProcess = updateProcess

    def __DeleteSettlement(self):
        operationsDocuments = self.settlement.Documents()
        journalInformations = self.settlement.JournalInformations()
        externalObjects = self.settlement.ExternalObjects()

        isAcknowledgedDocument = False
        for operationsDocument in operationsDocuments:
            if operationsDocument.Status() == OperationsDocumentStatus.SENT_SUCCESSFULLY:
                isAcknowledgedDocument = True
            else:
                try:
                    Utils.LogAlways('Deleting operations document record %d' % operationsDocument.Oid())
                    operationsDocument.Delete()
                except Exception as error:
                    Utils.RaiseCommitException(str(error) + '\nCould not delete document %d' % operationsDocument.Oid(), self.settlement)
                    
        if isAcknowledgedDocument:
            Utils.LogAlways('Settlement %d is referenced by a successfully sent document and will therefore not be deleted.' % self.settlement.Oid())
        elif len(journalInformations) > 0:
            self.__UpdateSettlementToStoredForAccounted()
            try:
                Utils.LogAlways('Settlement %d is referenced by a journal information and will therefore not be deleted. Settlement status will be set to void.' % self.settlement.Oid())
                self.settlement.Commit()
            except Exception as error:
                Utils.RaiseCommitException(str(error) + '\nCould not update settlement %d' % self.settlement.Oid(), self.settlement)
        else:
            for externalObject in externalObjects:
                for child in externalObject.ChildrenDepthFirst():
                    child.Delete()
                externalObject.Delete()

            Utils.LogAlways('Deleting %s settlement %d' % (self.settlement.SettlementType(), self.settlement.Oid()))
            try:
                if Validations.IsCorrectedSingleRecord(self.settlement):
                    child = self.settlement.Children()[0]
                    child.Parent(None)
                    child.Commit()
                self.settlement.Delete()
            except Exception as error:
                Utils.RaiseCommitException(str(error) + '\nCould not delete settlement %d' % self.settlement.Oid(), self.settlement)

    def __UpdateSettlementToStoredForAccounted(self):
        self.settlement.CorrectionSettlement(None)
        self.settlement.SplitParent(None)
        self.settlement.PartialParent(None)
        self.settlement.PairOffParent(None)
        self.settlement.Parent(None)
        self.settlement.RelationType(RelationType.STORED_FOR_ACCOUNTING)
        self.settlement.Status("Void");
        self.settlement.IsStoredForAccounting(True)

    def __InsertSettlement(self):
        trade = self.settlement.Trade()
        if trade:
            Utils.LogAlways('Inserting settlement of type %s for trade %d' % (self.settlement.SettlementType(), trade.Oid()))
        else:
            Utils.LogAlways('Inserting settlement of type %s' % self.settlement.SettlementType())
        try:
            self.CommitDiary()
            self.settlement.Commit()
        except Exception as error:
            Utils.RaiseCommitException(error, self.settlement)

    def __UpdateSettlement(self):
        if self.commitAction == CommitAction.RECALL:
            Utils.LogAlways('Recalling %s settlement %d' % (self.settlement.SettlementType(), self.settlement.Oid()))
        elif self.commitAction == CommitAction.UPDATE:
            if self.settlement.IsSimulated():
                Utils.LogAlways('Updating %s settlement %d' % (self.settlement.SettlementType(), self.settlement.Oid()))
        try:
            self.CommitDiary()
            if self.updateProcess:
                self.__UpdateSettlementAndSettlementProcess()
            else:
                self.settlement.Commit()
        except Exception as error:
            Utils.RaiseCommitException(error, self.settlement)

    def __UpdateSettlementAndSettlementProcess(self):
        oldProcess = self.settlement.GetSettlementProcess()
        updatedProcess = acm.Operations.HandleUpdateOnSettlementProcess(self.settlement, oldProcess, "")
        self.settlement.UpdateStatusFromSettlementProcess(updatedProcess)
        self.settlement.Commit()
        if oldProcess and updatedProcess:
            if updatedProcess.Original() is not oldProcess:
                updatedProcess.Commit()
            else:
                oldProcess.Apply(updatedProcess)
                oldProcess.Commit()

    def CommitDiary(self):
        if self.settlement.HasDiary():
            diary = self.settlement.Diary()
            self.settlement.Diary().Commit()
            self.settlement.Diary(diary)

    def Commit(self):
        if self.commitAction == CommitAction.DELETE:
            self.__DeleteSettlement()
        elif self.commitAction == CommitAction.INSERT:
            self.__InsertSettlement()
        elif self.commitAction == CommitAction.UPDATE or \
             self.commitAction == CommitAction.RECALL:
            self.__UpdateSettlement()
        else:
            raise Exception('Incorrect commit action: %d' % self.commitAction)


