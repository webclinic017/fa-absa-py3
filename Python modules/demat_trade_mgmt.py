"""-----------------------------------------------------------------------------
PURPOSE                 :   This module will process the incoming nessages relating to the trade confirmation
                            settlement of coupons of the trades on the instrument.
DEPARTMENT AND DESK     :   MM
REQUESTER               :   Linda Breytenbach
DEVELOPER               :   Manan Ghosh
CR NUMBER               :
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date            Change no       Developer       Description
--------------------------------------------------------------------------------
2016-08-19      CHNG0003744247  Manan Ghosh     Initial Implementation
2017-08-26      2017 Upgrade    Willie vd Bank  Removed import of FOperationsUtils
2018-05-11      CHG1000406751   Willie vd Bank  Removed a print statement which was causing confusion on the ATS log
2021-01-27      FAOPS-899       Joshua Mvelase  Modified get_reference function to read reference from add info
"""

import acm
from datetime import datetime
import re
import time
from at_time import acm_date
import at_addInfo
from demat_functions import GetFirstTrade
from at_logging import getLogger


LOGGER = getLogger(__name__)
MATCH_PENDING = '0101'
MATCH_SUCCESS = '0201'
MATCH_READY_SETTL = '0251'
MATCH_OVERDUE = '0108'
MATCH_SETTLED = '0601'
MATCH_CANCELLED = '0401'
MATCH_FAIL_CP_OVERDUE = '0301'
MATCH_FAIL_NO_SEC = '0302'
MATCH_FAIL_SOR_FRZN = '0305'
MATCH_FAIL_CRNCY_DL = '0350'
MATCH_MISSING_COUNTER = '0809'
MATCH_REJECT_FORMAT = '901'
MATCH_REJECT_CONTENT_PS = '902'  # Pre Settle confirmation
MATCH_REJECT_CONTENT = '903'

CONF_RELEASED = 'Released'
CONF_ACKNOWLEDGED = 'Acknowledged'
CONF_PENDING_MATCH = 'Pending Matching'
CONF_MATCHED = 'Matched'
CONF_VOID = 'Void'
CONF_MATCH_FAILED = 'Matching Failed'

INTEREST = 'INTR'
REDEMPTION = 'REDM'
PARTIAL_REDEMPTION = 'PCAL'
EARLY_REDEMPTION = 'MCAL'


SETTLE_RELEASED = 'Released'
SETTLE_AUTHORISED = 'Authorised'
SETTLE_HOLD = 'Hold'
SETTLE_VOID = 'Void'

DEMAT_MATCH_REQUEST = 'Demat Match Request'


def commit_conf(conf):
    try:
        conf.Commit()
        update_ok = True
    except Exception as error:
        update_ok = False
        LOGGER.info("Failed to commit Confirmation with Id {oid}".format(oid=conf.Oid()))
        LOGGER.exception(error)

    return update_ok


def update_conf_status(conf, to_status, status_desc):
    update_ok = True

    if conf.Status() == to_status:
        if conf.Text() != status_desc:
            conf.Text(status_desc)
            update_ok = commit_conf(conf)
        return update_ok

    LOGGER.info('updating conf status from {status} to {to_status}'.format(status=conf.Status(), to_status=to_status))
    if conf.Status() == CONF_RELEASED:
        if to_status == CONF_ACKNOWLEDGED:
            conf.Status(to_status)
            conf.Text(status_desc)
            update_ok = commit_conf(conf)
        elif to_status in [CONF_PENDING_MATCH, CONF_MATCHED, CONF_MATCH_FAILED]:
            conf.Status(CONF_ACKNOWLEDGED)
            LOGGER.info('Confirmation status transition invalid from [%s] to [%s] status!' % (CONF_RELEASED, to_status))
            LOGGER.info('Updating [%s] to [%s] ' % (CONF_RELEASED, CONF_ACKNOWLEDGED))
            update_ok = commit_conf(conf)
            if update_ok:
                update_ok = update_conf_status(conf, to_status, status_desc)
        else:
            LOGGER.warning(
                'Confirmation status transition invalid from [%s] to [%s] status!' % (CONF_PENDING_MATCH, to_status))
            update_ok = False

    elif conf.Status() == CONF_ACKNOWLEDGED:
        if to_status in [CONF_PENDING_MATCH]:
            conf.Status(to_status)
            conf.Text(status_desc)
            update_ok = commit_conf(conf)
        elif to_status in [CONF_MATCHED, CONF_MATCH_FAILED]:
            conf.Status(CONF_PENDING_MATCH)
            LOGGER.warning(
                'Confirmation status transition invalid from [%s] to [%s] status!! ' % (CONF_ACKNOWLEDGED, to_status))
            LOGGER.info('Updating [%s] to [%s] ' % (CONF_ACKNOWLEDGED, CONF_PENDING_MATCH))
            update_ok = commit_conf(conf)
            if update_ok:
                update_ok = update_conf_status(conf, to_status, status_desc)

        else:
            LOGGER.warning('Confirmation status transition invalid from [%s] to [%s] status!! ' % (CONF_PENDING_MATCH,
                                                                                                   to_status))
            update_ok = False

    elif conf.Status() == CONF_PENDING_MATCH:
        if to_status in [CONF_MATCHED, CONF_MATCH_FAILED, CONF_VOID]:
            conf.Status(to_status)
            conf.Text(status_desc)
            update_ok = commit_conf(conf)

        else:
            LOGGER.warning(
                'Confirmation status transition invalid from [%s] to [%s] status!! ' % (CONF_PENDING_MATCH, to_status))
            update_ok = False

    else:
        error_message = 'Invalid status transition request!! from {current_status} to {new_status}'
        error_message.format(current_status=conf.Status(), new_status=to_status)
        LOGGER.info(error_message)

    return update_ok


