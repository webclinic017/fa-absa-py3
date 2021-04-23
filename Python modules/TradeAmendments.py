"""-----------------------------------------------------------------------------------------
2006-11-30 - Tina Viljoen (Sungard)
Module
    Amendment Listener
    (c) Copyright 2006 by Front Capital Systems. All rights reserved

"C:\Program Files\Front\Front Arena\ATS\ATS\ats.exe" -server "10.110.92.110:9101" -kerberos -module_name TradeAmendments

DESCRIPTION
Amendment Diary
2014-12-11    Andrei Conicov     Code refactorization. Have added the amendment reason and PV.
2015-01-25    Andrei Conicov     Have added the acm_diff function. Checking if the prev day XML was correctly closed.
2015-02-09    Andrei Conicov     The date from the file name is not cached and the deleted additional infos related to amendment reason are ignored. 
2015-09-15    Marcelo Almiron    Modified requires_amendment_reason to handle FOption crossed barrier conditions
                                 and transfered logic from Gvalidation.input_amendment_reason.
2016-09-29    Andrei Conicov     Have added the ael version of some functions.
2017-02-28    Andrei Conicov     Have added logging
2018-02-06    Ondrej Bahounek    Allow ATS_ECONTRD_AMD_PRD update user.
                                 Improve logging.
2018-11-13    Libor Svoboda      FtF-CAL: Disable amend reason logic based on add infos.
-----------------------------------------------------------------------------------------"""

import ael
import acm
import time
import os
from Queue import Queue
from datetime import datetime, timedelta
import at_addInfoSpecEnum
from at_calculation_space import calculate_value

from at_logging import getLogger, ats_start, ats_stop

LOGGER = getLogger(__name__)
HANDLER = None  # this is the MQ handler

SYS_PROC = ael.Group[495]  # 'System Processes'
INT_PROC = ael.Group[494]  # 'Integration Process'
SYS_EXCLUDE = (SYS_PROC, INT_PROC)

AMD_ECO_TRCKR_USER = acm.FUser[3312].Name()  # "ATS_ECONTRD_AMD_PRD"
ALLOWED_UPDATE_USERS = (AMD_ECO_TRCKR_USER, )

# Need to make sure that the XML is correctly closed.
_close_xmls = False
_xmls_closed = False
_server_path = "//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/"
_local_path = "C:\\tmp\\TradeAmendments\\"
# Synchronized queue to hold the requests.
request_queue = Queue()

def _use_win_path():
    return os.name == 'nt'

def setPath(newdate=None):
    if not newdate:
        newdate = ael.date_today().to_string('%Y%m%d')
    f_path = (_local_path if _use_win_path() else _server_path)
    return "{0}TradeAmendments_Final{1}.xml".format(f_path, newdate)  

def setStatusPath(newdate=None):
    if not newdate:
        newdate = ael.date_today().to_string('%Y%m%d')
    f_path = (_local_path if _use_win_path() else _server_path)
    return "{0}TradeStatusAmendments_Final{1}.xml".format(f_path, newdate)

def start():
    global HANDLER
    global _close_xmls
    global _xmls_closed
    
    HANDLER = ats_start("TradeAmendments")
        
    LOGGER.info("Start in main")
    _close_xmls = False
    _xmls_closed = False
    _close_prev_day()
    _init_xml()

    ael.Instrument.subscribe(listener)
    ael.Leg.subscribe(listener)
    ael.CashFlow.subscribe(listener)
    ael.Reset.subscribe(listener)
    ael.Trade.subscribe(listener)
    ael.Payment.subscribe(listener)
    ael.AdditionalInfo.subscribe(listener)

def work():
    ''' This method is execute every 10 seconds '''
    global _close_xmls
    global _xmls_closed

    while not request_queue.empty():
        try:
            ta_params, operation = request_queue.get()
            output, status_output = _worker(ta_params, operation)
            _persist(output, status_output)
        except Exception as ex:
            LOGGER.exception("Something went wrong")

    if _close_xmls and not _xmls_closed:
        _close_xml()

def stop():
    '''Executed when the ATS is stopped.
    Have to unsubscribe and correctly close the XML.
    '''
    LOGGER.info("Stopping...")
    global _close_xmls
    global _xmls_closed

    _close_xmls = True

    if _close_xmls and not _xmls_closed and request_queue.empty():
        _close_xml()

    ael.Instrument.unsubscribe(listener)
    ael.Leg.unsubscribe(listener)
    ael.CashFlow.unsubscribe(listener)
    ael.Reset.unsubscribe(listener)
    ael.Trade.unsubscribe(listener)
    ael.Payment.unsubscribe(listener)
    ael.AdditionalInfo.unsubscribe(listener)

    ats_stop(HANDLER)

def listener(o, entity, arg, operation):
    """ Processes the operation and outputs the result to an XML file """
    entity_original = ael.get_old_entity()
    entity_original_clone = pp_original = None
    if entity_original:
        pp_original = entity_original.pp()
        entity_original_clone = entity_original.clone()
    tm_params = TradeAmendmentParams(entity, entity_original_clone, entity.pp(), pp_original)

    # have to process the deleted entity in the listener, it does not exist in the worker
    if operation == 'delete':
        _process_delete_out_of_order(tm_params)
    else:
        request_queue.put((tm_params, operation))

