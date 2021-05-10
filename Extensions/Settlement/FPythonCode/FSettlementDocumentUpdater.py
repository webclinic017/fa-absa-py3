""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementDocumentUpdater.py"
import acm

# Settlement
from FSettlementSecurityUpdateEngine import SecurityUpdateEngine
from FSettlementEnums import SettlementStatus, RelationType
from FSettlementCommitter import CommitAction
from FSettlementQueries import GetSameOidAndSentSuccessfullyQuery, GetSameOidQuery, GetSwiftMessageNotTypeQuery, GetSwiftMessageOrTypeQuery

# Operations
from FOperationsProvidedObject import IEngineTask
from FOperationsAMBAMessage import AMBAMessageException
from FOperationsExceptions import CommitException
from FOperationsDocumentEnums import OperationsDocumentStatus
from FOperationsAMBAMessage import TypeOfChange

#-------------------------------------------------------------------------
class FSettlementDocumentUpdater(IEngineTask):

    #-------------------------------------------------------------------------
    def __init__(self, configuration):
        self.__settlementCommiter = configuration.settlementCommitterIF
        self.__nettingRuleCache = configuration.nettingRuleCacheIF
        self.__ambaMessageCreator = configuration.ambaMessageIF

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def PO_Clear(self):
        pass

    #-------------------------------------------------------------------------
    def ST_Run(self, msg, obj):
        ambaMessage = self.__ambaMessageCreator(msg)
        assert ambaMessage.GetNameOfUpdatedTable() == 'OPERATIONSDOCUMENT'
        if ambaMessage.GetTypeOfUpdate() == 'UPDATE':
            self.__Update(ambaMessage)
        elif ambaMessage.GetTypeOfUpdate() == 'INSERT':
            self.__Insert(ambaMessage)

    #-------------------------------------------------------------------------
    def __Insert(self, ambaMessage):
        self.__Update(ambaMessage)

    #-------------------------------------------------------------------------
    def __Update(self, ambaMessage):
        tables = ambaMessage.GetTableAndChildTables()
        operationsDocumentTable = tables[0]

        try:
            settlementId = int(operationsDocumentTable.GetAttribute('SETTLEMENT_SEQNBR').GetCurrentValue())
            if settlementId == 0:
                self.__provider.LP_Log("Ignoring OperationsDocument for confirmation")
                return
            status = operationsDocumentTable.GetAttribute('STATUS').GetCurrentValue()
            operationsDocumentId = operationsDocumentTable.GetAttribute('SEQNBR').GetCurrentValue()
            updateUser = operationsDocumentTable.GetAttribute('OWNER_USRNBR.USERID').GetCurrentValue()
            opdoc = acm.FOperationsDocument[operationsDocumentId]
            if opdoc:
                if opdoc.Settlement() and settlementId and (settlementId != opdoc.Settlement().Oid()):
                    self.__provider.LP_Log("Got OperationsDocument %s AMB message but wrong settlement %d (expected %d)" % (operationsDocumentId, settlementId, opdoc.Settlement().Oid()))

        except AMBAMessageException as error:
            self.__provider.LP_Log('AMBAMessageException in %s: %s' % (self.ST_Run.__name__, str(error)))
            return
        self.__provider.LP_LogVerbose("Got OperationsDocument %s updated by user %s" % (operationsDocumentId, updateUser))
        if operationsDocumentTable.GetTypeOfChange() == TypeOfChange.INSERT or operationsDocumentTable.GetAttribute('STATUS').HasChanged():
            if opdoc:
                self.__UpdateStatusAfterOperationsDocument(status, opdoc.Settlement())
        if opdoc:
            try:
                SecurityUpdateEngine(self.__nettingRuleCache).UpdateSettlementsAfterOperationsDocumentChange(opdoc.Settlement(), ambaMessage)
            except CommitException as error:
                self.__provider.LP_Log('Error while committing settlements: %s' % str(error))
        

    #-------------------------------------------------------------------------
    def __UpdateStatusAfterOperationsDocument(self, status, settlement):
        if not settlement:
            return
        if settlement:
            settlementStatus = settlement.Status()
            if status == OperationsDocumentStatus.SENT_SUCCESSFULLY:
                if settlementStatus == SettlementStatus.PENDING_CANCELLATION:
                    if GetSwiftMessageOrTypeQuery(settlement).Select().Size() == \
                        GetSwiftMessageNotTypeQuery(settlement).Select().Size():
                        settlement.Status(SettlementStatus.AUTHORISED)
                        settlement.STP()
                elif settlementStatus == SettlementStatus.NOT_ACKNOWLEDGED:
                    if self.__AllowedToGoFromNackToAck(settlement):
                        self.__SetAcknowledgedStatus(settlement)
                        settlement.IsSwiftNAK(False)
                elif settlementStatus == SettlementStatus.RELEASED:
                    if GetSameOidAndSentSuccessfullyQuery(settlement).Select().Size() == \
                        GetSameOidQuery(settlement).Select().Size():
                        self.__SetAcknowledgedStatus(settlement)
            elif status == OperationsDocumentStatus.SEND_FAILED:
                settlement.Status(SettlementStatus.NOT_ACKNOWLEDGED)
                settlement.IsSwiftNAK(True)
            elif status == OperationsDocumentStatus.EXCEPTION:
                settlement.Status(SettlementStatus.NOT_ACKNOWLEDGED)
                settlement.IsInsufficientMessageData(True)
            else:
                return

            try:
                self.__settlementCommiter(settlement, CommitAction.UPDATE).Commit()
            except CommitException as exceptionString:
                self.__provider.LP_Log('Tried to change settlement status from %s to %s' % (settlementStatus, settlement.Status()))
        

    #-------------------------------------------------------------------------
    def __SetAcknowledgedStatus(self, settlement):
        if settlement.IsSecurity() and settlement.RelationType() in [RelationType.CANCELLATION, RelationType.CANCEL_CORRECT]:
            settlement.Status(SettlementStatus.PENDING_CLOSURE)
        else:
            settlement.Status(SettlementStatus.ACKNOWLEDGED)

    #-------------------------------------------------------------------------
    def __AllowedToGoFromNackToAck(self, settlement):
        return ((settlement.Status() == SettlementStatus.NOT_ACKNOWLEDGED) \
                and settlement.IsSwiftNAK() \
                and GetSameOidAndSentSuccessfullyQuery(settlement).Select().Size() == \
                    GetSameOidQuery(settlement).Select().Size())
