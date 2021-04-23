"""-----------------------------------------------------------------------------
PURPOSE                 :   This will query relevant Business Process.
                            If an entry exists on either one of these states,
                            * Ready
                            * TopUpReduce To Be Sent
                            * DeIssue To Be Sent

                            The ATS will process the instrument, generate a SWIFT MT message, place it on MQ, and apply the relevant event:
                            "new ISIN request sent"
                            "Topup Deissue request sent"
                            "Deissue Request sent"
                            on the Business Process + Add the sent SWIFT message as a NOTE on the event for historical purposes.
DEPATMENT AND DESK      :   MM
REQUESTER               :   Linda Breytenbach
DEVELOPER               :   Rohan van der Walt
CR NUMBER               :
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no       Developer       Description
--------------------------------------------------------------------------------
2014-10-30  XXXXXXX         Rohan vd Walt   Initial Implementation
2016-11-28  CHNG0004147753  Gabriel Marko   send_isin_request reworked
2017-03-28  CHNG0004439301  Gabriel Marko   DEMAT ISIN confirmation email
2017-12-11  CHNG0005220511  Manan Ghosh     DIS go-live
2019-07-22  Upgrade2018     Jaysen Naicker  Make code 2018 compatible
"""


import acm, ael
import datetime
import demat_swift_mt598
import gen_mq
import FOperationsUtils as Utils
import traceback
import re
import gen_swift_functions
import demat_config

from pprint import pprint
from at_ael_variables import AelVariableHandler
from demat_isin_mgmt_menex import current_authorised_amount
from demat_isin_mgmt_confirmation import send_isin_report
from at_logging import getLogger

LOGGER = getLogger(__name__)
MMSS_ISIN_REQUEST_STATE_CHART_NAME = 'MM ISIN Management'
SYSTEM_GROUPS = ['Integration Process']

ACTION = {
    "NEW" : "ISSU",
    "TOPUP" : "TOPU",
    "REDUCE" : "REDU",
    "DEISSUE" : "DISS"
}

def create_mmss_isin_request_statechart(replace_existing = True):
    try:
        if replace_existing:

            state_chart = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]
            if state_chart:
                processes = acm.BusinessProcess.FindBySubjectAndStateChart(None, state_chart)
                for p in processes:
                    p.Delete()
                state_chart.Delete()
                print "REMOVED"
            else:
                print 'State Chart not removed, could not be found with name:', MMSS_ISIN_REQUEST_STATE_CHART_NAME

        state_chart = acm.FStateChart(name = MMSS_ISIN_REQUEST_STATE_CHART_NAME)
        state_chart.BusinessProcessesPerSubject('Single Active') # Can be Single or Unlimited
        state_chart.Commit()

        state_chart.CreateState('New ISIN Request to be sent')
        state_chart.CreateState('New ISIN Request MQ ACKNACK')
        state_chart.CreateState('New ISIN Request Pending')
        state_chart.CreateState('TopUp Reduce Request to be sent')
        state_chart.CreateState('TopUp Reduce Request MQ ACKNACK')
        state_chart.CreateState('TopUp Reduce Request Pending')
        state_chart.CreateState('DeIssue Request to be sent')
        state_chart.CreateState('DeIssue Request MQ ACKNACK')
        state_chart.CreateState('DeIssue Request Pending')
        state_chart.CreateState('DeIssued')
        state_chart.CreateState('Active')
        state_chart.CreateState('New ISIN Failed Response')
        state_chart.CreateState('Topup Reduce Failed Response')
        state_chart.CreateState('Deissue Failed Response')
        state_chart.Commit()

        ready_state = state_chart.ReadyState()
        states = state_chart.StatesByName()
        state_new_isin_req_tbs = states['New ISIN Request to be sent']
        state_new_isin_req_ack = states['New ISIN Request MQ ACKNACK']
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

        new_isin_event = acm.FStateChartEvent('Request ISIN')
        new_isin_request_sent_event = acm.FStateChartEvent('Sent ISIN Request')
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

        ready_state.CreateTransition(new_isin_event, state_new_isin_req_tbs)
        state_new_isin_req_tbs.CreateTransition(new_isin_request_sent_event, state_new_isin_req_ack)
        state_new_isin_req_ack.CreateTransition(ack_event, state_new_isin_req_waiting)
        state_new_isin_req_ack.CreateTransition(nack_event, state_failed_new_request)
        state_new_isin_req_waiting.CreateTransition(new_isin_request_received_event, state_active)
        state_new_isin_req_waiting.CreateTransition(failed_response_event, state_failed_new_request)

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

        state_failed_new_request.CreateTransition(retry_event, state_new_isin_req_tbs)
        #state_failed_new_request.CreateTransition(cancel_event, state_active)      #Cancel not possible on New Isin Request Failed. - Only Resend

        state_failed_amend_request.CreateTransition(retry_event, state_amend_req_tbs)
        state_failed_amend_request.CreateTransition(cancel_event, state_active)

        state_failed_deissue_request.CreateTransition(retry_event, state_deissue_req_tbs)
        state_failed_deissue_request.CreateTransition(cancel_event, state_active)

        state_active.CreateTransition(amend_event, state_amend_req_tbs)
        state_active.CreateTransition(deissue_event, state_deissue_req_tbs)
        state_chart.Commit()

    except Exception as error:
        LOGGER.error('Creation of State Chart Failed')
        LOGGER.exception(error)