class TradeAmendmentParams(object):
    def __init__(self, e, e_original, pp, pp_original):
        self.e = e
        self.e_original = e_original
        self.pp = pp
        self.pp_original = pp_original
        
    def __str__(self):
        return "e: '{0}', e_o: '{1}'".format(self.e, self.e_original)

def _close_prev_day():
    ''' Check if the file for the previous day has been correctly closed. The closing xml element Today.'''
    date = datetime.today() + timedelta(days=-1)
    date = date.strftime('%Y%m%d')
    path = setPath(date)
    status_path = setStatusPath(date)

    _close_prev_day_xml(path)
    _close_prev_day_xml(status_path)

def _close_prev_day_xml(path):
    ''' Check if the file for the previous day has been correctly closed. The closing xml element Today.'''
    if not os.path.isfile(path):
        LOGGER.warning("Checking if XML valid but file not found '%s'", path)
        return

    xml_file = file(path)

    correct = False
    for line in xml_file:
        if "</TODAY>" in line:
            correct = True

    if not correct:
        _write_to_xml(path)

def _init_xml():
    path = setPath()
    status_path = setStatusPath()

    _create_xml(path)
    _create_xml(status_path)

def _close_xml():
    global _xmls_closed

    path = setPath()
    status_path = setStatusPath()

    _write_to_xml(path)
    _write_to_xml(status_path)
    _xmls_closed = True

def _persist(output, status_output):
    path = setPath()
    status_path = setStatusPath()
    _create_xml(path)
    _create_xml(status_path)
    _try_write_to_xml(path, output)
    _try_write_to_xml(status_path, status_output)

def _worker(ta_params, op):
    """ Processes the operation and outputs the result to an XML file """

    output = ""
    status_output = ""
    # could not find a method that would tell if the entity has been deleted
    # have to try and touch the entity and cache the exception
    try:
        if hasattr(ta_params.e, "record_type"):
            ta_params.e.record_type
        else:
            LOGGER.info("Warning, the entity has no record_type. Operation: '%s'. Args: '%s'", op, str(ta_params))
            return output, status_output
    except RuntimeError, ex:
        if str(ex) in ('entity is deleted', 'Unknown entity type'):
            return output, status_output
        else:
            LOGGER.exception("Something went wrong.")
            return output, status_output

    if op == 'insert':
        output = _process_insert(ta_params)

    # this doesn't work, delete has to be processed in the listener
    # if op == 'delete':
        # output = _process_delete(ta_params)

    if op == 'update':
        output, status_output = _process_update(ta_params)

    return output, status_output

def _create_xml(path):
    # Create initial file for the day.
    if not os.path.exists(path):
        amendment = open(path, 'w')
        line = '<?xml version=' + "'1.0'" + ' encoding=' + "'ISO-8859-1'" + '?>\n'
        amendment.writelines(line)
        amendment.writelines('<TODAY>')
        amendment.close()

def _write_to_xml(path):
    amendment_new = open(path, 'a')
    amendment_new.write('</TODAY>\n')
    amendment_new.close()

def _try_write_to_xml(path, output):

    # writes the output to the XML file
    if not os.path.exists(path):
        amendment = open(path, 'w')
        amendment.writelines('<TODAY>')
        amendment.writelines(output)
        amendment.close()
    else:
        # If the entity already exist append to file
        amendment = open(path, 'a')
        amendment.writelines(output)
        amendment.close()

def _process_insert(ta_params):

    output = ""
    # INSERTS
    # ADDITIONAL PAYMENTS - INSERT
    # ADDITIONAL INFOS - INSERT
    if ta_params.e.record_type in ('Payment', 'AdditionalInfo'):

        # USER
        if ta_params.e.creat_usrnbr.grpnbr not in SYS_EXCLUDE or \
                ta_params.e.updat_usrnbr.name in ALLOWED_UPDATE_USERS:
            # ADDITIONAL PAYMENTS
            if ta_params.e.record_type == 'Payment':
                output = _process_insert_payment(ta_params)
            # ADDITIONAL INFO
            if ta_params.e.record_type == 'AdditionalInfo':
                output = _process_insert_add_info(ta_params)

    return output

_ignore_columns = ['record_type', 'creat_time', 'creat_usrnbr', 'updat_time'
                   , 'updat_usrnbr', 'paynbr', 'trdnbr', 'archive_status'
                   , 'original_curr', 'fx_transaction', 'our_accnbr', 'valid_from', 'text']

