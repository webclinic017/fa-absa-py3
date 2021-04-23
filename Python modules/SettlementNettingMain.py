#  Developer           : Heinrich Cronje
#  Purpose             : SND implementation
#  Department and Desk : Operations
#  Requester           : Miguel
#  CR Number           : 662927

import acm, ael
import amb
import time
import collections
#ambAddress = 'jhbpcs00071n01:9300'

try:    
    import FOperationsUtils as Utils
except Exception, error:
    print("Faild to import FOperationsUtils, "  + str(error))

try:
    from FSettlementUtils import Params as SettlementParams
except Exception, error:
    print("Faild to import FSettlementUtils, "  + str(error))

try:
    import SettlementNettingProcess
except Exception, error:
    print("Faild to import SettlementNettingProcess, "  + str(error))

ambMsgNbr = 0
maxUpdateCollisions = 5
eventDeque = collections.deque()
nrOfTries  = 0

dbTables = ['SETTLEMENT']

def event_cb(channel, event, arg):
    ''' Main callback function for AMB messages. The events are placed in a
    queue that is then processed by work_cb. '''
    Utils.LogTrace()

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
        Utils.Log(False, 'Added event to event queue')
    else:
        Utils.Log(True, 'Unknown event %s' % eventString)

def work():
    ''' Process the event queue. '''
    if len(eventDeque) == 0:
        return

    Utils.LogTrace()
    global nrOfTries
    queueMember = eventDeque.popleft()
    (eventCopy, channel, msgNbr) = queueMember
    if (len(eventDeque) > 0):
        Utils.Log(True, '>>> Processing event, %d in queue.' % len(eventDeque))
    buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)
    msg = buf.mbf_read()
    isUpdateCollision = SettlementNettingProcess.SettlementNettingProcess(msg)
    if isUpdateCollision: #An update collision occurred
        nrOfTries = nrOfTries + 1
        eventDeque.appendleft(queueMember) # reprocess the message
        Utils.Log(True, '>>> Event re-entered in the queue (try #%d). %d members in the queue.' %
            (nrOfTries, len(eventDeque)))
    else:
        nrOfTries = 0
    amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
    msg.mbf_destroy_object()
    buf.mbf_destroy_buffer()
    print('>>> Waiting for events...\n')
    #print 'sleep'
    #time.sleep(60)
def start():
    try:
        ''' Set up AMB connection. '''
        Utils.LogTrace()
        Utils.Log(False, 'Settlement Netting ATS start-up commenced at %s' % (time.ctime()))

        try:
            Utils.Log(False, 'Setting up AMB subscriptions...')
            amb.mb_init(SettlementParams.ambAddress)
            reader = amb.mb_queue_init_reader(SettlementParams.receiverMBNameNetting, event_cb, None)
            for dbTable in dbTables:
                subscriptionString = SettlementParams.receiverSource + '/' + dbTable
                amb.mb_queue_enable(reader, subscriptionString)
            Utils.Log(True, 'Settlement Netting ATS start-up completed.')

        except RuntimeError, runtimeError:
            errStr = 'Settlement Netting ATS start-up failed, %s' % runtimeError
            Utils.Log(True, errStr)

        print('>>> Waiting for events...\n')
        amb.mb_poll()
    except Exception, error:
        print("Failed to run start, "  + str(error))

def stop():
    ''' Stop. '''
    Utils.LogTrace()

    return

def status():
    ''' Status. '''
    Utils.LogTrace()

    return
