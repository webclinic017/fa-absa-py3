""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLConnectorATS.py"
import acm
import amb
import FOperationsATSRoutines
from FACLWebService import FACLWebService
from FOperationsATSRoutines import FOperationsATSRoutines
from FOperationsATSRoutines import FOperationsATSEngine
from FACLMessageRouter import FACLWriteToAMB
from FACLArMLResponse import FACLArMLResponse
import FOperationsUtils as Utils
import time
import re

class FACLConnectorATSEngine(FOperationsATSEngine):
    retryOnExceptionDescription = ['Deadlock condition encountered']

    def __init__(self, parameters, ws, responseBuilder, writerClass):
        super(FACLConnectorATSEngine, self).__init__('ConnectorATS', [parameters.channel], parameters, 'FACLParametersTemplate')
        self.ws = ws
        self.senderMBName = parameters.senderMBName
        self.maxNumberOfRetries = parameters.numberOfRetries
        self.retryDelayBase = parameters.retryDelayBase
        self.responseBuilder = responseBuilder
        self.writerClass = writerClass
        self.statsSubject = parameters.senderSource + '/FACL_STATS'
    
    def IsCreateObjectFromAMBAMessage(self, msg):
        return False    
        
    def Start(self):
        self.writer=self.writerClass(self.senderMBName)
    
    def Work(self, mbf_object, obj):
        arml_obj = mbf_object.mbf_find_object('ARML_MSG','MBFE_BEGINNING')
        request = arml_obj.mbf_get_value()
        replySubject = mbf_object.mbf_find_object('SOURCE').mbf_get_value()

        try:
            Utils.LogVerbose('Raw ArML request: %s' % request)

            start = time.time()
            response = self._pushMessage( request )
            stop = time.time()
            Utils.LogVerbose('Time to process request: %.2f seconds' % (stop - start))
            
            Utils.LogVerbose('Raw ArML response: %s' % response)
            
            source = self._getSource()
            if replySubject:
                self.writer.Send(response, replySubject, source)
                Utils.LogVerbose('Response sent to subject %s' % replySubject)
            statsContents = {'ARML_REQUEST':request, 'ARML_RESPONSE':response}
            self.writer.Send(statsContents, self.statsSubject, source)
            
        except Exception, e:
            import traceback
            s = 'Failed to send message to ACR\n' + traceback.format_exc()            
            Utils.LogAlways(s)
        
    def _getSource(self):
        try:
            import win32api, win32con
            user = win32api.GetUserNameEx(win32con.NameSamCompatible)
            computer = win32api.GetComputerName()
        except:
            import getpass, socket
            user = getpass.getuser()
            computer = socket.gethostname()
            
        return '%s::%s' % (user, computer)
            
    def _pushMessage( self, request ):
        responseArml, response, exceptionOccurred = self._processRequest( request )
        
        counter = 0
        while exceptionOccurred:
            counter += 1
            if counter > 5:
                Utils.LogAlways('FACLConnectorATSEngine::_pushMessage, too many iterations, unhandled error from ACL:\n%s' % response.Exceptions())
                break
            if response.ActionAlreadyInProgress():
                # ACL waiting for confirmation, send reject and then send a Deal.Modify
                newRequest = UpdateActionInRequest( request, "Deal.Reject" )
                if newRequest:
                    Utils.LogVerbose("FACLConnectorATSEngine::_pushMessage Changing action to Deal.Reject")
                    responseArml, response, exceptionOccurred = self._processRequest( newRequest )
                else:
                    break
                if request:
                    Utils.LogVerbose("FACLConnectorATSEngine::_pushMessage resending previous request")
                    responseArml, response, exceptionOccurred = self._processRequest( request )
                else:
                    break
                
            elif response.ActionAddExistingDeal():
                # trying to add a deal which already exists in ACL, change action from Deal.Add to Deal.Modify
                request = UpdateActionInRequest( request, "Deal.Modify" )
                if request:
                    Utils.LogVerbose("FACLConnectorATSEngine::_pushMessage Changing action to Deal.Modify")
                    responseArml, response, exceptionOccurred  = self._processRequest( request )
                else:
                    break
                
            elif response.ActionModifyNonExistingDeal():
                # ACL does not recognize the deal we try to modify
                # change action from Deal.Modify to Deal.Add
                request = UpdateActionInRequest( request, "Deal.Add" )
                if request:
                    Utils.LogVerbose("FACLConnectorATSEngine::_pushMessage Changing action to Deal.Add")
                    responseArml, response, exceptionOccurred  = self._processRequest( request )
                else:
                    break
                    
            elif response.ActionConfirmWhenNoActionInProgress():
                # ACL have no action in progress for deal
                # change action from Deal.Confirm to Deal.Modify
                request = UpdateActionInRequest( request, "Deal.Modify" )
                if request:
                    Utils.LogVerbose("FACLConnectorATSEngine::_pushMessage Changing action to Deal.Modify")
                    responseArml, response, exceptionOccurred  = self._processRequest( request )
                else:
                    break
                    
            elif response.ActionDealAlreadyReversed():
                if GetAction(request).upper() == 'DEAL.REVERSE':
                    break
                # Deal is reversed on ACR side, can´t modify it
                # change action from Deal.Modify to Deal.Add
                request = UpdateActionInRequest( request, "Deal.Add" )
                if request:
                    Utils.LogVerbose("FACLConnectorATSEngine::_pushMessage Changing action to Deal.Add")
                    responseArml, response, exceptionOccurred  = self._processRequest( request )
                else:
                    break
            else:
                break

        return responseArml
            
            
    def _processRequest(self, request):
        responseArml = None
        numRetries = 0
        exceptionOccurred = False
        
        while True:
            responseArml = self.ws.ProcessRawArMLRequest(request)
            response = self.responseBuilder(responseArml)
            exceptionOccurred = response.ExceptionOccurred()
            if exceptionOccurred and self._isRetryPossible(response.Exceptions()):
                numRetries += 1
                if numRetries <= self.maxNumberOfRetries:
                    sleepTime = self.retryDelayBase * numRetries
                    Utils.LogVerbose('Retry number %s of %s in %s seconds' % (numRetries, self.maxNumberOfRetries, sleepTime))
                    time.sleep(sleepTime)
                else:
                    break
            else:
                break
        return responseArml, response, exceptionOccurred
        
    def _isRetryPossible(self, exceptions):
        isRetryPossible = False
        for exDesc in FACLConnectorATSEngine.retryOnExceptionDescription:
            for e in exceptions:
                exceptionDescription = e[2]
                if exDesc in exceptionDescription:
                    isRetryPossible = True
                    break
            if isRetryPossible:
                break
            
        return isRetryPossible
    
    
