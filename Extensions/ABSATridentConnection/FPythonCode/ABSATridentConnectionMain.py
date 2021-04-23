""" Compiled: NONE NONE """

"""----------------------------------------------------------------------------
MODULE
    ABSATridentConnection - Module that subscribes to AMB messages.

    (c) Copyright 2010 by SunGard Front ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm
import amb
import time
import collections
import FOperationsAMBAMessage
from FOperationsAMBAMessage import AMBAMessageException
import ATSParameters as Params
import exceptions

try:
    import FOperationsUtils as Utils
except Exception, error:
    print "Failed to import FOperationsUtils, "  + str(error)

try:
    from ABSAFMQConnector import ABSAFMQConnector as ABSAFMQConnector
except Exception, error:
    print "Failed to import ABSAFMQConnector, "  + str(error)

try:
    from ABSABARMLAMBAPoster import ABSABARMLAMBAPoster as ABSABARMLPoster
except Exception, error:
    print "Failed to import ABSABARMLPoster, "  + str(error)


ambMsgNbr = 0
maxUpdateCollisions = 5
eventDeque = collections.deque()
nrOfTries  = 0
try:
    MQConnector = ABSAFMQConnector()
    BARMLPoster = ABSABARMLPoster()
except Exception, e:
    print 'Failed to create MQConnector or BARMLPoster: ', str(e)
    
dbTables = ['OPERATIONSDOCUMENT']

class UpdateCollisionException(exceptions.Exception):
    def init(self, args = None):
        self.args = args

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
        Utils.Log(True, 'Added event, %d in queue.' % len(eventDeque))
    else:
        Utils.Log(True, 'Unknown event %s' % eventString)


def GetDocument(operationsDocument):
    if operationsDocument.Size() > 0:
        return operationsDocument.Data().decode("hex").decode("zlib")
    return ""


def BARMLProcessing(message):
    Utils.LogTrace()
    messageAsString = message.mbf_object_to_string()
    BCConnectionFailed = False
    obj = None

    try:
        obj = acm.AMBAMessage.CreateSimulatedObject(messageAsString)
    except Exception, error:
        Utils.Log(True, 'Error in acm.AMBAMessage.AffirmationProcessing: %s. \nAMBA message:\n %s' % \
                 (error, messageAsString))

    if obj and obj.IsKindOf(acm.FOperationsDocument):
        operationsDocument = obj
    else:
        return False
    if not obj:
        Utils.Log(True, 'No object found in AffirmationProcess')
        # The object was deleted and was not found by CreateSimulatedObject
        return BCConnectionFailed

    Utils.Log(True, 'Got ' + str(obj.Class().Name()) + ' with name ' + str(obj.Name() + \

              ' updated by user ' + obj.UpdateUser().Name()))

    if operationsDocument.Status() == 'Pending generation':
        BARML = GetDocument(operationsDocument)
        if BARML != "":
            BCConnectionFailed = MQConnector.PushMessage(BARML, operationsDocument)

    try:
        acm.AMBAMessage.DestroySimulatedObject(obj)
    except Exception, error:
        Utils.Log(True, 'Error in acm.AMBAMessage.DestroySimulatedObject: %s. \nAMBA message:\n %s' % \
                 (error, messageAsString))

    return BCConnectionFailed

def work():
    ''' Process the event queue. '''
    if len(eventDeque) == 0:
        try:
            message = MQConnector.PeakMessage()
        except Exception, e:
            pass
        
        if message:
            try:
                BARMLPoster.ConvertToAmbaAndPost(str(message))
            except Exception, e:
                print '****Error*****', e
                MQConnector.PushMessage(message, None)
                
            MQConnector.AcceptMessage()
            
    else:
        Utils.LogTrace()
        global nrOfTries
        queueMember = eventDeque.popleft()
        (eventCopy, channel, msgNbr) = queueMember
        if (len(eventDeque) > 0):
            Utils.Log(True, '>>> Processing event, %d in queue.' % len(eventDeque))
        buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)
        msg = buf.mbf_read()
        BARMLProcessingFailed = BARMLProcessing(msg)
        if BARMLProcessingFailed: #An update collision occurred
            nrOfTries = nrOfTries + 1
            eventDeque.appendleft(queueMember) # reprocess the message
            Utils.Log(True, '>>> Connection to BCTools failed or pushing message to BCTools failed.\n>>> Event re-entered in the queue (try #%d). %d members in the queue.' %
                (nrOfTries, len(eventDeque)))
        else:
            nrOfTries = 0
            amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
        msg.mbf_destroy_object()
        buf.mbf_destroy_buffer()
        print('>>> Waiting for events...\n')


def start():
    try:
        #''' Set up AMB connection. '''
        Utils.LogTrace()
        Utils.Log(False, 'Document ATS start-up commenced at %s' % (time.ctime()))

        try:
            Utils.Log(False, 'Setting up AMB subscriptions...')
            amb.mb_init(Params.ambAddress)
            reader = amb.mb_queue_init_reader(Params.tridentConnectionReceiverMBName, event_cb, None)
            for dbTable in dbTables:
                subscriptionString = Params.receiverSource + '/' + dbTable
                amb.mb_queue_enable(reader, subscriptionString)
            Utils.Log(True, 'Documentation ATS start-up completed.')

        except RuntimeError, runtimeError:
            errStr = 'Documentation ATS start-up failed, %s' % runtimeError
            Utils.Log(True, errStr)

        print('>>> Waiting for events...\n')
        amb.mb_poll()
    except Exception, error:
        print "Failed to run start, "  + str(error)


def stop():
    ''' Stop. '''
    if MQConnector:
        MQConnector.__del__()
    Utils.LogTrace()

    return


def status():
    ''' Status. '''
    Utils.LogTrace()

    return
