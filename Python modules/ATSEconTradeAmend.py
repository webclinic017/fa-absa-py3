"""
Description
===========
Date                          :  2014-10-17
Purpose                       :  Module used to monitor updates to objects that don't have proper access rights defined around them
Department and Desk           :  PCG MO/FO
Requester                     :  Letitia Roux
Developer                     :  Andrei Conicov
CR Number                     :

https://confluence.barcapint.com/display/ABCAPFA/Economic+trade+amendments+ATS

"C:\Program Files\Front\Front Arena\ATS\ATS\ats.exe" -server "10.110.92.110:9101" -kerberos -module_name ATSEconTradeAmend

History
=======

Date          CR              Developer           Description
====          ======          ================    =============
2014-10-24    CHNG0002365110  Andrei Conicov      Initial Implementation
2014-11-14    CHNG0002450582  Andrei Conicov      Have removed the trade filter, which slows down the ATS
2016-02-16    CHNG0003451131  Andrei Conicov      Ignore the inserts made by FMAINTENACE
2016-10-27                    Andrei Conicov      Using at_logging and transactions
2018-02-06                    Ondrej Bahounek     Allow ATS_TRD_AMD_PRD update user.
                                                  Improve logging.
"""

import acm
import ael
from comment_history import JSONTextObjectCommentHistory
import traceback
from datetime import datetime
from Queue import Queue
from at_logging import getLogger, ats_start, ats_stop

LOGGER = getLogger(__name__)
HANDLER = None  # this is the MQ handler

_PREFIX = 'TrAm'
_ADD_INFO_E_A_OPS_CONF = 'EconoAmendOPSConf'
_IMPORTANT_TRD_FIELDS = {'acquire_day', 'connected_trdnbr.trdnbr', 'contract_trdnbr.trdnbr',
                             'correction_trdnbr.trdnbr', 'counterparty_ptynbr.ptynbr', 'curr.insid',
                             'fee', 'mirror_trdnbr.trdnbr', 'premium', 'price', 'quantity', 'time',
                             'trade_curr.insid', 'trade_process', 'type', 'value_day'}
_COMMIT_ADD_INFO_RETRIES = 2
_COMMIT_TEXT_OBJ_RETRIES = 2
# Synchronized queue to hold the requests.
request_queue = Queue()

SYS_PROC = ael.Group[495]  # 'System Processes'
INT_PROC = ael.Group[494]  # 'Integration Process'
SYS_EXCLUDE = (SYS_PROC, INT_PROC)

AMD_TRCKR_USER = acm.FUser[3319].Name()  # 'ATS_TRD_AMD_PRD'
ALLOWED_UPDATE_USERS = (AMD_TRCKR_USER, )


def start():
    global HANDLER
    HANDLER = ats_start("ATSEconTradeAmend")
    
    LOGGER.info("Start in main")
    ael.Trade.subscribe(_listener)
    ael.AdditionalInfo.subscribe(_listener)

def stop():
    LOGGER.stop("Stopping... (%s in queue)", request_queue.qsize())
    ael.Trade.unsubscribe(_listener)
    ael.AdditionalInfo.unsubscribe(_listener)
    
    ats_stop(HANDLER)

def work():
    while not request_queue.empty():
        entity, entity_original, operation = request_queue.get()
        _process(entity, entity_original, operation)

def _listener(o, entity, arg, operation):
    """Adds the entity and the original entity to the request queue."""
    if entity.record_type == "AdditionalInfo" and entity.addinf_specnbr.rec_type != "Trade":
        return

    entity_original = ael.get_old_entity()
    if entity_original:
        entity_original = entity_original.clone()
    request_queue.put((entity, entity_original, operation))

