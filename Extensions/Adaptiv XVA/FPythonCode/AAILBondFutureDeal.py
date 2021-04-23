""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAILBondFutureDeal.py"
import acm
from AAComposer import PairList, CashFlowDataDictionary, CashFlowList
import AAUtilFunctions as Util
import AADataUtilFunctions as DataUtil
import AAParameterDictionary
import math
import AADealsCreator

QUOTATION_PERC_NOMINAL = acm.FQuotation["Pct of Nominal"]

def quoteToPercentNominal(leg_infos, static_legs, instrument, from_quotation, from_price, value_date):
    from_quote = acm.DenominatedValue(from_price, None, value_date)
    
    return instrument.QuoteToQuote(from_quote, value_date, leg_infos, static_legs, from_quotation, QUOTATION_PERC_NOMINAL).Number() / 100.0

def addSimpleCashflowForTrade(deals, trade, curve_name, pay_date, ccy, amount, mtm=None, reference=None):
    if pay_date > acm.Time.DateToday() and amount:
        deal = PairList()
        deal["Object"] = "FixedCashflowDeal"
        deal["Reference"] = reference if reference else trade.Oid()
        deal["MtM"] = Util.getMtMValue(mtm)
        deal["Currency"] = ccy.Name()
        deal["Discount_Rate"] = curve_name
        deal["Calendars"] = ccy.Calendar().Name()
        deal["Payment_Date"] = Util.createDateStringFromDateTime(pay_date)
        deal["Amount"] = amount
    
        deals.Add(deal.compose())

def createILBondFutureDealString(future, trades, static_legs, value_date, mtm):
    bond = future.Underlying()
    if not bond.IsKindOf("FIndexLinkedBond"):
        raise Exception("Bond Future mapping only supports Index Linked bonds.")
    
    pricing_parameters = AAParameterDictionary.ParameterDictionary()
    
    legs = bond.Legs()
    leg_infos = [leg.LegInformation(value_date) for leg in legs]
        
    deals = acm.FArray()
    for leg, static_leg_info in zip(legs, static_legs):
        yield_leg = YieldInflationCashflowListDeal(static_leg_info, value_date)
        discount_curve = pricing_parameters.AddDiscountCurveAndGetName(leg.MappedDiscountLink())
        for trade in trades:
            yield_leg.setTradeInfo(trade.Oid(), trade.Quantity(), mtm)
            yield_leg.setForwardDate(future.ExpiryDate())
            yield_leg.addDeal(deals, pricing_parameters, True)
            yield_leg.addDeal(deals, pricing_parameters, False)

            pct_nominal = quoteToPercentNominal(leg_infos, static_legs, bond, future.Quotation(), trade.Price(), value_date) 
            cost = -trade.Quantity() * future.ContractSize() * pct_nominal
             
            addSimpleCashflowForTrade(deals, trade, discount_curve, future.ExpiryDate(), future.Currency(), cost, mtm)
        
    returnDictionary = AAParameterDictionary.createReturnDictionary(deals, pricing_parameters)
    return returnDictionary


