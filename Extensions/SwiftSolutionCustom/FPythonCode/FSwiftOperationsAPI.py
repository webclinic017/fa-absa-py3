""" Compiled: 2019-07-01 15:14:44 """

#__src_file__ = "extensions/swift/etc/FSwiftOperationsAPI.py"
"""----------------------------------------------------------------------------
MODULE:
    FOperationsSwiftAPI

DESCRIPTION:
    This is a READ ONLY module. This API provides a facade to several utility
    operations functions and methods which are private, but published.


(c) Copyright 2017 FIS FRONT ARENA. All rights reserved.
----------------------------------------------------------------------------"""

import importlib
import acm
import FOperationsAMBAMessage
import FSwiftMessageTypeCalculator
import FOperationsUtils as Utils
import FOperationsDocumentProcess
import FOperationsDocumentService
from FSettlementEnums import SettlementStatus
from FSwiftExceptions import DocServiceSwiftMessageException


#-------------------------------------------------------------------------
def _assertIsSettlementOrConfirmation(fObject):
    assert hasattr(fObject, 'IsKindOf') and (fObject.IsKindOf(acm.FSettlement) or fObject.IsKindOf(acm.FConfirmation)), "Argument not of type FSettlement or FConfirmation"

#-------------------------------------------------------------------------
def _assertIsSettlement(fObject):
    assert hasattr(fObject, 'IsKindOf') and fObject.IsKindOf(acm.FSettlement), "Argument not of type FSettlement"

#-------------------------------------------------------------------------
def _importModuleFromString(module):
    imp_module = None
    try:
        imp_module = importlib.import_module(module)
    except Exception as e:
        Utils.Log(True, 'Error when importing module %s: %s' % (module, e))
        imp_module = __import__(module)
    return imp_module

#-------------------------------------------------------------------------
def _getModuleHandle(fObject):
    module = ''
    try:
        mt_type = FSwiftMessageTypeCalculator.Calculate(fObject)
        moduleName = 'FSwiftMT%s' % str(mt_type)
        module = _importModuleFromString(moduleName)
    except Exception as e:
        Utils.Log(True, 'Error when importing module %s: %s' % (moduleName, e))
    return module

#-------------------------------------------------------------------------
def SuppressPaymentMessageAck(settlement):
    """ Function SuppressPaymentMessageAck
        Executes FSuppressPaymentMessageAck action
        on a settlement

        INPUT:  FSettlement settlement
        OUTPUT: -                                                   """

    _assertIsSettlement(settlement)
    try:
        suppressPaymentMessageAck = acm.FSuppressPaymentMessageAck(settlement)
        suppressPaymentMessageAck.Execute()
        suppressPaymentMessageAck.CommitResult()
    except Exception as error:
        Utils.RaiseCommitException(error)

#-------------------------------------------------------------------------
def PartialSettlement(settlement, settledAmount):
    """ Function PartialSettlement
        Executes FPartialSettlement action
        on a settlement and returns a list with all
        inserted settlements.

        INPUT:  FSettlement settlement
                double settledAmount
        OUTPUT: List of inserted settlements                        """

    _assertIsSettlement(settlement)
    try:
        partialSettlement = acm.FPartialSettlement(settlement, settledAmount)
        partialSettlement.Execute()
        result = partialSettlement.CommitResult()
        return result.InsertedSettlements()
    except Exception as error:
        Utils.Log(True, 'Error when executing action PartialSettlement on settlement %d: %s' % (settlement.Oid(), error))
        raise error

#-------------------------------------------------------------------------
def SetSettledDataOnHierarchy(settlement, settledDate, cashAmount, settledAmount):
    """ Function SetSettledDataOnHierarchy
        Sets values such as settled date, cash amount, etc on a hierarchy
        of Delivery versus Payment settlements. Sets the status of the parent
        to 'Settled'

        INPUT:  FSettlement settlement
                String settledDate
                double cashAmount
                double settledAmount
        OUTPUT: -                                                   """

    _assertIsSettlement(settlement)
    try:
        acm.Operations.SetSettledDataOnHierarchy(settlement, settledDate, cashAmount, settledAmount)
    except Exception as error:
        raise error
    acm.BeginTransaction()
    try:
        settlement.Commit()
        for child in settlement.Children():
            child.Commit()
        acm.CommitTransaction()
    except Exception as error:
        acm.AbortTransaction()
        Utils.RaiseCommitException(error)

#-------------------------------------------------------------------------
def PartialChildren(settlement):
    """ Function PartialChildren
        Returns all partial children of a settlement

        INPUT:  FSettlement settlement
        OUTPUT: List of partial children                            """

    _assertIsSettlement(settlement)
    return settlement.PartialChildren()