def _process(entity, entity_original, operation):
    """ If someone "authorised" amends the trade, the changes are
    logged to a text object and EconoAmendOPSConf is set to No.
    If a new trade is created the value of the EconoAmendOPSConf
    is deleted.
    Security Lending Desk trades where the borrower and Fund lender
    fields are populated are removed from the amendment tracker.
    """

    # could not find a method that would tell if the entity has been deleted
    # have to try and touch the entity and cache the exception
    try:
        entity.record_type
    except RuntimeError, ex:
        if str(ex) in ('entity is deleted', 'Unknown entity type'):
            return
        else:
            LOGGER.exception("Could not determine entity type (%s in queue)", request_queue.qsize())
            return

    process = False
    if entity.record_type == "Trade" and operation in ('insert', 'update'):
        process = True

    if entity.record_type == "AdditionalInfo" and operation in ('update'):
        if (entity.addinf_specnbr.rec_type == "Trade" and
                entity.addinf_specnbr.field_name == _ADD_INFO_E_A_OPS_CONF):
            process = True

    if not process:
        return

    if entity.record_type == "Trade":
        LOGGER.info("Processing %s, operation %s, trdnbr: %s (%s in queue)", entity.record_type,
                                                                             operation,
                                                                             entity.trdnbr,
                                                                             request_queue.qsize())
        if operation == "update":

            # ignore the changes made by system users
            if entity.updat_usrnbr.grpnbr in SYS_EXCLUDE and \
                    entity.updat_usrnbr.name not in ALLOWED_UPDATE_USERS:
                LOGGER.info("Trade %s %s operation is ignored exclude: group '%s' (%s in queue)",
                            entity.trdnbr, operation, entity.updat_usrnbr.grpnbr.grpid, request_queue.qsize())
                return

            if  entity.status not in ['BO Confirmed', 'BO-BO Confirmed', 'FO Confirmed', 'Terminated']:
                LOGGER.info("Trade %s %s operation is ignored exclude: status '%s' (%s in queue)",
                            entity.trdnbr, operation, entity.status, request_queue.qsize())
                return

            if entity.insaddr.instype in ['CFD', 'Stock']:
                LOGGER.info("Trade %s %s operation is ignored exclude: ins type '%s' (%s in queue)",
                            entity.trdnbr, operation, entity.insaddr.instype, request_queue.qsize())
                return

            if entity.counterparty_ptynbr.ptyid2 in ['SAFEX', 'JSE', 'JSE SECURITIES EXCHANGE SOUTH AFRICA']:
                LOGGER.info("Trade %s %s operation is ignored exclude: counterparty '%s' (%s in queue)",
                            entity.trdnbr, operation, entity.counterparty_ptynbr.ptyid, request_queue.qsize())
                return

            # do not filter using TF, it is too slow and memory consuming

            _set_economic_amend_add_info(entity, entity_original)
        if operation == "insert" and entity.updat_usrnbr != ael.User['FMAINTENANCE']:
            _drop_economic_amend_add_info(entity, _COMMIT_ADD_INFO_RETRIES)

    if (entity.record_type == "AdditionalInfo" and
            operation == "update" and
            entity.addinf_specnbr.rec_type == "Trade"):
        _log_add_info_amendment(entity)

def _set_economic_amend_add_info(trade, trade_original):
    """Sets additional infos if specific trade fields have been amended.

    If the specific trade fields have been modified, sets:
    EconoAmendOPSConf to No
    """
    changes = _check_attr(trade, trade_original)
    delete_text_object = _check_text_object_to_remove(trade)
    if changes and not delete_text_object:
        _set_add_info(trade, _ADD_INFO_E_A_OPS_CONF, 'No', _COMMIT_ADD_INFO_RETRIES)
        _update_text_object(trade, changes, _COMMIT_TEXT_OBJ_RETRIES)
    else:
        if delete_text_object:
            _set_add_info(trade, _ADD_INFO_E_A_OPS_CONF, 'Yes', _COMMIT_ADD_INFO_RETRIES)
            _delete_text_object(trade, _COMMIT_TEXT_OBJ_RETRIES)
        else:
            # check if can delete the text object
            _process_economic_amend_add_info_change(trade)

def _drop_economic_amend_add_info(trade, retries=0):
    """ Deletes the additional info"""
    try:
        ael.begin_transaction()
        
        trade = ael.Trade[trade.trdnbr]
        clone_trade = trade.clone()
        need_to_commit = False
        for a in clone_trade.additional_infos():
            if a.addinf_specnbr.field_name == _ADD_INFO_E_A_OPS_CONF:
                LOGGER.info("Deleting add info (%s in queue)", request_queue.qsize())
                a.delete()
                need_to_commit = True
                break
        
        if need_to_commit:
            clone_trade.commit()
        
        ael.commit_transaction()
    except Exception:
        ael.abort_transaction()
        if retries == 0:
            LOGGER.exception("Failed to delete additional info")
        else:
            LOGGER.debug("Failed to delete additional info")
        if retries > 0:
            _drop_economic_amend_add_info(trade, retries - 1)

