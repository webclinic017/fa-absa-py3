""" Compiled: NONE NONE """
#-----------------------------------------------------------------------------------------------------------------
#  Developer           : Anwar
#  Purpose             : ISDA Matrix definitions used for confirmations to Trident
#  Department and Desk : Operations
#  Requester           : Miguel
#  CR Number           : 617525
#-----------------------------------------------------------------------------------------------------------------

import acm, ABSA_XML_IRCapFloor_Template, ABSA_XML_IRSwap_Template, ABSA_XML_FRA_Template, ABSA_XML_Swaption, ABSA_XML_CommodityForward, ABSA_XML_MetalLoanDeposit, ABSA_XML_CommodityOption, ABSA_XML_PhysicalOption, ABSA_XML_CommoditySwaption, ABSA_XML_CommoditySwap
import datetime, time, ael
import ABSADocumentStatusTransitions
import FOperationsUtils as Utils
from ABSADataContainer import ABSADataContainer
from ABSAFOperationsXML import InvalidTagException
from ABSAFOperationsXML import InvalidEventException
from ISDA_MATRIX import *
from ISDA_COMMODITY_MATRIX import *

def Get_Confirmation():
    return ABSADataContainer.GetConfirmation()

#***** ABSA_XML_Main_Template Functions *****
def Get_Product_XML(trade):
    instype = trade.Instrument().InsType()
    undinstype = trade.Instrument().UnderlyingType()
    if instype in ('Swap', 'CurrSwap', 'IndexLinkedSwap'):
        return ABSA_XML_IRSwap_Template.Get_IRSwap(trade)
    elif instype in ('Cap', 'Floor'):
        return ABSA_XML_IRCapFloor_Template.Get_IRCapFloor(trade)
    elif instype == 'FRA':
        return ABSA_XML_FRA_Template.Get_FRA(trade)
    elif instype == 'Curr':
        if Get_Und_Comm_Type(trade.Instrument()):
            return ABSA_XML_CommodityForward.Get_CommodityForward(trade)
    elif instype == 'Deposit':
        if Get_Und_Comm_Type(trade.Instrument()):
            return ABSA_XML_MetalLoanDeposit.Get_MetalLoanDeposit(trade)
    elif instype == 'Future/Forward':
        if undinstype == 'Commodity':
            if Get_Und_Comm_Type(trade.Instrument().Underlying()):
                return ABSA_XML_CommoditySwap.Get_CommoditySwap(trade)
    elif instype == 'Option':
        if undinstype == 'Commodity':
            if Get_Und_Comm_Type(trade.Instrument().Underlying()):
                return ABSA_XML_CommodityOption.Get_CommodityOption(trade)
        elif undinstype == 'Curr':
            if Get_Und_Comm_Type(trade.Instrument().Underlying()):
                return ABSA_XML_PhysicalOption.Get_PhysicalOption(trade)
        #elif Is_Swaption(trade):
        elif undinstype == 'Swap':
            if Get_Und_Comm_Type(trade.Instrument().Underlying()):
                return ABSA_XML_CommoditySwaption.Get_CommoditySwaption(trade)
            else:
                return ABSA_XML_Swaption.Get_Swaption(trade)
        elif Is_CapletFloorlet(trade):
            return ABSA_XML_IRCapFloor_Template.Get_IRCapFloor(trade)

    return None
    
def Get_Product_XML_IRSwap(trade):
    return ABSA_XML_IRSwap_Template.Get_IRSwap(trade)

def Get_Event_Name(confirmation):
    valid_lowest_event = ('New Trade', 'Close', 'Partial Close')
    conf_event = confirmation.EventChlItem().Name()
    conf_status = confirmation.Status()
    trade_status = confirmation.Trade().Status()
    novation = confirmation.Trade().add_info('NovationTermination')
    lowest_conf = ABSADocumentStatusTransitions.GetBottommostConfirmation(confirmation)
    conf_type = confirmation.Type()
    
    if conf_status == 'Pending Document Generation':
        if lowest_conf.EventChlItem().Name() in valid_lowest_event and lowest_conf.Type() == 'Default':
            if trade_status == 'Void':
                if conf_type == 'Cancellation':
                    return 'Cancellation'
            if trade_status == 'BO Confirmed':
                if conf_event == 'New Trade' and conf_type == 'Default':
                    if novation == 'NovationRemainingParty':
                        return 'NovationRemainingParty'
                    return 'New'
                if conf_type == 'Amendment':
                    return 'Amendment'
                if conf_event == 'Close' and conf_type == 'Default':
                    if novation == 'NovationOut':
                        return 'NovationOut'
                    return 'FullTermination'
                if conf_event == 'Partial Close' and conf_type == 'Default':
                    if novation == 'NovationOut':
                        return 'NovationOut'
                    return 'FullTermination'
                if conf_type == 'Cancellation':
                    return 'Cancellation'
            if trade_status == 'BO-BO Confirmed':
                if conf_type == 'Amendment':
                    return 'Amendment'
                if conf_event == 'Close' and conf_type == 'Default':
                    if novation == 'NovationOut':
                        return 'NovationOut'
                    return 'FullTermination'
                if conf_event == 'Partial Close' and conf_type == 'Default':
                    if novation == 'NovationOut':
                        return 'NovationOut'
                    return 'FullTermination'
                if conf_type == 'Cancellation':
                    return 'Cancellation'
            if trade_status == 'Terminated':
                if conf_event == 'Close' and conf_type == 'Default':
                    if novation == 'NovationOut':
                        return 'NovationOut'
                    return 'FullTermination'
                if conf_event == 'Partial Close' and conf_type == 'Default':
                    if novation == 'NovationOut':
                        return 'NovationOut'
                    return 'FullTermination'
            return 'Undefined'
        else:
            raise InvalidEventException, 'The event type of the lowest level of confirmation ' + (str)(confirmation.Oid()) + ' is not supported.'
                
    return 'Undefined'

def Get_Event_Reason(confirmation):
    event_reason = acm.FArray()
    event_name = Get_Event_Name(confirmation)
    trade = confirmation.Trade()
    novationTermination = trade.add_info('NovationTermination')
    if event_name == 'New':
        if novationTermination != '':
            if novationTermination.__contains__('Partial'):
                event_reason.Add(novationTermination)
            elif novationTermination == 'NovationIn':
                event_reason.Add(novationTermination)
            return event_reason
        if trade.CorrectionTrade():
            if trade.Counterparty().Name() != trade.CorrectionTrade().Counterparty().Name():
                event_reason.Add('CancellationRebook')
                return event_reason
        if trade.Instrument().InsType() in ('Swap', 'FRA', 'Future/Forward'):
            if Is_NewFromExercise(trade):
                event_reason.Add('Exercise')
                return event_reason
    elif event_name == 'FullTermination':
        if novationTermination != '':
            if not novationTermination == 'NovationIn':
                event_reason.Add(novationTermination)
            return event_reason
    elif event_name == 'Cancellation':
        #ABCAPFATLMIRD-35 
        #2010-10-13 - Anwar commented out -> Migs comment on issue: Please remove event reason for all cancellation event messages, in order to avoid breaking Trident STP
        '''
        if novationTermination != '':
            event_reason.Add(novationTermination)
            return event_reason
        '''
        #ABCAPFATLMIRD-35
        new_trades = acm.FTrade.Select('correctionTrade = %i' %trade.Oid())
        for t in new_trades:
            if t.Oid() != trade.Oid() and t.Counterparty().Name() != trade.Counterparty().Name():
                event_reason.Add('CancellationRebook')
                return event_reason
    return None

def Get_Event_Reason_Value(object):
    return object

def Get_Confirmation_Create_Date(confirmation):
    return datetime.date.fromtimestamp(confirmation.CreateTime())

def Get_Confirmation_Create_Time(confirmation):
    return time.strftime('%H:%M:%S', time.localtime(confirmation.CreateTime()))

#def Get_Trade_Date(trade):
#    return trade.Trade().TradeTime()[:10]

#def Get_Trade_Time(trade):
#    return trade.Trade().TradeTime()[11:]

#def Get_Trade_Create_DateTime(trade):
#    return datetime.datetime.fromtimestamp(trade.CreateTime())

def Get_Trade_Create_Date(trade):
    return datetime.date.fromtimestamp(trade.CreateTime())

#def Get_Trade_Create_Date_From_Conf(confirmation):
#    return Get_Trade_Create_Date(confirmation.Trade())

def Get_Trade_Create_Time(trade):
    return time.strftime('%H:%M:%S', time.localtime(trade.CreateTime()))

#def Get_Trade_Create_Time_From_Conf(confirmation):
#    return Get_Trade_Create_Time(confirmation.Trade())

def Is_Related_Trade(trade):
    if trade.CorrectionTrade():
        return trade

    if trade.Contract():
        if trade.Contract().Oid() != trade.Oid():
            return trade
            
    return None

def Get_Related_Trade(trade):
    if trade.CorrectionTrade():
        return trade.CorrectionTrade().Oid()

    if trade.Contract():
        if trade.Contract().Oid() != trade.Oid():
            return trade.Contract().Oid()
            
    return None

