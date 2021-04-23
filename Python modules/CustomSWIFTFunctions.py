'''CustomSWIFTFunctions : last updated on Wed Apr 06 11:39:43 2016. '''
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CustomSWIFTFunctions
PURPOSE                 :       The modules has functions to populate tasgs in custom SWIFT messages
DEPARTMENT AND DESK     :       Operations
REQUESTER               :       Linda Breytenbach
DEVELOPER               :       Manan Ghosh
CR NUMBER               :       CHNG0003744247 (2016-08-19)
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no           Developer               Description
-------------------------------------------------------------------------------------------------------------
2016-08-23      CHNG0003898744      Manan Ghosh             Changed to use prod header settings
2017-08-28                          Willie vd Bank          Updated CashFlowBase input parameters and
                                                            added demat config lookup to MESSAGE_USER_REFERENCE
                                                            as part of 2017 upgrade
2017-12-11      CHNG0005220511      Manan Ghosh             DIS go-live
2017-12-13      CHNG0005233100      Willie vd Bank          Modified COUPON_PERIOD to return different values for DIS 
                                                            and Demat
2020-07-27      FAOPS-780           Ntokozo Skosana         Added functionality to support combination instruments
2020-09-02      FAOPS-881/883       Tawanda Mukhalela       Added support for Redemption Confirmations
2021-01-27      FAOPS-899           Joshua Mvelase          Modified INTERNAL_TRADE_REFERENCE to cater for Demat ID
                                                            confirmations unique ID
2021-04-12      FAOPS-1136          Metse Moshobane         changed the MT564's :92A::INTR// tag to use Forwd rate 
                                                            (float rate + spread) 

