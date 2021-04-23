"""-----------------------------------------------------------------------------
PURPOSE                 :  This will query relevant Business Process.
                           If an entry exists on either one of these states,
                           * Ready
                           * TopUpReduce To Be Sent
                           * DeIssue To Be Sent

                           The ATS will process the instrument, generate a SWIFT MT message, place it on MQ, and apply the relevant event:
                           "new ISIN request sent"
                           "Topup Deissue request sent"
                           "Deissue Request sent"
                           on the Business Process + Add the sent SWIFT message as a NOTE on the event for historical purposes.

DEPATMENT AND DESK      :  DIS
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Manan Ghosh
CR NUMBER               :
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date            Change no       Developer          Description
--------------------------------------------------------------------------------
2017-12-11      CHNG0005220511  Manan Ghosh        Initial Implementation
2019-04-25      FAOPS-450       Stuart Wilson      Added redemption additional payments generation
2019-07-22      Upgrade2018     Jaysen Naicker     Make code 2018 compatible
2020-03-17      FAOPS-623       Ntokozo Skosana    Allow payments to made even though there is a
                                                   mismatch because ABSA is the calculating agent.
2020-07-29      FAOPS-780       Ntokozo Skosana    Added capability to get cash flow associated with
                                                   trade
2020-10-28      Bug Fix         Ntokozo Skosana    Fix function '_check_if_payment_should_be_generated' that was
                                                    incorrectly blocking additional payments from generating.
2020-10-05      FAOPS-881/883   Tawanda Mukhalela   Added Support for Redemption Processing
"""

import re
import acm, ael
from datetime import datetime
import demat_swift_mt598
import FOperationsUtils as Utils
import traceback
import time
import at_addInfo
import gen_swift_functions
import demat_config
from demat_functions import dis_coupon_amount_calc
from demat_isin_mgmt_menex import dis_initial_amount, dis_unissued_amount, dis_authorised_amount
from CustomSWIFTFunctions import ENTITLED_COUPON_PAYMENT
from collections import defaultdict
from at_time import acm_date, to_date, to_datetime
from demat_functions import GetFirstTrade
from demat_isin_mgmt_confirmation import send_isin_report
from at_logging import getLogger
from DocumentConfirmationGeneral import create_document_confirmation


LOGGER = getLogger(__name__)
DIS_ISIN_MGMT_BPS = 'DIS Pending New ISIN'
dis_instr_dict = defaultdict(lambda x, y: 'No Instrument for this key value !! ')
dis_isin_messages = dict()
unprocessed_isin_confos = None

INTEREST = 'INTR'
REDEMPTION = 'REDM'
PARTIAL_REDEMPTION = 'PCAL'
EARLY_REDEMPTION = 'MCAL'
PTY_SARB = 'SARB'
COUPON_PAYMENT = 'Coupon Payment'
COUPON = 'Coupon'
COUPON_GROSS_UP = 'Coupon Gross up Payment'
COUPON_RECEIVABLE = 'Coupon Receivable'
REDEMPTION_T = 'Redemption'
REDEMPTION_RECEIVABLE_T = 'Redemption Receivable'

TOLERANCE = 2.0

SYSTEM_GROUPS = ['Integration Process']

DIS_ISIN_MGMT_STATE_CHART_NAME = 'DIS ISIN Management'

ACTION = {
    "NEW" : "ISSU",
    "TOPUP" : "TOPU",
    "REDUCE" : "REDU",
    "DEISSUE" : "DISS"
}

VALID_ACQUIRERS = (
    'BAGL ACQUIRER', 'GROUP TREASURY', 'STRUCT NOTES DESK',
    'SYNDICATE TRADING', 'CREDIT DERIVATIVES DESK',
    'CREDIT DERIVATIVES DESK NONCSA', 'FMAINTENANCE', 'ALCO DESK ISSUER'
)


def _listener(obj, entity, arg, operation):
    """Adds the entity and the original entity to the processing queue queue."""
    global dis_instr_dict
    bp = acm.FBusinessProcess[entity.seqnbr]
    dis_instr_dict[create_ins_key(bp)] = bp