def _log_add_info_amendment(add_info):
    """ If the provided additional info is of type EconoAmendOPSConf
    and is equal to Yes, the text object that corresponds to the trade
    is deleted."""

    if add_info.addinf_specnbr.field_name != _ADD_INFO_E_A_OPS_CONF:
        # escape if this is not the addinfo that has to be monitored
        return

    if add_info.value == 'No':
        return

    trade = ael.Trade[add_info.recaddr]
    if not trade:
        LOGGER.warning("Could not find trade %s", add_info.recaddr)
        return

    _delete_text_object(trade, _COMMIT_TEXT_OBJ_RETRIES)

def _process_economic_amend_add_info_change(trade):
    """Process the change of the EconoAmendOPSConf add info."""

    # The value of the EconoAmendOPSConf are updated, and both are set to Yes
    #    The text object is deleted

    if trade.add_info(_ADD_INFO_E_A_OPS_CONF) == 'Yes':
        _delete_text_object(trade, _COMMIT_TEXT_OBJ_RETRIES)

def _delete_text_object(trade, retries=0):
    """Delete the text object that corresponds to the specified trade. """

    acm_trade = acm.FTrade[trade.trdnbr]
    if not acm_trade:
        LOGGER.warning("Could not find the trade with trade number %s", trade.trdnbr)
        return

    ael.poll()
    text_obj = JSONTextObjectCommentHistory(acm_trade, _PREFIX)
    # have to save the result before deleting the text object

    if not text_obj.text_object:
        return

    LOGGER.info("Deleting text_object for trade %s", trade.trdnbr)
    LOGGER.info("\n".join(text_obj.formatted_comments()))
    
    try:
        text_obj.delete()
    except Exception:
        if retries == 0:
            LOGGER.exception("Failed to delete text_object")
        else:
            LOGGER.debug("Failed to delete text_object")
        if retries > 0:
            _delete_text_object(trade, retries - 1)

def _update_text_object(trade, changes, retries=0):
    """ Save the changes to the text object

    trade - trade
    changes - dictionary: {attribute, value}
    """

    ael.poll()
    user = trade.updat_usrnbr.userid
    LOGGER.info("Setting text_object to \"%s\" for trade %s, user '%s'",
                changes, trade.trdnbr, user)

    acm_trade = acm.FTrade[trade.trdnbr]
    if not acm_trade:
        LOGGER.warning("Could not find the trade %s", trade.trdnbr)
        return

    text_obj = JSONTextObjectCommentHistory(acm_trade, _PREFIX)

    for att, val in changes.items():
        change = "{0}: {1}".format(att, str(val))
        text_obj.append(change, None, user)
    try:
        text_obj.save()
    except Exception, ex:
        if retries == 0:
            LOGGER.exception("Failed to save the text_object")
        else:
            LOGGER.debug("Failed to save the text_object")
        if retries > 0:
            _update_text_object(trade, changes, retries - 1)

def _set_add_info(trade, add_info_name, add_info_value, retries=0):
    """Sets an ael additional info field on a given trade."""

    ael.poll()
    is_set = trade.add_info(_ADD_INFO_E_A_OPS_CONF) == add_info_value
    # ignore the operation if the value is already set
    if is_set:
        return

    LOGGER.info("Setting add_info %s to %s for trade %s",
                add_info_name, add_info_value, trade.trdnbr)
    # It is necessary to make sure, that the trade was not updated by another user
    try:
        ael.begin_transaction() 
        
        trade = ael.Trade[trade.trdnbr]
        clone_trade = trade.clone()
        for add_info in clone_trade.additional_infos():
            if add_info.addinf_specnbr.field_name == add_info_name:
                add_info.value = str(add_info_value)
                clone_trade.commit()
                ael.poll()  # tests are failing if not updated
                LOGGER.info('Value set to: %s', trade.add_info(add_info_name))

        ael.commit_transaction()
    except Exception:
        ael.abort_transaction()
        if retries == 0:
            LOGGER.exception("Failed to update the add_info")
        if retries > 0:
            _set_add_info(trade, add_info_name, add_info_value, retries - 1)
        return


    LOGGER.info('Adding new add info')
    try:
        ael.begin_transaction() 
        new_add_info = ael.AdditionalInfo.new(clone_trade)
        new_add_info.addinf_specnbr = ael.AdditionalInfoSpec[add_info_name]
        new_add_info.value = str(add_info_value)

        new_add_info.commit()
        
        ael.commit_transaction()
    except Exception:
        ael.abort_transaction()
        if retries == 0:
            LOGGER.exception("Failed to create the add_info")
        else:
            LOGGER.debug("Failed to create the add_info")
        if retries > 0:
            _set_add_info(trade, add_info_name, add_info_value, retries - 1)

