
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_HANDLER_AMB_WRITER
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module create an AMB Writer which will be available on a Handler Container.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import amb
import time
'''----------------------------------------------------------------------------------------------------------
Importing Custom Modules
----------------------------------------------------------------------------------------------------------'''
import AMB_Reader_Writer as ambReaderWriter
from FC_UTILS import FC_UTILS as UTILS
import FC_HANDLER_BASE as HANDLER_BASE
def event_cb_writer(channel, event, arg):
    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == UTILS.Constants.fcGenericConstants.DISCONNECT:
        UTILS.Logger.flogger.info(UTILS.Constants.fcExceptionConstants.AMB_WRITER_RECEIVED_DISCONNECT_EVENT)

'''----------------------------------------------------------------------------------------------------------
Class containing the AMB writer and method to create the writer.
----------------------------------------------------------------------------------------------------------'''
class FC_HANDLER_AMB_WRITER(HANDLER_BASE.FC_HANDLER_BASE):
    def __init__(self, ambHost, ambPort, mbSenderName, senderSource, senderSubject, multiSubjectAllocationNbr, isConnected):
        self._ambHost = ambHost
        self._ambPort = ambPort
        self._mbSenderName = mbSenderName
        self._senderSource = senderSource
        self._senderSubject = senderSubject
        self.multiSubjectAllocationNbr = multiSubjectAllocationNbr
        self.ambWriter = None
        self.isConnected = isConnected
    
    def initialise(self):
        self.__createAMBWriter()
    
    def __createAMBWriter(self):
        self.ambWriter = ambReaderWriter.AMB_Writer('%s:%s' %(self._ambHost, self._ambPort), self._mbSenderName, event_cb_writer,\
                            self._senderSource, self._senderSubject)
        while True:
            if self.ambWriter.open_AMB_Sender_Connection_Kerberos(UTILS.Parameters.fcGenericParameters.AmbPrincipal,
                                                                      UTILS.Parameters.fcGenericParameters.AmbUser, '',
                                                                      UTILS.ComponentName, int(
                            UTILS.Parameters.fcGenericParameters.AmbSingleSignOn),  self.isConnected) is False:
                UTILS.Logger.flogger.info(UTILS.Constants.fcExceptionConstants.AMB_WRITER_CONNECTTION_COULD_NOT_HAVEN_BEEN_EST\
                    %(self._ambHost, self._ambPort, self._mbSenderName, self._senderSubject))
                UTILS.Logger.flogger.info('Trying to reconnect in 5 seconds to AMB...')
                time.sleep(5.0)
            else:
                break


