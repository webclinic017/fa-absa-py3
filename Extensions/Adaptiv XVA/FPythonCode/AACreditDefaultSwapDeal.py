""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACreditDefaultSwapDeal.py"
import sys
import AAUtilFunctions as Util
import AAComposer
import AAParameterDictionary
import acm
import AADataUtilFunctions

CREDIT_DEFAULT_LEG_TYPE = 'Credit Default'
FIXED_LEG_TYPE = 'Fixed'
FLOAT_LEG_TYPE = 'Float'


class AACreditDefaultSwapDeal(object):
    def __init__(self, cds, trades, positionTradeQuantities, staticLegInformations, valuationDate, cfInformation, logger):
        self.cdSwap = cds
        self.trades = trades
        self.positionTradeQuantities = positionTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation 
        self._logger = logger

    def __getPayRateString(self, otherLeg):
        rate = 0
        if (otherLeg.LegType() == FIXED_LEG_TYPE):
            rate = otherLeg.FixedRate()

        return str(rate * 100) + 'bp'

    def __getBuySell(self, creditDefaultLeg):
        retVal = 'Buy'
        if (creditDefaultLeg.PayLeg()):
            retVal = 'Sell'

        return retVal

    def __getCouponSchedule(self, trade, couponLeg):
        items = AAComposer.CashFlowDataDictionary()
        flows = AAComposer.CashFlowList()
        items['Items'] = flows

        for singleFlow in couponLeg.CashFlows():
            flows.append(self.__getCashFlowRow(trade, singleFlow))

        return items

    def __getStaticInfoForLeg(self, cashFlow):
        retVal = None
        for statInfo in self.staticLegInformations:
            if statInfo != None and statInfo.AcmLeg() == cashFlow.Leg():
                retVal = statInfo
                break; 
        return retVal

    def __getCreditDefaultLegInfo(self, trade):
        cdLeg = None
        paymentLeg = None
        legAndTrades = trade.LegAndTrades()
        legs = [x.Leg() for x in legAndTrades]
        if (len(legs) < 2):
            return cdLeg, paymentLeg

        cdLeg = legs[0]
        paymentLeg = legs[1]
        if (cdLeg.LegType() != 'Credit Default'):
            cdLeg = legs[1]
            paymentLeg = legs[0]

        return cdLeg, paymentLeg

    def __getSurvivalProbabilityCurve(self, cds):
        retVal = ""
        if (cds == None):
            return retVal

        instrument = cds.Underlying()
        if (instrument == None):
            return retVal

        cdsMappedLink = instrument.MappedCreditLink()
        if (cdsMappedLink == None):
            return retVal

        creditCurve = cdsMappedLink.Link()
        try:
            retVal = AADataUtilFunctions.getCounterPartyID(creditCurve)
        except:
            if (self._logger):
                self._logger.error('Failed: ' + str(sys.exc_info()[0]))

        return retVal;

    def getCreditDefaultSwapDealString(self, trade, parameterDict):
        deal = AAComposer.PairList()
        
        creditDefaultLeg, otherLeg = self.__getCreditDefaultLegInfo(trade)
        if (creditDefaultLeg == None or otherLeg == None): # TODO log something
            return deal
        rollingPeriod = str(otherLeg.RollingPeriod())
        rollingPeriod = rollingPeriod.upper()
        if (rollingPeriod == '12M'):
            rollingPeriod = '1Y'

        deal['Object'] = 'DealDefaultSwap'
        deal['Name'] = self.cdSwap.Name() # + ' ' + trade.Name()
        deal['Reference'] = Util.createAALabel(self.cdSwap.Name())

        deal['Survival_Probability'] = self.__getSurvivalProbabilityCurve(self.cdSwap)
        
        deal['Effective_Date'] = Util.createDateString(self.cdSwap.StartDate())
        deal['Maturity_Date'] = Util.createDateString(self.cdSwap.EndDate())
        deal['Currency'] = self.cdSwap.Currency().Name()
        deal['Discount_Rate'] = parameterDict.AddDiscountCurveAndGetName(self.cdSwap.MappedDiscountLink())
        deal['Pay_Frequency'] = rollingPeriod

        deal['Pay_Rate'] = self.__getPayRateString(otherLeg)
        deal['Recovery_Rate'] = deal['Survival_Probability']
        deal['Buy_Sell'] = self.__getBuySell(creditDefaultLeg)
        deal['Principal'] = trade.Nominal()
        deal['Accrual_Day_Count'] = Util.createDayCountString(otherLeg.DayCountMethod())

        upfront = trade.Premium() / trade.Nominal() 
        deal['Upfront'] = str(100 * upfront) + '%'
        deal['Upfront_Date'] = Util.createDateString(trade.ValueDay())

        return deal

    def __getCreditDefaultExplicitLegString(self, trade, parameterDict):
        deal = AAComposer.PairList()
        creditDefaultLeg, otherLeg = self.__getCreditDefaultLegInfo(trade)

        deal['Object'] = 'DealDefaultSwapExplicit'
        deal['Reference'] = self.cdSwap.Name() + ".1" # + ' ' + trade.Name()
        deal['Reference'] = Util.createAALabel(self.cdSwap.Name())
        deal['Survival_Probability'] = self.__getSurvivalProbabilityCurve(self.cdSwap)
        deal['Currency'] = self.cdSwap.Currency().Name()
        deal['Discount_Rate'] = parameterDict.AddDiscountCurveAndGetName(self.cdSwap.MappedDiscountLink())
        deal['Pay_Rate'] = self.__getPayRateString(otherLeg)
        deal['Recovery_Rate'] = deal['Survival_Probability']
        deal['Buy_Sell'] = self.__getBuySell(creditDefaultLeg)
        deal['Coupon_Schedule'] = self.__getCouponSchedule(trade, otherLeg)
        return deal.compose()

    def __getCashFlowFixedLegString(self, trade, parameterDict):
        deal = AAComposer.PairList()
        deal['Object'] = 'FixedCashflowDeal'
        deal['Reference'] = self.cdSwap.Name() + ".2"
        deal['Currency'] = self.cdSwap.Currency().Name()
        deal['Discount_Rate'] = parameterDict.AddDiscountCurveAndGetName(self.cdSwap.MappedDiscountLink())
        deal['Payment_Date'] = Util.createDateString(trade.ValueDay())
        deal['Amount'] = str(trade.Premium())
        return deal.compose()

    def __getCashFlowRow(self, trade, cashFlow):
        row = AAComposer.CashFlowDataDictionary()
        row['Accrual_Start'] = Util.createDateString(cashFlow.StartDate())
        row['Accrual_End'] = Util.createDateString(cashFlow.EndDate())
        row['Accrual_Year_Fraction'] = self.__getStaticInfoForLeg(cashFlow).CalendarInformation().YearsBetween( \
            cashFlow.StartDate(), cashFlow.EndDate(), cashFlow.Leg().DayCountMethod())
        row['Accrual_Day_Count'] = Util.createDayCountString(cashFlow.Leg().DayCountMethod())
        row['Principal'] = trade.Nominal()
        row['Payment_Date'] = Util.createDateString(max(cashFlow.PayDate(), cashFlow.EndDate()))
        return row

    def __getContainerForLegs(self, cdsDeal, cdsExplicit, singleCashFlow):
        retVal = \
        '<Properties>{0}</Properties>'\
        '<Deals>'\
            '<Deal>{1}</Deal>'\
            '<Deal>{2}</Deal>'\
        '</Deals>'\
        .format(cdsDeal, cdsExplicit, singleCashFlow)
        return retVal
    
    def __getCreditDefaultDealAsCashFlows(self):
        parameterDict = AAParameterDictionary.ParameterDictionary()
        allDeals = acm.FArray()
        for trade in self.trades:
            cdsExplicit = self.__getCreditDefaultExplicitLegString(trade, parameterDict)
            singleCashFlow = self.__getCashFlowFixedLegString(trade, parameterDict)
            cdsDeal = self.getCreditDefaultSwapDealString(trade, parameterDict)
            allDeals.Add(self.__getContainerForLegs(cdsDeal, cdsExplicit, singleCashFlow))
            
        return AAParameterDictionary.createReturnDictionary(allDeals, parameterDict)

    def get(self):
        return self.__getCreditDefaultDealAsCashFlows()