def Is_Closed_Trade_Details(trade):
    if Is_Full_Termination(trade) or Is_Full_Novation_Out(trade):
        return trade
    return None

def Is_Full_Termination(trade):
    if trade.Type() == 'Closing':
        confirmations = acm.FConfirmation.Select('trade = %i' %trade.Oid())
        for c in confirmations:
            if c.EventChlItem().Name() == 'Close':
                if trade.add_info('NovationTermination') == '':
                    return trade
    return None

def Is_Full_Novation_Out(trade):
    if trade.add_info('NovationTermination') == 'NovationOut':
        return trade
    return None

#def Get_CP_SDS_ID(trade):
#    return trade.Counterparty().add_info('BarCap_SMS_CP_SDSID')

#def Get_LE_SDS_ID(trade):
#    return trade.Counterparty().add_info('BarCap_SMS_LE_SDSID')

#def Get_Broker_SDS_ID(trade):
#    return trade.Broker().add_info('BarCap_SMS_CP_SDSID')

def Get_Product_Type(trade):
    instype = trade.Instrument().InsType()
    undinstype = trade.Instrument().UnderlyingType()
    if (instype == 'CurrSwap') or (instype == 'Swap' and Get_Product_Subtype(trade) != 'Unverified'):
        return 'InterestRateSwap'
    elif instype == 'FRA':
        return 'ForwardRateAgreement'
    elif instype in ('Cap', 'Floor'):
        return 'InterestRateCapFloor'
    elif instype == 'IndexLinkedSwap':
        for l in trade.Instrument().Legs():
            if l.RollingPeriodCount() != 0:
                return 'Unverified'
        return 'InflationSwap'
    #elif Is_Swaption(trade):
    #    return 'Swaption'
    elif instype == 'Curr':
        if Get_Und_Comm_Type(trade.Instrument()):
            return 'CommodityForward'
    elif instype == 'Deposit':
        if Get_Und_Comm_Type(trade.Instrument()):
            return 'MetalLoanDeposit'
    elif instype == 'Future/Forward':
        if undinstype == 'Commodity':
            if Get_Und_Comm_Type(trade.Instrument().Underlying()):
                return 'CommoditySwap'
    if instype == 'Option':
        if undinstype == 'Commodity':
            return 'CommodityOption'
        elif undinstype == 'Curr':
            if Get_Und_Comm_Type(trade.Instrument().Underlying()):
                #return 'PhysicalOption'
                return 'CommodityOption'
        elif undinstype == 'Swap':
            if Get_Und_Comm_Type(trade.Instrument().Underlying()):
                return 'CommoditySwaption'
            else:
                return 'Swaption'
        elif Is_CapletFloorlet(trade):
            return 'InterestRateCapFloor'
    return 'Unverified'

def Get_Product_Subtype(object):
    if object.RecordType() == 'Trade':
        instrument = object.Instrument()
        instype = instrument.InsType()
    elif object.RecordType() == 'Instrument':
        instrument = object
        instype = instrument.InsType()
    if instype == 'Swap':
        floatLeg = 0
        fixedLeg = 0
        cf = acm.FArray()
        last_cf_payDay = ''
        for l in instrument.Legs():
            if l.LegType() == 'Float':
                floatLeg = floatLeg + 1
            if l.LegType() == 'Fixed':
                fixedLeg = fixedLeg + 1
            cf.Add(l.CashFlows().Size())
            for c in l.CashFlows():
                if last_cf_payDay <= c.PayDate():
                    last_cf_payDay = c.PayDate()
        if min(cf) == 1 and l.Instrument().ExpiryDate()[:10] == last_cf_payDay:
            zeroFlag = 0
            for l in instrument.Legs():
                if l.LegType() == 'Fixed' and l.RollingPeriodCount() == 0:
                    zeroFlag = 1
            if zeroFlag:
                for l in instrument.Legs():
                    if l.LegType() == 'Float' and l.RollingPeriodCount() != 0:
                        return 'ZeroCouponIRSwap'
        if floatLeg == 2:
            return 'BasisIRSwap'
        if fixedLeg == 1 and floatLeg == 1:
            return 'SimpleIRSwap'
    elif instype == 'CurrSwap':
        for l in instrument.Legs():
            if l.NominalScaling() == 'FX':
                return 'MtmCrossCurrencyIRSwap'
        return 'CrossCurrencyIRSwap'
    elif instype == 'FRA':
        return 'ForwardRateAgreement'
    elif instype == 'Cap':
        if instrument.Legs().At(0).Digital():
            return 'DigitalCap'
        return 'VanillaCap'
    elif instype == 'Floor':
        if instrument.Legs().At(0).Digital():
            return 'DigitalFloor'
        return 'VanillaFloor'
    elif instype == 'IndexLinkedSwap':
        return 'ZeroCouponInflationSwap'
    elif instype == 'Curr':
        if Get_Und_Comm_Type(instrument):
            return 'PhysicalForward'
    elif instype == 'Future/Forward':
        undinstype = instrument.UnderlyingType()
        if undinstype == 'Commodity':
            if Get_Und_Comm_Type(instrument.Underlying()):
                return 'FinancialFixedFloatingSwap'
    elif instype == 'Deposit':
        if Get_Und_Comm_Type(instrument):
            #return 'MetalLoan'
            return 'MetalDeposit'
    if instype == 'Option':
        undinstype = instrument.UnderlyingType()
        if undinstype == 'Commodity':
            return 'FinancialOption'
        elif undinstype == 'Curr':
            if Get_Und_Comm_Type(instrument.Underlying()):
                return 'PhysicalOption'
        elif undinstype == 'Swap':
            if Get_Und_Comm_Type(instrument.Underlying()):
                return 'FinancialSwaption'
            elif Is_Swaption(instrument):
                return Get_Product_Subtype(instrument.Underlying())
        elif Is_CapletFloorlet(instrument):
            if Is_Caplet(instrument):
                return 'FRAOptionCaplet'
            else:
                return  'FRAOptionFloorlet'
    return 'Unverified'

def Get_Premium_Payments(trade):
    payments = acm.FArray()
    confirmation = Get_Confirmation()
    event_name = Get_Event_Name(confirmation)
    for p in trade.Payments():
        if p.Party().Name() == trade.Counterparty().Name():
            if p.Type() in ('Premium', 'Cash'):
                payments.Add(p)
            elif event_name in ('FullTermination', 'PartialTermination') and p.Type() == 'Termination Fee':
                payments.Add(p)
    payments.SortByProperty('PayDay', True)
    return payments

def Get_Payment_PayOrReceive(payment):
    if payment.Amount() < 0:
        return 'Pay'
    return 'Receive'

def Get_Pay_Day_Method(payment):
    for l in payment.Trade().Instrument().Legs():
        return Get_Leg_PayDayMethod(l)
    return 'NotApplicable'

def Get_Leg_PayDayMethod(leg):
    method = leg.PayDayMethod()
    methodMap = {'Following':'FOLLOWING','Preceding':'PRECEDING','Mod. Following':'MODFOLLOWING','Mod. Preceding':'MODPRECEDING','FRN Convention':'FRN','IMM':'MODFOLLOWING','Monthly IMM':'MODFOLLOWING','EOM':'EOM','CDS Convention':'NotApplicable','BMA Convention':'NotApplicable','FOM':'NotApplicable'}
    if methodMap.has_key(method):
        return methodMap[method]
    return 'NotApplicable'
    
#def Get_Leg_PayDayMethod_Trade(trade):
#    return Get_Leg_PayDayMethod(trade.Instrument().Underlying().Legs()[0])

#***** ABSA_XML_Main_Template Functions *****
#*****          End                     *****

#***** ABSA_XML_IRSwap_Template Functions *****

def Get_Insrt_PayOrReceive(object):
    if object.RecordType() == 'Trade':
        trade = object
    else:
        trade = Get_Confirmation().Trade()
        leg = object
    if trade.Instrument().InsType() not in ('Option', 'Future/Forward'):
        cf_total = 0
        for cf in leg.CashFlows():
            if not(cf.CashFlowType() in ('Fixed Amount', 'Return')):
                projected_entity = cf.Calculation().Projected(ABSADataContainer.GetCalculationSpace(), trade)
                if projected_entity != 0:
                    cf_total = cf_total + projected_entity.Value().Number()
        if cf_total < 0:
            return 'Pay'
        return 'Receive'
    elif Is_Swaption(trade):
        ins = trade.Instrument()
        if trade.Nominal() < 0:   #AbCap = Sell
            if ins.IsCallOption():          #true = Payer
                fixer = False   #AbCap pays float
            else:                           #false = Reciever
                fixer = True    #AbCap pays fixed
        else:                   #AbCap = Buy
            if ins.IsCallOption():          #True = Payer
                fixer = True    #AbCap pays fixed
            else:                           #False = Reciever
                fixer = False   #AbCap pays float
        if leg.LegType() == 'Fixed':
            if fixer:
                return 'Pay'
        elif leg.LegType() == 'Float':
            if not fixer:
                return 'Pay'
        return 'Receive'
    else:       #for Future/Forwards and CapletFloorlets
        if trade.Nominal() < 0:   #AbCap = Sell
            fixer = False   #AbCap pays float
        else:                   #AbCap = Buy
            fixer = True    #AbCap pays fixed
        if not fixer:
            return 'Pay'
        return 'Receive'
 
