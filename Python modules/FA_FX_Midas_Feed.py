#-----------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module connects to the ini amb to listen to the Fx Amaba messages.
#  Department and Desk : Front Arena BTB/RTB
#  Requester           : Front Arena BTB/RTB
#  CR Number           : 587810
#-----------------------------------------------------------------------------------------------------------------

import amb, acm, ael
import collections
import time
import datetime

fmt = '%Y-%m-%d %H:%M:%S'

from Midas_AddInfos   import setAdditionalInfo, otherTrade
from Midas_xmlProcess import ProcessAMBMessage

try:
    import FOperationsUtils as Utils
except Exception, error:
    print "Failed to import FOperationsUtils, "  + str(error)
    
reader  = None
receive = 'MIDAS_PROD_RECEIVER'
Subject = 'ADS_MIDAS_PROD/'
tables  = ['TRADE']
                         
def AmbaMessage(msg):
    
    AmbMsg  = msg.mbf_find_object("TRADE")
    MsgType = msg.mbf_find_object("TYPE")
    AddInfo = AmbMsg.mbf_find_object("ADDITIONALINFO")
            
    if MsgType.mbf_get_value() in ('INSERT_TRADE', 'UPDATE_TRADE'):
    
        if AmbMsg:
        
            t = ael.Trade[int(AmbMsg.mbf_find_object("TRDNBR").mbf_get_value())]
            creat_time = AmbMsg.mbf_find_object("TIME").mbf_get_value()
            
            time1 = time.strptime(creat_time, fmt)
            
            dt1 = datetime.datetime(*time.strptime(creat_time, fmt)[:6])  
            dt2 = datetime.datetime(*time.strptime(creat_time, fmt)[:6])+ datetime.timedelta(minutes=10)
            
            if t.add_info('MIDAS_MSG') == 'Not Sent':
                
                while dt1 <= dt2:
                    time.sleep(1.0)
                    dt1 = dt1 + datetime.timedelta(seconds=1)
                
                if ael.date(creat_time[0:10])== ael.date_today():
                                            
                    # Spot and Outright
                    if int(AmbMsg.mbf_find_object("TRADE_PROCESS").mbf_get_value()) in (4096, 8192):
                        
                        if acm.FTrade[t.trdnbr].CurrencyPair():
                            
                            ProcessAMBMessage(t.trdnbr)
                            setAdditionalInfo(t, 'MIDAS_MSG', 'Sent')
                        else:
                            setAdditionalInfo(t, 'MIDAS_MSG', 'Not Sent_Invalid Currency Pair')
                    
                    # Fx Swap
                    elif int(AmbMsg.mbf_find_object("TRADE_PROCESS").mbf_get_value()) in (16384, 32768) and  AmbMsg.mbf_find_object("TRDNBR").mbf_get_value() == AmbMsg.mbf_find_object("CONNECTED_TRDNBR").mbf_get_value():
                                                
                        FxList = []
                        FxList.append(otherTrade(t))
                        FxList.append(t)
                        
                        for trade in FxList:
                            
                            if acm.FTrade[trade.trdnbr].CurrencyPair():
                                setAdditionalInfo(trade, 'MIDAS_MSG', 'Sent')
                            else:
                                setAdditionalInfo(t, 'MIDAS_MSG', 'Not Sent_Invalid Currency Pair')
                        ael.poll()
                        ProcessAMBMessage(t.trdnbr)           
                            
def event_cb(channel, event, arg):

    ambMsgNbr = 0
    eventDeque = collections.deque()
    
    try:
        if amb.mb_event_type_to_string(event.event_type):
            eventstring = amb.mb_event_type_to_string(event.event_type)
            
            if eventstring == 'Message':
                                
                eventDeque.append((amb.mb_copy_message(event.message), channel, ambMsgNbr))
                Utils.Log(True, 'Added event, %d in queue.' % len(eventDeque))
                
                queueMember = eventDeque.popleft()
                (eventCopy, channel, msgNbr) = queueMember
                                    
                buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)
                msg = buf.mbf_read()
                message = msg.mbf_object_to_string()
                
                if message:
                    AmbMsg = AmbaMessage(msg)     
            else:
                Utils.Log(True, 'Unknown event %s' % eventstring)
                       
    except RuntimeError, error:
        print error

def start():   
    
    try:
        # Initialize message bus
        amb.mb_init('jhbpcs00072n01:9300')
        
        # Create a channel for reading
        reader = amb.mb_queue_init_reader(receive, event_cb, None)
        for tbl in tables:
            subject = Subject + tbl
            amb.mb_queue_enable(reader, subject)
           
        print 'Waiting for messages. . .'
        amb.mb_poll()
        
    except RuntimeError, extraInfo:
        print "init failed (%s)" % extraInfo