def _process_insert_payment(ta_params):
    """Returns the output"""
    LOGGER.info("Processing payment insert %s (%s in queue)", ta_params.e.paynbr, request_queue.qsize())
    t = ta_params.e.trdnbr
    if t.status == 'Simulated':
        return ""

    key = ta_params.e.paynbr
    # Loop through changes and add to output xml
    # Add new fields
    cols = []
    for value in ta_params.pp.split('\n'):
        if value != '':
            # splits each line by a double space and removes any whitespace.
            val_old = ''
            name, val_new = _get_val_payment(value)
            if name not in _ignore_columns:
                cols.append(_get_column_element(key, name, val_old, val_new))

    return _get_entity_element(ta_params.e, t, key, cols)

def _process_insert_add_info(ta_params):

    LOGGER.info("Processing add info '%s' insert %s (%s in queue)",
        ta_params.e.addinf_specnbr.field_name, ta_params.e.valnbr, request_queue.qsize())
    
    if ta_params.e.addinf_specnbr.field_name in (at_addInfoSpecEnum.AMEND_REASON_INS,
                                                 at_addInfoSpecEnum.AMEND_REASON_TRD,
                                                 at_addInfoSpecEnum.AMEND_REASON_TYPE_INS,
                                                 at_addInfoSpecEnum.AMEND_REASON_TYPE_TRD,
                                                 ):
        return ""
    
    t = None
    # check if the additional info is on a trade
    if ta_params.e.addinf_specnbr.rec_type == 'Trade':
        t = ael.Trade[ta_params.e.recaddr]

    # Updated for CFDs.
    if ta_params.e.addinf_specnbr.rec_type == 'Instrument':
        ins = ael.Instrument[ta_params.e.recaddr]
        if ins.instype == 'Portfolio Swap' and len(ins.trades()) > 0:
            t = ins.trades()[0]

    if not t or t.status == 'Simulated':
        return ""

    key = ta_params.e.valnbr

    # Add new fields
    cols = []
    for value in ta_params.pp.split('\n'):
        if value != '':
            # splits each line by a double space and removes any whitespace.
            e_new = value.split('  ')
            name = e_new[0].strip()
            val_old = ''
            val_new = e_new[len(e_new) - 1].strip()
            if name == 'value':
                name = ta_params.e.addinf_specnbr.field_name
                cols.append(_get_column_element(ta_params.e.valnbr, name, val_old, val_new))

    return _get_entity_element(ta_params.e, t, key, cols)

def _process_delete_out_of_order(ta_params):
    '''Process the changes and persist to file'''
    output = _process_delete(ta_params)
    if output:
        _persist(output, "")

def _process_delete(ta_params):
    """Returns the output"""
    output = ""
    # DELETES
    if ta_params.e.record_type in ('Payment', 'AdditionalInfo'):

        # USER
        if ta_params.e.updat_usrnbr.grpnbr not in SYS_EXCLUDE or \
                ta_params.e.updat_usrnbr.name in ALLOWED_UPDATE_USERS:
            # ADDITIONAL PAYMENTS
            if ta_params.e.record_type == 'Payment':
                output = _process_delete_payment(ta_params)
            # ADDITIONAL INFO
            if ta_params.e.record_type == 'AdditionalInfo':
                output = _process_delete_add_info(ta_params)
    return output

def _process_delete_payment(ta_params):
    LOGGER.info("Processing payment delete %s (%s in queue)", ta_params.e.paynbr, request_queue.qsize())
    t = ta_params.e.trdnbr
    if t.status == 'Simulated':
        return ""

    key = ta_params.e.paynbr
    # Add new fields
    cols = []
    for value in ta_params.pp.split('\n'):
        if value != '':
            val_new = ''
            name, val_old = _get_val_payment(value)
            if name not in _ignore_columns:
                cols.append(_get_column_element(key, name, val_old, val_new))

    return _get_entity_element(ta_params.e, t, key, cols)

def _get_val_payment(value):
    val = ""
    # splits each line by a double space and removes any whitespace.
    e_old = value.split('  ')
    name = e_old[0].strip()
    if name in ('premium', 'quantity', 'price', 'amount'):
        val = (str)((float)(e_old[len(e_old) - 1].strip()))
    elif name == 'ptynbr':
        try:
            ptynbr = int(e_old[len(e_old) - 1].strip())
            val = ael.Party[ptynbr].ptyid
        except:
            val = ''
    elif name == 'curr':
        cur = int(e_old[len(e_old) - 1].strip())
        val = ael.Instrument[cur].insid
    else:
        val = e_old[len(e_old) - 1].strip()

    return (name, val)