def create_mmss_isin_request_statechart(replace_existing=True):

    try:
        if replace_existing:
            state_chart = acm.FStateChart[DIS_ISIN_MGMT_STATE_CHART_NAME]
            if state_chart:
                processes = acm.BusinessProcess.FindBySubjectAndStateChart(None, state_chart)
                for p in processes:
                    p.Delete()
                state_chart.Delete()
                state_chart.Delete()
                print "REMOVED"
            else:
                print 'State Chart not removed, could not be found with name:', DIS_ISIN_MGMT_STATE_CHART_NAME

        state_chart = acm.FStateChart(name = DIS_ISIN_MGMT_STATE_CHART_NAME)
        state_chart.BusinessProcessesPerSubject('Single Active') # Can be Single or Unlimited
        state_chart.Commit()

        state_chart.CreateState('New ISIN Request Pending')
        state_chart.CreateState('TopUp Reduce Request to be sent')
        state_chart.CreateState('TopUp Reduce Request MQ ACKNACK')
        state_chart.CreateState('TopUp Reduce Request Pending')
        state_chart.CreateState('DeIssue Request to be sent')
        state_chart.CreateState('DeIssue Request MQ ACKNACK')
        state_chart.CreateState('DeIssue Request Pending')
        state_chart.CreateState('DeIssued')
        state_chart.CreateState('Active')
        state_chart.CreateState('Topup Reduce Failed Response')
        state_chart.CreateState('Deissue Failed Response')
        state_chart.Commit()

        ready_state = state_chart.ReadyState()
        states = state_chart.StatesByName()
        state_new_isin_req_waiting = states['New ISIN Request Pending']
        state_amend_req_tbs = states['TopUp Reduce Request to be sent']
        state_amend_req_ack = states['TopUp Reduce Request MQ ACKNACK']
        state_amend_req_waiting = states['TopUp Reduce Request Pending']
        state_deissue_req_tbs = states['DeIssue Request to be sent']
        state_deissue_req_ack = states['DeIssue Request MQ ACKNACK']
        state_deissue_req_waiting = states['DeIssue Request Pending']
        state_inactive = states['DeIssued']
        state_active = states['Active']
        state_failed_new_request = states['New ISIN Failed Response']
        state_failed_amend_request = states['Topup Reduce Failed Response']
        state_failed_deissue_request = states['Deissue Failed Response']

        await_isin_event = acm.FStateChartEvent('Await ISIN')
        new_isin_request_received_event = acm.FStateChartEvent('ISIN response received')
        amend_event = acm.FStateChartEvent('Request Topup or Reduce')
        amend_request_sent_event = acm.FStateChartEvent('Sent Topup Reduce Request')
        amend_request_received_event = acm.FStateChartEvent('Topup Reduce Response Received')
        deissue_event = acm.FStateChartEvent('Request Deissue')
        deissue_request_sent_event = acm.FStateChartEvent('Sent Deissue Request')
        deissue_request_received_event = acm.FStateChartEvent('Deissue Response Received')
        failed_response_event = acm.FStateChartEvent('Failed Response Received')
        nack_event = acm.FStateChartEvent('NACK Received')
        ack_event = acm.FStateChartEvent('ACK Received')
        retry_event = acm.FStateChartEvent('Resend')
        cancel_event = acm.FStateChartEvent('Cancel')

        ready_state.CreateTransition(await_isin_event, state_new_isin_req_waiting)
        state_new_isin_req_waiting.CreateTransition(new_isin_request_received_event, state_active)
        state_new_isin_req_waiting.CreateTransition(fail_isin_match_event, state_new_isin_req_exception)
        state_new_isin_req_exception.CreateTransition(retry_isin_match_event, state_new_isin_req_waiting)


        state_amend_req_tbs.CreateTransition(amend_request_sent_event, state_amend_req_ack)
        state_amend_req_ack.CreateTransition(ack_event, state_amend_req_waiting)
        state_amend_req_ack.CreateTransition(nack_event, state_failed_amend_request)
        state_amend_req_waiting.CreateTransition(amend_request_received_event, state_active)
        state_amend_req_waiting.CreateTransition(failed_response_event, state_failed_amend_request)

        state_deissue_req_tbs.CreateTransition(deissue_request_sent_event, state_deissue_req_ack)
        state_deissue_req_ack.CreateTransition(ack_event, state_deissue_req_waiting)
        state_deissue_req_ack.CreateTransition(nack_event, state_failed_deissue_request)
        state_deissue_req_waiting.CreateTransition(deissue_request_received_event, state_inactive)
        state_deissue_req_waiting.CreateTransition(failed_response_event, state_failed_deissue_request)

        state_failed_amend_request.CreateTransition(retry_event, state_amend_req_tbs)
        state_failed_amend_request.CreateTransition(cancel_event, state_active)

        state_failed_deissue_request.CreateTransition(retry_event, state_deissue_req_tbs)
        state_failed_deissue_request.CreateTransition(cancel_event, state_active)

        state_active.CreateTransition(amend_event, state_amend_req_tbs)
        state_active.CreateTransition(deissue_event, state_deissue_req_tbs)
        state_chart.Commit()
        print 'Creation of State Chart Created'
    except Exception, e:
        print 'Creation of State Chart Failed', e


def list_dis_instr():

    global dis_instr_dict

    not_processed_bps = acm.FStoredASQLQuery[DIS_ISIN_MGMT_BPS].Query().Select()

    for bp in not_processed_bps:
        dis_instr_dict[create_ins_key(bp)] = bp


def initialize():

    global unprocessed_isin_confos

    ael.BusinessProcess.subscribe(_listener)

    unprocessed_isin_confos    = acm.FCustomTextObject.Select01("name = 'SWIFT_MESSAGES' and subType = 'SWIFT'", "" )
    msgtext                    = unprocessed_isin_confos.Text()
    msglist                    = msgtext.split('\n')

    for msg in msglist:
        msgfields                        = msg.split(':')
        dis_isin_messages[msgfields[0]]  = msgfields[1:]


def deinitialize():

    global dis_instr_dict

    ael.BusinessProcess.unsubscribe(_listener)
    save_messages()


def save_messages():
    """ Saves the unprocessed messages in Text Object """

    global unprocessed_isin_confos
    global dis_isin_messages

    for key in dis_isin_messages.keys() :
        print type(key), '   ',  type(dis_isin_messages[key])

    messages = [key + ':' + dis_isin_messages[key] for key in dis_isin_messages.keys() if type(dis_isin_messages[key]) is str]
    print messages
    unprocessed_isin_confos.Text('\n'.join(messages))


def get_isin(message):
    """
    Get the instrument ISIN
    """
    isin = gen_swift_functions.get_text_from_tag(':35B:ISIN ', message)

    return isin


def get_capital_event(message):
    """
    Get the capital event reference no
    """
    cap_evnt = gen_swift_functions.get_text_from_tag(':20C::CORP//', message)

    return cap_evnt


def get_record_date(message):
    """
    Get the record date
    """
    rec_date = gen_swift_functions.get_text_from_tag(':98A::RDTE//', message)

    return rec_date


def get_coupon_period(message):
    """
    Function to get the coupon period
    """

    coupon_period_string = gen_swift_functions.get_text_from_tag(':69A::INPE//', message)
    coupon_period = coupon_period_string.split('/')

    return coupon_period[0],  coupon_period[1]


def get_issuer_agent(message):
    """
    Function to get the confirmation number
    """
    issuer_agent = gen_swift_functions.get_text_from_tag(':97A::SAFE//ISSA', message)

    return issuer_agent


