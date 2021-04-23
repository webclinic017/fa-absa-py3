'''----------------------------------------------------------------------------------------------------------
MODULE                  :       PACE_MM_ATS
PROJECT                 :       PACE MM
PURPOSE                 :       This module serves as the ATS logic. It will read, process and post messages from
                                and to the AMB.
DEPARTMENT AND DESK     :       Money Market Desk
REQUASTER               :       PACE MM Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       822638
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-09-01      822638          Heinrich Cronje                 Initial Implementation
2012-08-08      390267          Heinrich Cronje                 Commented out the first Message Accept instruction.

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module will the "module_name" in the installed ATS on the server. When the ATS is started the
    start function is called.
    
    On this start-up, two connections to the AMB are created. A sender to sent NOT_ACKNOWLEDGE message
    to the AMB and a reader to read ADS and External AMBA messages from the AMB.
'''

import amb, time, collections
import FOperationsUtils as Utils
import PACE_MM_Parameters as Params
from PACE_MM_Message_Processing import PACE_MM_Message_Processing as Message_Process
from PACE_MM_Message_Creator import PACE_MM_Message_Creator as Message_Creator
from AMB_Reader_Writer import AMB_Writer as AMB_Writer, AMB_Reader as AMB_Reader

ambMsgNbr = 0
eventDeque = collections.deque()

'''--------------------------------------------------------------------
    Callback function for posting message onto the AMB
--------------------------------------------------------------------'''
def event_cb_AMB_Sender(channel, event, arg):
    pass

write_AMB = AMB_Writer(Params.ambAddress, Params.senderMBName, event_cb_AMB_Sender, Params.senderExternalSource, Params.senderExternalSource)
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
    '''--------------------------------------------------------------------
                            Process the Event Queue
    --------------------------------------------------------------------'''
    if len(eventDeque) == 0:
        return
    
    queueMember = eventDeque.popleft()
    (eventCopy, channel, msgNbr) = queueMember
    if (len(eventDeque) > 0):
        Utils.Log(True, '>>> Processing event, %d in queue.' % len(eventDeque))
    #amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
    
    buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)
    
    Utils.Log(True, '===================================================================')
    Utils.Log(True, 'The PACE_MM_ATS received the following AMB message with msgnbr: %s' % str(eventCopy.id))
    Utils.Log(True, '===================================================================')
    
    msg = buf.mbf_read()
    #print msg.mbf_object_to_string()

    pace_MM_Message_Processing = Message_Process(eventCopy.subject, msg)
    processAMBAMessage = pace_MM_Message_Processing.process_AMBA_message()
    
    if processAMBAMessage:
        post_To_AMB_Success = False
        pace_MM_Message_Create = Message_Creator(processAMBAMessage)
        pace_mm_message = pace_MM_Message_Create.create_PACE_MM_Message()

        for message in pace_mm_message:
            post_To_AMB_Success = write_AMB.post_Message_To_AMB(message)
            if not post_To_AMB_Success:
                Utils.Log(True, 'Error: Could not post the following message onto the AMB:\n%s' % message.mbf_object_to_string())
                return

    amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
    msg.mbf_destroy_object()
    buf.mbf_destroy_buffer()
    print('>>> Waiting for events...\n')
    
def start(*rest):
    try:
        '''--------------------------------------------------------------------
            Start up AMB Connection to read ADS and External AMBA Messages
        --------------------------------------------------------------------'''
        Utils.Log(False, 'PACE_MM ATS start-up commenced at %s' % (time.ctime()))
        try:
            Utils.Log(False, 'Setting up AMB subscriptions...')
            reader_AMB = AMB_Reader(Params.ambAddress, Params.receiverMBName, event_cb, Params.subscriptionSourceList)
            if not reader_AMB.open_AMB_Receiver_Connection():
                Utils.Log(True, 'ERROR: Could not open the Receiver AMB connection.')
                raise Exception('ERROR: Could not open the Receiver AMB connection.')
                
            Utils.Log(True, 'PACE_MM ATS start-up completed.')

        except RuntimeError, runtimeError:
            Utils.Log(True, 'PACE_MM ATS start-up failed, %s' % runtimeError)

        print ('>>> Waiting for events...\n')
        amb.mb_poll()
    except Exception, error:
        Utils.Log(True, "Failed to run start, "  + str(error))

def stop():
    ''' Stop. '''
    return


def status():
    ''' Status. '''
    
    return
