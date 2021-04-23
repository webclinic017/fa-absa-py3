'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_ATS
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module is the CBFETR ATS.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       235281
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-02-22      235281          Heinrich Cronje                 Initial Implementation
2013-08-17      CHNG0001209844  Heinrich Cronje                 BOPCUS 3 Upgrade

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    On start up, this ATS will receive an AMBA message and process it to get a portfolio and date.
    This portfolio and date will be used to retreive valid Money Flows for CBFETR and construct BOP Reporting AMBA
    messages.
    These messages will be posted to the AMB where the FA Service model will pick up the messages and process them further.
'''

import amb, time, collections, gc, acm, os
import FOperationsUtils as Utils
import CBFETR_Parameters as Params
from AMB_Reader_Writer import AMB_Writer as AMB_Writer, AMB_Reader as AMB_Reader
from CBFETR_Message_Processing import CBFETR_AMBA_Message_Process as AMBA_Message_Process, CBFETR_AMBA_Message_Amend as AMBA_Message_Amend
from CBFETR_Helper_Functions import Data_Selection as Data_Selection, Message_Info_MESSAGE as Message_Info

ambMsgNbr = 0
eventDeque = collections.deque()
global ATS_STATUS
ATS_STATUS = 'RUNNING'

'''--------------------------------------------------------------------
    Callback function for posting message onto the AMB