def get_entl_amount(message):
    """
    Get the amount from field 19B
    """
    amount = gen_swift_functions.get_text_from_tag(':19B::ENTL//', message)[3:].replace(',', '.')
    if amount:
        try:
            number_amount = float(amount)
        except Exception as ex:
            print ex
            raise AttributeError('Could not get ENTL amount from field 19B of message')

        return number_amount


def get_cash_flow_event_type(message):
    """
    Function to get the cash flow event type
    """
    cash_flow_type = gen_swift_functions.get_text_from_tag(':22F::CAEV//', message)

    return cash_flow_type


def get_pay_date(message):
    """
    Get the cash flow pay date
    """
    pay_date = gen_swift_functions.get_text_from_tag(':98A::PAYD//', message)

    return pay_date


def create_ins_key(bp):
    """
    Creates a key for the instrument associated with the Business Process
    """

    ins = bp.Subject()

    if ins.IsKindOf(acm.FInstrument):

        if not ins.AdditionalInfo().Demat_Issuer_BPID():
            issuer_bpid = 'XXXXXXXX'
            Utils.Log(True, "Issuer on Instrument [%s] does not have a BPID !! " % (ins.Name()) )
        else:
            issuer_bpid = ins.AdditionalInfo().Demat_Issuer_BPID()
            if issuer_bpid.find('/') > 0:
                issuer_bpid_prts = issuer_bpid.split('/')
                issuer_bpid = issuer_bpid_prts[1]

        mminstype = ins.AdditionalInfo().MM_MMInstype() or ''
        authorised_amount = dis_initial_amount(ins) or 0.0
        ins_key = ('%s_%s_%s_%s_%s' % (issuer_bpid, to_date(ins.StartDate()).strftime('%Y%m%d'),
                                       to_datetime(ins.ExpiryDate()).strftime('%Y%m%d'),
                                       '{0:013.2f}'.format(authorised_amount).replace('.', 'X'),
                                       mminstype.ljust(4, 'X')))

        return ins_key

    return None


def get_combination_cash_flows(trd, pay_date, cash_flow_event_type):
    '''
    Get the cash flows from the combination
    instrument that corresponding to the
    pay day
    '''

    cash_flows = []
    cash_flow_type = _get_cashflow_type(cash_flow_event_type)

    for mf in trd.MoneyFlows():
        if mf.Type() in cash_flow_type and mf.SourceObject().IsKindOf(acm.FCashFlow):
            cash_flow = mf.SourceObject()
            cash_flows.append(cash_flow)

    return _get_cash_flows_on_pay_day(cash_flows, pay_date, cash_flow_type)


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

def _get_cashflow_type(cash_flow_event_type):
    if cash_flow_event_type == INTEREST:
        return ['Coupon', 'Fixed Rate', 'Float Rate']

    if cash_flow_event_type == REDEMPTION:
        return ['Redemption', 'Fixed Amount']
    return None

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


def create_message_key(message):
    """
    Creates message key from incoming NEWM event message
    """

    issuer_bpid  = gen_swift_functions.get_text_from_tag(':95R::ISSR/STRA/', message)
    maturity_dt  = gen_swift_functions.get_text_from_tag(':98A::MATU//', message)
    issue_dt     = gen_swift_functions.get_text_from_tag(':98A::ISSU//', message)
    amount       = gen_swift_functions.get_text_from_tag(':36B::QISS//FAMT/', message)
    instype      = gen_swift_functions.get_text_from_tag(':22H::TYPE//', message)
    amount       = float(amount.replace(',', '.'))
    amount = '{0:013.2f}'.format(amount).replace('.', 'X')

    return '%s_%s_%s_%s_%s' % (issuer_bpid, issue_dt, maturity_dt, amount, instype)


def new_isin_request_tbs(bp):
    new_isin_request_sent_event = acm.FStateChartEvent('Sent ISIN Request')
    try:
        init_amount = float(bp.CurrentStep().DiaryEntry().Parameters()['Initial Amount'])
    except Exception, ex:
        print 'Error: Init amount paramter not understood\nUsing 0.0'
        print ex
        init_amount = 0.0
    step_id = bp.CurrentStep().Oid()
    param_dict = { "Initial Amount": init_amount }
    try:
        #Place on MQ
        mq_mess = gen_mq.MqMessenger('MeridianOutCustMq')
        try:
            swift_msg = str(demat_swift_mt598.from_instrument(bp.Subject(), ACTION['NEW'], init_amount, step_id))
        except Exception, swift_gen_ex:
            print 'Exception during message generation', swift_gen_ex
            traceback.print_exc()
            return
        notes = [swift_msg]
        mq_mess.Put(swift_msg)
        bp.HandleEvent(new_isin_request_sent_event, params = param_dict, notes = notes)
        bp.Commit()
    except Exception, ex:
        Utils.Log(True, "Could not place swift message on MQ\nError:%s" % ex)


def topup_reduce_request_tbs(bp):
    amend_amount = float(bp.CurrentStep().DiaryEntry().Parameters()['Amend Amount'])
    step_id = bp.CurrentStep().Oid()
    if amend_amount > 0:
        action = ACTION['TOPUP']
    else:
        action = ACTION['REDUCE']
    topup_reduce_request_sent_event = acm.FStateChartEvent('Sent Topup Reduce Request')
    param_dict = { "Amend Amount": amend_amount}
    try:
        #Place on MQ
        mq_mess = gen_mq.MqMessenger('MeridianOutCustMq')
        try:
            swift_msg = str(demat_swift_mt598.from_instrument(bp.Subject(), action, abs(amend_amount), step_id))
        except Exception, swift_gen_ex:
            print 'Exception during message generation', swift_gen_ex
            traceback.print_exc()
            return
        notes = [swift_msg]
        mq_mess.Put(swift_msg)
        bp.HandleEvent(topup_reduce_request_sent_event, params = param_dict, notes = notes)
        bp.Commit()
    except Exception, ex:
        Utils.Log(True, "Could not place swift message on MQ\nError:%s" % ex)
        traceback.print_exc()
        #sendNotificationMail(ex)