def _process_delete_add_info(ta_params):
    LOGGER.info("Processing add info '%s' delete %s (%s in queue)",
        ta_params.e.addinf_specnbr.field_name, ta_params.e.valnbr, request_queue.qsize())
    
    if ta_params.e.addinf_specnbr.field_name in (at_addInfoSpecEnum.AMEND_REASON_INS,
                                                 at_addInfoSpecEnum.AMEND_REASON_TRD,
                                                 at_addInfoSpecEnum.AMEND_REASON_TYPE_INS,
                                                 at_addInfoSpecEnum.AMEND_REASON_TYPE_TRD,
                                                 ):
        return ""
    
    # check if the additional info is on a trade
    t = None
    if ta_params.e.addinf_specnbr.rec_type == 'Trade':
        t = ael.Trade[ta_params.e.recaddr]
    # Updated for CFDs.
    if ta_params.e.addinf_specnbr.rec_type == 'Instrument':
        ins = ael.Instrument[ta_params.e.recaddr]
        if ins.instype == 'Portfolio Swap':
            t = ins.trades()[0]

    if not t or t.status == 'Simulated':
        return ""

    key = ta_params.e.valnbr
    # Add new fields
    cols = []
    for value in ta_params.pp.split('\n'):
        if value != '':
            # splits each line by a double space and removes any whitespace.
            e_old = value.split('  ')
            name = e_old[0].strip()
            val_new = ''
            val_old = e_old[len(e_old) - 1].strip()

            if name == 'value':
                name = ta_params.e.addinf_specnbr.field_name
                cols.append(_get_column_element(key, name, val_old, val_new))

    return _get_entity_element(ta_params.e, t, key, cols)

def _process_update(ta_params):
    """ Returns the tuple (output, status_output) """
    output = ""
    status_output = ""
    # TRADE
    if ta_params.e.record_type == 'Trade':
        output, status_output = _process_update_trade(ta_params)

    # USER
    elif ta_params.e.updat_usrnbr.grpnbr not in SYS_EXCLUDE or \
                ta_params.e.updat_usrnbr.name in ALLOWED_UPDATE_USERS:
                
        func_process = lambda t, key, ins = None : _process_update_entity(ta_params, key, t, ins)

        t = key = None
        if ta_params.e.record_type == 'Reset':
            key = ta_params.e.resnbr
            t = _get_trade(ta_params.e.cfwnbr.legnbr.insaddr.trades())
            output = func_process(t, key)

        if ta_params.e.record_type == 'CashFlow':
            key = ta_params.e.cfwnbr
            t = _get_trade(ta_params.e.legnbr.insaddr.trades())
            output = func_process(t, key)

        if ta_params.e.record_type == 'Leg':
            key = ta_params.e.legnbr
            t = _get_trade(ta_params.e.insaddr.trades())
            output = func_process(t, key, ta_params.e.insaddr)

        if ta_params.e.record_type == 'Instrument':
            key = ta_params.e.insaddr
            t = _get_trade(ta_params.e.trades())
            output = func_process(t, key, ta_params.e)

        if ta_params.e.record_type == 'AdditionalInfo':
            key = ta_params.e.valnbr
            # check if the additional info is on a trade
            if ta_params.e.addinf_specnbr.rec_type == 'Trade':
                t = ael.Trade[ta_params.e.recaddr]

            # Updated for CFDs.
            if ta_params.e.addinf_specnbr.rec_type == 'Instrument':
                ins = ael.Instrument[ta_params.e.recaddr]
                if ins.instype == 'Portfolio Swap':
                    t = ins.trades()[0]

            if t and t.status != 'Simulated':
                output = func_process(t, key)

        if ta_params.e.record_type == 'Payment':
            key = ta_params.e.paynbr
            t = ta_params.e.trdnbr
            if t.status != 'Simulated':
                output = func_process(t, key)
    
    # First stage of TradeAmendments decommissioning, 
    # add infos won't be processed anymore.
    #_clean_amend_reason(ta_params.e);

    return (output, status_output)

def _process_update_trade(ta_params):
    """ Returns the tuple (output, status_output) """
    LOGGER.info("Processing trade update %s (%s in queue)", ta_params.e.trdnbr, request_queue.qsize())
    output = status_output = ""

    if ta_params.e.status == 'Simulated':
        return (output, status_output)

    # USER and STATUS
    # Herman 2008-02-12 changes to status: changes by system processes to Voided or Terminated must be included
    is_sys_process = ta_params.e.updat_usrnbr.grpnbr in SYS_EXCLUDE
    if (is_sys_process and ta_params.e.status in ('Void', 'Terminated')) or not is_sys_process:
        key = ta_params.e.trdnbr
        cols = _get_amended_columns(ta_params, key)
        output = _get_entity_element(ta_params.e, ta_params.e, key, cols)

        status_col = _get_status_column(ta_params, key)
        if status_col:
            status_output = _get_entity_element(ta_params.e, ta_params.e, key, [status_col])



    return (output, status_output)