def update_settlement_status(trdnbr, status):
    trd = acm.FTrade[trdnbr]
    settlements = trd.Settlements().AsArray()

    for settlement in settlements:
        if settlement.Type() != 'Premium':
            continue
        settlement.Status(status)
        settlement.Commit()
        break


def get_reference(message):
    """
    Function to get the confirmation number 
    """
    refer_pattern = '\{4:.*:20C::RELA//\w{2}\d{6}/(\d*).*\}'
    refer_m = re.search(refer_pattern, message, re.DOTALL)
    reference_number = refer_m.group(1)
    reference_number = get_reference_from_demat_add_info(reference_number)
    return refer_m and reference_number or None


def get_reference_from_demat_add_info(confirmation_id):
    additional_info_spec_id = acm.FAdditionalInfoSpec['Demat_ID'].Oid()
    additional_info = acm.FAdditionalInfo.Select01("addInf = {additional_info_spec_id} and fieldValue = '{add_info_value}'"
                                                   .format(additional_info_spec_id=additional_info_spec_id, 
                                                           add_info_value=confirmation_id), '')
    return additional_info.Parent().Oid() if additional_info else confirmation_id


def get_error_ref(message):
    """
    Function to get the confirmation number 
    """
    refer_pattern = '\{4:.*:21:FAC-(\d*)-1.*\}'
    refer_m = re.search(refer_pattern, message, re.DOTALL)

    if refer_m is None:
        refer_pattern = '\{4:.*:20C::RELA//FAC-(\d*)-1.*\}'
        refer_m = re.search(refer_pattern, message, re.DOTALL)

    return refer_m and refer_m.group(1) or None


def get_coupon_period(message):
    """
    Function to get the confirmation number 
    """
    coupon_period_pattern = '\{4:.*:69A::INPE//(\d{8})/(\d{8}).*\}'
    coupon_period_m = re.search(coupon_period_pattern, message, re.DOTALL)

    return coupon_period_m and (coupon_period_m.group(1), coupon_period_m.group(2)) or (None, None)


def get_issuer_agent(message):
    """
    Function to get the confirmation number 
    """
    issuer_agent_pattern = '\{4:.*:97A::SAFE//ISSA(\w{2}\d{6}).*\}'
    issuer_agent_pattern_m = re.search(issuer_agent_pattern, message, re.DOTALL)

    return issuer_agent_pattern_m and issuer_agent_pattern_m.group(1) or None


def get_cash_flow_type(message):
    """
    Function to get the cash flow type 
    """
    cash_flow_type_pattern = '\{4:.*:22F::CAEV//(\w{4}).*\}'
    cash_flow_type_m = re.search(cash_flow_type_pattern, message, re.DOTALL)

    return cash_flow_type_m and cash_flow_type_m.group(1) or None


def get_ban(message):
    """
    Function to get the BAN from message 
    """
    ban_pattern = '\{4:.*:20C::BANN//(.{9}).*\}'

    ban_m = re.search(ban_pattern, message, re.DOTALL)

    return ban_m and ban_m.group(1) or None