def deissue_request_tbs(bp):
    deissue_request_sent_event = acm.FStateChartEvent('Sent Deissue Request')
    try:
        #Place on MQ
        mq_mess = gen_mq.MqMessenger('MeridianOutCustMq')
        try:
            swift_msg = str(demat_swift_mt598.from_instrument(bp.Subject(), ACTION['DEISSUE'], current_authorised_amount(bp.Subject())))
        except Exception, swift_gen_ex:
            print 'Exception during message generation', swift_gen_ex
            traceback.print_exc()
            return
        notes = [swift_msg]
        mq_mess.Put(swift_msg)
        bp.HandleEvent(deissue_request_sent_event, notes = notes )
        bp.Commit()
    except Exception, ex:
        Utils.Log(True, "Could not place swift message on MQ\nError:%s" % ex)


def send_isin_request(bp):

    swift_to_be_sent_states = {
        'New ISIN Request to be sent': new_isin_request_tbs,
        'TopUp Reduce Request to be sent': topup_reduce_request_tbs,
        'DeIssue Request to be sent': deissue_request_tbs
    }

    #Only these types are valid for Swift Generation - If other instrument types are tried to process it can break
    if bp.Subject().InsType() in ['FRN', 'CD', 'CLN', 'Bond', 'Zero', 'IndexLinkedBond']:
        current_state = bp.CurrentStep().State().Name()
        if current_state in swift_to_be_sent_states:
            try:
                print '%s Handling business process: %s %s' % (
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    bp.Subject().Name(),
                    current_state
                )
                swift_to_be_sent_states[current_state](bp)
                bp.Commit()
            except Exception, ex:
                Utils.Log(True, "Could not process and commit change to Business Process\nError:%s" % ex)
                #sendNotificationMail(ex)
    else:
        print 'Instrument type not supported for Swift generation'


def new_isin_request_received(bp, success=True, note=None):
    if success:
        new_isin_request_received = acm.FStateChartEvent('ISIN response received')



        amount = gen_swift_functions.get_value_from_tag(':36B::QISS//FAMT/', note[0]).replace(',', '.')
        bp.Subject().Isin(gen_swift_functions.get_isin(note[0]))
        bp.HandleEvent(new_isin_request_received, params = { "Amount":str(amount)}, notes = note )

        bp.Commit()

        try:
            send_isin_report("New", bp.Subject())
        except:
            print("Report was not sent.")

    else:
        failed_response_received = acm.FStateChartEvent('Failed Response Received')
        bp.HandleEvent(failed_response_received, params = None, notes = note )
        bp.Commit()


def topup_reduce_request_received(bp, success = True, note = None ):
    if success:
        action = gen_swift_functions.get_text_from_tag(':22F::CONF/STRA/', note[0])
        amount = float(gen_swift_functions.get_value_from_tag(':36B::QISS//FAMT/', note[0]).replace(',', '.'))
        if 'REDU' in action:
            amount = -amount
        topup_reduce_received = acm.FStateChartEvent('Topup Reduce Response Received')
        bp.HandleEvent(topup_reduce_received, params = {"Amount":str(amount)}, notes = note )
        bp.Commit()

        try:
            send_isin_report('Reduce' if 'REDU' in action else 'Topup', bp.Subject())
        except:
            print("Report was not sent.")
    else:
        failed_response_received = acm.FStateChartEvent('Failed Response Received')
        bp.HandleEvent(failed_response_received, params = None, notes = note )
        bp.Commit()


def deissue_request_received(bp, success = True, note = None ):
    if success:
        deissue_request_received = acm.FStateChartEvent('Deissue Response Received')
        amount = -float(gen_swift_functions.get_value_from_tag(':36B::QISS//FAMT/', note[0]).replace(',', '.'))
        bp.HandleEvent(deissue_request_received, params = {"Amount":str(amount)}, notes = note)
        bp.Commit()
    else:
        failed_response_received = acm.FStateChartEvent('Failed Response Received')
        bp.HandleEvent(failed_response_received, params = None, notes = note )
        bp.Commit()


'''
Moved to gen_swift_functions script - As these parsing functions would make more sense in a general location

* def get_msg_type(message):
* def get_trans_ref(message):
* def get_isin(message):
'''


def process_ack_nack(mtmessage):
    print 'Processing ACK/NACK'
    msg_type = gen_swift_functions.get_msg_type(mtmessage)
    trx_ref, bpstep_id = gen_swift_functions.get_trans_ref(mtmessage)
    state_chart = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]
    processes = acm.BusinessProcess.FindBySubjectAndStateChart(acm.FInstrument[int(trx_ref)], state_chart)
    if len(processes) == 1:
        bp = processes[0]
        cs = bp.CurrentStep()
        #Verify that bp_id on received SWIFT, was sent from last "To Be Sent" node
        if bpstep_id != '':
            max_iterations = 10
            cnt = 1
            step = cs.PreviousStep()
            while step.State().Name()[-10:].lower() != 'to be sent':
                step = step.PreviousStep()
                cnt += 1
                if cnt > max_iterations:
                    raise Exception('Could not find last "To Be Sent" state within 10 iterations back of Pending state')
            if int(step.Name()) != int(bpstep_id):
                raise Exception('Received message was not sent from previous "To Be Sent" state - Ignoring')
        if msg_type == '598-155':   #ACK Received for this type
            #process ack here....
            if bp.CanHandleEvent('ACK Received'):
                ack_received = acm.FStateChartEvent('ACK Received')
                bp.HandleEvent(ack_received, notes = [mtmessage] )
                bp.Commit()
        else:
            raise Exception('Unknown Message Type')
    else:
        raise Exception('Duplicates or No Instrument found in ISIN management State Chart, could not handle response message')