def _clean_amend_reason(e, retries=2):
    if e.record_type not in ['Trade', 'Instrument']:
        return

    amend_add_info_name = ""
    amend_type_add_info_name = ""
    op_id = ""
    if e.record_type == 'Trade':
        amend_add_info_name = at_addInfoSpecEnum.AMEND_REASON_TRD
        amend_type_add_info_name = at_addInfoSpecEnum.AMEND_REASON_TYPE_TRD
        op_id = "Trade %d" % e.trdnbr
    if e.record_type == 'Instrument':
        amend_add_info_name = at_addInfoSpecEnum.AMEND_REASON_INS
        amend_type_add_info_name = at_addInfoSpecEnum.AMEND_REASON_TYPE_INS
        op_id = "Instrument %s" % e.insid

    # Clean up the amendment reason.
    if e.add_info(amend_add_info_name) or e.add_info(amend_type_add_info_name):
        ael.poll()
        ael.begin_transaction()
        try:
            tc = e.clone()
            need_to_commit = False
            for addinfo in list(tc.additional_infos()):
                field_name = addinfo.addinf_specnbr.field_name
                if field_name in [amend_add_info_name, amend_type_add_info_name]:
                    LOGGER.info("%s: Deleting add info '%s'", op_id, field_name)
                    addinfo.delete()
                    need_to_commit = True
                    
            if need_to_commit:
                tc.commit()
            ael.commit_transaction()
        except Exception:
            ael.abort_transaction()
            if retries > 0:
                _clean_amend_reason(e, retries - 1)
            else:
                LOGGER.exception("Failed to delete add infos on %s", op_id)

def _get_trade(trades):
    """ Returns the last trade with the confirmed status """
    t = None
    for trade in trades:
        if trade.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
            t = trade
    return t

def _process_update_entity(ta_params, key, t=None, ins=None):
    """ Returns the Entity element """
    trdnbr = t.trdnbr if t else 0
    insid = ins.insid if ins else ''
    LOGGER.info("Processing %s update %s (trdnbr:%s, insid:%s)",
        ta_params.e.record_type, key, trdnbr, insid)
    
    output = ""
    if t:
        cols = _get_amended_columns(ta_params, key)
        output = _get_entity_element(ta_params.e, t, key, cols)

    # BenchMark Instrument
    if not output and ins and ins.add_info('Prod_Benchmark_Ins') == 'Yes':
        t = ''
        cols = _get_amended_columns(ta_params, key)
        output = _get_entity_element(ta_params.e, t, key, cols, ins)

    return output

def _get_amended_columns(ta_params, key):
    """ Returns a list of Column elements for the amended fields """
    columns, status_change = _get_amendments(ta_params, ta_params.e.record_type, key)
    cols = []
    for _, _, col in columns.values():
        cols.append(col)
    LOGGER.info("%s amended columns.", len(cols))
    return cols

def _get_status_column(ta_params, key):
    """ Returns the Column element if the status field has been amended """
    columns, _ = _get_amendments(ta_params, ta_params.e.record_type, key)

    if not columns.has_key('status'):
        return ""

    val_old, val_new, col = columns['status']
    if not (val_old == 'Simulated' and val_new == 'Void'):
        return col
    else:
        return ""

def _get_amendments(ta_params, entity_type, key):
    """Returns a tuple (dictionary, status_changed).

     a dictionary of Column elements for amended fields and the status changed flag"""
    amendold = ta_params.pp_original.split('\n')
    amendnew = ta_params.pp.split('\n')

    if entity_type in ("Trade", "Instrument"):
        # Add the present value column.
        # The old entity has the previous values, but
        # calculations act use the new ones. When the entity is
        # cloned, then the previous values are used.
        old_entity_clone = ta_params.e_original.clone()

        old_pv = old_entity_clone.present_value()
        new_pv = ta_params.e.present_value()
        
        template = 'present_value  {0}'
        amendold.append(template.format(old_pv.value()))
        amendnew.append(template.format(new_pv.value()))

        # calculate end cash
        try:
            old_cash_end = calculate_value("FTradeSheet", acm.Ael.AelToFObject(old_entity_clone), 'Portfolio Cash End')
            new_cash_end = calculate_value("FTradeSheet", acm.Ael.AelToFObject(ta_params.e), 'Portfolio Cash End')
            template = 'cash_end  {0}'
            if hasattr(old_cash_end, "Number"):
                old_cash_end = old_cash_end.Number()
            if hasattr(new_cash_end, "Number"):
                new_cash_end = new_cash_end.Number()
            amendold.append(template.format(old_cash_end))
            amendnew.append(template.format(new_cash_end))
        except RuntimeError:
            LOGGER.exception("Could not calculate the 'Portfolio Cash End'.")

    cols = {}
    status_change = False
    for x in xrange(len(amendold)):
        if amendold[x] == amendnew[x]:
            continue
        # splits each line by a double space and removes any whitespace.
        e_old = amendold[x].split('  ')
        e_new = amendnew[x].split('  ')
        val_old = e_old[len(e_old) - 1].strip()
        val_new = e_new[len(e_new) - 1].strip()
        name = e_old[0].strip()
        if name in ('premium', 'quantity', 'price', 'amount'):
            val_old = (str)((float)(val_old))
            val_new = (str)((float)(val_new))

        # Herman 2008-02-12 changes to status: include status change if status change is void, terminated or FO Confirmed
        if entity_type == 'Trade' and name == 'status' and val_new not in ('Void', 'Terminated', 'FO Confirmed'):
            status_change = True

        if entity_type == 'AdditionalInfo' and name == 'value':
            ent = ael.AdditionalInfo[key]
            name = ent.addinf_specnbr.field_name

        if name not in ('updat_time', 'updat_usrnbr', 'version_id', 'bo_trdnbr', 'execution_time',
                        'your_ref', 'optional_key', 'start_period.unit', 'start_period.count',
                        'end_period.unit', 'end_period.count'):
            cols[name] = (val_old, val_new, _get_column_element(key, name, val_old, val_new))
        
    # If the only changed column is cash_end, then don't report as amendment,
    # because the update is result of a deleted addinfo and that was already reported
    # in deleted operation.
    # Thus remove cash_end and return empty columns.
    if len(cols) == 1 and 'cash_end' in cols:
        cols.popitem()
    
    return (cols, status_change)