def _check_attr(trade, trade_original):
    """Returns the differences between the provided two trades,
     for the attributes specified in _important_trd_fields.
    """

    diffs = {}
    # loop through the important_attr set to identify a change in the value of an attribute
    for attribute in _IMPORTANT_TRD_FIELDS:
        att = attribute.split('.')[0]
        att_2 = None
        val_e2_att = None
        val_e1 = getattr(trade, att, 0)
        val_e2 = getattr(trade_original, att, 0)
        # have to check the value, not the object
        if "." in attribute:
            att_2 = attribute.split('.')[1]
            val_e2_att = val_e2
            val_e1 = getattr(val_e1, att_2, 0)
            val_e2 = getattr(val_e2, att_2, 0)

        if val_e1 != val_e2:  # test if the attribute value has changed
            # print 'Value of {0} has changed: Old={1}, New={2}'.format(att, val_e1, val_e2)
            # we want to see 'human readable' values
            if att_2 == 'ptynbr' and hasattr(val_e2_att, 'ptyid'):
                val_e2 = getattr(val_e2_att, 'ptyid', 0)
            diffs[att] = val_e2

    return diffs

def _get_trades_from_invokation_info(invokationInfo):
    trades = []
    try:
        selection = invokationInfo.ExtensionObject().ActiveSheet().Selection()
        cells = selection.SelectedCells()
        for cell in cells:
            rowObject = cell.RowObject()
            trade = rowObject.Trade()
            trades.append(trade.Oid())
    except:
        traceback.print_exc()

    return set(trades)

def _check_text_object_to_remove(trade):
    """ Checks if the text object has to be deleted or change has to be ignored.

    Security Lending Desk trades where the borrower and Fund lender
    fields are populated need to be removed.
    Fields SL_G1Counterparty1 and SL_G1Counterparty2.
    """
    acquirer = trade.acquirer_ptynbr
    is_acquirer = acquirer.ptyid in ['SECURITY LENDINGS DESK']
    if (is_acquirer and
        trade.add_info('SL_G1Counterparty1') != '' and
        trade.add_info('SL_G1Counterparty2') != ''):
        return True
    return False

def print_economic_amendments_by_trdnbr(trdnbr):
    """Print the economic amendments for the specified trade number"""
    print "Trade: {0}".format(trdnbr)
    trade = acm.FTrade[trdnbr]
    text_obj = JSONTextObjectCommentHistory(trade, _PREFIX)

    if text_obj.text_object:
        print "\n".join(text_obj.formatted_comments())
    else:
        print "No changes..."

def ops_conf(invokationInfo):
    """Sets the EconoAmendOPSConf add info to Yes"""
    trades = _get_trades_from_invokation_info(invokationInfo)
    for trdnbr in trades:
        _set_add_info(ael.Trade[trdnbr], _ADD_INFO_E_A_OPS_CONF, "Yes", _COMMIT_ADD_INFO_RETRIES)

def get_economic_amendments_full(trdnbr):
    trade = acm.FTrade[trdnbr]
    text_obj = JSONTextObjectCommentHistory(trade, _PREFIX)
    return str("; ".join(text_obj.comments()))

def get_economic_amendments(trdnbr):
    trade = acm.FTrade[trdnbr]
    text_obj = JSONTextObjectCommentHistory(trade, _PREFIX)

    if not text_obj.comments():
        return ""

    changes = text_obj.comments()
    result = []
    keys = set(map(lambda c: c['message'].split(":")[0], changes))
    for key in keys:
        changes_by_key = filter(lambda c: c['message'].split(":")[0] == key, changes)

        changes_by_key.sort(cmp=lambda a, b:cmp(b['datetime'], a['datetime']))

        result.append(changes_by_key[0]['message'])

    return str("; ".join(result))

def get_economic_amendments_login_time(trdnbr):
    """Returns a string that contains the login and time for the last change"""
    trade = acm.FTrade[trdnbr]
    text_obj = JSONTextObjectCommentHistory(trade, _PREFIX)

    if not text_obj.comments():
        return ""

    changes = text_obj.comments()
    changes.sort(cmp=lambda a, b:cmp(b['datetime'], a['datetime']))

    return str("{0}:{1}".format(changes[0]['datetime'], changes[0]['login']))

def print_economic_amendments(invokationInfo):
    """Print the economic amendments to log window"""
    print "Economic amendments ..."
    trades = _get_trades_from_invokation_info(invokationInfo)
    for trdnbr in trades:
        print_economic_amendments_by_trdnbr(trdnbr)
    print "-"*40