def get_utrn(message):
    """
    Function to get the UTRN from message 
    """
    utrn_pattern = '\{4:.*:20C::UTRN//(.{6}).*\}'
    utrn_m = re.search(utrn_pattern, message, re.DOTALL)

    return utrn_m and utrn_m.group(1) or None


def get_proc_status(message):
    """
    Function to get the matching status of the 
    trade at Strate
    """
    p_stat_pattern = '\{4:.*:25D::IPRC/STRA/(\d{4}).*-\}'
    p_stat_m = re.search(p_stat_pattern, message, re.DOTALL)

    return p_stat_m and p_stat_m.group(1) or None


def get_error_status(message):
    """
    Function to get the matching status of the trade at Strate
    """
    p_stat_pattern = '\{4:.*:12:(\d{3}).*-\}'
    p_stat_m = re.search(p_stat_pattern, message, re.DOTALL)

    return p_stat_m and p_stat_m.group(1) or None


def get_payment_amount(message):
    """
    Function to get the payment amount per CSD participant
    """
    pmt_pattern = '\{4.*:32B:ZAR(\d{1,12}),(\d{0,2}).*\}'
    pmt_m = re.search(pmt_pattern, message, re.DOTALL)

    if not pmt_m is None:
        return pmt_m.group(1), pmt_m.group(2)
    else:
        return None, None


def get_reducing_amount(message):
    """
    GEts the reducing amount per CSD participant
    """
    pmt_pattern = '\{4.*:36B::ENTL//FAMT/(\d{1,12}),(\d{0,2}).*\}'
    pmt_m = re.search(pmt_pattern, message, re.DOTALL)

    return pmt_m.group(1), pmt_m.group(2)


def get_bic_code(message):
    bic_pattern = '\{4.*:57A://(\w{8})\n(\w{8}).*\}'
    bic_m = re.search(bic_pattern, message, re.DOTALL)

    if not bic_m is None:
        return bic_m.group(1), bic_m.group(2)
    else:
        return None, None


def get_account_no(message):
    acc_pattern = '\{4.*:58D:/(\w{0,34})\n.*-\}'
    acc_m = re.search(acc_pattern, message, re.DOTALL)

    if not acc_m is None:
        return acc_m.group(1)
    else:
        return None


def get_settle_capital_event(message):
    cap_evnt_pattern = '\{4.*:21:(\w{13}).*-\}'
    cap_evnt_m = re.search(cap_evnt_pattern, message, re.DOTALL)

    if not cap_evnt_m is None:
        return cap_evnt_m.group(1)
    else:
        return None


def get_capital_event(message):
    """
    Get the capital event reference no
    """
    cap_evnt_pattern = '\{4:.*:20C::CORP//(\d{10}).*-\}'
    cap_evnt_m = re.search(cap_evnt_pattern, message, re.DOTALL)

    return cap_evnt_m and cap_evnt_m.group(1) or None


def get_cap_evnt_confirm(message):
    """
    Get the capital event confirm no
    """
    cap_evnt_conf_pattern = '\{4:.*:20C::SEME//(\d{14}).*-\}'
    cap_evnt_conf_m = re.search(cap_evnt_conf_pattern, message, re.DOTALL)

    return cap_evnt_conf_m and cap_evnt_conf_m.group(1) or None


def get_isin(message):
    """
    Get the instrument ISIN
    """
    isin_pattern = '\{4:.*:35B:ISIN\s(.{12}).*-\}'
    isin_m = re.search(isin_pattern, message, re.DOTALL)

    return isin_m and isin_m.group(1) or None


def get_pay_date(message):
    """
    Get the cash flow pay date
    """
    pay_date_pattern = '\{4:.*:98A::PAYD//(\d{8}).*-\}'
    pay_date_m = re.search(pay_date_pattern, message, re.DOTALL)

    return pay_date_m and pay_date_m.group(1) or None


def get_record_date(message):
    """
    Get the cash flow record date
    """
    record_date_pattern = '\{4:.*:98A::RDTE//(\d{8}).*-\}'
    record_date_match = re.search(record_date_pattern, message, re.DOTALL)

    return record_date_match.group(1)


