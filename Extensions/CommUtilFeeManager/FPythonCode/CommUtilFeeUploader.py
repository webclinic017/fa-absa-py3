'''
MODULE
    CommUtilFeeUploader - This module provides content how handle Commitment fees. 
   
HISTORY
    Date        Developer               Notes
    2017-10-09  Ntuthuko Matthews       created
    2019-02-27  Ntuthuko Matthews       recalculate the utilrate if the value is zero
'''

import acm
import CommFeeCalculation as calc
import logging
from at_logging import getLogger
from DataAccessUtil import DataAccess
from DataClass import CommUtilFee
from HelperFunctions import HelperFunctions


def GetCalcSpace():
    CONTEXT = acm.GetDefaultContext()
    return acm.Calculations().CreateCalculationSpace(CONTEXT, 'FTradeSheet')


class CommUtilFeeModel(object):
    LOGGER = getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)

    def __init__(self, trade):
        self.commUtilFee = None
        self.prefix = ''
        self.name = ''
        self.currentNominal = None
        self.utilRate = 0
        self.utilised = 0
        self.linked = 0
        self.trade = trade
        self.cmfTrades = None
        self.space = GetCalcSpace()
        self.dataAccess = DataAccess()
        self.helperFunctions = HelperFunctions()

    def CurrentNominal(self, trade, prefix='CMF'):
        try:
            self.trade = trade
            trade_list = []
            name = '{0}{1}'.format(prefix, self.trade.Name())
            trades = HelperFunctions().get_trade_list()
            self.cmfTrades = calc.CMFTrades(self.trade, name)
            trade_list = self.cmfTrades._get_sub_trades(trades)
            self.currentNominal = sum([float(self.space.CalculateValue(acm.FTrade[t],
                                                                       'DDM Nominal TXN CCY'))
                                       for t in trade_list])
            return self.currentNominal
        except Exception as e:
            self.LOGGER.error('99: {0}'.format(e))
            return 0

    def CalculateFeeRate(self, commUtilFee, prefix='UTF'):
        try:
            self.prefix = prefix
            if self.prefix == 'UTF':
                if commUtilFee:
                    self.commUtilFee = commUtilFee

                rate = None
                self.currentNominal = float(self.CurrentNominal(self.trade, 'UTF'))
                calc_rate = self.CalculateUtilRate()
                period_days = float(HelperFunctions().get_period_days(self.dataAccess, self.trade, self.cmfTrades))
                day_count = (int)(str(self.commUtilFee.DayCount.lstrip('Act/')))
                rate = self.currentNominal * calc_rate * (period_days / day_count)
                rate = round(rate, 2)

                self.LOGGER.debug('Period Days = {0}'.format(period_days))
                self.LOGGER.debug('Day Count = {0}'.format(day_count))
                self.LOGGER.debug('Formula = Current Nominal * Rate * (Period Days / Day Count)')
                self.LOGGER.debug('Utilization Fee Calc = {0} * {1} * ({2} / {3})'.format(self.currentNominal,
                                                                                          calc_rate, period_days,
                                                                                          day_count))
                self.LOGGER.debug('Utilization Fee = {0}'.format(rate))

                return rate
            else:
                return str(self.commUtilFee.CommitFeeRate)
        except Exception as e:
            self.LOGGER.error('100: {0}'.format(e))
            return 0

    def CalculateUtilRate(self):
        try:
            if self.prefix == 'UTF':
                self.currentNominal = float(self.CurrentNominal(self.trade, 'UTF'))
                self.utilised = float(self.currentNominal) / float(self.commUtilFee.FacilityMax)
                rate_percentage = round(self.utilised * 100, 2)
                self.utilRate = HelperFunctions().get_rate(self.dataAccess, rate_percentage, self.trade)

                self.LOGGER.debug('Current Nominal = {0}'.format(self.currentNominal))
                self.LOGGER.debug('Facility Limit = {0}'.format(self.commUtilFee.FacilityMax))
                self.LOGGER.debug('Facility Utilised = {0}'.format(round(self.utilised, 2)))
                self.LOGGER.debug('Rate (%) = {0}'.format(rate_percentage))
                self.LOGGER.debug('Rate = {0}'.format(self.utilRate))

                if abs(self.utilRate) == 0:
                    func = acm.GetFunction('msgBox', 3)
                    result = func("Warning", "The Utilization Fee Rate is 0. Do you want to recalculate?", 1)
                    if result == 1:
                        self.CalculateUtilRate()

                return float(self.utilRate) / 100
            return 0
        except Exception as e:
            self.LOGGER.error('101: {0}'.format(e))
            return 0

    def Put(self, commUtilFee, feeType):
        self.commUtilFee = commUtilFee
        self.prefix = HelperFunctions.fee_type(feeType)
        self.name = '{0}{1}'.format(self.prefix, self.trade.Name())
        self.feeRate = self.commUtilFee.CommitFeeRate

        if self.prefix == 'UTF':
            self.feeRate = self.CalculateFeeRate(None)
            self.commUtilFee.Limit = 0
            self.commUtilFee.Utilised = self.utilised
            self.utilised = 0

            # don't override the last_run_date
            previous_record = self.Get(feeType)
            self.commUtilFee.PreviousRunDate = previous_record.PreviousRunDate
            self.commUtilFee.LastRunDate = previous_record.LastRunDate

        self.record = [{'CalcUtilFee': '1' if self.commUtilFee.CalcUtilFee else '0',
                        'CalcCommFee': '1' if self.commUtilFee.CalcCommFee else '0',
                        'PM_FacilityMax': str(self.commUtilFee.FacilityMax),
                        'PM_Limit': str(self.commUtilFee.Limit),
                        'PM_CommitFeeRate': str(self.feeRate),
                        'PM_FacilityExpiry': str(self.commUtilFee.FacilityExpiry),
                        'PM_CommitFeeBase': str(self.commUtilFee.CommitFeeBase),
                        'CommitPeriod': str(self.commUtilFee.CommitPeriod),
                        'Rolling Convention': str(self.commUtilFee.RollingConvention),
                        'FeeType': str(self.commUtilFee.FeeType),
                        'DayCount': str(self.commUtilFee.DayCount),
                        'UtilFeeRate': str(self.utilRate),
                        'Utilised': str(self.commUtilFee.Utilised),
                        'Linked': '1' if self.commUtilFee.Linked else '0',
                        'PreviousRunDate': str(self.commUtilFee.LastRunDate),
                        'LastRunDate': str(self.commUtilFee.LastRunDate),
                        }]
        try:
            self.dataAccess.Save(self.record, self.name)
        except Exception as e:
            self.LOGGER.error('102: {0}'.format(e))

    def New(self):
        return CommUtilFee()

    def Get(self, feeType):
        self.prefix = HelperFunctions.fee_type(feeType)
        self.name = '{0}{1}'.format(self.prefix, self.trade.Name())
        self.record = self.dataAccess.Select(self.name)
        commUtilFee = self.New()
        if self.record:
            if 'FeeType' in self.record.keys():
                commUtilFee.FeeType = str(self.record['FeeType'])
            else:
                commUtilFee.FeeType = 'Commitment'
            if 'CalcUtilFee' in self.record.keys():
                commUtilFee.CalcUtilFee = (True if str(self.record['CalcUtilFee']) == '1' else False)
            else:
                commUtilFee.CalcUtilFee = False
            if 'Linked' in self.record.keys():
                commUtilFee.Linked = (True if str(self.record['Linked']) == '1' else False)

            if 'LastRunDate' in self.record.keys():
                commUtilFee.LastRunDate = str(self.record['LastRunDate'])

            if 'PreviousRunDate' in self.record.keys():
                commUtilFee.PreviousRunDate = str(self.record['PreviousRunDate'])

            if 'UtilFeeRate' in self.record.keys():
                commUtilFee.UtilFeeRate = str(self.record['UtilFeeRate'])

            if 'Utilised' in self.record.keys():
                commUtilFee.Utilised = str(self.record['Utilised'])

            commUtilFee.CalcCommFee = (True if str(self.record['CalcCommFee']) == '1' else False)
            commUtilFee.FacilityMax = str(self.record['PM_FacilityMax'])
            commUtilFee.Limit = str(self.record['PM_Limit'])
            commUtilFee.CommitFeeRate = str(self.record['PM_CommitFeeRate'])
            commUtilFee.FacilityExpiry = str(self.record['PM_FacilityExpiry'])
            commUtilFee.CommitFeeBase = str(self.record['PM_CommitFeeBase'])
            commUtilFee.CommitPeriod = str(self.record['CommitPeriod'])
            commUtilFee.RollingConvention = str(self.record['Rolling Convention'])
            try:
                commUtilFee.DayCount = str(self.record['DayCount'])
            except KeyError as e:
                self.LOGGER.error('103: {0}'.format(e))
                self.LOGGER.debug(str(e))

        return commUtilFee

    def Dispose(self):
        self.space = None
        self.commUtilFee = None
