'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_Booking_Class
PROJECT                 :       PACE MM
PURPOSE                 :       This module will do all the message requests from MMG (PACE MM).
                                nodes to make the messages smaller.
DEPARTMENT AND DESK     :       Money Market and IT
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation
2012-08-08      390267          Heinrich Cronje                 Payment Instructions are now received from PACE MM
                                                                and will now be added to the Additional Info field
                                                                Settle_Type on the cashflow so that it is available
                                                                in Settlement Manager.
2012-11-22      603220          Heinrich Cronje                 PACE MM EOY Deployment - SSI Implementation. Integrate
                                                                PACE MM SSI selection into Front Arena.
2013-01-21      743799          Heinrich Cronje                 Fixed Amount Cash Flow is thrown away on the commit of
                                                                the instrument. Added a section to add the Fixed Amount
                                                                on a second commit, after the instrument commit.
2014-09-22                      Matthias Riedel                 Accomodate BARX Non Zar Trades
2015-11-10      BARXMM-64       Kirsten Good                    Set the Cashflow ResetType to Weighted for Call Deposits
                                                                Fixed Rate Adjustable. Interest will now generate correctly.
                                                                Check if cashflows exist and create or update accordingly.
2017-01-13      ABITFA-4481     Vojtech Sidorin                 Update the use of FCallDepositFunctions.
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module contains four Committing classes:

        Call_Account_Trading    :       This class caters for all Call Deposit transactions. The main use is to
                                        Adjust Deposit.
        PACE_MM_Trade_Booking   :       This class books new Call Deposits and new Fixed Term Deposits.
        PACE_MM_Trade_Voiding   :       This class Voids Call Deposits and Fixed Term Deposits.
        PACE_MM_Acknowledgement :       This class sets the PACE MM ID to the relevant entities when an
                                        Acknowledgement is received.