#-------------------------------------------------------------------------
def Documents(fObject):
    """ Function Documents
        Returns all FOperationsDocument objects that
        refer to fObject

        INPUT:  FObject fObject (FSettlement or FConfirmation)
        OUTPUT: List of FOperationsDocument objects                 """

    _assertIsSettlementOrConfirmation(fObject)
    return fObject.Documents()

#-------------------------------------------------------------------------
def CashAmount(settlement):
    """ Function CashAmount
        Returns the cash amount of a settlement

        INPUT:  FSettlement settlement
        OUTPUT: Total cash amount of the settlement.
                In the case of a Delivery versus Payment
                settlement, the sum of all children settlement
                cash is returned.                                   """

    _assertIsSettlement(settlement)
    return settlement.CashAmount()

#-------------------------------------------------------------------------
def AMBAMessage(message):
    """ Function AMBAMessage
        Returns an FOperationsAMBAMessage object created from the
        actual AMB message

        INPUT:  AMB message
        OUTPUT: An FOperationsAMBAMessage object                    """

    return FOperationsAMBAMessage.AMBAMessage(message)

#-------------------------------------------------------------------------
def CreateAmbaMessageFromString(string):
    """ Function CreateAMBAMessageFromString
        Returns an FOperationsAMBAMessage object created from a
        string

        INPUT:  String string
        OUTPUT: An FOperationsAMBAMessage object                    """

    return FOperationsAMBAMessage.CreateAmbaMessageFromString(string)

#-------------------------------------------------------------------------
def Calculate(fObject):
    """ Function Calculate
        Returns the SWIFT MT type of an FObject

        INPUT:  FObject fObject (FSettlement or FConfirmation)
        OUTPUT: int messageType                                     """

    _assertIsSettlementOrConfirmation(fObject)

    """
        ****************ImP NOTE*****************************
        This is a temporary fix for SwiftSolution issue with longform confirmations
    """
    #if fObject.IsKindOf(acm.FConfirmation):
    #    assert fObject.IsApplicableForSWIFT(), 'Confirmation is not applicable for SWIFT'

    return FSwiftMessageTypeCalculator.CalculateMTOperations(fObject, False)

#-------------------------------------------------------------------------
def InDocumentCreationStatus(fObject):
    """ Function InDocumentCreationStatus
        Returns whether the given object has a status which allows
        for the creations of an FOperationsDocument

        INPUT:  FObject  fObject (FSettlement or FConfirmation)
        OUTPUT: bool True or False                                  """

    _assertIsSettlementOrConfirmation(fObject)
    return FOperationsDocumentProcess.InDocumentCreationStatus(fObject)

#-------------------------------------------------------------------------
def IsMissingMTDocument(fObject):
    """ Function IsMissingMTDocument
        Returns True if there are no MTMessages referring
        to this object.

        INPUT:  FObject fObject (FSettlement or FConfirmation)
        OUTPUT: bool True or False                                  """

    _assertIsSettlementOrConfirmation(fObject)
    return FOperationsDocumentProcess.IsMissingMTDocument(fObject)

#-------------------------------------------------------------------------
def InSendDocumentStatus(fObject):
    """ Function InSendDocumentStatus
        Returns True if the FObject has a status which allows for
        the dispatch of an FOperationsDocument

        INPUT:  FObject fObject (FSettlement or FConfirmation)
        OUTPUT: bool True or False                                  """

    _assertIsSettlementOrConfirmation(fObject)
    return FOperationsDocumentProcess.InSendDocumentStatus(fObject)

#-------------------------------------------------------------------------
def CreateDocumentService(parameters):
    """ Function CreateDocumentService
        Returns an instance of the document service used in PRIME.

        INPUT:  FDocumentationParameters parameters
        OUTPUT: Instance of AdaptivDoc111 or
                Custom Document Service (if implemented)            """

    return FOperationsDocumentService.CreateDocumentService(parameters)

#-------------------------------------------------------------------------
def GetPartyDetails(fObject):
    """ Function GetPartyDetails
        Returns a list of dictionaries containing SWIFT specific party
        information

        INPUT:  FObject fObject (FSettlement or FConfirmation)
        OUTPUT: List of dictionaries                                """

    _assertIsSettlementOrConfirmation(fObject)
    module = _getModuleHandle(fObject)
    return module.GetPartyDetails(fObject)