def acm_diff(original_entity, modified_entity, ignore_cols=[]):
    """Returns a dictionary {column name: (old value, new value} of all amended columns."""
    modified_columns = dict(list(zip([col.Name() for col in modified_entity.Table().Columns()], modified_entity.ColumnValues())))
    original_columns = dict(list(zip([col.Name() for col in original_entity.Table().Columns()], original_entity.ColumnValues())))
    result = {}
    for key in modified_columns.keys():
        if str(key) not in ignore_cols and modified_columns[key] != original_columns[key]:
            result[str(key)] = (original_columns[key], modified_columns[key])

    return result

def ael_diff(original_entity, modified_entity, ignore_cols=[]):
    """Returns a dictionary {column name: (old value, new value} of all amended columns."""
    modified_columns = {}
    original_columns = {}
    for col_name in  modified_entity.columns():
        modified_columns[col_name] = getattr(modified_entity, col_name)
    for col_name in  original_entity.columns():
        original_columns[col_name] = getattr(original_entity, col_name)

    result = {}
    for key in modified_columns.keys():
        if str(key) not in ignore_cols and modified_columns[key] != original_columns[key]:
            result[str(key)] = (original_columns[key], modified_columns[key])

    return result

def _is_diff_in_payments(original_entity, modified_entity):
    ''' Returns True if the payments have possibly been amended'''
    # Need to use some heuristic, the payment id cannot be used for matching

    # Check at first the number of payments
    if len(original_entity.Payments()) != len(modified_entity.Payments()):
        return True
    ignore_sys_columns = ['paynbr', 'trdnbr']
    for original_payment in original_entity.Payments():
        matched_payment = None
        for modified_payment in modified_entity.Payments():
            if (modified_payment.CreateTime() == original_payment.CreateTime()
                and modified_payment.Type() == original_payment.Type()
                and modified_payment.Text() == original_payment.Text()
                and modified_payment.Amount() == original_payment.Amount()):
                matched_payment = modified_payment
                break
        # No match found
        if not matched_payment:
            return True
        # The payments are different
        if acm_diff(original_payment, matched_payment, ignore_sys_columns):
            return True

    # No differences found
    return False

def _is_diff_in_add_infos(original_entity, modified_entity, ignore=[]):
    ''' Return True is any of not ignore additional info has been amended'''

    original_add_info = str(original_entity.AdditionalInfo())
    modified_add_info = str(modified_entity.AdditionalInfo())

    if original_add_info == modified_add_info:
        return False

    original_add_info = [i.strip() for i in original_add_info.splitlines()][2:]
    modified_add_info = [i.strip() for i in  modified_add_info.splitlines()][2:]
    def _dict(add_infos):
        result = {}
        for item in add_infos:
            key, value = item.split('=')
            result[key.strip()] = value
        return result

    original_add_info = _dict(original_add_info)
    modified_add_info = _dict(modified_add_info)
    for key in original_add_info.keys():
        if original_add_info[key] != modified_add_info[key]:
            if key not in ignore:
                LOGGER.info("Additional info '%s' amended: %s->%s",
                            key, original_add_info[key], modified_add_info[key])
                return True

    return False        


# These columns get changed when the object is "cloned" but the
# user should not be able to change them
IGNORE_ADD_INFOS = ['econoAmendOPSConf']
IGNORE_SYS_COLS = ['trdnbr', 'connected_trdnbr', 'insaddr', 'optkey3_chlnbr']

IGNORE_COLS_TRADE = ['your_ref']
IGNORE_COLS_EXOTIC = ['barrier_crossed_status', 'seqnbr']


def _trade_requires_amendment_reason(original, modified):
    ''' Return True if it is necessary to provide an amendment reason.

    entity, original_entity - acm objects'''

    monitored_trade_statuses = ['BO Confirmed', 'BO-BO Confirmed', 'Terminated', 'Void']

    # Status rule
    if original.Status() in monitored_trade_statuses:
        if modified.Status() not in monitored_trade_statuses:
            # No need to add a reason when changing the status.
            return False
    else:
        return False
        
    # Status rule
    if original.Status() == 'BO Confirmed' and  modified.Status() == 'BO-BO Confirmed':
        return False

    # Column by column rules
    amendments = acm_diff(original, modified, IGNORE_COLS_TRADE + IGNORE_SYS_COLS)
    if amendments:
        return True
    if _is_diff_in_payments(original, modified):
        LOGGER.info('Payment probably amended')
        return True
    if _is_diff_in_add_infos(original, modified, IGNORE_ADD_INFOS):
        return True
        
    # No condition was detected to require amendment reason:
    return False