def _ImportInstanceParameters(atsInstanceName):
    try:
        from FACLParameters import ConnectorATSSettings
        paramClass = getattr(ConnectorATSSettings, atsInstanceName)
        return paramClass
    except Exception, e:
        raise Exception('Could not find any configuration parameters for ATS instance named %s: %s' % (atsInstanceName, str(e)))
    
def GetAction( request ):
    pattern = re.compile('<Action>(.+?)</Action>', re.IGNORECASE)
    action = pattern.search(request)
    if action:
        return action.group(1)
    else:
        return ''

def UpdateActionInRequest( request, newAction ):
    regPatt = 'Deal.Modify|Deal.Add|Deal.Reject|Deal.Reverse|Deal.Confirm'
    pattern = re.compile(regPatt, re.IGNORECASE)
    if not re.search(pattern, request):
        Utils.LogVerbose( "ERROR UpdateActionInRequest, could not find Action in the following request, trying to update to: %s \n %s" % (newAction, request) )
        return None
    else:
        return pattern.sub(newAction, request)
    
    
def InitATS():
    from FACLParameters import CommonSettings, ConnectorATSSettings
    parameters = _ImportInstanceParameters(acm.UserName())
    ws = FACLWebService(CommonSettings.armlServiceUrl, ConnectorATSSettings.maxMsgBufSize)
    responseBuilder = FACLArMLResponse
    writerClass = FACLWriteToAMB
    engine = FACLConnectorATSEngine(parameters, ws, responseBuilder, writerClass)
    return FOperationsATSRoutines(engine) 

def work():
    global ats
    if ats:
        ats.Work()

def start():
    global ats
    ats = InitATS()
    ats.Start()