def isin_mgmt_incoming(mtmessage, msg_type, file=None):
    """
    Handle incoming MT message and update Business Process accordingly
    """

    global dis_instr_dict
    global dis_isin_messages

    list_dis_instr()

    action = gen_swift_functions.get_text_from_tag( ':22F::CONF/STRA/', mtmessage)

    ins = None
    bpstep_id = ''

    if action == ACTION['NEW'] and msg_type in ['598-154']:

        message_key = create_message_key(mtmessage)
        if message_key in dis_instr_dict :

            bp = dis_instr_dict[message_key]
            ins = bp.Subject()

            isin = gen_swift_functions.get_isin(mtmessage)
            external_id = gen_swift_functions.get_external_id(mtmessage)
            if ins and isin:
                dis_isin_messages.pop(message_key, None)
                ins.Isin(isin)
                if external_id is not None :
                    ins.ExternalId1(external_id)
                ins.Commit()
            else:
                dis_isin_messages[message_key] = file
                save_messages()
                Utils.Log(True, 'No instrument found for the message [MT%s] with message key [%s] ' % (msg_type, message_key) )
        else:
            dis_isin_messages[message_key] = file
            save_messages()
            Utils.Log(True, 'No instrument found for the message [MT%s] with message key [%s] ' % (msg_type, message_key))

    else:

        if msg_type in ['598-154', '598-902']:
            trx_ref, bpstep_id = gen_swift_functions.get_trans_ref_from_tag(':20C::RELA//', mtmessage)
        else:       #598-901 - Format Rejection message
            trx_ref, bpstep_id = gen_swift_functions.get_trans_ref_from_tag(':21:', mtmessage)
        state_chart = acm.FStateChart[DIS_ISIN_MGMT_BPS]
        if bpstep_id is None:
            raise Exception('Not ISIN Manangement Trx Ref %s' % trx_ref)

        ins = acm.FInstrument[int(trx_ref)]


    processes = None
    state_chart = DIS_ISIN_MGMT_STATE_CHART_NAME

    if ins is not None:
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(ins, state_chart)

    state_handling = {'Active':lambda *args, **kw_args: None, #If incoming swift message's trade is currently in Active state, i.e. not expecting a response, just ignore
            'TopUp Reduce Request Pending': topup_reduce_request_received,
            'DeIssue Request Pending':deissue_request_received,
            'New ISIN Request Pending':new_isin_request_received }

    if processes and len(processes) == 1:
        bp = processes[0]
        cs = bp.CurrentStep()

        #Verify that bp_id on received SWIFT, was sent from last "To Be Sent" node
        if bpstep_id != '' and cs.State().Name() != 'New ISIN Request Pending':
            max_iterations = 10
            cnt = 1
            step = cs.PreviousStep()
            while step.State().Name()[-10:].lower() != 'to be sent':
                step = step.PreviousStep()
                cnt += 1
                if cnt > max_iterations:
                    raise Exception('Could not find last "To Be Sent" state within 10 iterations back of Pending state')
            if int(step.Name()) != int(bpstep_id):
                raise Exception('Received message was not sent from previous "To Be Sent" state - Ignoring')
        #Check if the bp is still in awaiting ACK stage
        if bp.CurrentStep().State().Name()[-10:] == 'MQ ACKNACK':
            if bp.CanHandleEvent('ACK Received'):
                ack_received = acm.FStateChartEvent('ACK Received')
                bp.HandleEvent(ack_received, notes = [mtmessage])
                print 'Artificially applying an ACK received'
                bp.Commit()
        cstate = bp.CurrentStep().State().Name()
        if msg_type == '598-154':   #Confirmation
            state_handling[cstate](bp, success = True, note = [mtmessage])
        elif msg_type == '598-901': #Format Rejection
            state_handling[cstate](bp, success = False, note = ['901 - Format Rejection', mtmessage])
        elif msg_type == '598-902': #Content Rejection
            state_handling[cstate](bp, success = False, note = ['902 - Content Rejection', mtmessage])
        else:
            raise Exception('Unknown Message Type')
    else:
        raise Exception('Duplicates or No Instrument found in ISIN management State Chart, could not handle response message')


def get_message_function(message):
    """
    Function to get the function of the message.
    """
    msg_function = gen_swift_functions.get_text_from_tag(':23G:', message)
    return msg_function


def get_party_account(party, name):
    """
    Get the  account details of a party of account witb specific bank
    """
    sarb_acc = [account for account in party.Accounts() if account.CorrespondentBank().Name() == name]

    return len(sarb_acc) > 0 and sarb_acc[0] or None


def confirmation_touch(cf):
    confos = acm.FConfirmation.Select('cashFlow = %i status = Hold' %cf.Oid())
    for c in confos:
        c.Touch()
        c.Commit()


def update_cashflow_addinfo(cf, addinfo_list):

    try:
        cf = cf.StorageImage()
        for addinfovalues in addinfo_list:
            cf.AddInfoValue(addinfovalues[0], addinfovalues[1])

        cf.Commit()

    except Exception:

        raise RuntimeError('Could not commit dmeat add infos to cashflow: {oid}'.format(oid=cf.Oid()))


