""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendDealUtils.py"
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendDealUtils

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Business logic for creating / modifying security loans.
    Interface classes; the logic is implemented elsewhere. The classes only publish methods use as interface points.

------------------------------------------------------------------------------------------------"""

import acm
from DealDevKit import ReturnDomainDecorator
from ACMPyUtils import Transaction
import traceback
import FSecLendHandler
from FSecLendHandler import SecurityLoanTradeAction

# Interface for utilizing specific business logic relating to non-standard security loans.
# Get the wrapper by SecurityLoanWrapper.Wrap(Trade).
# This interface works with Logic Decorator objects.
class SecurityLoanWrapper(object):

    def __init__(self, trade):
        self.trade = trade
        if (trade.Instrument().IsClone()) or (trade.Instrument().IsInfant()):
            self.handler = FSecLendHandler.SecurityLoanHandler(self.trade.Instrument())
        else:
            self.handler = FSecLendHandler.SecurityLoanHandler(self.trade.Instrument().StorageImage())

        self.tradehandler = FSecLendHandler.SecurityLoanTradeHandler(trade)

    # -------------   Utility functions -------------

    def Trade(self):
        return self.trade

    def Instrument(self):
        return self.handler.Instrument()

    def ReceiveLeg(self):
        return self.handler.ReceiveLeg()

    def PayLeg(self):
        return self.handler.PayLeg()

    def Legs(self):
        return self.handler.Legs()

    def RebateLeg(self):
        return self.handler.RebateLeg()

    # Returns a wrapper to set/get the fee
    def FeePayLeg(self):
        return self.handler.FeePayLeg()

    def FeeReceiveLeg(self):
        return self.handler.FeeReceiveLeg()

    def FeeRebateLeg(self):
        return self.handler.FeeRebateLeg()

    # -------------  Methods used in deal entry UI  -------------

    @ReturnDomainDecorator('bool')
    def IsRebate(self, value='NoValue', *args):
        return self.handler.IsRebate(value, *args)

    @ReturnDomainDecorator('string')
    def UnderlyingSpotDays(self, *args):
        return self.handler.UnderlyingSpotDays(*args)

    @ReturnDomainDecorator('double')
    def InitialCashAmount(self, value='NoValue'):
        return self.tradehandler.InitialCashAmount(value)

    @ReturnDomainDecorator('double')
    def Nominal(self, value='NoValue'):
        return self.tradehandler.Nominal(value)

    @ReturnDomainDecorator('string')
    def RollType(self, value='NoValue', *args):
        return self.handler.RollType(value, *args)

    @ReturnDomainDecorator('bool')
    def IsDvPSettled(self, value='NoValue', *args):
        return self.handler.IsDvPSettled(value, *args)

    @ReturnDomainDecorator('bool')
    def IsPaymentDvPSettled(self, value='NoValue', *args):
        return self.tradehandler.IsPaymentDvPSettled(value, *args)

    @ReturnDomainDecorator('double')
    def DvpPaymentInitialMargin(self, value='NoValue', *args):
        return self.tradehandler.DvpPaymentInitialMargin(value, *args)

    @ReturnDomainDecorator('double')
    def DvPPaymentCashAmount(self, value='NoValue', *args):
        return self.tradehandler.DvPPaymentCashAmount(value, *args)

    @ReturnDomainDecorator('FCurrency')
    def DvpPaymentCashCurrency(self, value='NoValue', *args):
        return self.tradehandler.DvpPaymentCashCurrency(value, *args)

    @ReturnDomainDecorator('double')
    def CalcFXRate(self, fromCurr, toCurr,*args):
        return self.tradehandler.CalcFXRate(fromCurr, toCurr, *args)

    def RefreshDvPPaymentAmount(self, oldNominal, newNominal, *args):
        return self.tradehandler.RefreshDvPPaymentAmount(oldNominal, newNominal, *args)

    def UpdateDvPPayment(self, updateCurrency = False, *args):
        return self.tradehandler.UpdateDvPPayment(updateCurrency, *args)

    def IsFloatRebate(self, *args):
        return self.handler.IsFloatRebate(*args)

    def GetLegCurrentSingleReset(self, leg):
        return self.handler.GetLegCurrentSingleReset(leg)

    def RebateRate(self, value='NoValue'):
        return self.handler.RebateRate(value)

    def GetOrCreateDefaultIndexRefFixingDateRule(self, underlying):
        return self.handler.GetOrCreateDefaultIndexRefFixingDateRule(underlying)

    # -------------  Methods used in deal entry UI  -------------

    def HasCashCollateralPool(self, value=None):
        return self.handler.HasCashCollateralPool(value)

    def ExtendOpenEnd(self, newEndDate):
        self.handler.ExtendOpenEnd(newEndDate)

    def LegInitialNominalScalingEstimate(self, leg):
        return self.handler.LegInitialNominalScalingEstimate(leg)

    def LegInitialIndexFXEstimate(self, leg):
        return self.handler.LegInitialIndexFXEstimate(leg)

    # ------------------- Trade actions functions  -------------------

    def CreateTradeActionTrade(self,
                               quantity,
                               valueDay=None,
                               tradeTime=None,
                               status=None,
                               orderType=None,
                               pendingOrder=None):
        gui = self.Trade().GUI()
        tradeAction = FSecLendHandler.SecurityLoanTradeAction.CreateTradeActionTrade(self.Trade(), quantity, valueDay, tradeTime, status, orderType, pendingOrder)
        return acm.FBusinessLogicDecorator.WrapObject(tradeAction, gui)

    def CreateCloseTrade(self,
                          quantity,
                          valueDay=None,
                          tradeTime=None,
                          status=None,
                          orderType=None,
                          pendingOrder=None):
        gui = self.Trade().GUI()
        tradeAction = FSecLendHandler.SecurityLoanTradeAction.CreateCloseTrade(self.Trade(), quantity, valueDay, tradeTime, status, orderType, pendingOrder)
        return acm.FBusinessLogicDecorator.WrapObject(tradeAction, gui)

    def CreateAdjustTrade(self,
                          quantity,
                          valueDay=None,
                          tradeTime=None,
                          status=None,
                          orderType=None,
                          pendingOrder=None):
        gui = self.Trade().GUI()
        tradeAction = FSecLendHandler.SecurityLoanTradeAction.CreateAdjustTrade(self.Trade(), quantity, valueDay, tradeTime, status, orderType, pendingOrder)
        return acm.FBusinessLogicDecorator.WrapObject(tradeAction, gui)

    # ------------------- Trade actions utils -------------------

    def _RemainingQuantity(self):
        return FSecLendHandler.SecurityLoanTradeAction._RemainingQuantity(self.Trade())

    def _AdjustValueDate(self, valueDay):
        return FSecLendHandler.SecurityLoanTradeAction._AdjustValueDate(self.Trade(), valueDay)

    # ------------------- Wrappers -------------------

    # Returns a wrapper to set/get the fee
    def Fee(self):
        return FeeWrapper(self.PayLeg())

    # Use this method to get the wrapper interface object for an existing trade
    @classmethod
    def Wrap(cls, target):
        if isinstance(target, acm._pyClass('FTrade')):
            return cls.Wrap(acm.FBusinessLogicDecorator.WrapObject(target))
        elif isinstance(target, acm._pyClass('FTradeLogicDecorator')):
            return cls(target)
        elif isinstance(target, acm._pyClass('FDealPackage')):
            trades = target.Trades()
            return cls.Wrap(trades.First()) if trades.Size() == 1 else None

    def Save(self, generateCashflows=True, excludeHistorical=True):
        with Transaction():
            if generateCashflows:
                self.handler.RegenerateCashFlows(excludeHistorical)
            self.Instrument().Commit()
            self.Trade().Commit()



# Interface Wrapper for handling fee:s from spread resets

class FeeWrapper(object):

    def __init__(self, leg):
        self.leg = leg
        self.legHandler = FSecLendHandler.SecurityLoanLegHandler(leg)

    def LastFeeDay(self):
        return self.legHandler.LastFeeDay()

    def FirstOrLastFixedStoredSpreadReset(self):
        return self.legHandler.FirstOrLastFixedStoredSpreadReset()

    def FeeAtDate(self, date, fee='NoValue'):
        return self.legHandler.FeeAtDate(date, fee)

    def StartingFee(self, value='NoValue'):
        return self.legHandler.StartingFee(value)

    def AdjustFixingDate(self, baseDate):
        return self.legHandler.AdjustFixingDate(baseDate)

    def SpreadResetAtDate(self, date):
        return self.legHandler.SpreadResetAtDate(date)

    def SpreadResetBoundaries(self):
        return self.legHandler.SpreadResetBoundaries()

    def CalendarInformation(self):
        return self.legHandler.CalendarInformation()


def GetStartingFee(leg):
    return FeeWrapper(leg).StartingFee()


def SetStartingFee(leg, fee):
    FeeWrapper(leg).StartingFee(fee)


def GetFeeFromFixings(leg, date):
    wrapper = FeeWrapper(leg)
    date = wrapper.AdjustFixingDate(date)
    return FeeWrapper(leg).FeeAtDate(date)


def GetFixingEstimates(estimateDates, leg):
    try:
        if estimateDates.IsEmpty():
            return []
        spreadFixings = acm.FArray()
        spreadFixings.AddAll([v for cf in leg.CashFlows() for v in cf.Resets() if v.ResetType() == "Spread"])
        spreadFixings.SortByProperty('Day')
        spreadFixingEstimateValues = list()
        i = 0
        value = 0.0
        for f in spreadFixings:
            if i >= len(estimateDates):
                break
            if f.IsFixed():
                value = f.FixFixingValue()
            if f.Day() == acm.Time.AsDate(estimateDates[i]):
                spreadFixingEstimateValues.append(
                    acm.GetFunction('denominatedvalue', 4)(value, None, None, estimateDates[i])
                )
                i = i + 1
        return spreadFixingEstimateValues
    except Exception as e:
        return [acm.Math.NotANumber()]


# Class for creating security loan instruments
class SecurityLoanCreator(object):

    # Use this function to create a new security loan instrument.
    # Keyword accepted are the arguments for function SecurityLoanSetDefaultFields.
    @classmethod
    def CreateInstrument(cls, **kwargs):
        instrument = acm.DealCapturing.CreateNewInstrument('Security Loan')
        cls.SecurityLoanSetDefaultFields(instrument, **kwargs)
        return instrument

    # Use this function to create a new master security loan instrument.
    # Keyword accepted are the arguments for function MasterSecurityLoanSetDefaultFields.
    @classmethod
    def CreateMasterSecurityLoan(cls, **kwargs):
        underlying = kwargs.get('underlying')
        if underlying:
            if not acm.FSecurityLoan.Select('underlying = {0} and productTypeChlItem = "{1}"'.
                                                    format(underlying.Originator().Oid(), "Master Security Loan")):
                instrument = acm.DealCapturing.CreateNewInstrument('Security Loan')
                cls.MasterSecurityLoanSetDefaultFields(instrument, **kwargs)
                return instrument
            else:
                raise Exception('There already exists a master security loan for ' + underlying.Name())

    # Use this function to create a new master security loan trade.
    # Keyword accepted are the arguments for function SecurityLoanTradeSetDefaultFields.
    # Arguments for orders are set to None.
    @classmethod
    def CreateMasterSecurityLoanTrade(cls, instrument, **kwargs):
        kwargs.update({
            'source': None,
            'collateralAgreement': None,
            'pendingOrder': None})
        return cls.CreateTrade(instrument, **kwargs)

    # Use this function to create a new security loan instrument.
    # Keyword accepted are the arguments for function SecurityLoanTradeSetDefaultFields.
    @classmethod
    def CreateTrade(cls, instrument, **kwargs):
        trade = acm.DealCapturing.CreateNewTrade(instrument)
        cls.SecurityLoanTradeSetDefaultFields(trade, **kwargs)
        return trade if trade else None

    @classmethod
    def SecurityLoanSetDefaultFields(cls, instrument, **kwargs):
        securityLoan = FSecLendHandler.SecurityLoanHandler(acm.FBusinessLogicDecorator.WrapObject(instrument))
        securityLoan.SecurityLoanSetDefaultFields(**kwargs)

    @classmethod
    def SecurityLoanTradeSetDefaultFields(cls, trade,**kwargs):
        securityLoanTrade = FSecLendHandler.SecurityLoanTradeHandler(acm.FBusinessLogicDecorator.WrapObject(trade))
        securityLoanTrade.SecurityLoanTradeSetDefaultFields(**kwargs)

    @classmethod
    def MasterSecurityLoanSetDefaultFields(cls, instrument, **kwargs):
        masterSecurityLoan = FSecLendHandler.SecurityLoanHandler(acm.FBusinessLogicDecorator.WrapObject(instrument))
        masterSecurityLoan.MasterSecurityLoanSetDefaultFields(**kwargs)


def SecurityLoanTradeSetDefaultFields(trade):
    return SecurityLoanCreator.SecurityLoanTradeSetDefaultFields(trade)


def SecurityLoanSetDefaultFields(instrument):
    return SecurityLoanCreator.SecurityLoanSetDefaultFields(instrument)


def MasterSecurityLoanSetDefaultFields(instrument):
    return SecurityLoanCreator.MasterSecurityLoanSetDefaultFields(instrument)