def get_msg_type(message):
    """
    Returns message type and subtype e.g. 598-155 or 598-154
    """
    type_pattern = '\{2:[OI](\d{3}).*\}'
    sub_type_pattern = '{4:.*:12:(\d{3}).*}'

    type_m = re.search(type_pattern, message, re.DOTALL)
    sub_type_m = re.search(sub_type_pattern, message, re.DOTALL)

    if not sub_type_m is None:
        return '%s-%s' % (type_m.group(1), sub_type_m.group(1))
    else:
        return '%s' % (type_m.group(1))


def get_trans_ref(message):
    """
    Get the transaction reference 
    """
    trans_ref_pattern = '.*:20:(\d{0,15})-?(\d{0,15})[:\n]'
    trans_ref_m = re.search(trans_ref_pattern, message)

    return trans_ref_m.group(1), trans_ref_m.group(2)


def get_cashflow(ins, pay_date, cash_flow_type):
    """
    Get the cash flow from the Instrument 
    corresponding to the pay date 
    """
    if ins is None:
        return None

    legs = ins.Legs()
    if legs:
        payleg = [leg for leg in legs]
    else:
        payleg = []

    cf_type = []

    if cash_flow_type == INTEREST:
        cf_type = ['Fixed Rate', 'Float Rate']

    if cash_flow_type == REDEMPTION:
        cf_type = ['Fixed Amount']

    cashflow = []
    if len(payleg) > 0:
        cfs = payleg[0].CashFlows()
        cal = acm.FCalendar['ZAR Johannesburg']

        pay_date = time.strptime(pay_date, '%Y%m%d')

        if cal.CalendarInformation().IsNonBankingDay(
                acm.Time().DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday)):
            pay_date = cal.CalendarInformation().AdjustBankingDays(
                acm.Time().DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday), 1)
        else:
            pay_date = cal.CalendarInformation().AdjustBankingDays(
                acm.Time().DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday), 0)

        if not cfs is None:
            cashflow = [cf for cf in cfs if cf.PayDate() == pay_date and cf.CashFlowType() in cf_type]

    return len(cashflow) > 0 and cashflow[0] or None


def get_cashflow_cap_evnt(ins, cap_event):
    """
    Get the cash flow from the Instrument 
    corresponding to the capital event no
    """
    legs = ins and ins.Legs() or None
    if legs:
        payleg = [leg for leg in legs]
    else:
        payleg = []

    cashflow = []

    if len(payleg) > 0:
        cfs = payleg[0].CashFlows()

        if not cfs is None:
            cashflow = [cf for cf in cfs if cf.AdditionalInfo().Demat_CE_Reference() == cap_event]
    return len(cashflow) > 0 and cashflow[0] or None


def update_capital_evntno(message):
    """
    Update capital event reference no
    """
    isin = get_isin(message)
    cap_evnt = get_capital_event(message)
    (start_date, end_date) = get_coupon_period(message)
    issuer_agent = get_issuer_agent(message)
    cash_flow_type = get_cash_flow_type(message)
    pay_date = get_pay_date(message)
    ins = acm.FInstrument.Select01("isin = '%s' " % (isin), '')
    cf = get_cashflow(ins, pay_date, cash_flow_type)
    if cash_flow_type == REDEMPTION:
        _process_redemption_cashflow(ins, pay_date, cap_evnt, message)
    else:
        if cf:
            try:
                cf_event_type = get_cashflow_evnt_type(message)
                if cf_event_type in ['NEWM', 'REPL']:
                    at_addInfo.save(cf, 'Demat_CE_Reference', cap_evnt)
                    at_addInfo.save(cf, 'Demat_Coupon_Period', '%s/%s' % (start_date, end_date))
                    isvalid = True
                    if cash_flow_type == INTEREST:
                        start_date = datetime.strptime(start_date, '%Y%m%d')
                        start_date = start_date.strftime('%Y-%m-%d')

                        isvalid = isvalid and start_date == acm_date(cf.StartDate())

                    validflag = isvalid and True or False
                    at_addInfo.save(cf, 'Demat_Calc_Approvl', validflag)
                    cf.Commit()

                success_message = 'Updated Capital Event Reference number {cap_event}'
                success_message += 'on cash flow {cf_oid} on Instrument {ins}'
                LOGGER.info(success_message.format(cap_event=cap_evnt, cf_oid=cf.Oid(), ins=ins.Name()))

            except Exception as error:
                LOGGER.warning(
                    'Failed to commit CashFlow with id {oid} on Instrument {ins}'.format(oid=cf.Oid(), ins=ins.Name()))
                LOGGER.exception(error)
        else:
            error_message = 'No Cashflow found for Instrument {ins}: Capital Event Reference number update failed'
            print(error_message.format(ins=ins.Name()))