def update_capital_evntno(message):
    """
    Update capital event reference no
    """
    isin                   = get_isin(message)
    cap_evnt               = get_capital_event(message)
    record_date            = get_record_date(message)
    cash_flow_event_type         = get_cash_flow_event_type(message)
    pay_date               = get_pay_date(message)
    status                 = ''
    ins      = acm.FInstrument.Select01("isin = '%s' " % (isin), '')
    first_trd = GetFirstTrade(ins)
    if not first_trd:
        raise ValueError('None of the trades on the instrument {} qualify for Capital Event Update'.format(ins.Name()))

    if cash_flow_event_type == INTEREST:
        (start_date, end_date) = get_coupon_period(message)

    if ins.InsType() == 'Combination':
        comb_cashflows = get_combination_cash_flows(first_trd, pay_date, cash_flow_event_type)
        if comb_cashflows:
            for cf in comb_cashflows:
                if cf:
                    message_function = get_message_function(message)

                    if message_function in ['NEWM', 'REPL']:
                        isvalid = _update_cash_flow_add_info(cf, message)
                        _set_demat_pre_set_add_info(first_trd)
                        LOGGER.info('Trade Number [%i] updated' % (first_trd and first_trd.Oid() or 0))
                    LOGGER.info('Updated Capital Event Reference number [%s] on cash flow [%s]' %
                                (cap_evnt, str(cf.Oid())))
                else:
                    LOGGER.info('Exception: No cash flow found, Capital Event Reference number update failed')

    if cash_flow_event_type == REDEMPTION:
        if first_trd and first_trd.Acquirer().Name() in VALID_ACQUIRERS:
            _process_redemption_cashflow(ins, pay_date, cap_evnt, message)
    elif cash_flow_event_type in (PARTIAL_REDEMPTION, EARLY_REDEMPTION):
        if first_trd and first_trd.Acquirer().Name() in VALID_ACQUIRERS:
            _process_partial_and_early_redemption(ins, first_trd, pay_date, cap_evnt, cash_flow_event_type, message)
    else:
        try:
            cf = get_cashflow(ins, pay_date, cash_flow_event_type)
        except TypeError:
            cf = None

        if cf:
            cf_event_type = get_message_function(message)
            if cf_event_type in ['NEWM', 'REPL']:
                isvalid = _update_cash_flow_add_info(cf, message)
                at_addInfo.save(first_trd, 'MM_DEMAT_PRE_SETT', 'Yes')
                canCreatePayment = _check_if_payment_should_be_generated(ins, cf, cash_flow_event_type )
                if canCreatePayment and isvalid:
                    _create_payment(cf, ins, message)
                else:
                    LOGGER.info('Cannot create payment')
                LOGGER.info('Trade Number [%i] updated' % (first_trd and first_trd.Oid() or 0))
            LOGGER.info('Updated Capital Event Reference number [%s] on cash flow [%s]' % (cap_evnt, str(cf.Oid())))
        else:
            if cash_flow_event_type == INTEREST:
                _process_redemption_interest(ins, pay_date, cap_evnt, cash_flow_event_type, message)
            else:
                print 'Exception: No cash flow found, Capital Event Reference number update failed'


def _update_cash_flow_add_info(cf, message):


    isin = get_isin(message)
    cap_evnt = get_capital_event(message)
    record_date = get_record_date(message)
    cash_flow_event_type = get_cash_flow_event_type(message)
    (start_date, end_date) = get_coupon_period(message)
    status = ''
    ins = acm.FInstrument.Select01("isin = '%s' " % (isin), '')

    add_info_list = list()
    add_info_list.append(['Demat_CE_Reference', cap_evnt])
    add_info_list.append(['Demat_Record_Date', record_date])
    if cash_flow_event_type == INTEREST:
        add_info_list.append(['Demat_Coupon_Period', '%s/%s' % (start_date, end_date)])
    elif cash_flow_event_type == REDEMPTION:
        add_info_list.append(['Demat_Coupon_Period', 'REDEMPTION'])
    update_cashflow_addinfo(cf, add_info_list)

    isvalid = True

    if cash_flow_event_type in [INTEREST, REDEMPTION]:

        pay_date = get_pay_date(message)
        pay_date = datetime.strptime(pay_date, '%Y%m%d')
        pay_date = pay_date.strftime('%Y-%m-%d')

        isvalid = isvalid and pay_date == acm_date(cf.PayDate())
        if not isvalid:
            status = ' Pay Date Mismatch'

        authorised_amount = dis_authorised_amount(ins)
        coupon_payment = ENTITLED_COUPON_PAYMENT(cf)
        strate_entl_amount = get_entl_amount(message)

        coupon_payment = coupon_payment and coupon_payment[3:]
        coupon_payment = coupon_payment.replace(',', '.')

        if coupon_payment is None:
            coupon_payment = 0.0

        validate_amount = 0.0

        if cash_flow_event_type == INTEREST:
            try:
                validate_amount = float(coupon_payment)
            except Exception, ex:
                print 'Payment : Exception ', ex
        elif cash_flow_event_type == REDEMPTION:
            validate_amount = authorised_amount

        cpn_calc_diff = validate_amount - strate_entl_amount
        cpn_valid = (cpn_calc_diff >= 0.0 and cpn_calc_diff < TOLERANCE)
        # Payment needs to be made even though there is a payment mismatch
        isvalid = isvalid
        if not cpn_valid:
            status = status + '| Calculation mismatch'

    validflag = isvalid and 'Yes' or 'No'
    at_addInfo.save(cf, 'Demat_Calc_Approvl', validflag)
    if status:
        at_addInfo.save(cf, 'Demat_Coupon_Valida', status)
    cf.Commit()
    confirmation_touch(cf)
    return isvalid


def _check_if_payment_should_be_generated(ins, cf, cash_flow_event_type):
    first_trd = GetFirstTrade(ins)
    payment_amount = _get_payment_amount(cash_flow_event_type, ins, cf)
    instrument = first_trd.Instrument()
    if instrument is None:
        LOGGER.info('No instrument')
        return False
    if cash_flow_event_type not in [INTEREST, REDEMPTION]:
        LOGGER.info('Cash Flow Type is invalid')
        return False
    if instrument.IssuingPayingAgent() is None:
        LOGGER.info('Issuing Paying Agent is blank')
        return False
    if payment_amount == 0.0:
        LOGGER.info('Coupon Amount is zero')
        return False
    return True