class YieldInflationCashflowListDeal:
    def __init__(self, static_leg_info, value_date):
        self.value_date = value_date
        self.leg = static_leg_info.AcmLeg()
        self.leg_info = self.leg.LegInformation(value_date)
        self.static_leg_info = static_leg_info
        self.cashflow_info = static_leg_info.CashFlowInformations()
        self.nominal = static_leg_info.ContractSize() * static_leg_info.NominalFactor()
        
        self.identifier = None
        self.quantity = None
        self.mtm = None

        self.forward_date = None
        
    def setTradeInfo(self, identifier, quantity, mtm=None):
        self.identifier = identifier
        self.quantity = quantity
        self.mtm = mtm    
        
    def setForwardDate(self, forward_date):
        self.forward_date = forward_date
        
    def _isPayLeg(self, leg):
        if self.quantity > 0.0:
            return leg.PayLeg()
        else:
            return not leg.PayLeg()

    def _calcNotional(self, flow):
        return abs(self.nominal * self.quantity * flow.NominalFactor())        

    def _getInflationEstimates(self, flow):

        final_date = flow.InflationScalingDays()[0]
        final_value = 0.0
        if flow.InflationScalingsAreFixed(self.value_date):
            final_value = flow.InflationScalingValues(self.leg_info, self.value_date)[0].Number()
            
        return Util.createDateStringFromDateTime(final_date), final_value
       
    def _createIndexLinkedFlows(self, fixed, description):
        items = CashFlowDataDictionary()
        flows = CashFlowList()

        for flow in self.cashflow_info:
            final_date, final_value = self._getInflationEstimates(flow)
            r = CashFlowDataDictionary()
            r["Payment_Date"] = Util.createDateStringFromDateTime(flow.PayDate())
            if description == "INFLATION FIXED":
                r["Notional"] = flow.FixedAmount() * self._calcNotional(flow)
            else:
                r["Notional"] = self._calcNotional(flow)

            r["Base_Reference_Date"] = ""
            r["Base_Reference_Value"] = self.leg.InflationBaseValue()
            r["Final_Reference_Date"] = final_date
            r["Final_Reference_Value"] = final_value
            r["Accrual_Start_Date"] = ""
            r["Accrual_End_Date"] = ""
            r["Accrual_Day_Count"] = Util.createDayCountString(self.leg.DayCountMethod())
            r["Accrual_Year_Fraction"] = flow.Period()

            if description == "INFLATION FIXED":
                r["Yield"] = "100%"
            elif description == "INFLATION COUPON":
                r["Yield"] = "%f %%" % (100.0 * flow.Rate(self.leg_info))
            else:
                r["Yield"] = "%f %%" % self.leg.FixedRate()

            r["Margin"] = "%f bp" % 0.0 
            r["Rate_Multiplier"] = 1
            r["Is_Coupon"] = "Yes"
            flows.append(r)

        items["Items"] = flows
        
        return items
    
    def addDeal(self, deals, pricing_parameters, fixed):
        cpi_leg = self.leg
        currency = cpi_leg.Currency()
        curve_name = pricing_parameters.AddDiscountCurveAndGetName(cpi_leg.MappedDiscountLink())
        pricing_parameters.AddInflationLegAndGetName(cpi_leg)
        priceIndex = cpi_leg.InflationScalingRef()
        inflationMappingLink = priceIndex.MappedRepoLink(priceIndex.Currency())
        ycComponent = inflationMappingLink.Link().YieldCurveComponent()
        
        index_name = None
        if ycComponent.IsKindOf("FSeasonalityCurve"):
            index_name = DataUtil.parameterName(ycComponent.UnderlyingCurve()) # TODO: Remove this dependency
        else:
            index_name = DataUtil.parameterName(ycComponent) # TODO: Remove this dependency
    
        if fixed:
            description = "INFLATION FIXED"
        elif cpi_leg.LegType() == "Zero Coupon Fixed":
            description = "INFLATION COUPON"
        else:
            description = "INFLATION FLOAT"
        
        deal = PairList()
        deal["Object"] = "YieldInflationCashflowListDeal"
        deal["Reference"] = self.identifier
        deal["MtM"] = Util.getMtMValue(self.mtm)
        deal["Tags"] = ""
        deal["Currency"] = currency.Name()
        deal["Discount_Rate"] = curve_name
        deal["Cashflows"] = self._createIndexLinkedFlows(fixed, description)
        deal["Buy_Sell"] = Util.getBuySellFlag(self._isPayLeg(cpi_leg))
        deal["Is_Forward_Deal"] = "Yes" if self.forward_date else "No"
        deal["Index"] = index_name
        deal["Description"] = description   
        deal["Issuer"] = ""
        deal["Survival_Probability"] = ""
        deal["Recovery_Rate"] = ""
        deal["Settlement_Date"] = Util.createDateStringFromDateTime(self.forward_date) if self.forward_date else ""
        deal["Repo_Rate"] = ""
        deal["Calendars"] = cpi_leg.PayCalendar().Name()
        deal["Investment_Horizon"] = ""
        
        deals.Add(deal.compose())