def Get_Frequency_Period(leg):
    if leg.RollingPeriodCount() == 0:
        return 'T'
    return leg.RollingPeriodUnit()[0]

def Get_Frequency_Period_Multiplier(leg):
    multiplier = leg.RollingPeriodCount()
    if multiplier == 0:
        return 1
    return multiplier
    
#Anwar 2010-09-21
def Get_IndexTenor_Frequency_Period(leg):
    if Is_Averaging(leg):
        if leg.ResetType() == 'Weighted':
            return 'D'

    if Is_ZAR_PRIME_Rate(leg):
        if (leg.RollingPeriodCount() == 1 and leg.RollingPeriodUnit()[0] == 'D') or (leg.ResetPeriodCount() == 1 and leg.ResetPeriodUnit()[0] == 'D'):
            return 'D'
            
    if leg.RollingPeriodCount() == 0:
        return 'T'
    return leg.RollingPeriodUnit()[0]

def Get_IndexTenor_Frequency_Period_Multiplier(leg):
    if Is_Averaging(leg):
        if leg.ResetType() == 'Weighted':
            return 1
            
    multiplier = leg.RollingPeriodCount()

    if multiplier == 0:
        return 1

    if Is_ZAR_PRIME_Rate(leg):
        if (multiplier == 1 and leg.RollingPeriodUnit()[0] == 'D') or (leg.ResetPeriodCount() == 1 and leg.ResetPeriodUnit()[0] == 'D'):
            return 1
            
    return multiplier
#Anwar

def Get_CashFlow_Nominal(cashflow):
    trade = Get_Confirmation().Trade()
    cf_nominal = cashflow.Calculation().Projected(ABSADataContainer.GetCalculationSpace(), trade).Value().Number()
    return cf_nominal

def Get_CF_Nominal(object):
    trade = Get_Confirmation().Trade()
    if Is_CapletFloorlet(trade):
        return abs(trade.Nominal())
    else:
        if object.RecordType() == 'CashFlow':
            return Get_CashFlow_Nominal_Amount(object)
        return Get_CashFlow_Nominal_Amount_Reset(object)

def Get_CashFlow_Nominal_Amount(cashflow):
    trade = Get_Confirmation().Trade()
    cf_nominal = ('%.2f' % (abs(cashflow.Calculation().Nominal(ABSADataContainer.GetCalculationSpace(), trade).Value().Number())))
    return cf_nominal

def Get_CashFlow_Nominal_Amount_Reset(reset):
    return Get_CashFlow_Nominal_Amount(reset.CashFlow())

def Get_CashFlow_Status_Object(object):
    if object.RecordType() == 'CashFlow':
        return Get_Cashflow_Status(object)
    return Get_Cashflow_Status_Reset(object)
    
def Get_Cashflow_Status(cashflow):
    if cashflow.Leg().LegType() == 'Fixed':
        return 'Known'
    elif cashflow.Leg().LegType() == 'Float':
        for r in cashflow.Resets():
            if r.FixingValue() != 0:
                return 'Known'
    return 'Projected'

def Get_Cashflow_Status_Reset(reset):
    return Get_Cashflow_Status(reset.CashFlow())

def Is_Floating_CF_Type(cashflow):
    if cashflow.CashFlowType() == 'Float Rate':
        return cashflow
    return None

def Get_CurrSwap_CF(leg):
    if leg.Instrument().InsType() == 'CurrSwap':
        return leg.CashFlows()
    return None

def __Get_Calendar(leg):
    calendars = acm.FArray()
    if leg.PayCalendar():
        calendars.Add(leg.PayCalendar())
    if leg.Pay2Calendar():
        calendars.Add(leg.Pay2Calendar())
    if leg.Pay3Calendar():
        calendars.Add(leg.Pay3Calendar())
    if leg.Pay4Calendar():
        calendars.Add(leg.Pay4Calendar())
    if leg.Pay5Calendar():
        calendars.Add(leg.Pay5Calendar())
    
    return calendars


def Get_Calendar(leg):
    calendars = __Get_Calendar(leg)
    #if Is_LIBOR_Linked(leg):
    #    calendars = Add_GBP_London(calendars)
    return calendars


def Get_Calendar_Map(calendar):
    cal_dict = {'AUD Sydney':'AUSY','BRL Brasilia':'BRBR','CAD Toronto':'CATO','CHF Zurich':'CHZU','CNY Beijing':'CNBE','CZK Prague':'CZPR','DEM Frankfurt':'DEFR','DKK Copenhagen':'DKCO','GBP London':'GBLO','HKD Hong Kong':'HKHK','HUF Budapest':'HUBU','ILS Tel Aviv':'ILTA','INR New Delhi':'INMU','JPY Tokyo':'JPTO','MXN Mexico':'MXMC','MYR Kuala Lumpur':'MYKL','NOK Oslo':'NOOS','NZD Auckland':'NZAU','PLN Warsaw':'PLWA','SEK Stockholm':'SEST','SGD Singapore':'SGSI','Target':'EUTA','EUR Euro':'EUTA','THB - Thai':'THBA','TRY - Turkey':'TRIS','USD New York':'USNY','ZAR Johannesburg':'ZAJO','NZD Wellington':'NZWE'}
    if cal_dict.has_key(calendar.Name()):
        return cal_dict[calendar.Name()]
    return ""
    
def PassThrough(value):
    return value

#-------------------- Functions for Stub Period ------------------#
def Get_First_Or_Last_CF(leg, acm_date_field, flag):
    confirmation = Get_Confirmation()
    cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    cashFlowQuery.AddAttrNode('PayDate', 'GREATER', confirmation.Trade().ValueDay())
    cashFlowType = cashFlowQuery.AddOpNode('OR')
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Fixed Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Float Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Floorlet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Floorlet'))
    cashFlows = cashFlowQuery.Select().SortByProperty(acm_date_field, flag) # The last argument is "ascending"
    if cashFlows:
        return cashFlows[0]
    return None
    
def convert_Rolling_to_Year(leg):
    period_multiplier = {'Days': 365, 'Weeks': 52, 'Months': 12, 'Years': 1}
    #Anwar 2010-09-23
    #return leg.RollingPeriodCount() / float(period_multiplier[leg.RollingPeriodUnit()])
    try:
        return round(leg.RollingPeriodCount() / float(period_multiplier[leg.RollingPeriodUnit()]), 2)
    except:
        return 0
    #Anwar

def Get_Stub_Period_Object(leg):
    if convert_Rolling_to_Year(leg) != 0:
        instype = leg.Instrument().InsType()
        if instype in ('Swap', 'CurrSwap', 'IndexLinkedSwap'):
            stub = acm.FArray()
            first_cf = Get_First_Or_Last_CF(leg, 'EndDate', True)
            if first_cf:
                days_to_year = round(ael.date_from_string(first_cf.StartDate()).years_between(ael.date_from_string(first_cf.EndDate())), 2)
                rolling_period_to_year = round(convert_Rolling_to_Year(leg), 2)
                ratio = round((days_to_year/rolling_period_to_year), 2)
                if ((ratio <= 0.9) or (ratio >= 1.1)):
                    stub.Add(first_cf)
                    
                last_cf = Get_First_Or_Last_CF(leg, 'EndDate', False)
                if last_cf:
                    days_to_year = round(ael.date_from_string(last_cf.StartDate()).years_between(ael.date_from_string(last_cf.EndDate())), 2)
                    ratio = round((days_to_year/rolling_period_to_year), 2)

                    if ((ratio <= 0.9) or (ratio >= 1.1)):
                        stub.Add(last_cf)
                    
                    if len(stub):
                        return stub
    return None
    
def Get_Stub_Period_Type(cf):
    first_cf = Get_First_Or_Last_CF(cf.Leg(), 'EndDate', True)
    if first_cf:
        first_cf_flag = False
        if cf.Oid() == first_cf.Oid():
            first_cf_flag = True
        
        days_to_year = round(ael.date_from_string(cf.StartDate()).years_between(ael.date_from_string(cf.EndDate())), 2)
        rolling_period_to_year = round(convert_Rolling_to_Year(cf.Leg()), 2)
        ratio = round(days_to_year/rolling_period_to_year, 2)
        if first_cf_flag:
            if ratio < 1:
                return 'ShortInitial'
            return 'LongInitial'
        else:
            if ratio < 1:
                return 'ShortFinal'
            return 'LongFinal'
    return None

#-------------------- Stub Period Calculation End --------------------