'''

import acm
import ael

import FCallDepositFunctions as CallDepositFunctions
import PACE_MM_Parameters as Params
import SAGEN_IT_Functions as Gen_Utils

from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as Utils
from PACE_MM_TAL_Override import PACE_MM_TAL_Override as TALOverride


class Call_Account_Trading():
    def __init__(self, ins_object, amount, transaction_date, optionalKey, payment_instructions):
        self.__ins_object = ins_object
        self.__transaction_date = ael.date(transaction_date)
        self.__amount = float(amount)
        self.__optionalKey = optionalKey
        self.__payment_instructions = Utils.set_payment_instructions(payment_instructions)

    def __getLastCFRAStartDay(self):
        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', self.__ins_object.Legs().At(0).Oid())
        cashFlowQuery.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Call Fixed Rate Adjustable'))
        cashFlows = cashFlowQuery.Select().SortByProperty('EndDate', 0)
        if cashFlows:
            return cashFlows[0].StartDate()
        return None

    def __isCallBackdate(self):
        lastCFRAStartDay = ael.date(self.__getLastCFRAStartDay())
        if self.__transaction_date < lastCFRAStartDay:
            return 1
        return 0

    def callAccountTrading(self):
        backdateTransaction = self.__isCallBackdate()
        payDay = self.__transaction_date.first_day_of_month().add_months(1)

        if backdateTransaction:
            cashFlow = CallDepositFunctions.backdate(self.__ins_object, self.__amount, self.__transaction_date, payDay, self.__payment_instructions, flag=1)
        else:
            cashFlow = CallDepositFunctions.adjust(self.__ins_object, self.__amount, self.__transaction_date, self.__payment_instructions, flag=1)

        cashFlow.ExternalId(self.__optionalKey)

        try:
            Params.PACE_MM_EVENT_ID[str(cashFlow.Oid())] = self.__optionalKey
            cashFlow.Commit()
            acm.PollAllEvents()
        except Exception, e:
            print 'ERROR %s' %str(e)
            raise e

        try:
            Gen_Utils.set_AdditionalInfoValue_ACM(cashFlow, 'Settle_Type', self.__payment_instructions)
        except Exception, e:
            print 'ERROR %s' %str(e)
            raise e

        try:
            talOverride = TALOverride(self.__ins_object.Trades()[0], self.__payment_instructions)
        except:
            print 'ERROR - TAL Override'

        return cashFlow


class PACE_MM_Trade_Booking():
    def __init__(self, portfolio, instype, currency, counterparty, rate, nominalAmount, optionalKey, start_day, trade_day, payment_instructions, expiry = ael.date_today().add_days(1)):
        '''--------------------------------------------------------------------------
                                        Variables
        --------------------------------------------------------------------------'''
        acquirer = Params.VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION[currency][2]
        calendar = Params.VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION[currency][0]
        daycount = Params.VALID_CURR_CALENDAR_DAYCOUNT_ACQUIRER_COMBINATION[currency][1]

        self.__CURRENCY = acm.FCurrency[currency]
        self.__VAL_GROUP_CHL_NBR = 2176         #AC_GLOBAL_Funded
        self.__ACQUIRER = acm.FParty[acquirer]
        self.__TIME = acm.Time().TimeNow()
        self.__FUNDING_INSTYPE = Params.FUNDING_INSTYPE[currency == 'ZAR', instype]
        self.__TRADER = acm.User()
        self.__CALENDAR = acm.FCalendar[calendar]
        self.__DAYCOUNT_METHOD = Utils.GetEnum('DaycountMethod', daycount)
        self.__DATE_PERIOD_UNIT_DAYS = Utils.GetEnum('DatePeriodUnit', 'Days')

        self.__portfolio = acm.FPhysicalPortfolio[portfolio]
        self.__counterparty = counterparty
        self.__interestRate = rate
        self.__nominalAmount = float(nominalAmount)
        self.__start_day = ael.date(start_day)
        self.__value_day = ael.date(trade_day)
        self.__trade_time = self.__TIME.replace(self.__TIME[:10], trade_day)
        self.__expiry = ael.date(expiry)
        self.__contractSize = 1000000.00
        self.__quantity = self.__nominalAmount / self.__contractSize
        self.__optionalKey = optionalKey
        self.__payment_instructions = Utils.set_payment_instructions(payment_instructions)

        self.__daysBetweenStartExpiry = self.__start_day.days_between(self.__expiry)

        self.__instrumentDefaultDict = {'Currency' : self.__CURRENCY, 'Otc' : 1, 'SpotBankingDaysOffset' : 0, 'ExpiryDate' : self.__expiry, \
                                    'ValuationGrpChlItem' : self.__VAL_GROUP_CHL_NBR, 'ContractSize' : self.__contractSize, 'Quotation' : 'Yield', \
                                    'QuoteType' : Utils.GetEnum('QuoteType', 'Yield')}
        self.__legDefaultDict = {'LegType' : Utils.GetEnum('LegType', 'Fixed'), 'Decimals' : 11, 'StartDate' : self.__start_day, \
                                'DayCountMethod' : self.__DAYCOUNT_METHOD, 'EndDate' : self.__expiry, 'EndPeriodUnit' : self.__DATE_PERIOD_UNIT_DAYS, \
                                'FixedRate' : self.__interestRate, 'ResetDayOffset' : 0, 'AmortEndPeriodUnit' : self.__DATE_PERIOD_UNIT_DAYS, \
                                'AmortEndDay' : self.__expiry, 'AmortDaycountMethod' : self.__DAYCOUNT_METHOD, 'RollingPeriodBase' : self.__expiry, \
                                'AmortEndPeriodCount' : self.__daysBetweenStartExpiry}
        self.__tradeDefaultDict = {'Portfolio' : self.__portfolio, 'Counterparty' : self.__counterparty, 'Acquirer' : self.__ACQUIRER, \
                                    'Status' : Utils.GetEnum('TradeStatus', 'FO Sales'), 'Currency' : self.__CURRENCY, 'TradeTime' : self.__trade_time, \
                                    'ValueDay' : self.__value_day, 'AcquireDay' : self.__value_day, 'Quantity' : self.__quantity, \
                                    'Trader' : self.__TRADER, 'OptionalKey' : self.__optionalKey}
        self.__tradeAddInfoDefaultDict = {}

    def termBooking(self):
        #self.__FUNDING_INSTYPE = Params.FIXED_TERM_DEPOSIT_FUNDING_INSTYPE
        PRICE_FINDING_CHL_ITEM = 985

        '''--------------------------------------------------------------------------
                            Fixed Term Deposit Specific attributes
        --------------------------------------------------------------------------'''
        updateInstrumentDict = {'PriceFindingChlItem' : PRICE_FINDING_CHL_ITEM, 'ExpiryPeriod_count' : self.__daysBetweenStartExpiry}
        updateLegDict = {'EndPeriodCount' : self.__daysBetweenStartExpiry, 'ResetType' : Utils.GetEnum('ResetType', 'None'), \
                        'ResetCalendar' : self.__CALENDAR, 'StrikeType' : Utils.GetEnum('StrikeType', 'Absolute'), \
                        'PriceInterpretationType' : Utils.GetEnum('PriceInterpretType', 'As Reference')}

        deposit = acm.FDeposit()

        '''--------------------------------------------------------------------------
            Setting Attributes for Instrument and Leg and Committing the instrument
        --------------------------------------------------------------------------'''
        insdict = self.__instrumentDefaultDict
        insdict.update(updateInstrumentDict)
        Utils.set_Properties(deposit, insdict)

        leg = deposit.CreateLeg(1)

        legDict = self.__legDefaultDict
        legDict.update(updateLegDict)
        Utils.set_Properties(leg, legDict)
        commitFlag = 0

        deposit.Commit()
        acm.PollAllEvents()
        commitFlag = 1

        '''--------------------------------------------------------------------------
                                Specific Attributes for Trade
        --------------------------------------------------------------------------'''
        updateTradeDict = {'Instrument' : deposit, 'Premium' : -1 * self.__nominalAmount, 'Price' : self.__interestRate}
        updateTradeAddInfoDict = {'Funding_Instype' : Utils.get_ChoiceList_ACM(acm.FChoiceList.Select("list = 'Funding Instype'"), self.__FUNDING_INSTYPE)}

        '''--------------------------------------------------------------------------
                        Setting Attributes for Trade and Committing Trade
        --------------------------------------------------------------------------'''
        trade = acm.FTrade()

        tradedict = self.__tradeDefaultDict
        tradedict.update(updateTradeDict)
        Utils.set_Properties(trade, tradedict)

        tradeAddInfoDict = self.__tradeAddInfoDefaultDict
        tradeAddInfoDict.update(updateTradeAddInfoDict)

        acm.BeginTransaction()
        try:
            trade.Commit()
            Utils.set_Properties(trade.AdditionalInfo(), tradeAddInfoDict)
            trade.Commit()
            acm.CommitTransaction()

            try:
                talOverride = TALOverride(trade, self.__payment_instructions)
            except:
                print 'ERROR - TAL Override'

            return trade.Oid()
        except Exception, e:
            print 'ERROR %s' %str(e)
            acm.AbortTransaction()
            raise e

    def callAccountBooking(self, reinvest = False, pace_mm_event_id = None):
        #self.__FUNDING_INSTYPE = Params.CALL_DEPOSIT_FUNDING_INSTYPE
        CALL_REGION = Params.CALL_DEPOSIT_REGION
        ROLLING_BASE_DAY = self.__start_day.add_months(1).first_day_of_month()

        '''--------------------------------------------------------------------------
                            Call Deposit Specific attributes
        --------------------------------------------------------------------------'''
        cashFlowDefaultDict = {'CashFlowType' : Utils.GetEnum('CashFlowType', 'Fixed Amount'), 'PayDate' : self.__start_day, 'NominalFactor' : 1}

        updateInstrumentDict = {'ContractSize' : 1, 'OpenEnd' : Utils.GetEnum('OpenEndStatus', 'Open End'), 'Quotation' : 'Clean', \
                                'QuoteType' : Utils.GetEnum('QuoteType', 'Clean')}
        updateLegDict = {'LegType' : Utils.GetEnum('LegType', 'Call Fixed Adjustable'), 'InitialIndexValue' : self.__nominalAmount, \
                        'Reinvest' : reinvest, 'FixedCoupon': 1, 'RollingPeriodBase' : ROLLING_BASE_DAY, 'RollingPeriodCount' : 1, \
                        'RollingPeriodUnit' : Utils.GetEnum('DatePeriodUnit', 'Months'), 'FloatRateFactor' : 1, \
                        'ResetType' : Utils.GetEnum('ResetType', 'Weighted')}
        updateCashFlowFixedAmountDict = {'FixedAmount' : self.__nominalAmount}
        updateCashFlowRedemptionAmountDict = {'CashFlowType' : Utils.GetEnum('CashFlowType', 'Redemption Amount'), 'PayDate' : self.__expiry}
        updateCashFlowCallFixedRateAdjustableDict = {'CashFlowType' : Utils.GetEnum('CashFlowType', 'Call Fixed Rate Adjustable'), \
                                                    'StartDate' : self.__start_day, 'EndDate' : self.__expiry, 'PayDate' : self.__expiry, \
                                                    'FloatRateFactor' : 1, 'NominalFactor' : 0}
        cashFlowList = [updateCashFlowRedemptionAmountDict, updateCashFlowCallFixedRateAdjustableDict]

        '''--------------------------------------------------------------------------------------
            Setting Attributes for Instrument, Leg and Cash Flow and Committing the instrument
        --------------------------------------------------------------------------------------'''
        deposit = acm.FDeposit()

        insdict = self.__instrumentDefaultDict
        insdict.update(updateInstrumentDict)
        Utils.set_Properties(deposit, insdict)

        leg = deposit.CreateLeg(1)

        legDict = self.__legDefaultDict
        legDict.update(updateLegDict)
        Utils.set_Properties(leg, legDict)

        try:
            deposit.Commit()
            acm.PollAllEvents()
        except Exception, e:
            raise e

        try:
            for cashFlow in cashFlowList:
                found = False
                for cf in leg.CashFlows():
                    if Utils.GetEnum('CashFlowType', cf.CashFlowType()) == cashFlow['CashFlowType']:
                        # Found cashflow, updating...
                        cashFlowDict = cashFlowDefaultDict
                        cashFlowDict.update(cashFlow)
                        Utils.set_Properties(cf, cashFlowDict)
                        found = True
                if not found:
                    # Cashflow not found, creating...
                    cf = leg.CreateCashFlow()
                    cashFlowDict = cashFlowDefaultDict
                    cashFlowDict.update(cashFlow)
                    Utils.set_Properties(cf, cashFlowDict)
            try:
                deposit.Commit()
                acm.PollAllEvents()
            except Exception, e:
                raise e

            commitFlag = 0
            first_FA_CF = None

            try:
                commitFlag = 1

                found = False
                for cf in leg.CashFlows():
                    if Utils.GetEnum('CashFlowType', 'Fixed Amount') == Utils.GetEnum('CashFlowType', cf.CashFlowType()) :
                        # Found cashflow Fixed Amount, updating...
                        cf.PayDate(self.__start_day)
                        cf.FixedAmount(self.__nominalAmount)
                        cf.NominalFactor(1)
                        found = True
                if not found:
                    # Cashflow Fixed Amount not found, creating...
                    newCf = deposit.Legs()[0].CreateCashFlow()
                    newCf.PayDate(self.__start_day)
                    newCf.CashFlowType(Utils.GetEnum('CashFlowType', 'Fixed Amount'))
                    newCf.FixedAmount(self.__nominalAmount)
                    newCf.NominalFactor(1)

                deposit.Commit()
                acm.PollAllEvents()

                '''------------------------------------------------------------------------------------------------
                    Setting the External ID of the first Fixed Amount Cash Flow with the Optional Key of the Trade
                ------------------------------------------------------------------------------------------------'''
                first_FA_CF = Utils.get_first_FA_CF(deposit)
                first_FA_CF.ExternalId(pace_mm_event_id)
                first_FA_CF.Commit()
            except Exception, e:
                raise e

        except Exception, e:
            raise e

        try:
            if first_FA_CF:
                Gen_Utils.set_AdditionalInfoValue_ACM(first_FA_CF, 'Settle_Type', self.__payment_instructions)
        except Exception, e:
            print 'ERROR %s' %str(e)

        '''--------------------------------------------------------------------------
                                Specific Attributes for Trade
        --------------------------------------------------------------------------'''
        updateTradeDict = {'Instrument' : deposit, 'Quantity' : 1}
        updateTradeAddInfoDict = {'Funding_Instype' : Utils.get_ChoiceList_ACM(acm.FChoiceList.Select("list = 'Funding Instype'"), self.__FUNDING_INSTYPE), \
                                'Account_Name' : self.__counterparty.Name(), \
                                'Call_Region' : Utils.get_ChoiceList_ACM(acm.FChoiceList.Select("list = 'Call_Region'"), CALL_REGION)}

        '''--------------------------------------------------------------------------
                        Setting Attributes for Trade and Committing Trade
        --------------------------------------------------------------------------'''
        trade = acm.FTrade()

        tradedict = self.__tradeDefaultDict
        tradedict.update(updateTradeDict)
        Utils.set_Properties(trade, tradedict)

        tradeAddInfoDict = self.__tradeAddInfoDefaultDict
        tradeAddInfoDict.update(updateTradeAddInfoDict)

        acm.BeginTransaction()
        try:
            trade.Commit()
            Utils.set_Properties(trade.AdditionalInfo(), tradeAddInfoDict)
            trade.Commit()

            acm.CommitTransaction()

            try:
                talOverride = TALOverride(trade, self.__payment_instructions)
            except:
                print 'ERROR - TAL Override'

            return trade.Oid()
        except Exception, e:
            acm.AbortTransaction()
            raise e


class PACE_MM_Trade_Voiding():
    def __init__(self, trade, freeText):
        self.__trade = trade
        self.__freeText = freeText

    def voidTrade(self):
        trade = self.__trade
        trade.Text1(self.__freeText)
        trade.Status('Void')
        try:
            trade.Commit()
        except Exception, e:
            raise e


class PACE_MM_Acknowledgement():
    def __init__(self, object, BARX_ID):
        self.__object = object
        self.__barxID = BARX_ID

    def ackFixedTermDeposit(self):
        '''--------------------------------------------------------------------------
                    ACKNOWLEDGEMENT for Fixed Term Deposit - Optional Key
        --------------------------------------------------------------------------'''
        self.__object.OptionalKey(self.__barxID)
        self.__object.Unsimulate()
        acm.PollDbEvents()
        self.__object.OptionalKey(self.__barxID)
        try:
            self.__object.Commit()
        except Exception, e:
            raise e

    def ackCallDeposit(self):
        '''--------------------------------------------------------------------------
                    ACKNOWLEDGEMENT for Call Deposit - Optional Key
        --------------------------------------------------------------------------'''
        tradesQuery = acm.CreateFASQLQuery(acm.FTrade, 'AND')
        tradesQuery.AddAttrNode('Instrument.Oid', 'EQUAL', self.__object.Oid())
        trades = Utils.get_Common_Trade_Selection(tradesQuery)
        for t in trades:
            t.OptionalKey(self.__barxID)
            t.Unsimulate()
            acm.PollDbEvents()
            t.OptionalKey(self.__barxID)
            try:
                t.Commit()
            except Exception, e:
                raise e

    def ackCallDepositTransaction(self):
        '''--------------------------------------------------------------------------
            ACKNOWLEDGEMENT for Call Deposit Transaction - Cash Flow - External ID
        --------------------------------------------------------------------------'''
        try:
            self.__object.Leg().Instrument().FreeText('Refresh Cache')
            self.__object.Leg().Instrument().Unsimulate()
            acm.PollDbEvents()
            self.__object.ExternalId(self.__barxID)
            try:
                self.__object.Commit()
            except Exception, e:
                raise e

        except Exception, e:
            raise e