def _process_redemption_cashflow(instrument, pay_date, cap_evnt, message):
    """
    Processes Redemption cash flow on incoming 564 message
    """
    record_date = get_record_date(message)
    if not record_date:
        raise ValueError('Could not determine Record Date on 98A::RDTE//')
    if not cap_evnt:
        raise ValueError('Could not determine capital event value!!')
    cash_flow = _get_redemption_cashflow(instrument, pay_date)
    try:
        cash_flow.AdditionalInfo().Demat_CE_Reference(cap_evnt)
        cash_flow.AdditionalInfo().Demat_Calc_Approvl(True)
        cash_flow.AdditionalInfo().Demat_Record_Date(record_date)
        cash_flow.Commit()
        success_message = 'Updated Capital Event Reference number {cap_event}'
        success_message += 'on cash flow {cf_oid} on Instrument {ins}'
        LOGGER.info(success_message.format(cap_event=cap_evnt, cf_oid=cash_flow.Oid(), ins=instrument.Name()))
    except Exception as e:
        error_message = 'Failed to process REDM instruction on instrument {}. Could not create Fixed Amount Cash FLow'
        LOGGER.exception(error_message.format(instrument.Name()))
        raise e


def _get_redemption_cashflow(instrument, pay_date):
    """
    Gets redemption Cash FLow from instrument
    """
    pay_date = time.strptime(pay_date, '%Y%m%d')
    formatted_date = acm.Time.DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday)
    cash_flows = instrument.Legs().First().CashFlows()
    for cash_flow in cash_flows:
        if cash_flow.CashFlowType() != 'Fixed Amount':
            continue
        if cash_flow.PayDate() != formatted_date:
            continue
        return cash_flow

    raise ValueError('Could not find Redemption CashFlow on instrument {}'.format(instrument.Name()))


def update_capital_confirm(message):
    """
    Update capital event confirmation no
    """
    isin = get_isin(message)
    cap_evnt = get_capital_event(message)
    cap_evnt_conf = get_cap_evnt_confirm(message)
    ins = acm.FInstrument.Select01("isin = '%s' " % (isin), '')
    trd = GetFirstTrade(ins)
    cf = get_cashflow_cap_evnt(ins, cap_evnt)

    if cf:
        try:
            conf = acm.FConfirmation.Select01("cashFlow = %i" % cf.Oid(), "")
            if conf is not None:
                update_conf_status(conf, CONF_MATCHED, CONF_MATCHED + cap_evnt_conf)
                LOGGER.info('update_capital_confirm: Updated Confirmation Status [%s] on confirmation [%i] ' %
                CONF_MATCHED, conf.Oid())
            else:
                LOGGER.info('update_capital_confirm: Confirmation object not found for cashflow [%i] ' % cf.Oid())

        except Exception as error:
            LOGGER.warning('update_capital_confirm: Confirmation update failed for cashflow [%i]!! ' % cf.Oid())
            LOGGER.exception(error)
    else:
        error_message = 'No Cashflow found for Instrument {ins}: Capital Event Confirmation number update failed'
        LOGGER.warning(error_message.format(ins=ins.Name()))


def update_ban_utrn(message):
    """
    Confirms the trade and updates BAN and UTRN
    """
    ban = get_ban(message)
    utrn = get_utrn(message)
    conf_ref = get_reference(message)
    conf = acm.FConfirmation[int(conf_ref)]

    if conf and conf.Trade():
        trade = conf.Trade()
        try:
            acm.BeginTransaction()
            if ban is not None:
                LOGGER.info('Updating MM_DEMAT_BAN add info on trade {oid}'.format(oid=trade.Oid()))
                trade.AddInfoValue('MM_DEMAT_BAN', ban)
            if utrn is not None:
                LOGGER.info('Updating MM_DEMAT_UTRN add info on trade {oid}'.format(oid=trade.Oid()))
                trade.AddInfoValue('MM_DEMAT_UTRN', utrn)
            trade.Commit()
            acm.CommitTransaction()
        except Exception:
            acm.AbortTransaction()
            LOGGER.exception('update_ban_utrn: Update failed!')

    if not conf:
        LOGGER.error(
            'Failed to update BAN or UTRN. Confirmation with id {conf_ref} not Found'.format(conf_ref=conf_ref))
        return


