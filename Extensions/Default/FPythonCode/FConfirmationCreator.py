""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationCreator.py"
import acm

import FOperationsUtils as Utils
from FConfirmationSingletons import GetSingleton, ConfirmationPreventionRulesHandler
from FConfirmationHelperFunctions import FConfirmationHelperFunctions as HelperFunctions
from FConfirmationChecksum import CreateChecksum
from FConfirmationHookAdministrator import GetConfirmationHookAdministrator, ConfirmationHooks
from FConfirmationEnums import DatePeriodMethod

class FConfirmationCreator(object):

    @staticmethod
    def GetCutoffFromDefault():
        import FConfirmationParameters as ConfirmationParameters

        Today = acm.GetFunction('dateToday', 0)
        defaultDays = ConfirmationParameters.defaultDays
        if ConfirmationParameters.defaultChaserCutoffMethodBusinessDays:
            calendar = HelperFunctions.GetDefaultCalendar()
            adjustedDate = calendar.AdjustBankingDays(Today(), defaultDays)
        else:
            adjustedDate = acm.Time.DateAddDelta(acm.Time.DateToday(), 0, 0, defaultDays)
        return adjustedDate

    @staticmethod
    def GetCutoffFromBusinessDays(periodCount):
        calendar = HelperFunctions.GetDefaultCalendar()
        Today = acm.GetFunction('dateToday', 0)
        adjustedDate = calendar.AdjustBankingDays(Today(), periodCount)
        return adjustedDate

    @staticmethod
    def GetCutOffFromCalendarDays(days):
        months = 0
        years = 0
        return acm.Time.DateAddDelta(acm.Time.DateToday(), years, months, days)


    @staticmethod
    def SetChaserCutoff(confirmation):
        '''Sets cutoff time based on confinstruction. '''
        cutoff = None
        rule = HelperFunctions.GetConfInstructionRuleFromConfirmation(confirmation)
        if rule:
            chaserCutoffMethod = rule.ChaserCutoffMethod()
            if chaserCutoffMethod == DatePeriodMethod.DEFAULT:
                cutoff = FConfirmationCreator.GetCutoffFromDefault()
            elif chaserCutoffMethod == DatePeriodMethod.BUSINESS_DAYS:
                cutoff = FConfirmationCreator.GetCutoffFromBusinessDays(rule.ChaserCutoffPeriodCount())
            elif chaserCutoffMethod == DatePeriodMethod.CALENDAR_DAYS:
                cutoff = FConfirmationCreator.GetCutOffFromCalendarDays(rule.ChaserCutoffPeriodCount())
        confirmation.ChaserCutoff(cutoff)

    @staticmethod
    def GetExpiryDay(confirmation):
        hookAdmin = GetConfirmationHookAdministrator()
        expiryDayCount = hookAdmin.HA_CallHook(ConfirmationHooks.GET_EXPIRY_DAY_COUNT, confirmation)
        calendar = HelperFunctions.GetDefaultCalendar()
        Today = acm.GetFunction('dateToday', 0)
        adjustedDate = calendar.AdjustBankingDays(Today(), expiryDayCount)
        return adjustedDate


    @staticmethod
    def AddConfirmationData(underlyingObject, newConfirmation):
        import FConfirmationParameters as ConfirmationParameters

        newConfirmation.Checksum(CreateChecksum(newConfirmation))
        newConfirmation.ExpiryDay(FConfirmationCreator.GetExpiryDay(newConfirmation))
        if (ConfirmationParameters.setProtectionAndOwnerFromTrade):
            Utils.SetProtectionAndOwnerFromTrade(newConfirmation, underlyingObject.GetTrade())
        newConfirmation.Validate()
        return newConfirmation

    @staticmethod
    def AppendIfValidConfirmation(confirmation, confirmationList):
        if FConfirmationCreator.IsFxSwapLongFormPrevention(confirmation) == False:
            cprh = GetSingleton(ConfirmationPreventionRulesHandler)
            if cprh.IsPreventConfirmationCreation(confirmation) == False:
                confirmationList.append(confirmation)

    @staticmethod
    def SubjectList(event, underlyingObject):
        if event.subType == 'Cash Flow':
            for leg in HelperFunctions.GetLegs(underlyingObject.GetTrade().Instrument()):
                for cashFlow in leg.CashFlows():
                    yield cashFlow
        elif event.subType == 'Reset':
            for leg in HelperFunctions.GetLegs(underlyingObject.GetTrade().Instrument()):
                for reset in leg.Resets():
                    yield reset
        elif event.subType == 'Default':
            pass
        else:
            subTypeMethod = acm.FMethodChain(acm.FSymbol(str(event.subType)))
            subTypeObjects = subTypeMethod.Call([underlyingObject.GetTrade()])
            for subTypeObject in subTypeObjects:
                yield subTypeObject

    @staticmethod
    def IsSubTypeSatisfied(event, subTypeObject, trade):
        if "<type 'FASQLQuery'>" == str(type(event.subTypeRule)):
            return event.subTypeRule.IsSatisfiedBy(subTypeObject)
        return event.subTypeRule.IsSatisfiedBy(subTypeObject, trade)

    @staticmethod
    def CreateConfirmation(underlyingObject, events):
        confirmationList = list()
        for event in events:
            method = acm.FMethodChain(acm.FSymbol(str(event.receiver)))
            receiver = method.Call([underlyingObject.GetTrade()])
            if receiver != None:
                if receiver.IsKindOf(acm.FParty):
                    method = "Trade." + event.receiver
                    if event.subType == 'Default':
                        newConfirmation = acm.Operations.CreateConfirmation(underlyingObject.GetTrade(), event.eventName, None, receiver, method, None)
                        FConfirmationCreator.AddConfirmationData(underlyingObject, newConfirmation)
                        FConfirmationCreator.AppendIfValidConfirmation(newConfirmation, confirmationList)
                    else:
                        for subTypeObject in FConfirmationCreator.SubjectList(event, underlyingObject):
                            if FConfirmationCreator.IsSubTypeSatisfied(event, subTypeObject, underlyingObject.GetTrade()):
                                newConfirmation = acm.Operations.CreateConfirmation(underlyingObject.GetTrade(), event.eventName, subTypeObject, receiver, method, None)
                                FConfirmationCreator.AddConfirmationData(underlyingObject, newConfirmation)
                                FConfirmationCreator.AppendIfValidConfirmation(newConfirmation, confirmationList)
                else:
                    logmsg = "Method chain '%s' returned '%s', expected 'FParty'. No confirmation will be created for this receiver."
                    Utils.LogVerbose(logmsg % (event.receiver, receiver.Class().Name()))
            else:
                Utils.LogVerbose("Method chain '%s' did not return a value. No confirmation will be created for this receiver." % (event.receiver))
        return confirmationList

    @staticmethod
    def IsFxSwapLongFormPrevention(confirmation):
        isFxSwapLongFormPrevention = False
        if confirmation.IsApplicableForSWIFT() == False:
            if HelperFunctions.IsFarLegTrade(confirmation.Trade()):
                isFxSwapLongFormPrevention = True
        return isFxSwapLongFormPrevention

