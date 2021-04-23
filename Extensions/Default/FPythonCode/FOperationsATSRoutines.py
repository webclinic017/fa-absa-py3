""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsATSRoutines.py"

"""----------------------------------------------------------------------------
MODULE
    FOperationsATSRoutines - Common Operations ATS functions.

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

DEPENDENCY

NOTE

----------------------------------------------------------------------------"""

import acm, amb
import sys, traceback
import collections

try:
    import FOperationsUtils as Utils
except ImportError as error:
    print("Failed to import FOperationsUtils, "  + str(error))
try:
    import FOperationsExceptions as Exceptions
except ImportError as error:
    print("Failed to import AMBConnectionException from FOperationsUtils, "  + str(error))

ambMsgNbr = 0
eventDeque = collections.deque()
nrOfTries  = 0
isConnected = False

class FOperationsATSEngine(object):

    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        self.__name = name
        self.__dbTables = dbTables
        self.__paramsModule = paramsModule
        self.__paramsModuleTemplateName = paramsModuleTemplateName
        self.detailedLogging = self.__GetDetailedLogging()

    def GetName(self):
        return self.__name

    def GetDBTables(self):
        return self.__dbTables

    def GetParamsModule(self):
        return self.__paramsModule

    def GetParamsModuleName(self):
        return self.__paramsModule.__name__

    def IsCreateObjectFromAMBAMessage(self, dummyMsg):
        return True

    def GetParamsModuleTemplateName(self):
        return self.__paramsModuleTemplateName

    def __GetDetailedLogging(self):
        if hasattr(self.__paramsModule, 'detailedLogging'):
            return self.__paramsModule.detailedLogging
        return True


class FOperationsATSRoutines(object):

    def __init__(self, aTSEngine):
        '''
        Constructor
        '''
        self.__aTSName = aTSEngine.GetName()
        self.__dbTables = aTSEngine.GetDBTables()
        self.__aTSEngine = aTSEngine
        self.__aTSEngineModule = aTSEngine.GetParamsModule()
        self.__atsRunning = True
        self.__updateCollision = False


    def Start(self, taskParameters = None):
        ''' Set up AMB connection. '''
        global isConnected

        Utils.InitFromParameters(self.__aTSEngineModule, taskParameters)

        try:
            Utils.VerifyParameterModule(self.__aTSEngine.GetParamsModuleTemplateName(), self.__aTSEngine.GetParamsModuleName())
        except Exceptions.ParameterModuleException as parametersModuleError:
            Utils.LogAlways('%s ATS start-up failed.' % self.__aTSName)
            raise parametersModuleError

        try:
            Utils.InitAMBConnection(EventCB, self.__dbTables)
            isConnected = True
        except Exceptions.AMBConnectionException as AMBError:
            errStr = '%s ATS start-up failed. %s' % (self.__aTSName, AMBError)
            Utils.LogAlways(errStr)
            return
        try:
            self.__aTSEngine.Start()
        except SystemExit as systemExit:
            Utils.LogAlways('System halted.')
            raise systemExit
        else:
            Utils.LogAlways('%s ATS start-up completed.' % (self.__aTSName))
            print('>>> Waiting for events...\n')
            amb.mb_poll()


    def Work(self):
        ''' Process the event queue. '''
        global isConnected

        if isConnected == False:
            Utils.ReconnectRoutine(EventCB, self.__dbTables)
            amb.mb_poll()
            isConnected = True

        while len(eventDeque) > 0:
            global nrOfTries

            queueMember = eventDeque.popleft()
            (eventCopy, channel, msgNbr) = queueMember
            if (len(eventDeque) > 0):
                Utils.LogVerbose('>>> Processing event with mid %d (%d in queue).' % (eventCopy.id, len(eventDeque)))
            buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)
            msg = buf.mbf_read()  #should be intact for ack purposes
            obj = None

            try:
                if self.__aTSEngine.IsCreateObjectFromAMBAMessage(msg):
                    obj = self.__CreateObjectFromAMBAMessage(msg)
                    if obj != None:
                        self.__aTSEngine.Work(msg, obj)
                    else:
                        Utils.LogVerbose('No object corresponding to the AMBA message was found')
                        # The object was deleted and was not found by CreateSimulatedObject
                else:
                    self.__aTSEngine.Work(msg, obj)

                nrOfTries = 0
                self.__updateCollision = False

            except Exceptions.UpdateCollisionException as e:
                nrOfTries = nrOfTries + 1
                eventDeque.appendleft(queueMember) # reprocess the message
                Utils.LogAlways('>>> Event with mid %d re-entered in the queue (try #%d). %d members in the queue.' % (eventCopy.id, nrOfTries, len(eventDeque)))
                self.__updateCollision = True
            except SystemExit as _:
                Utils.LogAlways('System halted.')
                self.Stop()
            except Exceptions.InvalidHookException as e:
                raise e
            except Exception as e:
                Utils.LogAlways('>>> Exception caught when processing message with mid %d.' % (eventCopy.id))
                traceback.print_exc(file=sys.stdout)
                Utils.LogAlways('>>> AMBA Message:\n%s' % (msg.mbf_object_to_string()))
                raise e

            if eventCopy and not self.__updateCollision:
                try:
                    amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
                except Exception:
                    print("Did not succeed to accept queue message %s, trying again" % (str(msgNbr)))
                    amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
            if msg:
                msg.mbf_destroy_object()
            if buf:
                buf.mbf_destroy_buffer()

            try:
                acm.AMBAMessage.DestroySimulatedObject(obj)
            except Exception as e:
                Utils.LogAlways('Error in acm.AMBAMessage.DestroySimulatedObject: %s. \nAMBA message:\n %s' % (e, msg.mbf_object_to_string()))

            if self.__aTSEngine.detailedLogging:
                print('>>> Waiting for events...\n')

    def Stop(self):
        ''' Stop. '''
        self.__aTSEngine.Stop()
        return

    def Status(self):
        ''' Status. '''
        return self.__aTSEngine.Status()

    def __CreateObjectFromAMBAMessage(self, message):
        try:
            messageAsString = message.mbf_object_to_string()
            simulatedObject = acm.AMBAMessage.CreateSimulatedObject(messageAsString)
            return simulatedObject
        except Exception as e:
            raise Exceptions.MessageConversionException('Error in acm.AMBAMessage.CreateSimulatedObject.\nAMBA message:\n%s' % (messageAsString), e)
        if simulatedObject == None:
            raise Exceptions.MessageConversionException('Could not create simulated object from message.\nAMBA message:\n%s' % (messageAsString))


def EventCB(channel, event, dummyArg):
    ''' Main callback function for AMB messages. The events are placed in a
    queue that is then processed by work_cb. '''

    global ambMsgNbr
    global isConnected

    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == 'Status':
        try:
            ambMsgNbr = int(event.status.status)
        except ValueError:
            ambMsgNbr = 0
    elif eventString == 'Message':
        ambMsgNbr += 1
        eventDeque.append((amb.mb_copy_message(event.message), channel, ambMsgNbr))
        Utils.LogVerbose('Added event with mid %d (%d in queue).' % (event.message.id, len(eventDeque)))
    elif eventString == 'Disconnect':
        isConnected = False
    else:
        Utils.LogAlways('Unknown event %s' % eventString)