def Get_Rolling_Day(leg):
    payDayMethod = leg.PayDayMethod()
    if payDayMethod == 'IMM':
        return 'IMM'
    rollingBaseDay = int(ael.date_from_string(leg.RollingPeriodBase()).to_string('%d'))
    if rollingBaseDay == 31:
        return 'EOM'
    return rollingBaseDay

def Get_Pay_Relative_To(leg):
    if leg.Instrument().InsType() == 'FRA':
        return 'CalculationPeriodStartDate'
    return 'CalculationPeriodEndDate'

def Is_Non_Amortising(leg):
    if leg.AmortType() == 'None':
        return leg
    return None

def Is_Amortising(leg):
    if leg.AmortType() != 'None':
        return leg
    return None

def Get_First_CF_Nominal(leg):
    trade = Get_Confirmation().Trade()
    if Is_CapletFloorlet(trade):
        return abs(trade.Nominal())
    else:
        first_cf = Get_First_Or_Last_CF(leg, 'EndDate', True)
        if first_cf:
            cf_nominal = Get_CashFlow_Nominal_Amount(first_cf)
            return cf_nominal
    return None

def Get_All_Fixed_Amount(leg):
    confirmation = Get_Confirmation()
    cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    cashFlowQuery.AddAttrNode('PayDate', 'GREATER', confirmation.Trade().ValueDay())
    cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    cashFlowQuery.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Fixed Amount'))
    cashFlows = cashFlowQuery.Select().SortByProperty('PayDate', True) # The last argument is "ascending"
    if cashFlows:
        return cashFlows
    return None

def Get_All_Interest(leg):
    confirmation = Get_Confirmation()
    cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    cashFlowQuery.AddAttrNode('PayDate', 'GREATER', confirmation.Trade().ValueDay())
    cashFlowType = cashFlowQuery.AddOpNode('OR')
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Fixed Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Float Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Floorlet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Floorlet'))
    cashFlows = cashFlowQuery.Select().SortByProperty('PayDate', True) # The last argument is "ascending"
    if cashFlows:
        return cashFlows
    return None

def Is_Fixed_Leg(leg):
    if leg.LegType() == 'Fixed' and leg.Instrument().InsType() != 'IndexLinkedSwap':
        return leg
    elif leg.LegType() == 'Fixed' and leg.Instrument().InsType() == 'IndexLinkedSwap' and not leg.IndexRef():
        return leg
    return None

def Is_Float_Leg(leg):
    if (leg.LegType() == 'Float') or (leg.Instrument().InsType() == 'IndexLinkedSwap' and leg.IndexRef() and leg.IndexRef().Name() == 'SACPI'):
        return leg
    return None

def Convert_Fixed_Rate(leg):
    rate = leg.FixedRate()/100
    return rate

def Is_Float_Leg_Swap(leg):
    if leg.LegType() == 'Float':
        if leg.Instrument().InsType() in ('Swap', 'CurrSwap'):
            return leg
        elif leg.Instrument().InsType() == 'IndexLinkedSwap' and not leg.IndexRef():
            return leg
    return None

def Is_Initial_Rate(leg):
    first_cf = Get_First_Or_Last_CF(leg, 'PayDate', True)
    retVal = None
    if first_cf:
        if ael.date(first_cf.StartDate()) == ael.date(leg.Instrument().StartDate()) and (ael.date(first_cf.EndDate()) >= ael.date_today()):
        #if ael.date(first_cf.StartDate()) <= ael.date_today():
            if first_cf.Resets():
                resetQuery = acm.CreateFASQLQuery(acm.FReset, 'AND')
                resetQuery.AddAttrNode('CashFlow.Oid', 'EQUAL', first_cf.Oid())
                resetQuery.AddAttrNode('ResetType', 'NOT_EQUAL', Utils.GetEnum('ResetType', 'Nominal Scaling'))
                resetQuery.AddAttrNode('FixingValue', 'NOT_EQUAL', 0)
                reset = resetQuery.Select().SortByProperty('EndDate', True)
                if reset:
                    retVal = reset[0]
    return retVal
    
def Is_Inflation_Swap(leg):
    if leg.Instrument().InsType() == 'IndexLinkedSwap' and leg.IndexRef():
        if leg.IndexRef().Name() == 'SACPI':
            return leg
    return None

def Get_Day_Count_Method(leg):
    dayCountMethod = leg.DayCountMethod()
    dayCountMethodDict = {'Act/ActISDA':'ACT/ACT.ISDA', 'Act/365':'ACT/365.FIXED', 'Act/360':'ACT/360', '30E/360':'30E/360', '30/360':'30/360', 'NL/365':'ACT/365.FIXED', 'Act/ActAFB':'ACT/365.FIXED', 'Act/ActISMA':'ACT/ACT.ISMA', 'Act/364':'ACT/365.FIXED', '30/360SIA':'ACT/365.FIXED', '30E/365':'ACT/365.FIXED', '30/365':'ACT/365.FIXED', 'NL/360':'ACT/365.FIXED', 'NL/ActISDA':'ACT/365.FIXED', '30U/360':'ACT/365.FIXED', '30/360GERMAN':'ACT/365.FIXED', 'Bus/252':'BUS/252', 'Act/365L':'ACT/365L'}
    if dayCountMethodDict.has_key(dayCountMethod):
        return dayCountMethodDict[dayCountMethod]
    return None

def Get_CF_Nominal_Factor(cf):
    if cf.NominalFactor() != 1:
        return cf
    return None

def Get_CF_Nominal_Factor_Value(cf):
    return ('%.6f' % cf.NominalFactor())

def Get_CF_Nominal_Factor_Reset(reset):
    return Get_CF_Nominal_Factor(reset.CashFlow())

def Convert_Leg_Spread(cf):
    spread = ('%.6f' % (cf.Leg().Spread()/100))
    return spread

def Convert_Leg_Spread_Reset(reset):
    return Convert_Leg_Spread(reset.CashFlow())

def Convert_Leg_Spread_Leg(leg):
    return ('%.6f' % (leg.Spread()/100))

def Is_CF_Type_Float(cf):
    if cf.CashFlowType() == 'Float Rate':
        return cf
    return None

def Is_CF_Type_Float_Reset(reset):
    if Is_CF_Type_Float(reset.CashFlow()):
        return reset
    return None

def Is_CF_Type_Fixed(cf):
    if cf.CashFlowType() == 'Fixed Rate':
        return cf
    return None

def Is_CF_Type_Fixed_Reset(reset):
    if Is_CF_Type_Fixed(reset.CashFlow()):
        return reset
    return None

def Convert_CF_Fixed_Rate(cf):
    rate = cf.Leg().FixedRate()/100
    return rate

def Convert_CF_Fixed_Rate_Reset(reset):
    rate = reset.CashFlow().Leg().FixedRate()/100
    return rate

def Is_Zero_Coupon_Swap(leg):
    trade = Get_Confirmation().Trade()
    if Get_Product_Subtype(trade) == 'ZeroCouponIRSwap' and Get_Insrt_PayOrReceive(leg) == 'Pay':
        return leg
    return None

def Is_Early_Termination(trade):
    trade_date = ael.date(trade.TradeTime()[:10])
    expiry_date = ael.date(trade.Instrument().ExpiryDate()[:10])
    trade_length = trade_date.years_between(expiry_date)
    if trade_length >= 3.08:
        return trade
    return None

def Get_Swap_Exercise_Style(trade):
    trade_date = ael.date(trade.TradeTime()[:10])
    if not Is_Swaption(trade):
        expiry_date = ael.date(trade.Instrument().ExpiryDate()[:10])
    else:
        expiry_date = ael.date(trade.Instrument().Underlying().ExpiryDate()[:10])
    trade_length = trade_date.years_between(expiry_date)
    if trade_length >= 4.9:
        return 'Bermuda'
    return 'European'
    
def Get_Exercise_Style(trade):
    trade_date = ael.date(trade.TradeTime()[:10])
    if not Is_Swaption(trade):
        expiry_date = ael.date(trade.Instrument().ExpiryDate()[:10])
    else:
        expiry_date = ael.date(trade.Instrument().Underlying().ExpiryDate()[:10])
    trade_length = trade_date.years_between(expiry_date)
    if trade_length >= 4.9:
        return 'Bermuda'
    return 'European'

def Is_Bermuda_Exercise(trade):
    style = Get_Exercise_Style(trade)
    if style == 'Bermuda':
        return trade
    return None

def Is_European_Exercise(trade):
    style = Get_Exercise_Style(trade)
    if style == 'European':
        return trade
    return None
    
def Get_European_Unadjusted_Date(trade):
    trade_date = ael.date(trade.TradeTime()[:10])
    break_date = trade_date.add_years(3).to_string('%Y-%m-%d')
    return break_date

def Get_Principal_Exchange(trade):
    subType = Get_Product_Subtype(trade)
    if subType in ('MtmCrossCurrencyIRSwap', 'CrossCurrencyIRSwap'):
        leg = trade.Instrument().Legs().At(0)
        if leg.NominalAtEnd() and leg.NominalAtStart():
            if leg.AmortType() == 'None':
                return 'Both'
            return 'Front'
        elif leg.NominalAtEnd():
            return 'Back'
        elif leg.NominalAtStart():
            return 'Front'
    return 'None'

