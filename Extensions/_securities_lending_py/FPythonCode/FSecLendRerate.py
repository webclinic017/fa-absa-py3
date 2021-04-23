""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendRerate.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendRerate

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
     Actions for Rerate functionality making use of FSecLendDealUtils.

------------------------------------------------------------------------------------------------"""

#Assumptions: Fee rate is set on Spreads reset. Current Security Loan configuration set the Spread reset on the Fixed Rate leg (PayLeg) only.
#Rebate case is not supported yet.

import acm
from FSecLendDealUtils import FeeWrapper
from FSecLendHandler import SecurityLoanHandler, SecurityLoanLegHandler
import FLogger
from FParameterSettings import ParameterSettingsCreator


def GetLogger(name=''):
    aLogger = FLogger.FLogger.GetLogger(name)
    return aLogger

def SetLoggingLevel(aLogger, level):
    ''' Levels are 1-4 signifying
        1: Info: get warnings, errors and info
        2: Debug: get everything
        3: Warn: get warnings and errors
        4: Error: get only errors
    '''
    aLogger.Reinitialize(level=level)


LOGGER = GetLogger('SecLendRerate')


#Input: Trade


class SecLendRerate(SecurityLoanHandler):

    def __init__(self, instrument, fee=None, rerateDate=None):
        self.instrument = instrument
        self.fee = fee
        self.rerateDate = rerateDate
        self.mainLeg = None

    def SetFee(self, fee):
        self.fee = fee

    def SetRerateDate(self, rerateDate):
        self.rerateDate = rerateDate

    # -------------   Utility functions -------------

    def Instrument(self):
        return self.instrument

    def DefaultExtendDate(self):
        undSpotDays = self.Instrument().Underlying().SpotBankingDaysOffset()
        baseDate = acm.Time.DateToday()
        calendar = self.FixedOrRebateLeg().PayCalendar()
        return calendar.AdjustBankingDays(baseDate, undSpotDays)

    def Fee(self):
        return SecurityLoanLegHandler(self.FixedOrRebateLeg())

    def LastSpreadReset(self):
        return self.Fee().LastSpreadReset()

    def LastFeeReset(self):
        lastSpreadReset = self.LastSpreadReset()
        return self.Fee().FeeFromReset(lastSpreadReset)

    def RerateDate(self):
        if self.rerateDate is None:
            self.rerateDate = self.DefaultExtendDate()
        return self.rerateDate

    def FixedOrRebateLeg(self):
        if self.IsRebate():
            return self.ReceiveLeg()
        else:
            return self.PayLeg()

    def ExtendSecurityLoan(self):
        if self.RerateDate() > self.Fee().LastFeeDay():
            #Extend Instrument End Date one day more than the Rerate Date
            calendar = self.FixedOrRebateLeg().PayCalendar()
            extendToDate = calendar.AdjustBankingDays(self.rerateDate, 1)
            self.ExtendOpenEnd(extendToDate)

    def DoRerate(self):
        if self.rerateDate < acm.Time.DateToday():
            LOGGER.info('Fixing Date {0} is in the past. Not possible to rerate instrument {1} historically'.format(self.rerateDate, self.Instrument().Name()))
            return
        oldFee = self.GetLastFeeChangeFee()
        self.Fee().FeeAtDate(self.rerateDate, self.fee)
        self.FixSpreadResets(oldFee, self.fee, self.rerateDate)

    def SaveInstrument(self):
        self.Instrument().Commit()

    def GetLastFeeChangeReset(self):
        leg = self.FixedOrRebateLeg()
        i = 0
        prevReset = None
        for r in leg.Resets().SortByProperty('Day', False):
            if r.ResetType() == 'Spread' and r.IsFixed():
                if not prevReset:
                    prevReset = r
                if r.FixingValue() != prevReset.FixingValue():
                    return prevReset
                    i += 1
                prevReset = r
        if i < 1 and prevReset:
            return prevReset

    def GetLastFeeChangeFee(self):
        return self.GetLastFeeChangeReset().FixingValue()

    def GetLastFeeChangeDate(self):
        return self.GetLastFeeChangeReset().Day()


def SecLendRerateHanlder(ins):
    return SecLendRerate(ins)

def GetDateFromLastFixing(rerateHandler):
    return rerateHandler.GetLastFeeChangeDate()

def GetFeeFromLastFixing(rerateHandler):
    return rerateHandler.GetLastFeeChangeFee()


def FixedOrRebateLeg(instrument):
    prodType = instrument.ProductTypeChlItem()
    if (prodType is not None) and (prodType.StringKey() == 'Rebate Security Loan'):
        return instrument.RecLeg()
    else:
        return instrument.PayLeg()

def GetRerateFixingDate(rerateHandler):
    return rerateHandler.DefaultExtendDate()



