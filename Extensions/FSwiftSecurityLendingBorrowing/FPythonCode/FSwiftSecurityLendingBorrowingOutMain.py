"""----------------------------------------------------------------------------
MODULE
    FSwiftSecurityLendingBorrowingOutMain : FSwiftSecurityLendingBorrowingOutMain for listening business process updates
    and settlement updates.

FUNCTION
    process_bpr_step_update()
        Handles the business process updates
    process_settlements_update()
        Handles the settlement updates

VERSION: 2.1.1-0.5.2995

RESTRICTIONS/LIMITATIONS:
    1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
    2. This module is not customizable.
    3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import acm
import amb
import time
import FSwiftOperationsAPI
import FSwiftWriterLogger
import FSwiftCustomMessageCalculator
from FSwiftServiceSelector import bypass_Swift_Solutions
from FSwiftWriterUtils import ShouldDocumentsBeDeleted, RemoveOperationsDocument, InDocumentCreationStatus,\
    IsMissingMTDocument, InSendDocumentStatus, InOperationsDocumentCreationStatus, CreateOperationsDocument,\
    create_business_process_for, get_ack_nak_subject, append_mt_types_added_by_customer
SETTLE_STATUS_RELEASED = 'Released'
SETTLE_STATUS_PEND_CANC = 'Pending Cancellation'
try:
    SettlementStatus = FSwiftOperationsAPI.GetSettlementStatusEnum()
    SETTLE_STATUS_RELEASED = SettlementStatus.RELEASED
    SETTLE_STATUS_PEND_CANC = SettlementStatus.PENDING_CANCELLATION
except:
    pass
import FSwiftMLUtils
import FSwiftWriterUtils
import FSwiftSecurityLendingBorrowingOutProcessing
pkg_name = 'FSwiftSecurityLendingBorrowingOut'

notifier = FSwiftWriterLogger.FSwiftWriterLogger('SBL', pkg_name+'Notify_Config')

SUPPORTED_MT_MESSAGE = ['MT598_130', 'MT598_131', 'MT598_132']
"""Removed below line because it does not support messages which contain '_' in the name. You can directly add the supported message types in above list.  """
#SUPPORTED_MT_MESSAGE = append_mt_types_added_by_customer(SUPPORTED_MT_MESSAGES,pkg_name+'Generation_Config')

SUPPORTED_MX_MESSAGE = []

CONFIG_PARAM = FSwiftMLUtils.Parameters('FSwiftWriterAMBConfig')
swift_solution_params = FSwiftMLUtils.Parameters('FSwiftSolutionConfig')

FSecurityLendingBorrowingOut_CONFIG_PARAM = FSwiftMLUtils.Parameters(pkg_name+'_Config')
FSecurityLendingBorrowingOutgoingMsg_QUEUE = []


def CreateAMBAMessageFromString(string):
    messageBuffer = amb.mbf_create_buffer_from_data(string)
    messageObj = messageBuffer.mbf_read()
    ambaMessage = FSwiftOperationsAPI.AMBAMessage(messageObj)
    return ambaMessage


state_chart_name_list = set()
for msg in SUPPORTED_MT_MESSAGE:
    try:
        state_chart_name_list.add(FSwiftMLUtils.get_state_chart_name_for_mt_type(msg, 'Out'))
    except Exception, e:
        notifier.ERROR("Exception while getting state chart : %s"%str(e))
        notifier.DEBUG(str(e), exc_info=1)

def start():
    """ start function for the module FSecuritySettlementOutMain. User need to add subscription here """
    init_amb_reader()

def work():
    """work function for module FSecuritySettlementOutMain """
    process_messages_from_amb()


def event_reader_cb(reader_channel, event, arg):
    """callback function that is called to process each message"""
    event_string = amb.mb_event_type_to_string(event.event_type)
    if event_string == 'Message':
        copy_of_msg = amb.mb_copy_message(event.message)
        msg_id = amb.mb_last_write_message_id(reader_channel)
        msg_subject = event.message.subject
        if msg_subject != get_ack_nak_subject():
            FSecurityLendingBorrowingOutgoingMsg_QUEUE.append((msg_id, copy_of_msg))

def init_amb_reader():
    """ Create AMB reader"""
    global FSECURITY_LENDING_BORROWING_OUTGOING_READER
    FSECURITY_LENDING_BORROWING_OUTGOING_READER = getattr(FSecurityLendingBorrowingOut_CONFIG_PARAM, 'SecLendingBorrowingOut_AMBReceiver', None)
    amb_reader_inited = False
    try:
        FSECURITY_LENDING_BORROWING_OUTGOING_READER = amb.mb_queue_init_reader(FSECURITY_LENDING_BORROWING_OUTGOING_READER, event_reader_cb, None)
        notifier.INFO("Reader %s initialized" % str(FSECURITY_LENDING_BORROWING_OUTGOING_READER))

        bpr_subject = getattr(swift_solution_params, 'AMBASenderSource', None) + '/BUSINESSPROCESS'
        amb.mb_queue_enable(FSECURITY_LENDING_BORROWING_OUTGOING_READER, bpr_subject)

        settlement_subject = getattr(swift_solution_params, 'AMBASenderSource', None) + '/SETTLEMENT'
        amb.mb_queue_enable(FSECURITY_LENDING_BORROWING_OUTGOING_READER, settlement_subject)

        notifier.INFO("Subscribed to subject %s" % bpr_subject)
        notifier.INFO("Subscribed to subject %s" % settlement_subject)

        amb_reader_inited = True
    except Exception, error:
        notifier.ERROR("Could not initialize amb reader <'%s'>. App will now exit. %s"%(FSECURITY_LENDING_BORROWING_OUTGOING_READER, error))
        notifier.DEBUG(str(error), exc_info=1)
    return amb_reader_inited


def process_messages_from_amb():
    """ process messges from amb"""
    handle_outgoing_settlement_messages()

def handle_outgoing_settlement_messages():
    """ handle outgoing settlement messages"""
    counter = 1
    while list(FSecurityLendingBorrowingOutgoingMsg_QUEUE):
        try:
            mt_type = ''
            msg_id = FSecurityLendingBorrowingOutgoingMsg_QUEUE[0][0]
            msg_copy = FSecurityLendingBorrowingOutgoingMsg_QUEUE[0][1]
            buf = amb.mbf_create_buffer_from_data(msg_copy.data_p)
            msg = buf.mbf_read()
            amba_msg = CreateAMBAMessageFromString(msg.mbf_object_to_string())
            type_of_update = amba_msg.GetTypeOfUpdate()
            updated_table = amba_msg.GetNameOfUpdatedTable()
            tables = amba_msg.GetTableAndChildTables()
            if updated_table == 'BUSINESSPROCESS':
                bpr_table_lst = amba_msg.GetTablesByName(tables, 'BUSINESSPROCESS')
                if not bpr_table_lst:
                    bpr_table_lst = amba_msg.GetTablesByName(tables, 'BusinessProcess')
                    if not bpr_table_lst:
                        bpr_table_lst = amba_msg.GetTablesByName(tables, 'B92_BUSINESSPROCESS')
                if bpr_table_lst:
                    bpr_table = bpr_table_lst[0]
                    has_step_changed, current_step_according_to_amba = FSwiftMLUtils.get_current_step_according_to_amba(amba_msg, bpr_table, type_of_update)
                    bpr_oid = bpr_table.GetAttribute('SEQNBR').GetCurrentValue()
                    bpr_obj = acm.FBusinessProcess[bpr_oid]
                    if bpr_obj.CurrentStep().State().StateChart().Name() in state_chart_name_list:
                        if type_of_update == 'INSERT' or has_step_changed:
                            ext_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object_from_bpr(bpr_obj)
                            mt_type = FSwiftMLUtils.FSwiftExternalObject.get_mt_type_from_external_object(ext_obj)
                            if mt_type in SUPPORTED_MT_MESSAGE:
                                if int(current_step_according_to_amba) == bpr_obj.CurrentStep().Oid():
                                    process_bpr_step_update(bpr_obj, mt_type)
                                elif int(current_step_according_to_amba) > bpr_obj.CurrentStep().Oid():
                                    notifier.WARN("{0} ATS could not get updated business process object, will try again after 8 seconds....".format(mt_type))
                                    if counter < 3:
                                        counter = counter + 1
                                        time.sleep(8)
                                        continue
                                    else:
                                        notifier.WARN("%s ATS did not get updated business process object. Skipping processing of AMB message id %d" % (mt_type, msg_id))
            elif updated_table == 'SETTLEMENT':
                settlement_table_lst = amba_msg.GetTablesByName(tables, 'SETTLEMENT')
                if not settlement_table_lst:
                    settlement_table_lst = amba_msg.GetTablesByName(tables, 'Settlement')
                    if not settlement_table_lst:
                        settlement_table_lst = amba_msg.GetTablesByName(tables, 'B92_SETTLEMENT')
                if settlement_table_lst:
                    settlement_table = settlement_table_lst[0]
                    settlement_oid = settlement_table.GetAttribute('SEQNBR').GetCurrentValue()
                    settlement_status = settlement_table.GetAttribute('STATUS').GetCurrentValue()
                    settlement_obj = acm.FSettlement[settlement_oid]
                    if settlement_obj:
                        process_settlements_update(settlement_obj, settlement_status)
        except Exception, error:
            notifier.ERROR("%s Exception occurred while swift message processing: %s" % (mt_type, str(error)))
            notifier.DEBUG(str(error), exc_info=1)

        FSecurityLendingBorrowingOutgoingMsg_QUEUE.pop(0)
        counter = 1
        amb.mb_queue_accept(FSECURITY_LENDING_BORROWING_OUTGOING_READER, msg_copy, "okay")

def should_handle_this_update(fObject, settlement_status):
    """Returns mt_type if all conditions are met, otherwise returns False"""
    mt_types = []
    mt_type = None
    try:
        if settlement_status in ['SETTLEMENT_STATUS_RELEASED', 'SETTLEMENT_STATUS_PENDING_CANCELLATION', SETTLE_STATUS_RELEASED, SETTLE_STATUS_PEND_CANC]:
            mt_type = FSwiftMLUtils.calculate_mt_type_from_acm_object(fObject)
            #message_types = FSwiftCustomMessageCalculator.get_applicable_mt_type(fObject, mt_type)
            #print message_types
            # when mtType not in SUPPORTED_MT_MESSAGE means that this module need not handle updates of these message types.
            #for mt_type in message_types:
            mt_type = mt_type.split('-')[0]
            if FSwiftWriterUtils.swift_format_of_message(mt_type) == 'MT':
                mt_type = 'MT' + str(mt_type)
            # when mtType not in SUPPORTED_MT_MESSAGE means that this module need not handle updates of these message types.
            if mt_type not in SUPPORTED_MT_MESSAGE:
                return False
            
            message_generation_on = FSwiftWriterUtils.is_outgoing_message_generation_on_for(mt_type)
            if message_generation_on:
                should_be_generated_by_adaptivdocs = FSwiftWriterUtils.should_message_be_generated_by_adaptivdocs(mt_type) or bypass_Swift_Solutions(fObject)
                if should_be_generated_by_adaptivdocs:
                    notifier.DEBUG(
                        "%s Ignoring update on settlement %s because FParameter 'SHOULD_BE_GENERATED_BY_ADAPTIVDOCS' is set to True" % (
                        mt_type, str(fObject.Oid())))
                    return False
            else:
                notifier.WARN(
                    "%s Ignoring update on settlement %s because FParameter 'F%s_GenerationOn' is set to False" % (
                    mt_type, str(fObject.Oid()), str(mt_type)))
                return False
            return mt_type.strip('MT')
            #return message_types
    except Exception, e:
        if 'No such file or directory' in str(e):
            if mt_type not in SUPPORTED_MT_MESSAGE:
                return False
            notifier.ERROR("{0} No state chart name found for message type {0} as it is not supported".format(mt_type))
            return False
        notifier.ERROR("%s Error occurred while processing settlement update: %s" % (mt_type, str(e)))
        return False
            
def process_settlements_update(fObject, settlement_status):
    """ process settlement updates"""
    try:
        mt_type = should_handle_this_update(fObject, settlement_status)
        if not mt_type:
            return
        if mt_type:
            if ShouldDocumentsBeDeleted(fObject):
                documentsToDelete = RemoveOperationsDocument(fObject)
                for operationsDocument in documentsToDelete:
                    notifier.INFO("Deleting operationsDocument for settlement id %s" % (str(fObject.Oid())))
                    operationsDocument.Delete()

            #for each_mt in mt_types:

            each_mt = mt_type
            notifier.DEBUG("%s Processing update for settlement %s" % (each_mt, str(fObject.Oid())))

            if InDocumentCreationStatus(fObject) and IsMissingMTDocument(fObject):
                each_mt = 'MT' + each_mt
                sc = FSwiftMLUtils.get_state_chart_name_for_mt_type(each_mt, 'Out')
                shouldCreateDocument = True
                """if fObject.IsKindOf(acm.FSettlement):
                    if not fObject.MTMessages():
                        shouldCreateDocument = False"""
                if shouldCreateDocument:
                    create_bpr = True
                    external_obj = FSwiftMLUtils.FSwiftExternalObject.get_external_object(acm_obj = fObject, msg_typ=each_mt, integration_type='Outgoing')
                    if external_obj:
                        business_pro = FSwiftMLUtils.get_bpr_from_subject_statechart(external_obj, sc)
                        if business_pro:
                            create_bpr = False
                            if settlement_status in ['SETTLEMENT_STATUS_RELEASED', SETTLE_STATUS_RELEASED]:
                                if business_pro.CurrentStep().State().Name() in ['GenerationFailed', 'SendFailed']:
                                    FSwiftMLUtils.trigger_event(business_pro, 'Regenerate', '')
                    if create_bpr:
                        bpr = create_business_process_for(fObject, each_mt, sc)

    except Exception, e:
        notifier.ERROR("Error occurred while processing update for settlement %d: %s"%(fObject.Oid(), str(e)))
        notifier.DEBUG(str(e), exc_info=1)

def process_bpr_step_update(bpr, mt_type=''):
    """process bpr step update"""
    notifier.DEBUG("%s Processing step update for business process %s" % (mt_type, str(bpr.Oid())))
    swift_writer_config = FSwiftMLUtils.Parameters('FSwiftWriterConfig')
    max_retries = getattr(swift_writer_config, 'BPRCommitRetry', 3)
    counter = 1
    while counter <= max_retries:
        try:
            state_name = bpr.CurrentStep().State().Name()
            state_object = FSwiftSecurityLendingBorrowingOutProcessing.FSwiftSecurityLendingBorrowingOutProcessing(bpr)
            state_callback = getattr(state_object, 'process_state_%s'%(state_name.lower()), None)
            if state_callback:
                state_callback()
        except Exception, e:
            if "Update collision" in str(e):
                counter += 1
                notifier.ERROR("{0} Retrying after 8 seconds due to update collision".format(mt_type))
                time.sleep(8)
                continue#Retry
            else:
                notifier.ERROR("%s Error occurred while processing business process step update: %s" % (mt_type, str(e)))
                notifier.DEBUG(str(e), exc_info=1)
                break
        else:
            break