def new_isin_request_tbs(bp):
    new_isin_request_sent_event = acm.FStateChartEvent('Sent ISIN Request')

    try:
        init_amount = float(bp.CurrentStep().DiaryEntry().Parameters()['Initial Amount'])
    except Exception as error:
        print 'Error: Init amount paramter not understood\nUsing 0.0'
        LOGGER.exception(error)
        init_amount = 0.0

    bp_id = bp.Oid()
    param_dict = { "Initial Amount": init_amount }
    try:
        #Place on MQ
        mq_mess = gen_mq.MqMessenger('MeridianOutCustMq')
        try:
            swift_msg = str(demat_swift_mt598.from_instrument(bp.Subject(), ACTION['NEW'], init_amount, bp_id))
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
        sendNotificationMail(ex)



def topup_reduce_request_tbs(bp):
    amend_amount = float(bp.CurrentStep().DiaryEntry().Parameters()['Amend Amount'])
    bp_id = bp.Oid()
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
            swift_msg = str(demat_swift_mt598.from_instrument(bp.Subject(), action, abs(amend_amount), bp_id))
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
        sendNotificationMail(ex)


def deissue_request_tbs(bp):
    deissue_request_sent_event = acm.FStateChartEvent('Sent Deissue Request')
    bp_id = bp.Oid()
    try:
        #Place on MQ
        mq_mess = gen_mq.MqMessenger('MeridianOutCustMq')
        try:
            swift_msg = str(demat_swift_mt598.from_instrument(bp.Subject(), ACTION['DEISSUE'], current_authorised_amount(bp.Subject()), bp_id))
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
        sendNotificationMail(ex)


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
                sendNotificationMail(ex)
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
            # send_isin_report mustn't block the main process
            # in case the email isn't sent demat_resend_isin_email can be used.
            # The error details are logged by send_isin_report
            print("ERROR: Report was not sent.")

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
            # send_isin_report mustn't block the main process
            # in case the email isn't sent demat_resend_isin_email can be used.
            # The error details are logged by send_isin_report
            print("ERROR: Report was not sent.")
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
        cstate = cs.State().Name()
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
            if int(step.Oid()) != int(bpstep_id):
                LOGGER.warning('Received message was not sent from previous "To Be Sent" state - Ignoring')

        if msg_type == '598-155':   #ACK Received for this type
            #process ack here....
            if bp.CanHandleEvent('ACK Received'):
                ack_received = acm.FStateChartEvent('ACK Received')
                bp.HandleEvent(ack_received, notes = [mtmessage] )
                bp.Commit()
        else:
            LOGGER.warning('Unknown Message Type {msg_type}. ACK/NACK message type not handled'.format(msg_type=msg_type))
    else:
        LOGGER.warning('Duplicates or No Instrument found in ISIN management State Chart, could not handle response message')

