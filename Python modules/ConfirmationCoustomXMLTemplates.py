import acm
from FOperationsXML import FOperationsXML

amendment= '''\
<?xml version="1.0" encoding="ISO-8859-1"?>
<MESSAGE>
  <TRADE acmLoop = "Trade">
    <ACQUIRE_DAY><acmCode method ='AcquireDay'/></ACQUIRE_DAY>
    <CONNECTED_TRADE><acmCode method ='ConnectedTrade.Oid'/></CONNECTED_TRADE>
    <CONTRACT_TRDNBR><acmCode method ='Contract.Oid'/></CONTRACT_TRDNBR>
    <CORRECTION_TRADE><acmCode method ='CorrectionTrade.Oid'/></CORRECTION_TRADE>
    <COUNTERPARTY><acmCode method ='Counterparty.Name'/></COUNTERPARTY>
    <CURR><acmCode method ='Currency.Name'/></CURR>
    <FEE><acmCode method ='Fee'/></FEE>
    <ORIGINAL_CURRENCY><acmCode method ='OriginalCurrency.Oid'/></ORIGINAL_CURRENCY>
    <PREMIUM><acmCode method = 'Premium'/></PREMIUM>
    <PRICE><acmCode method = 'Price'/></PRICE>
    <QUANTITY><acmCode method = 'Quantity'/></QUANTITY>
    <TRADE_TIME><acmCode method = 'TradeTime'/></TRADE_TIME>
    <TRADE_CURRENCY><acmCode method = 'TradeCurrency'/></TRADE_CURRENCY>
    <TRX_TRADE><acmCode method = 'TrxTrade.Oid'/></TRX_TRADE>
    <TYPE><acmCode method = 'Type'/></TYPE>
    <VALUE_DAY><acmCode method = 'ValueDay'/></VALUE_DAY>
    <PAYMENT acmLoop = "Payments">
        <AMOUNT><acmCode method = 'Amount'/></AMOUNT>
        <CURRENCY><acmCode method ='Currency.Name'/></CURRENCY>
        <PAY_DAY><acmCode method ='PayDay'/></PAY_DAY>
        <PARTY><acmCode method ='Party.Name'/></PARTY>
        <TYPE><acmCode method ='Type'/></TYPE>
    </PAYMENT>
  </TRADE>
  <INSTRUMENT acmLoop = "Trade.Instrument">
    <CONTRACT_SIZE><acmCode method ='ContractSize'/></CONTRACT_SIZE>
    <CURRENCY><acmCode method ='Currency.Name'/></CURRENCY>
    <DAY_COUNT_METHOD><acmCode method ='DayCountMethod'/></DAY_COUNT_METHOD>
    <DIGITAL><acmCode method ='Digital'/></DIGITAL>
    <EX_COUPON_METHOD><acmCode method ='ExCouponMethod'/></EX_COUPON_METHOD>
    <EXPIRY_TIME><acmCode method ='ExpiryTime'/></EXPIRY_TIME>
    <EXOTIC_TYPE><acmCode method ='ExoticType'/></EXOTIC_TYPE>
    <EXPIRY_DATE><acmCode method ='ExpityDate'/></EXPIRY_DATE>
    <INS_TYPE><acmCode method ='InsType'/></INS_TYPE>
    <ORIGINAL_CURRENCY><acmCode method ='OriginalCurrency.Name'/></ORIGINAL_CURRENCY>
    <PAY_DAY_OFFSET><acmCode method ='PayDayOffset'/></PAY_DAY_OFFSET>
    <PAY_OFFSET_METHOD><acmCode method ='PayOffsetMethod'/></PAY_OFFSET_METHOD>
    <PAY_TYPE><acmCode method ='PayType'/></PAY_TYPE>
    <SETTLEMENT_TYPE><acmCode method ='SettlementType'/></SETTLEMENT_TYPE>
    <START_DATE><acmCode method ='StartDate'/></START_DATE>
    <STRIKE_CURRENCY><acmCode method ='StrikeCurrency.Name'/></STRIKE_CURRENCY>
    <STRIKE_PRICE><acmCode method ='StrikePrice'/></STRIKE_PRICE>
    <STRIKE_TYPE><acmCode method ='StrikeType'/></STRIKE_TYPE>
    <UNDERLYING><acmCode method ='Underlying.Name'/></UNDERLYING>
    <UNDERLYING_TYPE><acmCode method ='UnderlyingType'/></UNDERLYING_TYPE>
    <LEG acmLoop = "Legs">
        <AMORT_DAY_COUNT_METHOD><acmCode method ='AmortDaycountMethod'/></AMORT_DAY_COUNT_METHOD>
        <AMORT_END_DAY><acmCode method ='AmortEndDay'/></AMORT_END_DAY>
        <AMORT_END_NOMINAL_FACTOR><acmCode method ='AmortEndNominalFactor'/></AMORT_END_NOMINAL_FACTOR>
        <AMORT_END_PERIOD_COUNT><acmCode method ='AmortEndPeriodCount'/></AMORT_END_PERIOD_COUNT>
        <AMORT_END_PERIOD_UNIT><acmCode method ='AmortEndPeriodUnit'/></AMORT_END_PERIOD_UNIT>
        <AMORT_START_DAY><acmCode method ='AmortStartDay'/></AMORT_START_DAY>
        <AMORT_START_PERIOD_COUNT><acmCode method ='AmortStartPeriodCount'/></AMORT_START_PERIOD_COUNT>
        <AMORT_START_PERIOD_UNIT><acmCode method ='AmortStartPeriodUnit'/></AMORT_START_PERIOD_UNIT>
        <AMORT_TYPE><acmCode method ='AmortType'/></AMORT_TYPE>
        <CURRENCY><acmCode method ='Currency.Name'/></CURRENCY>
        <DAY_COUNT_METHOD><acmCode method ='DayCountMethod'/></DAY_COUNT_METHOD>
        <DIGITAL><acmCode method ='Digital'/></DIGITAL>
        <END_DATE><acmCode method ='EndDate'/></END_DATE>
        <END_PERIOD_COUNT><acmCode method ='EndPeriodCount'/></END_PERIOD_COUNT>
        <END_PERIOD_UNIT><acmCode method ='EndPeriodUnit'/></END_PERIOD_UNIT>
        <EXOTIC_TYPE><acmCode method ='ExoticType'/></EXOTIC_TYPE>
        <FIXED_COUPON><acmCode method ='FixedCoupon'/></FIXED_COUPON>
        <FIXED_RATE><acmCode method ='FixedRate'/></FIXED_RATE>
        <FLOAT_RATE_REFERENCE><acmCode method ='FloatRateReference.Name'/></FLOAT_RATE_REFERENCE>
        <NOMINAL_FACTOR><acmCode method ='NominalFactor'/></NOMINAL_FACTOR>
        <PAY_LEG><acmCode method ='PayLeg'/></PAY_LEG>
        <PAY_CALENDAR><acmCode method ='PayCalendar.Name'/></PAY_CALENDAR>
        <PAY_2_CALENDAR><acmCode method ='Pay2Calendar.Name'/></PAY_2_CALENDAR>
        <PAY_3_CALENDAR><acmCode method ='Pay3Calendar.Name'/></PAY_3_CALENDAR>
        <PAY_DAY_METHOD><acmCode method ='PayDayMethod'/></PAY_DAY_METHOD>
        <PAY_OFFSET_COUNT><acmCode method ='PayOffsetCount'/></PAY_OFFSET_COUNT>
        <PAY_OFFSET_UNIT><acmCode method ='PayOffsetUnit'/></PAY_OFFSET_UNIT>
        <RESET_CALENDAR><acmCode method ='ResetCalendar.Name'/></RESET_CALENDAR>
        <RESET_2_CALENDAR><acmCode method ='Reset2Calendar.Name'/></RESET_2_CALENDAR>
        <RESET_3_CALENDAR><acmCode method ='Reset3Calendar.Name'/></RESET_3_CALENDAR>
        <RESET_DAY_METHOD><acmCode method ='ResetDayMethod'/></RESET_DAY_METHOD>
        <RESET_DAY_OFFSET><acmCode method ='ResetDayOffset'/></RESET_DAY_OFFSET>
        <RESET_PERIOD_COUNT><acmCode method ='ResetPeriodCount'/></RESET_PERIOD_COUNT>
        <RESET_PERIOD_UNIT><acmCode method ='ResetPeriodUnit'/></RESET_PERIOD_UNIT>
        <RESET_TYPE><acmCode method ='ResetType'/></RESET_TYPE>
        <ROLLING_PERIOD_BASE><acmCode method ='RollingPeriodBase'/></ROLLING_PERIOD_BASE>
        <ROLLING_PERIOD_COUNT><acmCode method ='RollingPeriodCount'/></ROLLING_PERIOD_COUNT>
        <ROLLING_PERIOD_UNIT><acmCode method ='RollingPeriodUnit'/></ROLLING_PERIOD_UNIT>
        <SPREAD><acmCode method ='Spread'/></SPREAD>
        <START_DATE><acmCode method ='StartDate'/></START_DATE>
        <START_PERIOD_COUNT><acmCode method ='StartPeriodCount'/></START_PERIOD_COUNT>
        <START_PERIOD_UNIT><acmCode method ='StartPeriodUnit'/></START_PERIOD_UNIT>
        <STRIKE_PRICE><acmCode method ='StrikePrice'/></STRIKE_PRICE>
        <LEG_TYPE><acmCode method ='LegType'/></LEG_TYPE>
        <CASHFLOW acmLoop = "CashFlows">
            <END_DATE><acmCode method ='EndDate'/></END_DATE>
            <FIXED_AMOUNT><acmCode method ='FixedAmount'/></FIXED_AMOUNT>
            <FLOAT_RATE_FACTOR><acmCode method ='FloatRateFactor'/></FLOAT_RATE_FACTOR>
            <FLOAT_RATE_FACTOR_2><acmCode method ='FloatRateFactor2'/></FLOAT_RATE_FACTOR_2>
            <FLOAT_RATE_OFFSET><acmCode method ='FloatRateOffset'/></FLOAT_RATE_OFFSET>
            <NOMINAL_FACTOR><acmCode method ='NominalFactor'/></NOMINAL_FACTOR>
            <PAY_DATE><acmCode method ='PayDate'/></PAY_DATE>
            <FIXED_RATE><acmCode method ='FixedRate'/></FIXED_RATE>
            <SPREAD><acmCode method ='Spread'/></SPREAD>
            <SPREAD_2><acmCode method ='Spread2'/></SPREAD_2>
            <START_DATE><acmCode method ='StartDate' file = 'ConfirmationCoustomXMLTemplates'/></START_DATE>
            <STRIKE_PRICE><acmCode method ='StrikePrice'/></STRIKE_PRICE>
            <CASHFLOW_TYPE><acmCode method ='CashFlowType'/></CASHFLOW_TYPE>
        </CASHFLOW>
    </LEG>
  </INSTRUMENT>
</MESSAGE>
'''

def StartDate(cashFlow):
    import ael
    if ael.CashFlow[cashFlow.Oid()]:
        return ael.CashFlow[cashFlow.Oid()].start_day
    return "No cashflow found"

#print FOperationsXML.GenerateXmlFromTemplateAsString(amendment , acm.FConfirmation[9470])