def Get_Sales_Conf_Approve(confirmation):
    if confirmation.Trade().add_info('Sales Conf Approve') == 'Yes':
        return 'true'
    return 'false'

def Get_Reset_Day_Method(leg):
    method = leg.ResetDayMethod()
    methodMap = {'Following':'FOLLOWING','Preceding':'PRECEDING','Mod. Following':'MODFOLLOWING','Mod. Preceding':'MODPRECEDING','FRN Convention':'FRN','IMM':'MODFOLLOWING','Monthly IMM':'MODFOLLOWING','EOM':'EOM','CDS Convention':'NotApplicable','BMA Convention':'NotApplicable','FOM':'FOM'}
    if methodMap.has_key(method):
        return methodMap[method]
    return 'NotApplicable'

def Get_Reset_Calendar(leg):
    if leg.Instrument().InsType() == 'IndexLinkedSwap' and leg.IndexRef() and leg.IndexRef().Name() == 'SACPI':
        return Get_Calendar(leg)
        
    calendars = acm.FArray()
    if leg.ResetCalendar():
        calendars.Add(leg.ResetCalendar())
    if leg.Reset2Calendar():
        calendars.Add(leg.Reset2Calendar())
    if leg.Reset3Calendar():
        calendars.Add(leg.Reset3Calendar())
    if leg.Reset4Calendar():
        calendars.Add(leg.Reset4Calendar())
    if leg.Reset5Calendar():
        calendars.Add(leg.Reset5Calendar())
    
    #if Is_LIBOR_Linked(leg):
    #    calendars = Add_GBP_London(calendars)
    return calendars

def Get_Reset_Frequency_Period(leg):
    if Get_CompoundingMethod(leg) == 'None':
        return Get_Frequency_Period(leg)
        
    return leg.ResetPeriodUnit()[0]

def Get_Reset_Frequency_Period_Multiplier(leg):
    if Get_CompoundingMethod(leg) == 'None':
        return Get_Frequency_Period_Multiplier(leg)
        
    multiplier = leg.ResetPeriodCount()
    if multiplier == 0:
        return 1
    return multiplier

def Get_Reset_Day_Offset(leg):
    if leg.ResetDayOffset() <= 0:
        return leg.ResetDayOffset()
    return 0

def Is_Reset_In_Stub(leg):
    if leg.LegType() in ('Float', 'Cap'):
        return 'true'
    return 'false'

def Is_Compounding_CF_Object_Value(object):
    if object.RecordType() == 'CashFlow':
        return Is_Compounding_CF(object)
    return Is_Compounding_CF_Reset(object)

def Is_Compounding_CF(cf):
    if cf.CashFlowType() in ('Float Rate', 'Caplet', 'Digital Caplet', 'Floorlet', 'Digital Floorlet'):
        length = len(cf.Resets())
        if length >= 1:
            count = 0
            for r in cf.Resets():
                if r.ResetType() != 'Nominal Scaling':
                    count = count + 1
            if count > 1:
                return 'true'
    return 'false'

def Is_Compounding_CF_Reset(reset):
    return Is_Compounding_CF(reset.CashFlow())

def Is_Not_Compounding_CF_Object(object):
    if object.RecordType() == 'CashFlow':
        return object
    return None

def Is_Compounding_CF_Object(object):
    if object.RecordType() == 'Reset':
        return object
    return None

def Get_Bermuda_Unadjusted_Dates(trade):
    adjustedDate = acm.Time.DateAddDelta(trade.TradeTime(), 3, 0, 0)
    if not Is_Swaption(trade):
        maxDate = acm.Time.DateAddDelta(trade.Instrument().ExpiryDate(), 0, 0, -5)
    else:
        maxDate = acm.Time.DateAddDelta(trade.Instrument().Underlying().ExpiryDate(), 0, 0, -5)
    dates = acm.FArray()
    tempArray = acm.FArray()
    tempArray.Add(adjustedDate)
    dates.Add(tempArray)
    
    while adjustedDate < maxDate:
        adjustedDate = acm.Time.DateAddDelta(adjustedDate, 1, 0, 0)
        if adjustedDate < maxDate:
            tempArray = acm.FArray()
            tempArray.Add(adjustedDate)
            dates.Add(tempArray)
    return dates

def __Get_Calendar_Trade(instrument):
    cal = acm.FArray()
    for l in instrument.Legs():
        leg_cal = __Get_Calendar(l)
        for i in leg_cal:
            if i not in cal:
                cal.Add(i)
    return cal
    
def Get_Calendar_Trade(trade):
    if Get_Is_Commodity(trade):
        cal = acm.FArray()
        cal.Add(acm.FCalendar['ZAR Johannesburg'])
        return cal
    elif Is_Swaption(trade):
        instrument = trade.Instrument().Underlying()
        cal = __Get_Calendar_Trade(instrument)
        #if Is_LIBOR_Linked(instrument):
        #    cal = Add_GBP_London(cal)
    else:
        instrument = trade.Instrument()
        cal = __Get_Calendar_Trade(instrument)
        #if Is_LIBOR_Linked(trade):
        #    cal = Add_GBP_London(cal)
    return cal

def Get_Is_Commodity(object):
    trade = Get_Confirmation().Trade()
    if trade.Instrument().InsType() in ('Curr', 'Deposit'):
        if Get_Und_Comm_Type(trade.Instrument()):
            return 'Yes'
    elif trade.Instrument().InsType() in ('Option', 'Future/Forward'):
        if Get_Und_Comm_Type(trade.Instrument().Underlying()):
            return 'Yes'
    else:
        return ''

def Get_Calendar_Trade_London(trade):
    cal = __Get_Calendar_Trade(trade.Instrument())
    
    if (trade.Instrument().Currency().Name() in ('CHF', 'CZK', 'EUR', 'HUF', 'ILS', 'PLN', 'TRY', 'ZAR')):
        cal = Add_GBP_London(cal)
        
    if (trade.Instrument().Currency().Name() in ('CAD', 'USD', 'JPY')):
        if Is_LIBOR_Linked(trade):
            cal = Add_GBP_London(cal)
            
    if (trade.Instrument().Currency().Name() in ('NZD')):
        wellCal = acm.FCalendar['NZD Wellington']
        if not wellCal in cal:
            cal.Add(wellCal)
            
    if (trade.Instrument().Currency().Name() in ('MYR')):
        singCal = acm.FCalendar['SGD Singapore']
        if not singCal in cal:
            cal.Add(singCal)
        
    return cal

#Anwar ISDA Exercise
def Get_Calendar_ISDA(trade):
    cal = acm.FArray()
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        ISDACalendars = matrix[ISDA_EXERCISE_BUSINESS_DAYS]
        for item in ISDACalendars:
            cal.Add(item)
        return cal
    else:
        return None

def Get_Valuation_Calendar_ISDA(trade):
    cal = acm.FArray()
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        ISDACalendars = matrix[ISDA_SETTLE_VALUATION_BUSINESS_DAYS]
        for item in ISDACalendars:
            cal.Add(item)
        return cal
    else:
        return None
        
def Get_Exercise_Calendar_ISDA(trade):
    cal = acm.FArray()
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        ISDACalendars = matrix[ISDA_SETTLE_EXERCISE_BUSINESS_DAYS]
        for item in ISDACalendars:
            cal.Add(item)
        return cal
    else:
        return None

def Get_Calendar_Payment(payment):
    return Get_Calendar_Trade(payment.Trade())
    
def __ISDA_Libor_Exceptions(currencies, trade):
    instrument = trade.Instrument()
    if instrument.InsType() == 'CurrSwap':
        if 'USD' in currencies:
            if 'EUR' in currencies:
                return Is_LIBOR_Linked(instrument.Legs()[currencies.IndexOfFirstEqual('EUR')])
    elif Is_Swaption(instrument):
        if currencies in ('CAD', 'USD', 'EUR', 'AUD', 'JPY'):
            return Is_LIBOR_Linked(trade.Instrument().Underlying())
    else:
        if currencies in ('CAD', 'USD', 'EUR', 'JPY'):
            return Is_LIBOR_Linked(trade)
    return False
    