def update_trade_status(mtmessage):
    """
    This is to update the processing status at Strate
    based on the MT 548 message. 

    The statuses are as follows

        MATCH_PENDING               = '0101'
        MATCH_SUCCESS               = '0201'
        MATCH_READY_SETTL           = '0251'
        MATCH_OVERDUE               = '0108'
        MATCH_SETTLED               = '0601'
        MATCH_CANCELLED             = '0401'
        MATCH_FAIL_CP_OVERDUE       = '0301'
        MATCH_FAIL_NO_SEC           = '0302'
        MATCH_FAIL_SOR_FRZN         = '0305'
        MATCH_FAIL_CRNCY_DL         = '0350'
        MATCH_MISSING_COUNTER       = '0809'
        MATCH_REJECT_FOMRAT         = '0901'
        MATCH_REJECT_CONTENT        = '0903'

        CONF_RELEASED               = 'Released'
        CONF_ACKNOWLEDGED           = 'Acknowledged'
        CONF_PENDING_MATCH          = 'Pending Matching'
        CONF_MATCHED                = 'Matched'
        CONF_VOID                   = 'Void'
        CONF_MATCH_FAILED           = 'Matching Failed'
    """

    msg_type = get_msg_type(mtmessage)
    proc_stat = get_proc_status(mtmessage)
    conf_ref = get_reference(mtmessage)

    conf = acm.FConfirmation[int(conf_ref)]

    if not conf:
        LOGGER.error(
            'Failed to update trade Status. Confirmation with id {conf_ref} not Found'.format(conf_ref=conf_ref))
        return

    trd = conf.Trade()
    settle_status = None

    if proc_stat in [MATCH_PENDING, MATCH_OVERDUE]:

        if trd.Status() not in ['BO-BO Confirmed', 'Void']:
            trd.Status('BO Confirmed')

        update_ok = True
        if conf.Status() == CONF_RELEASED:
            update_ok = update_conf_status(conf, CONF_ACKNOWLEDGED, '')

        if proc_stat == MATCH_PENDING:
            if update_ok and conf.Status() in [CONF_ACKNOWLEDGED, CONF_PENDING_MATCH]:
                update_ok = update_conf_status(conf, CONF_PENDING_MATCH, '101 - Match Pending')
            settle_status = SETTLE_AUTHORISED

        if proc_stat == MATCH_OVERDUE:
            if update_ok and conf.Status() in [CONF_ACKNOWLEDGED, CONF_PENDING_MATCH]:
                update_ok = update_conf_status(conf, CONF_PENDING_MATCH, '108 - Match Pending')
            settle_status = SETTLE_HOLD

        if update_ok is True:
            LOGGER.info('Demat Trade: Processing proc_stat [%s] Pending Matching!' % proc_stat)

    elif proc_stat == MATCH_SUCCESS:

        if trd.Status() not in ['Void']:
            trd.Status('BO-BO Confirmed')
            first_trade = GetFirstTrade(trd)
            if first_trade is None or trd.Oid() == first_trade.Oid():
                LOGGER.info("Setting MM_DEMAT_PRE_SETT on trade {oid} to Yes".format(oid=trd.Oid()))
                trd.AddInfoValue('MM_DEMAT_PRE_SETT', 'Yes')

        update_ok = True
        if conf.Status() == CONF_RELEASED:
            update_ok = update_conf_status(conf, CONF_ACKNOWLEDGED, '')

        if update_ok and conf.Status() == CONF_ACKNOWLEDGED:
            update_ok = update_conf_status(conf, CONF_PENDING_MATCH, '')

        if update_ok and conf.Status() == CONF_PENDING_MATCH:
            update_ok = update_conf_status(conf, CONF_MATCHED, '201 - Matched')
            settle_status = SETTLE_AUTHORISED
            if update_ok is True:
                LOGGER.info('Demat Trade: Processing proc_stat[%s] Matched!' % proc_stat)

    elif proc_stat in [MATCH_CANCELLED]:
        if trd.Status() not in ['BO-BO Confirmed']:
            trd.Status('Void')

        update_ok = True
        if conf.Status() == CONF_RELEASED:
            update_ok = update_conf_status(conf, CONF_ACKNOWLEDGED, '')

        if update_ok and conf.Status() == CONF_ACKNOWLEDGED:
            update_ok = update_conf_status(conf, CONF_PENDING_MATCH, '')

        if update_ok and conf.Status() in [CONF_PENDING_MATCH]:
            update_ok = update_conf_status(conf, CONF_VOID, '401 - Cancelled')
            settle_status = SETTLE_VOID
            if update_ok is True:
                LOGGER.info('Demat Trade: Processing proc_stat [%s] Match Failed!' % proc_stat)

    elif proc_stat in [MATCH_MISSING_COUNTER, MATCH_REJECT_FORMAT, MATCH_REJECT_CONTENT]:

        if trd.Status() not in ['BO-BO Confirmed']:
            trd.Status('Void')
            trd.AddInfoValue('MM_DEMAT_PRE_SETT', 'No')

        update_ok = True
        if conf.Status() == CONF_RELEASED:
            update_ok = update_conf_status(conf, CONF_ACKNOWLEDGED, '')

        if update_ok and conf.Status() == CONF_ACKNOWLEDGED:
            update_ok = update_conf_status(conf, CONF_PENDING_MATCH, '')

        if update_ok and conf.Status() == CONF_PENDING_MATCH:
            update_ok = update_conf_status(conf, CONF_MATCH_FAILED, '%s - Match Fail' % (proc_stat[1:]))
        settle_status = SETTLE_VOID

        if update_ok:
            LOGGER.info('Demat Trade: Processing proc_stat [%s]  Match Failed!' % proc_stat)
    else:
        LOGGER.warning('Demat Trade: Cannot process status [%s]' % proc_stat)

    try:

        trd.Commit()
        conf.Commit()
        update_settlement_status(trd.Oid(), settle_status)

    except Exception as error:
        LOGGER.error('Unable to commit changes to Trade {trd_oid} and Confirmation {conf_oid}'.format(trd_oid=trd.Oid(),
                                                                                                      conf_oid=conf.Oid()
                                                                                                      ))
        LOGGER.exception(error)