def _get_payment_type(cash_flow_event_type):
    payment_type = None
    if cash_flow_event_type == INTEREST:
        payment_type = COUPON

    elif cash_flow_event_type == REDEMPTION:
        payment_type = REDEMPTION_T
    return payment_type


def _get_payment_rec_type(cash_flow_event_type):
    payment_rec_type = None
    if cash_flow_event_type == INTEREST:
        payment_rec_type = COUPON_RECEIVABLE

    elif cash_flow_event_type == REDEMPTION:
        payment_rec_type = REDEMPTION_RECEIVABLE_T
    return payment_rec_type


def _get_payment_amount(cash_flow_event_type, ins, cf):
    payment_amount = 0
    unissued_amount = dis_unissued_amount(ins)
    couponamount = dis_coupon_amount_calc(cf)
    if cash_flow_event_type == INTEREST:
        payment_amount = couponamount

    elif cash_flow_event_type == REDEMPTION:
        payment_amount = unissued_amount
    return payment_amount


def _set_demat_pre_set_add_info(trade):
    add_info = at_addInfo.get(trade, 'MM_DEMAT_PRE_SETT')
    if add_info is None:
        at_addInfo.save(trade, 'MM_DEMAT_PRE_SETT', 'Yes')
    elif add_info.FieldValue() == 'No':
        at_addInfo.save(trade, 'MM_DEMAT_PRE_SETT', 'Yes')
    elif add_info.FieldValue() == 'Yes':
        trade.Touch()
        trade.Commit()


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
    cash_flows = instrument.Legs()[0].CashFlows()
    if instrument.InsType() == 'Combination':
        cash_flows = _get_combination_cashflows(instrument)
    for cash_flow in cash_flows:
        if cash_flow.CashFlowType() != 'Fixed Amount':
            continue
        if cash_flow.PayDate() != formatted_date:
            continue
        return cash_flow

    raise ValueError('Could not find Redemption CashFlow on instrument {}'.format(instrument.Name()))


def _get_combination_cashflows(instrument):
    """
    Gets all applicable cash flows for the combination instrument
    """
    trade = GetFirstTrade(instrument)
    money_flows = trade.MoneyFlows()
    cash_flows = list()
    for money_flow in money_flows:
        cash_flow = money_flow.SourceObject()
        if money_flow.Type() == 'Fixed Amount' and cash_flow.IsKindOf(acm.FCashFlow):
            cash_flows.append(cash_flow)

    return cash_flows


def _process_partial_and_early_redemption(ins, first_trd, pay_date, cap_evnt, cash_flow_type, message):
    """
    Processes Partial and Early Redemption Cash FLows
    on incoming 564
    """
    reducing_amount, decimal = get_reducing_amount(message)
    total_reducing_amount = ",".join([reducing_amount, decimal]).replace(',', '.')
    if decimal in ['', None]:
        total_reducing_amount = reducing_amount
    if not _is_redemption_payment_available(first_trd, cap_evnt, cash_flow_type, total_reducing_amount, pay_date):
        _create_redemption_payment(ins, pay_date, cap_evnt, cash_flow_type, message, total_reducing_amount)
    _create_mt564_confirmation(ins, pay_date, cash_flow_type)


def _is_redemption_payment_available(first_trd, cap_evnt, cash_flow_type, total_reducing_amount, pay_date):
    """
    Checks for available payments to prevent duplicate payments
    """
    pay_date = time.strptime(pay_date, '%Y%m%d')
    formatted_date = acm.Time.DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday)
    payments = first_trd.Payments()
    for payment in payments:
        if payment.Text() != cap_evnt:
            continue
        if payment.Amount() != total_reducing_amount:
            continue
        if payment.PayDay() != formatted_date:
            continue
        if payment.Type() == 'Early Redemption' and cash_flow_type == EARLY_REDEMPTION:
            return True
        if payment.Type() == 'Partial Redemption' and cash_flow_type == PARTIAL_REDEMPTION:
            return True

    return False


def _process_redemption_interest(ins, pay_date, cap_evnt, cash_flow_type, message):
    """
    Processes Partial and Early Redemption Interest Cash FLows
    on incoming 564
    """
    interest_amount = get_entl_amount(message)
    _create_redemption_payment(ins, pay_date, cap_evnt, cash_flow_type, message, interest_amount)
    _create_mt564_confirmation(ins, pay_date, cash_flow_type)