#-------------------------------------------------------------------------
def GetAccountNumber(fObject):
    """ Function GetAccountNumber
        Returns an account number (the actual source of the account is
        dependent on the actual implementation which spans modules
        FSwiftMT540, FSwiftMT541, FSwiftMT542, FSwiftMT543).

        INPUT:  FObject fObject (FSettlement or FConfirmation)
        OUTPUT: String account number                               """

    _assertIsSettlementOrConfirmation(fObject)
    module = _getModuleHandle(fObject)
    return module.GetAccountNumber(fObject)

#-------------------------------------------------------------------------
def SetHiearchyToReplaced(settlement):
    """ Function SetHiearrchyToReplaced
        Sets the given settlement, including any descendants, to status
        Replaced.

        INPUT:  FFSettlement
        OUTPUT: -                                                   """

    _assertIsSettlement(settlement)
    settlement.Status(SettlementStatus.REPLACED)
    for child in settlement.Children():
        SetHiearchyToReplaced(child)

#-------------------------------------------------------------------------
def SettlementNeedsApproval(settlement):
    """ Function SettlementNeedsApproval
        Returns True if the settlement still needs to be processed
        in the settlement approval process.

        INPUT:  FFSettlement
        OUTPUT: bool True or False                                  """

    _assertIsSettlement(settlement)
    return settlement.IsApprovalNeeded()

#-------------------------------------------------------------------------
def ClearSettledDataOnHierarchy(settlement):
    """ Function ClearSettledDataOnHierarchy
        Clears Settled Day and Settled Amount on the given settlement, 
        including any children.

        INPUT:  FFSettlement
        OUTPUT: -                                                   """

    _assertIsSettlement(settlement)
    settlement.SettledAmount(0)
    settlement.SettledDay('')
    for child in settlement.Children():
        child.SettledAmount(0)
        child.SettledDay('')

#-------------------------------------------------------------------------
def CreateDocServiceSwiftMessages(fObject):
    """ Function CreateDocServiceSwiftMessages
        Creates the corespondent SWIFT message(s) for the given confirmation
        or settlement and returns it as a list of strings

        INPUT:  FObject fObject (FSettlement or FConfirmation)
        OUTPUT: A list of strings containing the created messages    """

    _assertIsSettlementOrConfirmation(fObject)
    
    if fObject.IsKindOf(acm.FConfirmation):
        assert fObject.IsApplicableForSWIFT(), 'Confirmation is not applicable for SWIFT'

    import ael
    import FOperationsDocumentService as DocumentMod
    import FSwiftMessageTypeExtractor as ExtractorMod
    import FDocumentationParameters as Params
    import FOperationsDocumentXMLCreator as XmlCreator

    createdDocuments = list()

    try:
        docService = DocumentMod.CreateDocumentService(Params)

        if fObject.IsKindOf(acm.FSettlement):
            import FSettlementSwiftXMLSpecifier

            rec = ael.Settlement[fObject.Oid()]
            xmlSpecifier = FSettlementSwiftXMLSpecifier.SettlementSwiftXMLSpecifier("", rec)
        else:
            import FConfirmationSwiftXMLSpecifier

            rec = ael.Confirmation[fObject.Oid()]
            xmlSpecifier = FConfirmationSwiftXMLSpecifier.ConfirmationSwiftXMLSpecifier("", rec)

        if docService.IsConnected():
            mtExtractor = ExtractorMod.FSwiftMessageTypeExtractor(docService)
            xml2 = XmlCreator.ToXml(xmlSpecifier)
            docIds = docService.CreateDocument(xml2)

            for docId in docIds:
                document = docService.GetDocument(docId, FOperationsDocumentService.DocumentFormat.ASCII).GetData()
                createdDocuments.append(document)
        else:
            raise Exception('Could not create document: No connection to document service.')

    except Exception as e:
        raise DocServiceSwiftMessageException('Failed to create message(s) : {}'.format(e))

    return createdDocuments

#-------------------------------------------------------------------------
# Exceptions
#-------------------------------------------------------------------------
def GetAMBAMessageExceptionException():
    from FOperationsExceptions import AMBAMessageException
    return AMBAMessageException

#-------------------------------------------------------------------------
# Confirmation Enums
#-------------------------------------------------------------------------
def GetConfirmationStatusEnum():
    from FConfirmationEnums import ConfirmationStatus
    return ConfirmationStatus

#-------------------------------------------------------------------------
def GetConfirmationTypeEnum():
    from FConfirmationEnums import ConfirmationType
    return ConfirmationType

#-------------------------------------------------------------------------
def GetDatePeriodMethodEnum():
    from FConfirmationEnums import DatePeriodMethod
    return DatePeriodMethod