#Anwar Here
def __Get_ISDA_MATRIX(trade):
    instrument = trade.Instrument()
    if instrument.InsType() == 'CurrSwap':
        currencies = acm.FArray()
        for l in instrument.Legs():
            currencies.Add(l.Currency().Name())
        LIBORLinked = __ISDA_Libor_Exceptions(currencies, trade)
        try:
            key = currencies[0] + '/' + currencies[1]            
            if LIBORLinked:
                key = key + '/LIBOR'
            return ISDA_CCS_MATRIX[key]
        except:
            try:
                key = currencies[1] + '/' + currencies[0]
                if LIBORLinked:
                    key = key + '/LIBOR'
                return ISDA_CCS_MATRIX[key]
            except:
                print 'No ISDA definition for trade in cross currency swap:', currencies.AsString()
                return None
    elif Is_Swaption(instrument):
        try:
            key = trade.Instrument().Currency().Name()
            if __ISDA_Libor_Exceptions(key, trade):
                key = key + '/LIBOR'
            return ISDA_SWAPTION_MATRIX[key]
        except:
            print 'No ISDA definition for trade in currency: ', trade.Instrument().Currency().Name()
            return None
    elif instrument.InsType() == 'Curr':
        try:
            key = trade.Currency().Name()
            if __ISDA_Libor_Exceptions(key, trade):
                key = key + '/LIBOR'
            return ISDA_VANILLA_MATRIX[key]
        except:
            print 'No ISDA definition for trade in currency: ', trade.Instrument().Currency().Name()
            return None
    else:
        try:
            key = trade.Instrument().Currency().Name()
            if __ISDA_Libor_Exceptions(key, trade):
                key = key + '/LIBOR'
            return ISDA_VANILLA_MATRIX[key]
        except:
            print 'No ISDA definition for trade in currency: ', trade.Instrument().Currency().Name()
            return None
        