-------------------------------------------------------------------------------------------------------------
'''

import acm
from datetime import datetime
from at_time import acm_date, to_date
import time
import demat_isin_mgmt_menex
from demat_functions import MM_EVENT_NEW_TRADE, MM_EVENT_MATCH_REQUEST, MM_EVENT_MATCH_PRESETTLE, DEMAT_TRADER_CSD_BPID, _struct_note_desk_trade
from math import fabs
from gen_absa_xml_config_settings import AbsaXmlConfigSettings
from demat_functions import GetFirstTrade
import re
import FSwiftParameters as Global
import FSwiftMTBase
import FSwiftMTConfirmation
import demat_config
from DocumentConfirmationGeneral import get_confirmation_redemption_event, get_confirmation_to_date


INTEREST                    = 'INTR'
REDEMPTION                  = 'REDM'

TODAY = acm.Time().DateToday()
TODAY = datetime.strptime(TODAY, '%Y-%m-%d').strftime('%Y-%m-%d')

config = AbsaXmlConfigSettings()
DAYS_IN_YEAR = 365.0


def IS_DIS(fobj):
    if fobj.IsKindOf(acm.FConfirmation) or fobj.IsKindOf(acm.FSettlement):
        trd = fobj.Trade()
        ins = trd.Instrument() if trd else None
        if ins:
            return ins.AdditionalInfo().DIS_Instrument()
    return False


def is_demat_interest(settle):

    trd = settle and settle.Trade()
    ins = trd and trd.Instrument()
    instype = ins.InsType()
    demat_interest = (instype == 'CD' and settle.Type() in ['Float Rate', 'Fixed Rate'])
    demat_interest = demat_interest or (instype in ['FRN', 'CLN'] and settle.Type() == 'Float Rate')

    return demat_interest


def calc_space_value(obj, field):

    if obj:
        context = acm.GetDefaultContext()
        calc_space = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')
        top_node = calc_space.InsertItem(obj)

        try:
            calculation = calc_space.CreateCalculation(top_node, field)
            return calculation.Value()
        except Exception, e:
            print 'Error Calculating %s ' % (field), e
            return 0


def formatNumber(number):
    """
    Function to replace '.' with ',' in numbers
    """

    return ','.join(number.split('.')).strip()


def format_number_comma_to_point(number):
    '''
    Function to replace ',' with '.' in numbers
    '''

    return number.replace(',', '.')


def MESSAGE_FUNCTION(confirmation):

    acm_trd = confirmation and confirmation.Trade()
    status = acm_trd and acm_trd.Status()

    if status == 'Void':
        return 'CANC'
    else:
        return 'NEWM'


def CAP_EVNT_MESSAGE_FUNCTION(confirmation):

    return 'NEWM'


def SUB_MESSAGE_TYPE(confirmation):
    '''
    Identifies the sub type of
    confirmation message for MT 598 message
    '''

    if confirmation.CashFlow():
        return '161'

    return '170'


def SENDER_BIC(confirmation):

    absa_swift_param = config.GetUniqueNode('AbcapSwiftParameters')
    absa_bic = config.GetValue(absa_swift_param, 'LogicalTerminalBic', True)
    absa_trd_bic_ext = config.GetValue(absa_swift_param, 'TradeBicExtension', True)#MG2
    absa_ins_bic_ext = config.GetValue(absa_swift_param, 'IsinMgmtBicExtension', True)#MG1
    absa_iss_agnt_bic_ext = config.GetValue(absa_swift_param, 'IssueragentBicExtension', True) #MG1

    acm_trd = confirmation and confirmation.Trade()
    status = acm_trd and acm_trd.Status()
    
    if confirmation.EventType() in [MM_EVENT_MATCH_REQUEST, '%s %s' % (MM_EVENT_MATCH_REQUEST, confirmation.Type())]:
        return absa_bic + absa_trd_bic_ext

    if confirmation.EventType() in [MM_EVENT_MATCH_PRESETTLE, '%s %s' % (MM_EVENT_MATCH_PRESETTLE, confirmation.Type())]:
        if acm_trd.Instrument().AdditionalInfo().Demat_Instrument():
            return absa_bic + absa_ins_bic_ext
        elif acm_trd.Instrument().AdditionalInfo().DIS_Instrument():
            return absa_bic + absa_iss_agnt_bic_ext

    return absa_bic + absa_ins_bic_ext


def RECEIVER_BIC(confirmation):

    strate_swift_param = config.GetUniqueNode('StrateSwiftParameters')
    strate_bic = config.GetValue(strate_swift_param, 'LogicalTerminalBic', True)
    
    return strate_bic


def LINK(confirmation):

    acm_trd = confirmation and confirmation.Trade()
    conf_event_type = '%s %s' % (MM_EVENT_MATCH_REQUEST, confirmation.Type())
    trade_status = acm_trd and acm_trd.Status()

    if confirmation.EventType() == conf_event_type and trade_status == 'Void':
        return 'LINK'

    return ''


def VERSION(confirmation):

    return confirmation.VersionId()


def TRANSACTION_REFERENCE(confirmation):

    acm_trd = None
    trans_ref = '%s-%d-%d'
    conf_no = confirmation.Oid()
    version_id = 1

    return trans_ref % (Global.FAC, conf_no, version_id)


def CATEGORY(confirmation):

    acm_trd = confirmation and confirmation.Trade()
    acm_ins = acm_trd and acm_trd.Instrument()
    acm_leg = acm_ins and acm_ins.Legs() and acm_ins.Legs()[0]
    ins_type = acm_ins and acm_ins.InsType()

    if ins_type == 'FRN' or (ins_type == 'CD' and acm_leg.FixedLeg() is None):
        return 'CATG3'
    elif ins_type == 'CD' and acm_leg.FixedLeg():
        return 'CATG2'
    else:
        return ''


def GENERIC_CATEGORY(confirmation):

    acm_trd = confirmation and confirmation.Trade()
    acm_ins = acm_trd and acm_trd.Instrument()
    acm_leg = acm_ins and acm_ins.Legs() and acm_ins.Legs()[0]
    ins_type = acm_ins and acm_ins.InsType()
    if ins_type == 'FRN' or (ins_type == 'CD' and acm_leg.FixedLeg() is None):
        return '3'
    elif ins_type == 'CD' and acm_leg.FixedLeg():
        return '2'
    else:
        return ''


def PREPARATION_DATETIME(confirmation):
    return '%s' % (datetime.today().strftime('%Y%m%d%H%M%S'))


def MATURITY_DATE(confirmation):
    acm_trd = confirmation.Trade()
    acm_ins = acm_trd and acm_trd.Instrument()  
    return '%s' % (datetime.strptime(acm_ins.ExpiryDate()[0:10], '%Y-%m-%d').strftime('%Y%m%d'))


def ISSUE_DATE(confirmation):
    acm_trd = confirmation.Trade()
    acm_ins = acm_trd and acm_trd.Instrument()  
    return '%s' % (datetime.strptime(acm_ins.StartDate(), '%Y-%m-%d').strftime('%Y%m%d'))


def INTERNAL_TRADE_REFERENCE(confirmation):

    if confirmation:
        Trader_BPID = DEMAT_TRADER_CSD_BPID
        reference_id = confirmation.add_info('Demat_ID')
        reference_id = reference_id if reference_id else confirmation.Oid()
        return '%s/%s' % (Trader_BPID, str(reference_id))

    return ''


def LINK_TRADE_REFERENCE(confirmation):

    if confirmation:
        Trader_BPID = DEMAT_TRADER_CSD_BPID
        return '%s/%s' % (
            Trader_BPID, str(
                confirmation and confirmation.ConfirmationReference() and confirmation.ConfirmationReference().Oid()
            ))

    return ''


def TRADE_DATE(confirmation):
    '''TODO: Confirm is trade Date is the trade creation date. Format the date as well'''
    if confirmation:
        tradeDate = confirmation.Trade().TradeTime()

        '''TODO: Create a function to format the datetime object and move the following functionality to the function'''
        if len(tradeDate) >= 10:
           tradeDate =  datetime.strptime(tradeDate[0:10], '%Y-%m-%d').strftime('%Y%m%d')
           return '%s' % (tradeDate)
    return ''


def SETTLEMENT_DATE(confirmation):

    if confirmation:
        settleDate = confirmation.Trade().ValueDay()
        '''TODO: Create a function to format the datetime object and move the following functionality to the function'''
        if len(settleDate) >=10:
            settleDate = datetime.strptime(settleDate[0:10], '%Y-%m-%d').strftime('%Y%m%d')
            return '%s' % (settleDate)
    return ''


def NEXT_RESET_DATE(confirmation):
    ''' Assumption is there is one reset per cash flow. Also it has been assumed that this is applicable to FRN'''
    nextResetDate = ''
    TODAY = acm.Time().DateToday()
    TODAY = datetime.strptime(TODAY, '%Y-%m-%d').strftime('%Y-%m-%d')

    ins = confirmation and confirmation.Trade() and confirmation.Trade().Instrument()
    if ins and ins.InsType() in ['FRN', 'CD']:
        legs = ins.Legs()
        if legs.Size() == 1 and legs[0].LegType() == 'Float':
            for cashflow in legs[0].CashFlows():
                resetDate = cashflow.Resets().Size() > 0 and cashflow.Resets()[0].Day() or ''

                if resetDate != '' and resetDate > TODAY:
                    if nextResetDate == '':
                        nextResetDate = resetDate
                    if nextResetDate > resetDate:
                        nextResetDate = resetDate

            if len(nextResetDate) >= 10:
                nextResetDate = datetime.strptime(nextResetDate[0:10], '%Y-%m-%d').strftime('%Y%m%d')
                return '%s' % nextResetDate
    return ''


def CURRENT_INTEREST_RATE(confirmation):
    ''' Assumption is there is one reset per cash flow. Also it has been assumed that this is applicable to FRN'''
    ins = confirmation and confirmation.Trade() and confirmation.Trade().Instrument()
    resetRate = 0.0
    if ins and ins.InsType() in ['FRN']:
        legs = ins.Legs()
        if legs.Size() == 1 and legs[0].LegType() == 'Float':
            for cashflow in legs[0].CashFlows():
                if TODAY >= cashflow.StartDate() and TODAY < cashflow.EndDate():
                    resetRate = cashflow.Resets().Size() > 0 and cashflow.Resets()[0].FixingValue() or 0.0
                    resetRateValue = formatNumber('%015.7f' % float(resetRate))

    return '0000000,0000000'


def NEXT_PAYMENT_DATE(confirmation):
    ''' Assumption '''
    ins = confirmation and confirmation.Trade() and confirmation.Trade().Instrument()
    nextPayDate = None
    if ins and ins.InsType() in ['FRN', 'CD']:
        legs = ins.Legs()
        if legs.Size() == 1 and legs[0].LegType() == 'Float':
            for cashflow in legs[0].CashFlows():
                if TODAY >= cashflow.StartDate() and TODAY < cashflow.EndDate():
                    nextPayDate = cashflow.PayDate()  
                    if nextPayDate and len(nextPayDate) >= 10:
                        nextPayDate = datetime.strptime(nextPayDate[0:10], '%Y-%m-%d').strftime('%Y%m%d')
                        return '%s' % nextPayDate
    return ''


def SETTLEMENT_TRANSACTION_TYPE(confirmation):

    trd = confirmation.Trade()
    dvpFlag = trd.AdditionalInfo().Demat_Deliv_vs_Paym()
    deliver_receive = (trd.Quantity() > 0) and 'R' or 'D'
    settle_type = dvpFlag and 'VP' or 'FP'
        
    return 'X%s%s' % (deliver_receive, settle_type)


def RECEIVER_TRADER_CSD_BP_ID(confirmation):

    trd = confirmation.Trade()
    if trd.Quantity() < 0:
        trader_CSD_BP_ID = trd.AdditionalInfo().MM_DEMAT_CP_BPID()
    elif trd.Quantity() > 0:
        trader_CSD_BP_ID = trd.AdditionalInfo().Demat_Acq_BPID()
    else:
        trader_CSD_BP_ID = ''

    return trader_CSD_BP_ID and str(trader_CSD_BP_ID) or ''


def DELIVERY_TRADER_CSD_BP_ID(confirmation):

    trd = confirmation.Trade()
    if trd.Quantity() > 0:
        trader_CSD_BP_ID = trd.AdditionalInfo().MM_DEMAT_CP_BPID()
    elif trd.Quantity() < 0:
        trader_CSD_BP_ID = trd.AdditionalInfo().Demat_Acq_BPID()
    else:
        trader_CSD_BP_ID = ''

    return trader_CSD_BP_ID and str(trader_CSD_BP_ID) or ''


def STRATE_REFERENCE_NUMBER(confirmation):

    trd = confirmation and confirmation.Trade()
    ins = trd and trd.Instrument()
    conf_day = to_date(confirmation.CreateTime())
    Demat_BAN = (trd and trd.AdditionalInfo().MM_DEMAT_BAN()) and trd.AdditionalInfo().MM_DEMAT_BAN() or ''
    Demat_UTRN = (trd and trd.AdditionalInfo().MM_DEMAT_UTRN()) and trd.AdditionalInfo().MM_DEMAT_UTRN() or ''
    Strate_Ref_No_Pre = '%sM%s' % (Demat_BAN, Demat_UTRN)
    Strate_CE_Ref_No = ''    
    settlements = [settle for settle in trd.Settlements()
                   if settle.ValueDay() == conf_day and is_demat_interest(settle)
                   ]
    for settle in settlements:
        cashFlow = settle.CashFlow()
        CE_Reference = cashFlow and cashFlow.AdditionalInfo().Demat_CE_Reference()
        Strate_CE_Ref_No = CE_Reference and CE_Reference or '000000'
    Strate_Ref_No = '%sCEM%s' % (str(conf_day.year), Strate_CE_Ref_No)

    return '%s%s' % (Strate_Ref_No_Pre, Strate_Ref_No)


def CAPITAL_EVENT_REFERENCE(confirmation):

    cash_flow = confirmation.CashFlow()
    if cash_flow:
        capital_event = cash_flow.AdditionalInfo().Demat_CE_Reference()
    else:
        capital_event = _get_payment_linked_to_confirmation(confirmation).Text()

    return str(capital_event)


def RECONCILIATION_DATE(confirmation):

    conf_date = datetime.fromtimestamp(confirmation.CreateTime())
    cashFlow = confirmation.CashFlow()
    if cashFlow:
        return cashFlow.AdditionalInfo().Demat_Record_Date() or conf_date.strftime('%Y%m%d')
    record_date = _get_payment_linked_to_confirmation(confirmation).add_info('REDM_Record_Date')
    return record_date or conf_date.strftime('%Y%m%d')


def COUPON_PERIOD(confirmation):
    """
    Gets the coupon Period
    """
    if _is_redemption_confirmation(confirmation):
        return ''
    cash_flow = confirmation.CashFlow()
    if not cash_flow:
        return _get_payment_linked_to_confirmation(confirmation).add_info('REDM_Coupon_Period')
    end_date = to_date(cash_flow.EndDate())
    if IS_DIS(confirmation):
        end_date = to_date(end_date.strftime('%Y-%m-%d')).strftime('%Y%m%d')
    else:
        end_date = to_date(end_date.strftime('%Y-%m-%d')+'-1d').strftime('%Y%m%d')
    couponPeriod = '%s/%s' % (to_date(cash_flow.StartDate()).strftime('%Y%m%d'), end_date)

    return cash_flow.AdditionalInfo().Demat_Coupon_Period() or couponPeriod


def _is_redemption_confirmation(confirmation):
    """
    Checks if confirmation is a redemption event
    """
    event_type = get_confirmation_redemption_event(confirmation)
    cash_flow = confirmation.CashFlow()
    if event_type in ('PCAL', 'MCAL'):
        return True
    if cash_flow and cash_flow.CashFlowType() == 'Fixed Amount':
        return True

    return False


def DAYS_ACCRUED_INTEREST(confirmation):
    """
    Calculates the Days Accrued for the Coupon Payment
    """
    cash_flow = confirmation.CashFlow()
    if cash_flow is None:
        event_type = get_confirmation_redemption_event(confirmation)
        if event_type == 'INTR':
            coupon_period = _get_payment_linked_to_confirmation(confirmation).add_info('REDM_Coupon_Period')
            return _calculate_interest_days(coupon_period)
        return 0

    coupon_period = cash_flow.AdditionalInfo().Demat_Coupon_Period()
    if coupon_period is None or coupon_period == '':
        return 0

    return _calculate_interest_days(coupon_period)


def _calculate_interest_days(coupon_period):
    """
    Calculate Coupon Period Days
    """
    start_date, end_date = coupon_period.split('/')
    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y%m%d')
    days = abs((end_date - start_date).days) + 1

    return str(days).zfill(3)


def get_spread(confirmation):
    cf = confirmation.CashFlow()
    if cf:
        return cf.Spread()
    else:
        return 0


def COUPON_RATE(confirmation):

    cf = confirmation.CashFlow()
    trade = confirmation.Trade()
    if cf is None or cf.CashFlowType() == 'Fixed Amount':
        event_type = get_confirmation_redemption_event(confirmation)
        if event_type == 'INTR':
            return _get_payment_linked_to_confirmation(confirmation).add_info('REDM_Coupon_Rate')
        return 0.0
    elif trade.Instrument().InsType() == 'Combination':
        resetValue = _get_combination_rate(confirmation, False)
    else:
        resetValue = 0.0
        leg = cf and cf.Leg()
        legtype = leg and leg.LegType() or 'None'
        if legtype == 'Fixed':
            resetValue = leg.FixedRate()
        elif cf:
            resets = [reset for reset in cf.Resets()] or []
            resetValue = len(resets) > 0 and resets[0].FixingValue() or 0.0
            resetValue += get_spread(confirmation)

    return formatNumber('%15.5f' % resetValue)


def format_date(date):

    pay_date = datetime.strptime(date[0:10], '%Y-%m-%d')
    return pay_date.strftime('%Y%m%d')


def get_cashflow(ins, pay_date, cash_flow_event_type):
    '''
    Get the cash flow from the Instrument
    corresponding to the pay date
    '''
    if ins is None:
        return None

    legs = ins.Legs()
    if legs:
        payleg = [leg for leg in legs]
    else:
        payleg = []

    cash_flow_type = _get_cashflow_type(cash_flow_event_type)
    valid_cash_flow = []

    if len(payleg) > 0:
        cash_flows = payleg[0].CashFlows()
        valid_cash_flow = _get_cash_flows_on_pay_day(cash_flows, pay_date, cash_flow_type)
    return len(valid_cash_flow) > 0 and valid_cash_flow[0] or None


def _get_combination_rate(conf, total_rate = True):
    """"
    This function gets the rates for combination instruments.
    If total_rate is set to True, it returns the rate  that is used to calculate the
    coupon.
    If total_rate is set to False, it returns the rate that is displayed on the message.
    """
    sum = 0.0
    trd = conf.Trade()

    pay_date = conf.CashFlow().PayDate()
    pay_date = datetime.strptime(pay_date, '%Y-%m-%d')

    pay_date = format_date(conf.CashFlow().PayDate())
    spread = conf.CashFlow().Spread()
    all_comb_cash_flows = get_combination_cash_flows(trd, pay_date, INTEREST)

    for cf in all_comb_cash_flows:
        if cf.CashFlowType() == 'Fixed Rate':
            fixed_rate = cf.FixedRate()
            break
    calculation_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    forward = conf.CashFlow().Calculation().ForwardRate(calculation_space)

    if total_rate:
        sum = forward + fixed_rate/100
    else:
        sum = forward - spread/100

    return sum*100


def _get_frn_rate(obj):
    """"
    This function gets the rates for FRN instruments booked by the SND.
    If total_rate is set to True, it returns the rate  that is used to calculate the
    coupon.
    If total_rate is set to False, it returns the rate that is displayed on the message.
    """
    sum = 0.0
    rec_leg_fixed_rate = None

    if obj.IsKindOf(acm.FCashFlow):
        cash_flow = obj
        ins = cash_flow.Leg().Instrument()
        trade = GetFirstTrade(ins)
    if obj.IsKindOf(acm.FConfirmation):
        trade = obj.Trade()
        cash_flow = obj.CashFlow()

    calculation_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    forward = cash_flow.Calculation().ForwardRate(calculation_space)
    trx_trade = _get_trx_trades(trade)

    for trade in trx_trade:
        instrument = trade.Instrument()
        if instrument.InsType() in ['CreditDefaultSwap', 'IndexLinkedSwap']:
            rec_leg_fixed_rate = instrument.Legs()[1].FixedRate()
            break
    if rec_leg_fixed_rate is None:
        raise ValueError('Cannot find fixed rate for coupon payment calculation')
    sum = forward + rec_leg_fixed_rate / 100

    return sum * 100


def _get_trans_ref_trade(trade):

    if trade:
        return trade.TrxTrade()


def _get_trx_trades(trade):
    trx_trade = _get_trans_ref_trade(trade)
    if trx_trade:
        return trx_trade.TrxTrades()
    return None


def _struct_notes_frn(trade):
    if not trade.IsKindOf(acm.FTrade):
        return False
    if not _struct_note_desk_trade(trade):
        return False
    instrument = trade.Instrument()
    if instrument.InsType() != 'FRN':
        return False
    return True


def _get_cf_period(conf):
    """
    This function returns the cash flow period for a Fixed Rate cashflow
    on a combination instrument. This value is used to calculate the
    coupon entitlement amount for combination instruments.
    """
    trd = conf.Trade()
    ins = trd.Instrument()
    pay_date = conf.CashFlow().PayDate()
    pay_date = datetime.strptime(pay_date, '%Y-%m-%d')
    cash_flow_event_type = 'INTR'

    pay_date = format_date(conf.CashFlow().PayDate())
    all_comb_cash_flows = get_combination_cash_flows(trd, pay_date, cash_flow_event_type)

    if ins.InsType() == 'Combination':
        for cf in all_comb_cash_flows:
            if cf.CashFlowType() == 'Fixed Rate':
                cash_flow = cf
                break
    else:
        cash_flow = get_cashflow(ins, pay_date, cash_flow_event_type)
    leg = cash_flow.Leg()
    static_leg_info = leg.StaticLegInformation(ins, pay_date, None)
    cf_info = cash_flow.CashFlowInformation(static_leg_info)
    cf_period = cf_info.Period()
    return cf_period


def TOTAL_ELIGIBLE_NOMINAL(fobj):

    if fobj.IsKindOf(acm.FConfirmation) or fobj.IsKindOf(acm.FSettlement):
        trd = fobj.Trade()
        ins = trd.Instrument()
    instrAuthAmount = 0.0
    if ins.AdditionalInfo().Demat_Instrument():
        instrAuthAmount = demat_isin_mgmt_menex.current_ins_issued_amount(ins)
    if ins.AdditionalInfo().DIS_Instrument():
        instrAuthAmount = demat_isin_mgmt_menex.current_ins_authorised_amount(ins)
    authorisedAmount = 0.0
    if type(instrAuthAmount) != str:
        authorisedAmount = instrAuthAmount and float(instrAuthAmount) or 0.0
    
    return formatNumber('%15.2f' % authorisedAmount)


def CREDIT_DEBIT_INDICATOR(confirmation):

    return 'CRED'


def ISIN(confirmation):

    trd = confirmation and confirmation.Trade()
    ins = trd and trd.Instrument()

    return 'ISIN %s' % (ins.Isin() or '')


def PAYMENT_DATE(confirmation):

    cash_flow = confirmation.CashFlow()
    if cash_flow:
        conf_day = to_date(cash_flow.PayDate())
        settle_day = acm_date(conf_day.strftime('%Y-%m-%d'))
        return str(to_date(settle_day).strftime('%Y%m%d'))
    else:
        pay_day = to_date(_get_payment_linked_to_confirmation(confirmation).PayDay())
        payment_date = acm_date(pay_day.strftime('%Y-%m-%d'))
        return str(to_date(payment_date).strftime('%Y%m%d'))


def ENTITLED_COUPON_PAYMENT(fobj):
    instrument = None
    trade = None
    if fobj.IsKindOf(acm.FConfirmation) or fobj.IsKindOf(acm.FSettlement):
        trade = fobj and fobj.Trade()
        cash_flow = fobj and _get_cash_flow(fobj)
        instrument = trade and trade.Instrument()


    if fobj.IsKindOf(acm.FCashFlow):
        cash_flow = fobj
        instrument = cash_flow.Instrument()
    currency = instrument and instrument.Currency().Name() or 'ZAR'
    ins_settlement_value = _get_instrument_settlement_value(instrument, cash_flow, fobj)

    return '%s%s' % (currency, formatNumber('%15.2f' % fabs(ins_settlement_value)))


def _get_cashflow_type(cash_flow_event_type):
    if cash_flow_event_type == INTEREST:
        return ['Coupon', 'Fixed Rate', 'Float Rate']

    if cash_flow_event_type == REDEMPTION:
        return ['Redemption', 'Fixed Amount']
    return None


def get_combination_cash_flows(trd, pay_date, cash_flow_event_type):
    '''
    Get the cash flows from the combination
    instrument that corresponding to the
    pay day
    '''

    cash_flows = []
    cash_flow_type = _get_cashflow_type(cash_flow_event_type)

    for money_flow in trd.MoneyFlows():
        if money_flow.Type() in cash_flow_type and money_flow.SourceObject().IsKindOf(acm.FCashFlow):
            cash_flow = money_flow.SourceObject()
            cash_flows.append(cash_flow)

    return _get_cash_flows_on_pay_day(cash_flows, pay_date, cash_flow_type)


def _get_cash_flows_on_pay_day(cash_flows, pay_date, cash_flow_type):

    if len(cash_flows) > 0:
        ''''
        This section of code checks which cashflow corresponds with payday
        '''
        cal = acm.FCalendar['ZAR Johannesburg']
        pay_date = time.strptime(pay_date, '%Y%m%d')

        if cal.CalendarInformation().IsNonBankingDay(
                acm.Time().DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday)):
            pay_date = cal.CalendarInformation().AdjustBankingDays(
                acm.Time().DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday), 1)
        else:
            pay_date = cal.CalendarInformation().AdjustBankingDays(
                acm.Time().DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday), 0)

        if cash_flows is not None:
            cash_flow = [cf for cf in cash_flows if cf.PayDate() == pay_date and cf.CashFlowType() in cash_flow_type]

    return cash_flow or None


def _get_instrument_settlement_value(ins, cf, obj = None):

    instype = ins and ins.InsType() or ''
    instr_auth_amount = demat_isin_mgmt_menex.current_ins_issued_amount(ins)

    if ins.AdditionalInfo().DIS_Instrument():
        instr_auth_amount = demat_isin_mgmt_menex.current_ins_authorised_amount(ins)

    authorised_amount = 0.0
    ins_settlement_value = 0.0
    cashflow_amount = 0.0
    first_trade = GetFirstTrade(ins)
    quantity = first_trade and first_trade.Quantity() or 1.0
    calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    if type(instr_auth_amount) != str:
        authorised_amount = instr_auth_amount and float(instr_auth_amount) or 0.0
        nominal_amount = _get_nominal_amount(ins)
        confirmation = obj if obj.IsKindOf(acm.FConfirmation) else None
        if confirmation:
            event_type = get_confirmation_redemption_event(confirmation)
            if event_type == 'PCAL':
                amount = _get_partial_redemption_amount(confirmation)
                return amount
            elif event_type == 'MCAL':
                amount = authorised_amount * 1.0
                return amount
            elif event_type == 'INTR':
                amount = _get_partial_redemption_amount(confirmation)
                return amount

        if cf.CashFlowType() in ['Float Rate', 'Fixed Rate']:
            leg = cf.Leg()
            staticLegInfo = leg.StaticLegInformation(ins, acm.Time().DateToday(), None)
            cashflow_amount = cf.Calculation().Projected(calc_space, first_trade).Number()
        elif cf.CashFlowType() == 'Fixed Amount':
            amount = authorised_amount * 1.0
            return amount

    if instype == "Combination":
        cf_period = _get_cf_period(obj)
        cf_rate = _get_combination_rate(obj, True) / 100
        ins_settlement_value = (cf_period*authorised_amount*cf_rate)
    elif first_trade and _struct_notes_frn(first_trade):
        pay_date = cf.PayDate()
        static_leg_info = leg.StaticLegInformation(ins, pay_date, None)
        cf_info = cf.CashFlowInformation(static_leg_info)
        cf_period = cf_info.Period()
        cf_rate = _get_frn_rate(obj) / 100
        ins_settlement_value = (cf_period*authorised_amount*cf_rate)
    else:
        ins_settlement_value = (cashflow_amount * authorised_amount / (nominal_amount * quantity))

    return ins_settlement_value


def _get_partial_redemption_amount(confirmation):
    """
    Gets the partial redemption amount from
    Partial Redemption Payment
    """
    payment = _get_payment_linked_to_confirmation(confirmation)
    return payment.Amount()


def _get_payment_linked_to_confirmation(confirmation):
    """
    Gets applicable payment
    """
    trade = confirmation.Trade()
    event_type = get_confirmation_redemption_event(confirmation)
    pay_date = get_confirmation_to_date(confirmation)
    payments = trade.Payments()
    for payment in payments:
        if to_date(payment.CreateTime()) != to_date(confirmation.CreateTime()):
            continue
        if event_type != payment.add_info('REDM_Type'):
            continue
        if payment.PayDay() != pay_date:
            continue

        return payment

    raise ValueError('Failed to calculate amount. Could Not find Redemption payment')


def ENTITLED_AMOUNT_36B(confirmation):
    """
    Gets formatted ENTITLED_COUPON_PAYMENT for 36B
    """
    formatted_amount = ENTITLED_COUPON_PAYMENT(confirmation)
    coupon_amount = formatted_amount.split('ZAR')[1]

    return coupon_amount


def _get_nominal_amount(ins):
    if ins is None:
        return 0.0
    if ins.InsType() == "Combination":
        first_trade = GetFirstTrade(ins)
        return first_trade.Premium()
    else:
        return ins.NominalAmount()


def _get_cash_flow(fobj):
    trd = fobj.Trade()
    ins = trd.Instrument()
    cash_flow_type = ['Coupon', 'Fixed Rate', 'Float Rate']
    if ins.InsType() == 'Combination':
        for mf in trd.MoneyFlows():
            if mf.Type() in cash_flow_type and mf.SourceObject().IsKindOf(acm.FCashFlow):
                cash_flow = mf.SourceObject()
                return cash_flow
    else:
        return fobj.CashFlow()


def TOTAL_COUPON_PAYMENT(confirmation):

    trd = confirmation.Trade()
    ins = trd.Instrument()
    csd_participant_id = trd.Counterparty().AdditionalInfo().Demat_CSD_Participa() or ''
    currency = ins.Currency().Name() or 'ZAR'
    instype = ins.InsType()
    conf_day = to_date(confirmation.CreateTime())
    settle_day = acm_date(conf_day.strftime('%Y-%m-%d') + '+1d')
    trades = [trade for trade in ins.Trades() if trade.Status() == 'BO-BO Confirmed']
    settlements = []
    settlementValue = 0.0
    for trade in trades:
        trd_csd_participant_id = trade.Counterparty().AdditionalInfo().Demat_CSD_Participa() or ''
        if csd_participant_id == trd_csd_participant_id:
            settlements += [settlement
                            for settlement in trade.Settlements()
                            if settlement.ValueDay() == settle_day and is_demat_interest(settlement)
                            ]

    for settlement in settlements:
        settlementValue += settlement.Amount()

    return '%s%s%s' % (conf_day.strftime('%Y%m%d'), currency, formatNumber('%015.2f' % fabs(settlementValue)))


def PAYEE_BIC(confirmation):
    trd = confirmation.Trade()
    acq = trd.Acquirer()
    acquirer_bic = acq.Swift() or ''
    return acquirer_bic


def BENEFICIARY_BIC(confirmation):
    trd = confirmation.Trade()
    cpy = trd.Counterparty()
    csdPartcipantBIC = cpy.AdditionalInfo().Demat_CSD_Partc_BIC() or ''
    return csdPartcipantBIC


def ISSUER_AGENT_ID(confirmation):

    trd = confirmation and confirmation.Trade()
    ins = trd and trd.Instrument()
    absa_swift_param = config.GetUniqueNode('AbcapSwiftParameters')
    issuer_agent_code = config.GetValue(absa_swift_param, 'AgentParticipantCode', True)
    dis_issuer_agent_code = config.GetValue(absa_swift_param, 'DisAgentParticipantCode', True)
    if ins.AdditionalInfo().DIS_Instrument():
        return dis_issuer_agent_code
    if ins.AdditionalInfo().Demat_Instrument():
        return issuer_agent_code


def CLIENT_SOR_ACCOUNT(confirmation):

    trd = confirmation and confirmation.Trade()
    sor_acc_pattern = '\w*/\w{2}\d{6}/(\d*)'
    demat_sor_account = trd.AdditionalInfo().Demat_Acq_SOR_Ac()
    sor_acc_m = re.search(sor_acc_pattern, demat_sor_account, re.DOTALL)

    return sor_acc_m and sor_acc_m.group(1) or ''


def NOMINAL_AMOUNT(confirmation):

    trd = confirmation and confirmation.Trade()
    ins = trd and trd.Instrument()
    nominal_amount = calc_space_value(trd, 'Trade Nominal')
    nominal_amount = fabs(nominal_amount)

    return '%s' % (formatNumber('%15.2f' % nominal_amount))


def SETTLEMENT_AMOUNT(confirmation):

    trd = confirmation.Trade()
    premium_amount = calc_space_value(trd, 'Trade Premium')
    premium_amount = fabs(premium_amount)
    premium_curr = trd and trd.Currency().Name()    

    return '%s%s' % (premium_curr, formatNumber('%15.2f' % (premium_amount)))
    
    
def INTEREST_RATE(confirmation):

    trd = confirmation.Trade()
    ins = trd.Instrument()
    legs = [leg for leg in ins.Legs()]
    if len(legs) == 1:
        leg = legs[0]
        if leg.IsFixedLeg():
            return '%2.4f %s' % (leg.FixedRate(), '%')
        elif leg.IsFloatLeg():
            return '%s + %2.4f %s' % (leg.FloatRateReference().Name(), leg.Spread(), '%')


def AGREEMENT_FLAG(confirmation):

    cash_flow = confirmation.CashFlow()
    if cash_flow:
        if cash_flow.AdditionalInfo().Demat_Calc_Approvl():
            return 'Y'

    return 'N'


def SEQREF(confirmation):
    """
    SEQREF together with SEQNBR builds field 20, Senders reference
    """
    if Global.FAC:
        return Global.FAC
    return ''


def MESSAGE_USER_REFERENCE(confirmation):

    acm_trd = confirmation.Trade()
    acm_ins = acm_trd.Instrument()
    absa_swift_param = config.GetUniqueNode('AbcapSwiftParameters')
    user_ref_ext = config.GetValue(absa_swift_param, 'UserReferenceExt', True)
    dis_user_ref_ext = config.GetValue(absa_swift_param, 'DisUserReferenceExt', True)

    if acm_ins.Instrument().AdditionalInfo().Demat_Instrument():
        return '108:'+str(int(time.time()*10))[-8:] + 'MS10' + user_ref_ext + '002'

    elif acm_ins.Instrument().AdditionalInfo().DIS_Instrument():
        return '108:'+str(int(time.time()*10))[-8:] + 'MS10' + dis_user_ref_ext + '002'


def GetNarrativeSeparator():
    return FSwiftMTBase.GetNarrativeSeparator()


def GetCodewordNewline():
    return FSwiftMTBase.GetCodewordNewline()


def GetNetwork(confirmation):
    return FSwiftMTConfirmation.GetNetwork(confirmation)
    
    
def GetTypeOfOperation(confirmation):
    return FSwiftMTConfirmation.GetTypeOfOperation(confirmation)


def GetCode(confirmation):
    ''' Mandatory field 22 '''
    return 'AMEND'


def EVENT_TYPE(confirmation):
    """
    Determines the Cash Flow event type to differentiate the Interest
    from Redemption in Adaptive
    """
    event_type = get_confirmation_redemption_event(confirmation)
    if event_type:
        if event_type == 'PCAL':
            return 'PCAL DIS'
        elif event_type == 'MCAL':
            return 'MCAL DIS'
        elif event_type == 'INTR':
            return 'INTR'
    else:
        cash_flow = confirmation.CashFlow()
        if cash_flow.CashFlowType() in ('Fixed Rate', 'Float Rate'):
            return 'INTR'
        elif cash_flow.CashFlowType() == 'Fixed Amount':
            if cash_flow.Leg().Instrument().AdditionalInfo().DIS_Instrument():
                return 'REDM DIS'
            elif cash_flow.Leg().Instrument().AdditionalInfo().Demat_Instrument():
                return 'REDM DEMAT'
        else:
            return ''