def _create_redemption_payment(ins, pay_date, cap_evnt, cash_flow_type, message, amount):
    """
    Creates the PCAL or MCAL Fixed Amount Cashflow
    """
    pay_date = time.strptime(pay_date, '%Y%m%d')
    formatted_date = acm.Time.DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday)
    record_date = get_record_date(message)
    first_trade = GetFirstTrade(ins)
    instrument = first_trade.Instrument()
    paying_agent = instrument.IssuingPayingAgent()
    currency = instrument.Currency()
    sarb_account = get_party_account(paying_agent, PTY_SARB)
    direction = 1
    if first_trade.Quantity() < 0:
        direction = -1
    try:
        payment = acm.FPayment()
        payment.Amount(float(amount) * direction)
        payment.PayDay(formatted_date)
        payment.Party(paying_agent)
        payment.Trade(first_trade)
        payment.ValidFrom(acm.Time.DateToday())
        payment.Currency(currency)
        payment.Account(sarb_account)
        payment.Text(cap_evnt)
        if cash_flow_type == EARLY_REDEMPTION:
            payment.Type('Early Redemption')
        elif cash_flow_type == PARTIAL_REDEMPTION:
            payment.Type('Partial Redemption')
        elif cash_flow_type == INTEREST:
            start_date, end_date = get_coupon_period(message)
            coupon_period = str(start_date) + '/' + str(end_date)
            rate = get_coupon_rate(message)
            payment.Type('Coupon')
            payment.AddInfoValue('REDM_Coupon_Period', coupon_period)
            payment.AddInfoValue('REDM_Coupon_Rate', rate)
        else:
            raise ValueError('Cash Flow Event Type {} not supported for Redemption Processing'.format(cash_flow_type))
        payment.AddInfoValue('REDM_Record_Date', record_date)
        payment.AddInfoValue('REDM_Type', cash_flow_type)
        payment.Commit()
        success_message = 'Updated Capital Event Reference number {cap_event}'
        success_message += ' on Payment {p_oid} on Instrument {ins}'
        LOGGER.info(success_message.format(cap_event=cap_evnt, p_oid=payment.Oid(), ins=ins.Name()))
    except Exception as e:
        error_message = 'Failed to process {} instruction on instrument {}. Could not create Redemption Payment'
        LOGGER.exception(error_message.format(cash_flow_type, ins.Name()))
        raise e


def _create_mt564_confirmation(ins, pay_date, cash_flow_type):
    """
    Create MT564 Confirmation
    """
    pay_date = time.strptime(pay_date, '%Y%m%d')
    formatted_date = acm.Time.DateFromYMD(pay_date.tm_year, pay_date.tm_mon, pay_date.tm_mday)
    confirmation_owner_trade = GetFirstTrade(ins)
    document_event_name = 'Demat PreSettle Conf'
    from_date = acm.Time.DateToday()
    create_document_confirmation(document_event_name, confirmation_owner_trade,
                                 from_date=from_date, to_date=formatted_date,
                                 redemption_event_type=cash_flow_type)


def get_reducing_amount(message):
    """
    Gets the reducing amount per CSD participant
    """
    pmt_pattern = '\{4.*:36B::ENTL//FAMT/(\d{1,12}),(\d{0,2}).*\}'
    pmt_m = re.search(pmt_pattern, message, re.DOTALL)

    return pmt_m.group(1), pmt_m.group(2)


def get_coupon_rate(message):
    """
    Gets  the coupon rate from MT564
    """
    rate_pattern = '\.*:92A::INTR//(\d*,\d*)'
    rate_match = re.search(rate_pattern, message, re.DOTALL)

    return rate_match.group(1)


def trade_mgmt_incoming(mtmessage, msg_type, file=None):
    """
    Handle incoming MT message and
    update Business Process accordingly
    """
    if msg_type == '564':
        update_capital_evntno(mtmessage)


def sendNotificationMail(exception):
    import smtplib
    config_dict = demat_config.get_config()
    notification_emails = config_dict['mq_connection_notifications']
    FROM = 'ABCapITRTBFrontArena@absacapital.com'
    MSG = str(exception)
    HOST = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(), 'mailServerAddress').Value()
    if not HOST:
        raise Exception("Could not initialise the smtp Host")
    try:
        ENVIRONMENT = ' - ' + acm.FInstallationData.Select('').At(0).Name()
    except:
        ENVIRONMENT = ''
    SUBJECT = 'Front Arena Outgoing Custom Swift Failure - ' + ENVIRONMENT
    for address in notification_emails:
        BODY = "\r\n".join([
            "From: %s" % FROM,
            "To: %s" % address,
            "Subject: %s" % SUBJECT,
            "", MSG])

        server = smtplib.SMTP(HOST)
        server.sendmail(FROM, address, BODY)
        server.quit()


def _create_payment(cf, ins, message):
    first_trd = GetFirstTrade(ins)
    cap_evnt = get_capital_event(message)
    cash_flow_event_type = get_cash_flow_event_type(message)

    payment_type = _get_payment_type(cash_flow_event_type)
    payment_amount = _get_payment_amount(cash_flow_event_type, ins, cf)
    payment_rec_type = _get_payment_rec_type(cash_flow_event_type)

    firstins = first_trd.Instrument()
    payingAgent = firstins.IssuingPayingAgent()
    sarb_account = get_party_account(payingAgent, PTY_SARB)
    payments = acm.FPayment.Select(" trade = %i  and payDay = '%s' and  type = '%s' " % (
        first_trd.Oid(), cf.PayDate(), payment_type))

    if payments.Size() == 0:

        payment = acm.FPayment()
        print 'Creating First Payment.. '
    else:
        payment = payments.At(0)
        print 'Payment [%s] already exists. Updating payment object ..' % (payment_type)

    payment.Amount(-1 * payment_amount)
    payment.Currency(first_trd.Currency())
    payment.PayDay(cf.PayDate())
    payment.Party(firstins.IssuingPayingAgent())
    payment.Trade(first_trd)
    payment.Type(payment_type)
    payment.Account(sarb_account)
    payment.Text(cap_evnt)
    payment.Commit()

    payments = acm.FPayment.Select(" trade = %i  and payDay = '%s' and  type = '%s' " % (
        first_trd.Oid(), cf.PayDate(), COUPON_RECEIVABLE))

    if payments.Size() == 0:
        payment = acm.FPayment()
        print 'Creating Second Payment.. '
    else:
        payment = payments.At(0)
        print 'Payment [%s] already exists. Updating payment object ..' % (payment_rec_type)

    payment.Amount(payment_amount)
    payment.Currency(first_trd.Currency())
    payment.PayDay(cf.PayDate())
    payment.Party(firstins.IssuingPayingAgent())
    payment.Trade(first_trd)
    payment.Type(payment_rec_type)
    payment.Account(sarb_account)
    payment.Text(cap_evnt)
    payment.Commit()