def Get_Calendar_Instr_ExerciseTime(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        return matrix[ISDA_BUSINESS_CENTRE]
    else:
        return None
        
def Get_Latest_ExerciseTime(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        return matrix[ISDA_LATEST]
    else:
        return None
        
def Get_Expiration_ExerciseTime(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        return matrix[ISDA_EXERCISE]
    else:
        return None

def Get_Earliest_ExerciseTime(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        return matrix[ISDA_EARLIEST]
    else:
        return None

def Get_Settlement_Currency(trade):
    trade = Get_Confirmation().Trade()
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        return matrix[ISDA_EXERCISE_CURR]
    else:
        return None

def Get_Cashsettlement_Period(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        return matrix[ISDA_CSPD_OFFSET]
    else:
        return -2
        
def Get_Swaption_CSPD(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        return matrix[ISDA_CASH_SETTLE_PD]
    else:
        return -2

#def Get_Calendar_Instr(trade):
#    cal_name = Get_Calendar_Map(trade.Instrument().Currency().Calendar())
#    return cal_name

def Get_Buy_Or_Sell(leg):
    trade = Get_Confirmation().Trade()
    if trade.Quantity() < 0:
        return 'Sell'
    return 'Buy'

def Convert_Strike_CF_Object(object):
    if object.RecordType() == 'CashFlow':
        return Convert_Strike_CF(object)
    return Convert_Strike_CF(object.CashFlow())
    
def Convert_Strike_CF(cf):
    strike = cf.Leg().StrikePrice()/100
    return strike

def Get_First_CF_PayDate(leg):
    first_cf = Get_First_Or_Last_CF(leg, 'PayDate', True)
    if first_cf:
        return first_cf.PayDate()
    return None

def Get_CF_PayOrReceive(cf):
    trade = Get_Confirmation().Trade()
    projected = Get_CashFlow_Nominal(cf)
    if trade.Quantity() * projected < 0:
        return 'Pay'
    return 'Receive'
    
def Get_All_Interest_CF_CurrSwap(leg):
    if leg.Instrument().InsType() == 'CurrSwap':
        confirmation = Get_Confirmation()
        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
        cashFlowQuery.AddAttrNode('PayDate', 'GREATER', confirmation.Trade().ValueDay())
        cashFlowType = cashFlowQuery.AddOpNode('OR')
        cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Float Rate'))
        cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Fixed Rate'))
        cashFlows = cashFlowQuery.Select().SortByProperty('PayDate', True) # The last argument is "ascending"
        if cashFlows:
            return cashFlows[0]
    return None

def Get_All_Fixed_Amount_CurrSwap(leg):
    if leg.Instrument().InsType() == 'CurrSwap':
        cashflows = Get_All_Fixed_Amount(leg)
        if cashflows:
            first_and_last_CF = acm.FArray()
            first_cf = cashflows[0]
            if (not first_cf.StartDate()) and (not first_cf.EndDate()):
                nominalAmount = Get_CashFlow_Nominal_Amount(first_cf)
                if float(nominalAmount):
                    first_and_last_CF.Add(first_cf)
                    
            if len(cashflows) > 1:                
                last_cf = cashflows[len(cashflows)-1]
                if (not last_cf.StartDate()) and (not last_cf.EndDate()):
                    nominalAmount = Get_CashFlow_Nominal_Amount(last_cf)
                    if float(nominalAmount):
                        first_and_last_CF.Add(last_cf)
            return first_and_last_CF

    return None

def Get_PrincipalExchangeType(cf):
    cfs = Get_All_Fixed_Amount_CurrSwap(cf.Leg())
    if cf.Oid() == cfs[0].Oid() and cf.Leg().NominalAtStart():
        return 'InitialExchange'
    return 'FinalExchange'
    
def Is_CurrSwap(leg):
    if leg.Instrument().InsType() == 'CurrSwap' and leg.NominalScaling() == 'FX':
        return leg
    return None

def Get_Calendar_Instr_From_Leg(leg):
    cal_name = Get_Calendar_Map(leg.Instrument().Currency().Calendar())
    return cal_name

def Get_CapFloor_EffectiveDate(leg):
    if leg.ExcludeFirstPeriod():
        return Get_First_Or_Last_CF(leg, 'PayDate', True).StartDate()
    return Get_UnadjustedDate(leg)

def Get_Leg_StartDate(leg):
    if leg.StartDate():
        return ael.date(leg.StartDate()).to_string('%Y-%m-%d')
    return ""

def Get_Leg_EndDate(leg):
    if leg.EndDate():
        return ael.date(leg.EndDate()).to_string('%Y-%m-%d')
    return ""

def Get_CF_PayDate(cf):
    if cf.PayDate():
        return ael.date(cf.PayDate()).to_string('%Y-%m-%d')
    return ""

def Is_CF_PayDate(cf):
    if Get_CF_PayDate(cf):
        return cf
    return None

def Get_CF_Reset_StartDate(object):
    if object.RecordType() == 'CashFlow':
        return Get_CF_StartDate(object)
    return Get_Reset_StartDate(object)

def Get_CF_StartDate(cf):
    if cf.StartDate():
        return ael.date(cf.StartDate()).to_string('%Y-%m-%d')
    return ""

def Get_Reset_StartDate(reset):
    if reset.StartDate():
        return ael.date(reset.StartDate()).to_string('%Y-%m-%d')
    return ""

def Get_CF_Reset_EndDate(object):
    if object.RecordType() == 'CashFlow':
        return Get_CF_EndDate(object)
    return Get_Reset_EndDate(object)
    
def Get_CF_EndDate(cf):
    if cf.EndDate():
        return ael.date(cf.EndDate()).to_string('%Y-%m-%d')
    return ""

def Get_Reset_EndDate(reset):
    if reset.EndDate():
        return ael.date(reset.EndDate()).to_string('%Y-%m-%d')
    return ""

def Get_Payment_PayDate(payment):
    if payment.PayDay():
        return ael.date(payment.PayDay()).to_string('%Y-%m-%d')
    return ""

def Get_Trade_Status(trade):
    confirmation = Get_Confirmation()
    event = Get_Event_Name(confirmation)
    if event in ('New', 'Amendment'):
        return 'Active'
    elif event == 'Cancellation':
        return 'Cancelled'
    elif event in ('FullTermination', 'PartialTermination'):
        return 'Terminated'
    return 'Active'

def Get_Pay_Offset_Count(leg):
    return leg.PayOffsetCount()
    
def Get_Pay_Offset_Unit(leg):
    if Get_Pay_Offset_Count(leg) == 0:
        return 'D'
    return leg.PayOffsetUnit()[0]

def Get_Rate_Observation(cf):
    for r in cf.Resets():
        if r.Day():
            return ael.date(r.Day()).to_string('%Y-%m-%d')
    return None

def Get_Rate_Observation_Reset(reset):
    if reset.Day():
        return ael.date(reset.Day()).to_string('%Y-%m-%d')
    return None

def Is_FirstRegularPeriodStartDate(leg):
    cf = Get_Stub_Period_Object(leg)
    if cf:
        first_cf = Get_First_Or_Last_CF(leg, 'EndDate', True)
        if first_cf:
            for c in cf:
                if c.Oid() == first_cf.Oid():
                    stub = Get_Stub_Period_Type(c)
                    if stub.__contains__('Initial'):
                        all_interest = Get_All_Interest(leg)
                        return all_interest[1]
    return None

def Is_FinalRegularPeriodEndDate(leg):
    cf = Get_Stub_Period_Object(leg)
    if cf:
        last_cf = Get_First_Or_Last_CF(leg, 'EndDate', False)
        if last_cf:
            for c in cf:
                if c.Oid() == last_cf.Oid():
                    stub = Get_Stub_Period_Type(c)
                    if stub.__contains__('Final'):
                        all_interest = Get_All_Interest(leg)
                        return all_interest[len(all_interest)-2]
    return None

def Is_Initial_Index_Level(leg):
    if leg.InitialIndexValue() != 0:
        return leg
    return None

def Is_Premium_On_Trade(trade):
    if not Is_Swaption(trade):
        if trade.Premium() != 0:
            return trade
    return None

def Get_Premium_PayOrReceive(trade):
    if trade.Premium() < 0:
        return 'Pay'
    return 'Receive'

def Get_Value_Date(object):
    trade = Get_Confirmation().Trade()
    if trade.ValueDay():
        return ael.date(trade.ValueDay()).to_string('%Y-%m-%d')
    return None

def Get_Pay_Day_Method_Trade(trade):
    for l in trade.Instrument().Legs():
        return Get_Leg_PayDayMethod(l)
    return 'NotApplicable'

def Get_Premium_Amount(trade):
    premium = ('%.2f' % (abs(trade.Premium())))
    return premium

def Get_Payment_Amount(payment):
    amount = ('%.2f' % (abs(payment.Amount())))
    return amount

def Get_Payment_Type(payment):
    paymentType = payment.Type()
    if paymentType == 'Premium':
        if payment.Trade().Instrument().InsType() in ('Cap', 'Floor'):
            if Is_Premium_On_Trade:
                return 'Fee'
            else:
                payments = Get_Premium_Payments(payment.Trade())
                for p in payments:
                    if p.Type == 'Premium':
                        if p.PayDay() < payment.PayDay():
                            return 'Fee'
                return 'Premium'
        return 'Fee'
    elif paymentType == 'Termination Fee':
        return 'TerminationFee'
    return 'Fee'

def Get_CashPriceMethod(trade):
    curr = acm.FArray()
    curr.Add(trade.Currency().Name())
    curr.Add(trade.Instrument().Currency().Name())
    for l in trade.Instrument().Legs():
        curr.Add(l.Currency().Name())
    if trade.Instrument().InsType() <> 'CurrSwap':        
        if 'JPY' in curr:
            return None
    return trade

def Get_zeroCouponYieldAdjustedMethod(trade):
    is_CashPriceMethod = Get_CashPriceMethod(trade)
    if is_CashPriceMethod:
        return None
    return trade

def Get_Premium_Type(trade):
    if trade.Instrument().InsType() in ('Cap', 'Floor'):
        return 'Premium'
    elif Is_CapletFloorlet(trade):
        return 'Premium'
    return 'Fee'

def Is_Compounding_Leg(leg):
    for c in leg.CashFlows():
        compounding = Is_Compounding_CF(c)
        if compounding == 'true':
            return True
    return False

def Get_All_Resets(leg):
    confirmation = Get_Confirmation()
    reset = acm.FArray()
    interest_cf = Get_All_Interest(leg)
    for c in interest_cf:
        if c.PayDate() > confirmation.Trade().ValueDay():
            for r in c.Resets():
                if r.ResetType() != 'Nominal Scaling':
                    reset.Add(r)
    reset.SortByProperty('Day', True)
    return reset

def Get_PaymentCalculationPeriod(leg):
    if Is_Compounding_Leg(leg):
        return Get_All_Resets(leg)
    return Get_All_Interest(leg)

def Get_AdjustedValueDate(object):
    if object.RecordType() == 'CashFlow':
        return Get_CF_PayDate(object)
    if ael.date(object.EndDate()) == ael.date(object.CashFlow().EndDate()):
        return Get_Reset_EndDate(object)
    return None

def Is_AdjustedValueDate(object):
    if Get_AdjustedValueDate(object):
        return object
    return None

def Get_CompoundingMethod(leg):
    resType = leg.ResetType()
    resetMap = {'None':'None','Single':'None','Weighted':'Straight','Unweighted':'Straight','Compound':'Straight','Flat Compound':'Flat','Assertive':'None','Estimate':'None','Return':'None','Nominal Scaling':'None','Weighted 1m Compound':'Straight','Weighted Average Compound':'Straight','Accretive':'None','Simple Overnight':'None','Daily Return':'None'}
    if resetMap.has_key(resType):
        return resetMap[resType]
    return 'None'

def Get_InterpolationMethod(leg):
    dayCountMethod = leg.DayCountMethod()
    if dayCountMethod.__contains__('360'):
        return 'American'
    return 'European'

def Is_PartialTermination(confirmation):
    if confirmation.Trade().add_info('NovationTermination') == 'PartialTermination' and confirmation.EventChlItem().Name() == 'New Trade':
        return confirmation
    return None

def Get_Legs_Conf(confirmation):
    return confirmation.Trade().Instrument().Legs()

def Get_partialTerminationAmount(leg):
    nominalShift = 0
    trade = Get_Confirmation().Trade()
    if trade.Contract():
        if trade.Contract().Oid() != trade.Oid():
            nominalShift = ('%.2f' % (abs(trade.Contract().Nominal()) - abs(trade.Nominal())))
    return nominalShift

def Is_SalesPersonID(trade):
    salesPersonReview = trade.add_info('SalesPersonReview')
    if salesPersonReview  != '':
        return trade
    return None

def Get_Is_SalesPersonID(trade):
    return trade.add_info('SalesPersonReview')

def Is_Averaging(leg):
    if leg.FloatRateReference():
        if leg.FloatRateReference().Name() in ('ZAR-PRIME-AVERAGE', 'ZAR-PRIME-AVERAGE-Reference Banks', 'ZAR-PRIME', 'ZAR-PRIME-1M', 'ZAR-PRIME-3M'):
            return leg
    return None

def Get_AveragingMethodology(leg):
    if leg.ResetType() == 'Weighted':
        return 'Weighted'
    return 'Unweighted'

def Convert_Reset_Rate(reset):
    rate = reset.FixingValue()/100
    return rate

def Get_ConfInstr_CP_SDSID(trade):
    confirmation = Get_Confirmation()
    party = confirmation.ConfInstruction().Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()
    return party

def Is_LIBOR_Linked(object):
    if object.RecordType() == 'Trade':
        for l in object.Instrument().Legs():
            if l.FloatRateReference():
                if 'LIBOR' in l.FloatRateReference().Name():
                    return True
    elif object.RecordType() == 'Leg':
        if object.FloatRateReference():
            if 'LIBOR' in object.FloatRateReference().Name():
                    return True
    elif object.RecordType() == 'Instrument':
        for l in object.Legs():
            if l.FloatRateReference():
                if 'LIBOR' in l.FloatRateReference().Name():
                    return True
    return False

def Add_GBP_London(array):
    londonCal = acm.FCalendar['GBP London']
    if not londonCal in array:
        array.Add(londonCal)
    return array
    
def Get_OperationsDocument(object):
    return ABSADataContainer.GetDocument().Oid()

def Is_ZAR_PRIME_Rate(leg):
    if leg.FloatRateReference():
        list = ['ZAR-PRIME-AVERAGE', 'ZAR-PRIME']
        if leg.FloatRateReference():
            if leg.FloatRateReference().Name() in list:
                return leg
    return None
    
def Get_UnadjustedDate(leg):
    confirmation = Get_Confirmation()
    cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
    cashFlowQuery.AddAttrNode('PayDate', 'GREATER', confirmation.Trade().ValueDay())
    cashFlowType = cashFlowQuery.AddOpNode('OR')
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Fixed Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Float Rate'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Caplet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Floorlet'))
    cashFlowType.AddAttrNode('CashFlowType', 'EQUAL', Utils.GetEnum('CashFlowType', 'Digital Floorlet'))
    cashFlows = cashFlowQuery.Select().SortByProperty('PayDate', True) # The last argument is "ascending"
    if cashFlows:
        return cashFlows[0].StartDate()
    return None

def Get_Trade_Buy_Or_Sell(trade):
    if trade.Quantity() < 0:
        return 'Sell'
    return 'Buy'

def Get_CashSettle(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        if matrix[ISDA_CASH_SETTLE_METHOD] == 'Cash':
            val = acm.FArray()
            val.Add(matrix[ISDA_CASH_SETTLE_RATE])
            return val
        else:
            return None
    else:
        return None
        
def Get_ParYieldCurveUnadjustedSettle(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        if matrix[ISDA_CASH_SETTLE_METHOD] == 'ParYieldCurveUnadjusted':
            return trade
    return None

def Get_ZeroCouponYieldSettle(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        if matrix[ISDA_CASH_SETTLE_METHOD] == 'ZeroCouponYield':
            return trade
    return None
        
def Get_ISDA_Source(obj):
    trade = Get_Confirmation().Trade()
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        if matrix[ISDA_CASH_SETTLE_RATE] != 'Reference Banks':
            return trade
    return None

def Get_Ref_Banks(obj):
    trade = Get_Confirmation().Trade()
    matrix = __Get_ISDA_MATRIX(trade)
    if matrix:
        if matrix[ISDA_CASH_SETTLE_RATE] == 'Reference Banks':
            return trade
    return None

def Get_SettlementType(trade):
    if trade.Instrument().SettlementType() == 'Physical Delivery':
        return 'Physical'
    else:
        return trade.Instrument().SettlementType()

'''
def Get_SwaptionUnadjustedDate(trade):
    ins = trade.Instrument()
    DaysAdj = int(Get_Cashsettlement_Period(trade))
    curr = ael.Instrument[ins.Currency().Name()]
    exp = ins.ExpiryDate()[:10]
    try:
        return str(acm.Time.DateAddDelta(ael.date(exp).add_banking_day(curr,DaysAdj),0,0,0))
    except:
        return '1900-01-01'
'''
    
def Get_Ins_Expiration(trade):
    ins = trade.Instrument()
    return ins.ExpiryDate()[:10]
    
def Get_Ins_Expiration_DayOfWeek(trade):
    return (acm.Time().DayOfWeek(Get_Ins_Expiration(trade))[0:3]).upper()
        
def GetLegs(trade):
    LegArray = acm.FArray()
    instype = trade.Instrument().InsType()
    if instype == 'Option':
        for l in trade.Instrument().Underlying().Legs():
            LegArray.Add(l)
        return LegArray
    else:
        for l in trade.Instrument().Legs():
            LegArray.Add(l)
        return LegArray

def Get_IsCash(trade):
    if Get_SettlementType(trade) == 'Cash':
        return trade
    else:
        return None
        
def Get_Option_Exercise_Style(trade):    
    if trade.Instrument().ExerciseType() == 'Bermudan':
        return 'Bermuda'
    return trade.Instrument().ExerciseType()
    
def Is_Option_Bermuda_Exercise(trade):
    style = Get_Option_Exercise_Style(trade)
    if style == 'Bermuda':
        return trade
    return None
    
def Is_Option_European_Exercise(trade):
    style = Get_Option_Exercise_Style(trade)
    if style != 'Bermuda':
        return trade
    return None
    
def Is_Cap(leg):
    trade = Get_Confirmation().Trade()
    if trade.Instrument().InsType() == 'Cap':
        return leg
    elif Is_Caplet(trade):
        return leg
    return None
    
def Is_Floor(leg):
    trade = Get_Confirmation().Trade()
    if trade.Instrument().InsType() == 'Floor':
        return leg
    elif Is_CapletFloorlet(trade):
        if not Is_Caplet(trade):
            return leg   
    return None

def Is_Caplet(object):
    if Is_CapletFloorlet(object):
        if object.Instrument().IsCallOption():
            return True
    return False

def Is_Swaption(object):
    if object.Instrument().InsType() == 'Option':
        if object.Instrument().UnderlyingType() == 'Swap':
            return True
    return False

def Is_CapletFloorlet(object):
    if object.Instrument().InsType() == 'Option':
        if object.Instrument().UnderlyingType() == 'FRA':
            return True
    return False

def Convert_Strike(leg):
    trade = Get_Confirmation().Trade()
    if Is_CapletFloorlet(trade):
        strike = Convert_Fixed_Rate(leg)
    else:
        strike = leg.StrikePrice()/100
    return strike
    
def Is_NewFromExercise(trade):
    ContractRef = trade.ContractTrdnbr()
    if ContractRef:
        ALL_LIVE_TRADES_TF = 'SAOps_IRD_Trades'
        IRD_TRADES = acm.FTradeSelection[ALL_LIVE_TRADES_TF]
        for t in IRD_TRADES.Trades():
            if Is_Swaption(t) or Is_CapletFloorlet(t):
                if t.Oid() == ContractRef:
                    if t.Type() == 'Normal':
                        return True
    return False
    
def Get_FRA_Discounting(trade):
    trade = Get_Confirmation().Trade()
    if Is_CapletFloorlet(trade):
        return trade
    return None
    
def Get_FallBackExerc(trade):
    matrix = __Get_ISDA_MATRIX(trade)
    Arr = acm.FArray()
    if Get_SettlementType(trade) == 'Physical':
        Arr.Add('true')
        return Arr
    else:
        if matrix:
            if matrix[ISDA_CASH_SETTLED_FALLBACK] == 'Fallback Exercise':
                Arr.Add('true')
                return Arr
    return None
    
def Get_AutomaticExerc(trade):
    Arr = acm.FArray()
    if Get_FallBackExerc(trade):
        return None
    else:
        Arr.Add('true')
        return Arr

def Get_Barcap_BTB(trade):
    if trade.add_info('Barcap BTB') == '':
        return 0.0
    else:
        return str(abs(int(trade.add_info('Barcap BTB'))))

def CallOrPut(trade):
    ins = trade.Instrument()
    if ins.IsCallOption():
        return 'Call'
    return 'Put'
    
def Get_Ins_StrikePrice(trade):
    ins = trade.Instrument()
    return ins.StrikePrice()
    
def Get_Ins_StartDate(trade):
    ins = trade.Instrument()
    return ins.StartDate()
    
def Get_Trd_Nominal(object):
    trade = Get_Confirmation().Trade()
    return abs(trade.Nominal())

def Get_Trd_Price(object):
    trade = Get_Confirmation().Trade()
    return trade.Price()

def Get_Trade_Quantity(object):
    trade = Get_Confirmation().Trade()
    return abs(trade.Quantity())

def Get_Trade_Currency(trade):
    return trade.Currency().Name()

def Get_Ins_SettleDays(trade):
    ins = trade.Instrument()
    return ins.PayDayOffset()

def Get_Premium_BuyOrSell(trade):
    if trade.Premium() < 0:
        return 'Buy'
    return 'Sell'
    
def Start_Cash(trade):
    try:
        calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
        Calc = calc_space.CalculateValue(trade, 'StartCash')
        return str(abs(round(Calc, 2)))
    except:
        return '0'

def End_Cash(trade):
    try:
        calc_space  = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
        Calc = calc_space.CalculateValue(trade, 'End Cash')
        return str(abs(round(Calc, 2)))
    except:
        return '0'

def Get_CurrPair(trade):
    return trade.Instrument().Currency().Name() + '.' + trade.Currency().Name()

def Get_SpotOffSet(trade):
    try:
        SpotOffSet = trade.Instrument().SpotBankingDaysOffset()
        '''
        if SpotOffSet == 1:
            return 'First'
        elif SpotOffSet == 2:
            return 'Second'
        elif SpotOffSet == 3:
            return 'Third'
        elif SpotOffSet == 4:
            return 'Fourth'
        elif SpotOffSet == 5:
            return 'Fifth'
        elif SpotOffSet == 6:
            return 'Sixth'
        elif SpotOffSet == 7:
            return 'Seventh'
        elif SpotOffSet == 8:
            return 'Eighth'
        elif SpotOffSet == 9:
            return 'Ninth'
        elif SpotOffSet == 10:
            return 'Tenth'
        else:
            return str(SpotOffSet)
        '''
        return str(SpotOffSet)
    except:
        return '0'

def LoopTwice(trade):
    #trade = Get_Confirmation().Trade()
    TrdArray = acm.FArray()
    TrdArray.Add(trade)
    TrdArray.Add(trade)
    #LoopTwice = [trade,trade]
    return TrdArray
    
def Get_Day_Count_Method_All(leg):
    try:
        return leg.DayCountMethod()
    except:
        return None
        
def Get_CommOption_Leg_Fixed(trade):
    Legs = GetLegs(trade)
    LegArray = acm.FArray()
    for l in Legs:
        if l.LegType() == 'Fixed':
            LegArray.Add(l)
    return LegArray

def Get_CommOption_Leg_Float(trade):
    Legs = GetLegs(trade)
    LegArray = acm.FArray()
    for l in Legs:
        if l.LegType() == 'Float':
            LegArray.Add(l)
    return LegArray

def Get_Und_Comm_Type(object):
    if object.RecordType() != 'Instrument':
        ins = object.Instrument()
    else:
        ins = object
    try:
        #PreciousMetal = ['XAU':'Gold','SILVER':'Silver','GOLD':'Gold','Gold':'Gold','XAG':'Silver','XPT':'Platinum','XPD':'Palladium']
        #BaseMetal = ['MAL','MCU','MPB','MNI','MSN','MZN']
        #Energy = ['WTI','BRT','GO_','GAS_OIL','Sing180FO']
        for i in ISDA_COMMODITY_MATRIX:
            if i in ins.Name():
                return ISDA_COMMODITY_MATRIX[i][ISDA_COMM_TYPE]
    except:
        return 'No ISDA definition for instrument: ', ins.Name()
    
def Get_Und_Comm_Unit(trade):
    ins = trade.Instrument()
    #Barrels = ['WTI','BRT']
    #MetricTons = ['GO_','GAS_OIL','Sing180FO']
    try:
        for i in ISDA_COMMODITY_MATRIX:
            if i in ins.Name():
                return ISDA_COMMODITY_MATRIX[i][ISDA_COMM_UNIT]
    except:
        return 'No ISDA definition for instrument: ', ins.Name()
        
def Get_Und_Comm_Name(trade):
    ins = trade.Instrument()
    try:
        for i in ISDA_COMMODITY_MATRIX:
            if i in ins.Name():
                return ISDA_COMMODITY_MATRIX[i][ISDA_COMM_NAME]
    except:
        return 'No ISDA definition for instrument: ', ins.Name()