#-------------------------------------------------------------------------
def GetEventTypeEnum():
    from FConfirmationEnums import EventType
    return EventType

#-------------------------------------------------------------------------
# Operations Enums
#-------------------------------------------------------------------------
def GetAccountTypeEnum():
    from FOperationsEnums import AccountType
    return AccountType

#-------------------------------------------------------------------------
def GetBarrierMonitoringEnum():
    from FOperationsEnums import BarrierMonitoring
    return BarrierMonitoring

#-------------------------------------------------------------------------
def GetBarrierOptionTypeEnum():
    from FOperationsEnums import BarrierOptionType
    return BarrierOptionType

#-------------------------------------------------------------------------
def GetBusinessEventStatusEnum():
    from FOperationsEnums import BusinessEventStatus
    return BusinessEventStatus

#-------------------------------------------------------------------------
def GetBusinessEventTypeEnum():
    from FOperationsEnums import BusinessEventType
    return BusinessEventType

#-------------------------------------------------------------------------
def GetCashFlowTypeEnum():
    from FOperationsEnums import CashFlowType
    return CashFlowType

#-------------------------------------------------------------------------
def GetExerciseTypeEnum():
    from FOperationsEnums import ExerciseType
    return ExerciseType

#-------------------------------------------------------------------------
def GetExoticEventTypeEnum():
    from FOperationsEnums import ExoticEventType
    return ExoticEventType

#-------------------------------------------------------------------------
def GetInsTypeEnum():
    from FOperationsEnums import InsType
    return InsType

#-------------------------------------------------------------------------
def GetLegTypeEnum():
    from FOperationsEnums import LegType
    return LegType

#-------------------------------------------------------------------------
def GetOpenEndStatusEnum():
    from FOperationsEnums import OpenEndStatus
    return OpenEndStatus

#-------------------------------------------------------------------------
def GetOperationsEnum():
    from FOperationsEnums import Operations
    return Operations

#-------------------------------------------------------------------------
def GetQuotationTypeEnum():
    from FOperationsEnums import QuotationType
    return QuotationType

#-------------------------------------------------------------------------
def GetSettleTypeEnum():
    from FOperationsEnums import SettleType
    return SettleType

#-------------------------------------------------------------------------
def GetSignOffStatusEnum():
    from FOperationsEnums import SignOffStatus
    return SignOffStatus

#-------------------------------------------------------------------------
def GetTradeStatusEnum():
    from FOperationsEnums import TradeStatus
    return TradeStatus

#-------------------------------------------------------------------------
def GetTradeTypeEnum():
    from FOperationsEnums import TradeType
    return TradeType

#-------------------------------------------------------------------------
def GetPartyTypeEnum():
    from FOperationsEnums import PartyType
    return PartyType

#-------------------------------------------------------------------------
# Operations Document Enums
#-------------------------------------------------------------------------
def GetDocumentFormatEnum():
    from FOperationsDocumentEnums import DocumentFormat
    return DocumentFormat

#-------------------------------------------------------------------------
def GetDataTypeEnum():
    from FOperationsDocumentEnums import DataType
    return DataType

#-------------------------------------------------------------------------
def GetOperationsDocumentStatusEnum():
    from FOperationsDocumentEnums import OperationsDocumentStatus
    return OperationsDocumentStatus

#-------------------------------------------------------------------------
def GetOperationsDocumentTypeEnum():
    from FOperationsDocumentEnums import OperationsDocumentType
    return OperationsDocumentType

#-------------------------------------------------------------------------
# Settlement Enums
#-------------------------------------------------------------------------
def GetSettlementStatusEnum():
    from FSettlementEnums import SettlementStatus
    return SettlementStatus

#-------------------------------------------------------------------------
def GetStatusExplanationEnum():
    from FSettlementEnums import StatusExplanation
    return StatusExplanation

#-------------------------------------------------------------------------
def GetRelationTypeEnum():
    from FSettlementEnums import RelationType
    return RelationType

#-------------------------------------------------------------------------
def GetSettlementDeliveryTypeEnum():
    from FSettlementEnums import SettlementDeliveryType
    return SettlementDeliveryType

#-------------------------------------------------------------------------
def GetNettingRuleTypeEnum():
    from FSettlementEnums import NettingRuleType
    return NettingRuleType

#-------------------------------------------------------------------------
def GetPartialSettlementTypeEnum():
    from FSettlementEnums import PartialSettlementType
    return PartialSettlementType

#-------------------------------------------------------------------------
def GetSettlementTypeEnum():
    from FSettlementEnums import SettlementType
    return SettlementType
