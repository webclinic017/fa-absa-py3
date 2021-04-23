'''-----------------------------------------------------------------------------
TASK                    :  Spark Code Optimization
PURPOSE                 :  To improve performance and memory usage of the process
DEPATMENT AND DESK      :  PCG/Ops
REQUESTER               :  Richard Gwilt\Linda Breytenbach
DEVELOPER               :  Paseka Motsoeneng
CR NUMBER               :  ABITFA-4028
--------------------------------------------------------------------------------
'''

import amb
import acm
import gc
import time
import collections
from AMB_Reader_Writer import AMB_Writer as AMB_Writer, AMB_Reader as AMB_Reader
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils
from Sparks_Util import SparksUtil
from datetime import datetime
import at_time
from XMLProcessor import XMLProcessor
import os
import FLogger
import traceback
from Sparks_Config import SparksConfig

MODULE_NAME = 'Sparks_ATS_Listener'

amb_message_number = 0
event_deque = collections.deque()


def trade_event_cb(channel, event, arg):
    global amb_message_number
    
    if amb.mb_event_type_to_string(event.event_type) == "Message":
        amb_message_number += 1
        event_string = amb.mb_event_type_to_string(event.event_type)
        event_deque.append((amb.mb_copy_message(event.message), channel, amb_message_number))
        
    else:
        SparksUtil.log(logger, 'Unspecified event...' + amb.mb_event_type_to_string(event.event_type) + ' type.')

def start():
    global logger, config, sparks_util
 
    logger = FLogger.FLogger(MODULE_NAME, 2, True, False, False, False, None)
    
    SparksUtil.log(logger, 'ATS attempting startup...')
    sparks_util = SparksUtil(acm.DateToday())
    config = SparksConfig()

    try:
        amb_reader = AMB_Reader(config.amb_server_ip, config.mb_name, trade_event_cb, config.subject_string)
        amb_reader.open_AMB_Receiver_Connection()
        SparksUtil.log(logger, 'AMB reader connected...')
    except RuntimeError, runtimeError:
        SparksUtil.log(logger, 'AMB connection failed.')

    amb.mb_poll();
    
def work():

    if len(event_deque) > 0:
        queue_item = event_deque.popleft()
        (event_copy, channel_number, amb_message_number) = queue_item
        
        message_buffer = amb.mbf_create_buffer_from_data(event_copy.data_p)
        amba_message = message_buffer.mbf_read()
        
        SparksUtil.log(logger, amba_message.mbf_object_to_string())
        
        try:
            ins_obj = AMBA_Utils.object_by_name(amba_message, ["+", "!"], "INSTRUMENT")
            trade_obj = AMBA_Utils.object_by_name(amba_message, ["+", "!"], "TRADE")

            prf_nbr = None
            currency_changed = None
            trades = []
            
            if ins_obj:
                ins_name = AMBA_Utils.get_AMBA_Object_Value(ins_obj, 'INSID')
                currency_changed = AMBA_Utils.get_AMBA_Object_Value(ins_obj, '!CURR.INSID')
                ins = acm.FInstrument[ins_name]
                trades = ins.Trades()            
            elif trade_obj:
                trd_nbr = AMBA_Utils.get_AMBA_Object_Value(trade_obj, "TRDNBR")
                prf_nbr = AMBA_Utils.get_AMBA_Object_Value(trade_obj, "PRFNBR")
                currency_changed = AMBA_Utils.get_AMBA_Object_Value(trade_obj, '!CURR.INSID')
                trades = [acm.FTrade[trd_nbr]]
            
            for trade in trades:
                if trade:
                    SparksUtil.log(logger, 'Processing trade:%s'%trade.Oid())
                    currency_name = trade.Currency().Name()
                    
                    if prf_nbr:
                        trade_portfolio = acm.FPhysicalPortfolio[prf_nbr]
                    else:
                        trade_portfolio = trade.Portfolio()
                    
                    if trade.Status() in ('BO Confirmed', 'BO-BO Confirmed', 'FO Confirmed', 'Terminated', 'Void') and trade_portfolio.add_info('MIDAS_Customer_Num'):
                        cut_off_date_object = at_time.datetime_from_string(acm.Time.DateToday() + ' ' + config.cut_off_time)
                        trade_update_time = at_time.datetime_from_string(at_time.acm_datetime(trade.UpdateTime()))
                        
                        if trade_update_time <= cut_off_date_object:
                            sparks_util.sendMoneyFlows([trade], currency_changed, True)
                        else:
                            SparksUtil.log(logger, 'Cut-off time for feeds is %s.'%(config.cut_off_time))
    
        except Exception as ex:
            SparksUtil.log(logger, 'Error in work event')
            traceback.print_exc()
            
def stop():
    sparks_util.disconnectQManager()

def status():
    return
    
def collect_garbage():
    acm.Memory().GcWorldStoppedCollect()
    gc.collect()
