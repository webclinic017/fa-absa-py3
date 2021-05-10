""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementQueries.py"
import acm
from FOperationsDocumentEnums import OperationsDocumentStatus

#-------------------------------------------------------------------------
def GetSwiftMessageNotTypeQuery(settlement):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    query.AddAttrNode('Settlement.Oid', 'EQUAL', settlement.Oid())
    nonCancellationNode = query.AddOpNode('AND')
    nonCancellationNode.AddAttrNode('SwiftMessageType', 'NOT_EQUAL', 192)
    nonCancellationNode.AddAttrNode('SwiftMessageType', 'NOT_EQUAL', 292)
    nonCancellationNode.AddAttrNode('SwiftMessageType', 'NOT_EQUAL', 192199)
    nonCancellationNode.AddAttrNode('SwiftMessageType', 'NOT_EQUAL', 292299)
    nonCancellationNode.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)
    return query

#-------------------------------------------------------------------------
def GetSwiftMessageOrTypeQuery(settlement):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    query.AddAttrNode('Settlement.Oid', 'EQUAL', settlement.Oid())
    succesefullCancellationNode = query.AddOpNode('OR')

    cancellation192Node = succesefullCancellationNode.AddOpNode('AND')
    cancellation192Node.AddAttrNode('SwiftMessageType', 'EQUAL', 192)
    cancellation192Node.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)

    cancellation292Node = succesefullCancellationNode.AddOpNode('AND')
    cancellation292Node.AddAttrNode('SwiftMessageType', 'EQUAL', 292)
    cancellation292Node.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)

    cancellation192199Node = succesefullCancellationNode.AddOpNode('AND')
    cancellation192199Node.AddAttrNode('SwiftMessageType', 'EQUAL', 192199)
    cancellation192199Node.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)

    cancellation292299Node = succesefullCancellationNode.AddOpNode('AND')
    cancellation292299Node.AddAttrNode('SwiftMessageType', 'EQUAL', 292299)
    cancellation292299Node.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)
    return query

#-------------------------------------------------------------------------
def GetSameOidQuery(settlement):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    query.AddAttrNode('Settlement.Oid', 'EQUAL', settlement.Oid())
    return query

#-------------------------------------------------------------------------
def GetSameOidAndSentSuccessfullyQuery(settlement):
    query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'AND')
    query.AddAttrNode('Settlement.Oid', 'EQUAL', settlement.Oid())
    query.AddAttrNode('Status', 'EQUAL', OperationsDocumentStatus.SENT_SUCCESSFULLY)
    return query
    