--------------------------------------------------------------------'''
def event_cb_AMB_Sender(channel, event, arg):
    pass

write_AMB = AMB_Writer(Params.ambAddress, Params.senderMBName, event_cb_AMB_Sender, Params.senderSource, Params.senderSource)
if not write_AMB.open_AMB_Sender_Connection():
    Utils.Log(True, 'ERROR: Could not open the Sender AMB connection.')
    raise Exception('ERROR: Could not open the Sender AMB connection.')

def event_cb(channel, event, arg):
    '''--------------------------------------------------------------------
        Main callback function for AMB messages. The events are placed
        in a queue that is then processed by work_cb. 
    --------------------------------------------------------------------'''
    
    global ambMsgNbr
    eventString = amb.mb_event_type_to_string(event.event_type)

    if eventString == 'Status':
        try:
            ambMsgNbr = int(event.status.status)
        except ValueError:
            ambMsgNbr = 0
    elif eventString == 'Message':
        ambMsgNbr += 1
        eventDeque.append((amb.mb_copy_message(event.message), channel, ambMsgNbr))
        Utils.Log(True, 'Added event, %d in queue.' % len(eventDeque))
    else:
        Utils.Log(True, 'Unknown event %s' % eventString)

def work():
    global ATS_STATUS
    if ATS_STATUS != 'RUNNING':
        return
    
    '''--------------------------------------------------------------------
                            Process the Event Queue
    --------------------------------------------------------------------'''
    if len(eventDeque) == 0:
        return

    queueMember = eventDeque.popleft()
    (eventCopy, channel, msgNbr) = queueMember
    if (len(eventDeque) > 0):
        Utils.Log(True, '>>> Processing event, %d in queue.' % len(eventDeque))
    
    buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)
    
    Utils.Log(True, '===================================================================')
    Utils.Log(True, 'The CBFETR_ATS received the following AMB message with msgnbr: %s' % str(eventCopy.id))
    Utils.Log(True, '===================================================================')
    
    msg = buf.mbf_read()
    print msg.mbf_object_to_string()

    '''--------------------------------------------------------------------
                                    Bypass
    --------------------------------------------------------------------'''
    #amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
    #msg.mbf_destroy_object()
    #buf.mbf_destroy_buffer()
    #return
    
    Utils.Log(True, 'Processing AMBA Message...')
    
    AMBA_Message_Process_Class = AMBA_Message_Process(msg)
    
    try:
        AMBA_Message_Process_Class.process_AMBA_Message()
    except Exception, e:
        handel_Exception('ERROR: %s' % str(e), AMBA_Message_Process_Class.AMBA_Request_Id)

        AMBA_Message_Process_Class = None
        
        amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
        msg.mbf_destroy_object()
        buf.mbf_destroy_buffer()

        collect_Garbage()

        print('>>> Waiting for events...\n')
        return
    
    data_Selection_Class = Data_Selection(AMBA_Message_Process_Class)
    
    try:
        data_Selection_Class.get_Scope_Objects()
    except Exception, e:
        handel_Exception('ERROR: %s' % str(e), AMBA_Message_Process_Class.AMBA_Request_Id)
        
        AMBA_Message_Process_Class = None
        data_Selection_Class = None
        
        amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
        msg.mbf_destroy_object()
        buf.mbf_destroy_buffer()

        collect_Garbage()

        print('>>> Waiting for events...\n')
        return
    
    try:
        data_Selection_Class.select_And_Create_Msgs()
    except Exception, e:
        handel_Exception('ERROR: %s' % str(e), AMBA_Message_Process_Class.AMBA_Request_Id)
        
        AMBA_Message_Process_Class = None
        data_Selection_Class = None
        
        amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
        msg.mbf_destroy_object()
        buf.mbf_destroy_buffer()

        collect_Garbage()

        print('>>> Waiting for events...\n')
        return
    
    nbr_of_msg = 0
    
    for message in data_Selection_Class.Messages:
        if post_Message(message):
            nbr_of_msg = nbr_of_msg + 1
        
    #Send Control message
    amend = AMBA_Message_Amend(data_Selection_Class.Control_Message, ['DATA', 'MESSAGE_DETAIL'], 'MESSAGE_COUNT', str(nbr_of_msg))
    post_Message(amend.AMBA_Message)

    #Destructors
    AMBA_Message_Process_Class = None
    data_Selection_Class = None
    
    amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
    msg.mbf_destroy_object()
    buf.mbf_destroy_buffer()

    collect_Garbage()

    '''--------------------------------------------------------------------
                                Check Memory of ATS
    --------------------------------------------------------------------'''
    Utils.Log(True, 'Currenct Memory Consuption: %s KB' %str(acm.Memory().VirtualMemorySize() / 1024.00))
    
    if int(acm.Memory().VirtualMemorySize()) / 1024.00 > Params.MEMORY_THRESHOLD:
        restart()
        
    print('>>> Waiting for events...\n')

def start(*rest):
    try:
        '''--------------------------------------------------------------------
            Start up AMB Connection to read External AMBA Messages
        --------------------------------------------------------------------'''
        Utils.Log(False, 'CBFETR ATS start-up commenced at %s' % (time.ctime()))
        try:
            Utils.Log(False, 'Setting up AMB subscriptions...')
            reader_AMB = AMB_Reader(Params.ambAddress, Params.receiverMBName, event_cb, Params.receiverSource)
            if not reader_AMB.open_AMB_Receiver_Connection():
                Utils.Log(True, 'ERROR: Could not open the Receiver AMB connection.')
                raise Exception('ERROR: Could not open the Receiver AMB connection.')
                
            Utils.Log(True, 'CBFETR ATS start-up completed.')

        except RuntimeError, runtimeError:
            Utils.Log(True, 'CBFETR ATS start-up failed, %s' % runtimeError)
        print ('>>> Waiting for events...\n')
        amb.mb_poll()
    except Exception, error:
        Utils.Log(True, "Failed to run start, "  + str(error))

def stop():
    ''' Stop. '''
    return


def status():
    ''' Status. '''
    Utils.LogTrace()

    return

def restart():
    global ATS_STATUS
    ATS_STATUS = 'SHUTING DOWN'
    Utils.Log(True, "WARNING: Memory usage above threshold!")
    Utils.Log(True, "WARNING: Restarting ATS...")
    os._exit(1)

def handel_Exception(AMBA_Error_Message_Text, request_id):
    error_msg = Message_Info('ERROR', request_id, AMBA_Error_Message_Text)
    post_Message(error_msg.AMBA_Error_Message)

def post_Message(message):
    post_To_AMB_Success = False
    post_To_AMB_Success = write_AMB.post_Message_To_AMB(message)
    if not post_To_AMB_Success:
        Utils.Log(True, 'Error: Could not post the following message onto the AMB:\n%s' % message.AMBA_Message.mbf_object_to_string())
    return post_To_AMB_Success

def collect_Garbage():
    acm.Memory().GcWorldStoppedCollect()
    gc.collect()
