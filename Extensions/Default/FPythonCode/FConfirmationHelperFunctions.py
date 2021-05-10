""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationHelperFunctions.py"
import acm
import FOperationsUtils as Utils
from FOperationsEnums import TradeStatus, TradeType
from FConfirmationEnums import ConfirmationStatus, ConfirmationType

#-------------------------------------------------------------------------
class FConfirmationHelperFunctions(object):
    postReleasedStatuses =   [ConfirmationStatus.RELEASED,
                              ConfirmationStatus.ACKNOWLEDGED,
                              ConfirmationStatus.NOT_ACKNOWLEDGED,
                              ConfirmationStatus.MATCHED,
                              ConfirmationStatus.PARTIAL_MATCH,
                              ConfirmationStatus.PENDING_MATCHING,
                              ConfirmationStatus.VOID,
                              ConfirmationStatus.MATCHING_FAILED
                              ]

    #-------------------------------------------------------------------------
    @staticmethod
    def IsPostReleasedConfirmation(confirmation):
        return confirmation.Status() in FConfirmationHelperFunctions.postReleasedStatuses

    #-------------------------------------------------------------------------
    @staticmethod
    def IsPreReleasedConfirmation(confirmation):
        return not FConfirmationHelperFunctions.IsPostReleasedConfirmation(confirmation)

    #-------------------------------------------------------------------------
    @staticmethod
    def GetTopmostConfirmation(confirmation):

        resultSet = acm.FConfirmation.Select('confirmationReference = %d' % confirmation.Oid())
        if len(resultSet) == 0:
            return confirmation
        else:
            return FConfirmationHelperFunctions.GetTopmostConfirmation(resultSet[0])

    #-------------------------------------------------------------------------
    @staticmethod
    def IsTopMostConfirmation(confirmation):
        resultSet = acm.FConfirmation.Select('confirmationReference  = %d' % confirmation.Oid())
        return (len(resultSet) == 0)

    #-------------------------------------------------------------------------
    @staticmethod
    def GetChaserRootConfirmation(confirmation):
        chasedConfirmation = confirmation.ChasingConfirmation()
        if chasedConfirmation:
            return FConfirmationHelperFunctions.GetChaserRootConfirmation(chasedConfirmation)
        else:
            return confirmation

    #-------------------------------------------------------------------------
    @staticmethod
    def IsApplicableForChaserGeneration(confirmation):
        rootConfirmation = FConfirmationHelperFunctions.GetChaserRootConfirmation(confirmation)
        return (FConfirmationHelperFunctions.IsTopMostConfirmation(rootConfirmation) and
                FConfirmationHelperFunctions.IsTopMostConfirmation(confirmation))

    #-------------------------------------------------------------------------
    @staticmethod
    def GetBottommostConfirmation(confirmation):
        referencedConfirmation = confirmation.ConfirmationReference()
        if referencedConfirmation:
            return FConfirmationHelperFunctions.GetBottommostConfirmation(referencedConfirmation)
        else:
            return confirmation

    #-------------------------------------------------------------------------
    @staticmethod
    def IsFarLegTrade(trade):
        return (trade.TradeProcessesToString().find('Swap Far Leg') > -1)

    #-------------------------------------------------------------------------
    @staticmethod
    def GetLegs(instrument):
        for leg in instrument.Legs():
            yield leg
        if instrument.IsKindOf(acm.FCombination):
            for ins in instrument.Instruments():
                for leg in FConfirmationHelperFunctions.GetLegs(ins):
                    yield leg

    #-------------------------------------------------------------------------
    @staticmethod
    def GetDefaultCalendar():
        try:
            calendar = acm.UsedValuationParameters().AccountingCurrency().Calendar()
        except Exception:
            calendar = acm.FCalendar['Target']
        return calendar

    #-------------------------------------------------------------------------
    @staticmethod
    def IsPastExpiryDay(confirmation):
        if not confirmation.ExpiryDay():
            return False
        Today = acm.GetFunction('dateToday', 0)
        return confirmation.ExpiryDay() < Today()

    #-------------------------------------------------------------------------
    @staticmethod
    def GetIsNewTradeEvent():
        query = acm.CreateFASQLQuery(acm.FTrade, 'OR')
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.FO_CONFIRMED))
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.BO_CONFIRMED))
        query.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.BO_BO_CONFIRMED))
        return query

    #-------------------------------------------------------------------------
    @staticmethod
    def GetConfInstructionRuleFromConfirmation(confirmation):
        bestRule = None
        for i in confirmation.ConfInstruction().ConfInstructionRules():
            if i.Type() == confirmation.Type():
                bestRule = i
            if i.Type() == ConfirmationType.DEFAULT and bestRule == None:
                bestRule = i
        return bestRule

    #-------------------------------------------------------------------------
    @staticmethod
    def HasConfirmationStructureBeenInReleased(confirmation):
        if confirmation.IsPostRelease() and confirmation.Status() != ConfirmationStatus.VOID:
            return True
        referencedConfirmation = confirmation.ConfirmationReference()
        if referencedConfirmation:
            return FConfirmationHelperFunctions.HasConfirmationStructureBeenInReleased(referencedConfirmation)
        else:
            return False

    #-------------------------------------------------------------------------
    @staticmethod
    def IsDateWithinMaxBankingDaysBackInterval(date, bankingDaysBack):
        dateToday = acm.Time.DateNow()
        calendar = FConfirmationHelperFunctions.GetDefaultCalendar()
        if date >= dateToday:
            return True
        daysBetween = calendar.BankingDaysBetween(date, dateToday)
        if daysBetween <= bankingDaysBack:
            return True
        return False

#-------------------------------------------------------------------------
def GetExpiryDay(confirmation):
    from FConfirmationCreator import FConfirmationCreator as ConfirmationCreator
    return ConfirmationCreator.GetExpiryDay(confirmation)

#-------------------------------------------------------------------------
def GetDefaultConfirmationProcessQuery():
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('Aggregate', 'EQUAL', 0)
    query.AddAttrNode('Type', 'NOT_EQUAL', Utils.GetEnum('TradeType', TradeType.CASH_POSTING))

    orQuery = query.AddOpNode('OR')
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.FO_CONFIRMED))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.BO_CONFIRMED))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.BO_BO_CONFIRMED))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.VOID))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.CONFIRMED_VOID))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.SIMULATED))
    orQuery.AddAttrNode('Status', 'EQUAL', Utils.GetEnum('TradeStatus', TradeStatus.TERMINATED))
    return query