def update_trade_exception(mtmessage):
    """
    The trade statuses are as follows:
        MATCH_REJECT_FORMAT         = '901'
        MATCH_REJECT_CONTENT_PS     = '902'
        MATCH_REJECT_CONTENT        = '903'
    """
    err_stat = get_error_status(mtmessage)
    conf_ref = get_error_ref(mtmessage)
    conf = acm.FConfirmation[int(conf_ref)]

    if not conf:
        LOGGER.warning('Failed to update trade. Confirmation with id {conf_ref} not Found'.format(conf_ref=conf_ref))
        return

    trd = conf.Trade()

    if err_stat in [MATCH_REJECT_FORMAT, MATCH_REJECT_CONTENT_PS, MATCH_REJECT_CONTENT]:

        try:
            conf.Commit()

            if conf.EventType() == DEMAT_MATCH_REQUEST:
                trd.Status('Void')
                trd.AddInfoValue('MM_DEMAT_PRE_SETT', 'No')
                trd.Commit()
        except Exception as error:
            LOGGER.error("Unable to change trade {oid} status to void!!".format(oid=trd.Oid()))
            LOGGER.exception(error)


def is_trade_message(message):
    """
    Function to get the confirmation number
    """
    refer_pattern = '\{4:.*:21:FAC-(\d*)-1.*\}'
    refer_m = re.search(refer_pattern, message, re.DOTALL)

    if refer_m is None:
        refer_pattern = '\{4:.*:20C::RELA//FAC-(\d*)-1.*\}'
        refer_m = re.search(refer_pattern, message, re.DOTALL)

    return not refer_m is None


def get_cashflow_evnt_type(message):
    """
    Function to get the confirmation event type
    """
    event_type_pattern = '\{4:.*:23G:(\w{4}).*\}'
    event_type_m = re.search(event_type_pattern, message, re.DOTALL)
    return event_type_m and event_type_m.group(1) or None


def trade_mgmt_incoming(mtmessage, msg_type):
    """
    Handle incoming MT message and
    update Business Process accordingly
    """
    if msg_type == '598-171':
        update_ban_utrn(mtmessage)
    elif msg_type == '564':
        update_capital_evntno(mtmessage)
    elif msg_type == '548':
        update_trade_status(mtmessage)
    elif msg_type == '566':
        update_capital_confirm(mtmessage)
    elif msg_type == '598-901':
        update_trade_exception(mtmessage)
    elif msg_type == '598-903':
        update_trade_exception(mtmessage)
    elif msg_type == '598-902':
        update_trade_exception(mtmessage)