def isin_mgmt_incoming(mtmessage, msg_type):
    '''
    Handle incoming MT message and update Business Process accordingly
    '''

    print "isin_mgmt_incoming", msg_type

    if msg_type in ['598-154', '598-902']:
        trx_ref, bpstep_id = gen_swift_functions.get_trans_ref_from_tag(':20C::RELA//', mtmessage)
    else:       #598-901 - Format Rejection message
        trx_ref, bpstep_id = gen_swift_functions.get_trans_ref_from_tag(':21:', mtmessage)
    state_chart = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]
    if bpstep_id is None:
        LOGGER.warning('Trx Ref {trx_ref} Not Handled by ISIN Management ..Skipping ')
        return

    ins = acm.FInstrument[int(trx_ref)]
    processes = acm.BusinessProcess.FindBySubjectAndStateChart(ins, state_chart)

    state_handling = {
        'Active':lambda *args, **kw_args: None, #If incoming swift message's trade is currently in Active state, i.e. not expecting a response, just ignore
        'New ISIN Request Pending': new_isin_request_received,
        'TopUp Reduce Request Pending': topup_reduce_request_received,
        'DeIssue Request Pending':deissue_request_received
    }

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
                    LOGGER.warning('Could not find last "To Be Sent" state within 10 iterations back of Pending state')
                    break
            if int(step.Oid()) != int(bpstep_id):
                message = 'Received message of type {msg_type} was not sent from previous "To Be Sent" state - Ignoring'
                LOGGER.warning(message.format(msg_type=msg_type))

        #Check if the bp is still in awaiting ACK stage
        if bp.CurrentStep().State().Name()[-10:] == 'MQ ACKNACK':
            if bp.CanHandleEvent('ACK Received'):
                ack_received = acm.FStateChartEvent('ACK Received')
                bp.HandleEvent(ack_received, notes = [mtmessage])
                LOGGER.info('Artificially applying an ACK received for Business Process with id {oid}'.format(oid=bp.Oid()))
                bp.Commit()
        cstate = bp.CurrentStep().State().Name()
        print ("bp: %s, cstate: %s") % (bp.Oid(), cstate)
        if msg_type == '598-154':   #Confirmation
            state_handling[cstate](bp, success = True, note = [mtmessage])
        elif msg_type == '598-901': #Format Rejection
            state_handling[cstate](bp, success = False, note = ['901 - Format Rejection', mtmessage])
        elif msg_type == '598-902': #Content Rejection
            state_handling[cstate](bp, success = False, note = ['902 - Content Rejection', mtmessage])
        else:
            LOGGER.warning('Unknown Message Type {msg_type}.Message type not handled'.format(msg_type=msg_type))
    else:
        LOGGER.warning('Duplicates or No Instrument found in ISIN management State Chart, could not handle response message')
    LOGGER.info('Processing Done Successfully')


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

#TESTING

response1 = """{1:F01ZYANZAJ0GXXX5155108779}
{2:O598ABSAZAJ0XMG1N}
{3:{108:53856335MM30C002}}
{4:
:20:4892925-15656
:12:901
:77E:
:79:7303/35B
7301/22F
7301/98A}"""

response2 = """{1:F01ABSAZAJ0AMG19660172982}{2:O5981751170816ZYANZAJ0DXXX64314299631708161751N}{3:{108:05768691MS10F002}}{4:
:20:1502725874559
:12:154
:77E:
:16R:GENL
:20C::RELA//6985013-8349117
:22F::CONF/STRA/ISSU
:16S:GENL
:16R:MMID
:95R::CSDP/STRA/ZA100019
:95R::ISSR/STRA/ZA700090
:95R::ISSA/STRA/ZA600200
:35B:ISIN ZAM004550666
ABPLNCD201808103IJ03XXXXPLP0,10000
:36B::QISS//FAMT/1000,
:97B::SAFE/STRA/IORT/10003176
:16R:FIA
:22F::PFRE/STRA/ISDF
:12A::CATG//3
:22H::TYPE//LNCD
:98A::MATU//20180816
:98A::ISSU//20170816
:22F::RTYP/STRA/VLIN
:36B::MINO//FAMT/1,
:17B::WITI//N
:17B::FCPM//Y
:17B::CPMI//Y
:17B::ACPC//N
:17B::ACPO//Y
:17B::OVER//N
:14F:ZAR-JIBAR3
:25:PLUS-0,1-PRCT
:22F::CCFR/STRA/NONE
:22F::RESF/STRA/ISDF
:16R:CRDDET
:98A::RESD//20171110
:98A::RESD//20180212
:98A::RESD//20180510
:16S:CRDDET
:16R:CPDDET
:98A::PAYD//20171110
:98A::PAYD//20180212
:98A::PAYD//20180510
:98A::PAYD//20180810
:16S:CPDDET
:16S:FIA
:16S:MMID
-}"""

#isin_mgmt_incoming(response2)