def _instrument_requires_amendment_reason(original, modified):
    ''' Return True if it is necessary to provide an amendment reason.

    entity, original_entity - acm objects'''

    # Have to load the instrument from db, the modified returns 0 trades.
    ins = acm.FInstrument[modified.Name()]
    if not ins:
        return False

    # Look for monitored trade
    has_monitored_trade = False
    for trade in ins.Trades():
        if trade.Status() in ['BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
            # Existence of a monitored trade justify further checking
            has_monitored_trade = True
            break

    if has_monitored_trade:
        
        # just FOption may be exempt of amendment reason
        if not original.IsKindOf('FOption'):
            return True
            
        # Checks if the only change in the barrier option is that the barrier
        # passed to be "crossed".
        if original.IsBarrier() and modified.IsKindOf('FOption') and modified.IsBarrier():
                
            if bool(acm_diff(original, modified, IGNORE_SYS_COLS)):
                return True
                
            m_exotics = modified.Exotics()
            crossed_barrier = False
            exotic_requires_reason = False
            for m_exotic in m_exotics:
                o_exotic = m_exotic.Original()
                exotic_requires_reason = exotic_requires_reason or bool(acm_diff(o_exotic, m_exotic, IGNORE_COLS_EXOTIC + IGNORE_SYS_COLS))
                if exotic_requires_reason:
                    return True
                if o_exotic.BarrierCrossedStatus() != 'Crossed' and m_exotic.BarrierCrossedStatus() == 'Crossed':
                    crossed_barrier = True
                            
            return not crossed_barrier

        else:
            # Non FOption barrier objects require amendment reason
            return True

    else:
        # FInstruments with no associated monitored trade do not require amendment reason
        return False

def requires_amendment_reason(original, modified):
    ''' Return True if it is necessary to provide an amendment reason.

    entity, original_entity - acm objects'''


    if modified.IsKindOf('FTrade'):
        return _trade_requires_amendment_reason(original, modified)
    elif modified.IsKindOf('FInstrument'):
        return _instrument_requires_amendment_reason(original, modified)
    else:
        # Only FTrade and FIstrument may require amendment reason
        return False
    
def _trade_requires_amendment_reason_ael(original, modified):
    ''' Return True if it is necessary to provide an amendment reason.

    entity, original_entity - acm objects'''

    monitored_trade_statuses = ['BO Confirmed', 'BO-BO Confirmed', 'Terminated', 'Void']

    # Status rule
    if original.status in monitored_trade_statuses:
        if modified.status not in monitored_trade_statuses:
            # No need to add a reason when changing the status.
            return False
    else:
        return False
        
    # Status rule
    if original.status == 'BO Confirmed' and  modified.status == 'BO-BO Confirmed':
        return False

    # Column by column rules
    amendments = ael_diff(original, modified, IGNORE_COLS_TRADE + IGNORE_SYS_COLS)
    if amendments:
        return True
    # TODO Payments and Additional infos will be processes later
#     if _is_diff_in_payments(original, modified):
#         print 'Payment probably amended'
#         return True
#     if _is_diff_in_add_infos(original, modified, IGNORE_ADD_INFOS):
#         return True
        
    # No condition was detected to require amendment reason:
    return False

def _instrument_requires_amendment_reason_ael(original, modified):
    ''' Return True if it is necessary to provide an amendment reason.

    entity, original_entity - acm objects'''

    # Have to load the instrument from db, the modified returns 0 trades.
    ins = ael.Instrument[modified.insid]
    if not ins:
        return False

    # Look for monitored trade
    has_monitored_trade = False
    for trade in ins.trades():
        if trade.status in ['BO Confirmed', 'BO-BO Confirmed', 'Terminated']:
            # Existence of a monitored trade justify further checking
            has_monitored_trade = True
            break

    if has_monitored_trade:
        
        # just FOption may be exempt of amendment reason
        if original.instype != 'Option':
            return True
            
        # Checks if the only change in the barrier option is that the barrier
        # passed to be "crossed".
        # TODO
        return True
#         if original.IsBarrier() and modified.instype == 'Option' and modified.IsBarrier():
#                 
#             if bool(ael_diff(original, modified, IGNORE_SYS_COLS)):
#                 return True
#                 
#             m_exotics = modified.exotics()
#             crossed_barrier = False
#             exotic_requires_reason = False
#             for m_exotic in m_exotics:
#                 o_exotic = m_exotic.original()
#                 exotic_requires_reason = exotic_requires_reason or bool(ael_diff(o_exotic, m_exotic, IGNORE_COLS_EXOTIC + IGNORE_SYS_COLS))
#                 if exotic_requires_reason:
#                     return True
#                 if o_exotic.BarrierCrossedStatus() != 'Crossed' and m_exotic.BarrierCrossedStatus() == 'Crossed':
#                     crossed_barrier = True
#                             
#             return not crossed_barrier
# 
#         else:
#             # Non FOption barrier objects require amendment reason
#             return True

    else:
        # FInstruments with no associated monitored trade do not require amendment reason
        return False

def requires_amendment_reason_ael(original, modified):
    ''' Return True if it is necessary to provide an amendment reason.

    entity, original_entity - acm objects'''

    if modified.record_type == 'Trade':
        return _trade_requires_amendment_reason_ael(original, modified)
    elif modified.record_type == 'Instrument':
        return _instrument_requires_amendment_reason_ael(original, modified)
    else:
        # Only FTrade and FIstrument may require amendment reason
        return False

def _get_entity_element(e, t, key, cols=[], ins=None):
    """ Returns the XML Entity element """
    if cols:
        output = '<Entity>\n'
        output += _static_columns(e, t, key, ins)
        output += "\n".join(cols)
        output += '</Entity>\n'
        return output
    else:
        return ""

def _get_column_element(key, name, val_old, val_new):
    """ Returns the XML Column element """
    cols = '<Column>\n'
    cols += '<Key>' + str(key) + '</Key>\n'
    cols += '<TimeStamp>' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '</TimeStamp>\n'
    cols += '<Name>' + name + '</Name>\n'
    cols += '<OriginalValue>' + _cleanup(val_old) + '</OriginalValue>\n'
    cols += '<CurrentValue>' + _cleanup(val_new) + '</CurrentValue>\n'
    cols += '</Column>'

    return cols

def _static_columns(e, t, key, ins=None):
    """Builds the static columns for the related trade of the instrumnet that has been amended"""
    column_data_keys = ["Name", "Key", "UpdatedUser", "UpdatedTime", "UpdatedUserGroup", "CreateTime", "TradeTime",
                        "TraderID", "Portfolio", "RelTrade", "Status", "RelInstrument", "ConfoSent", "ConfoText",
                        "Acquirer", "Counterparty", "BenchmarkInstrument", "Insid", "AmendmentReason", "Instype",
                        "AmendmentReasonType"]
    column_data = {}
    for col_name in column_data_keys:
        column_data[col_name] = ""

    column_data['Name'] = e.record_type
    column_data['Key'] = str(key)
    column_data['UpdatedUser'] = _cleanup(e.updat_usrnbr.userid)
    column_data['UpdatedTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(e.updat_time))
    column_data['UpdatedUserGroup'] = _cleanup(e.updat_usrnbr.grpnbr.grpid)
    if t:
        column_data['CreateTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(e.creat_time))
        column_data['TradeTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t.time))
        column_data['TraderID'] = _cleanup(t.creat_usrnbr.userid)
        column_data['Portfolio'] = _cleanup(t.prfnbr.prfid)
        column_data['RelTrade'] = str(t.trdnbr)
        column_data['Status'] = str(t.status)
        column_data['RelInstrument'] = _cleanup(t.insaddr.insid)
        column_data['ConfoSent'] = _cleanup(str(t.add_info('Confo Date Sent')))
        column_data['ConfoText'] = _cleanup(t.add_info('Confo Text'))
        # simulated trades may be missing the acquirer
        if t.acquirer_ptynbr:
            column_data['Acquirer'] = _cleanup(t.acquirer_ptynbr.ptyid)
        column_data['Counterparty'] = _cleanup(t.counterparty_ptynbr.ptyid)
        column_data['BenchmarkInstrument'] = 'No'
        column_data['AmendmentReason'] = _cleanup(t.add_info(at_addInfoSpecEnum.AMEND_REASON_TRD))
        column_data['AmendmentReasonType'] = _cleanup(t.add_info(at_addInfoSpecEnum.AMEND_REASON_TYPE_TRD))
        column_data['Insid'] = _cleanup(t.insaddr.insid)
        column_data['Instype'] = _cleanup(t.insaddr.instype)

    if e.record_type == 'Instrument':
        # !!!the instrument amendment reasons have priority
        if _cleanup(e.add_info(at_addInfoSpecEnum.AMEND_REASON_INS)):
            column_data['AmendmentReason'] = _cleanup(e.add_info(at_addInfoSpecEnum.AMEND_REASON_INS))
        if _cleanup(e.add_info(at_addInfoSpecEnum.AMEND_REASON_TYPE_INS)):
            column_data['AmendmentReasonType'] = _cleanup(e.add_info(at_addInfoSpecEnum.AMEND_REASON_TYPE_INS))
    if ins:
        column_data['BenchmarkInstrument'] = 'Yes'
        column_data['Insid'] = _cleanup(ins.insid)
        column_data['Instype'] = _cleanup(ins.instype)

    output = ''
    for c_key, item in column_data.items():
        output = output + "<{0}>{1}</{0}>\n".format(c_key, item)

    return output

def _cleanup(origstring):
    string = origstring
    string = string.replace('&', '&amp;')
    string = string.replace('"', '&quot;')
    string = string.replace('<', "&lt;")
    string = string.replace('>', '&gt;')
    string = string.replace("'", "&apos;")
    return string
