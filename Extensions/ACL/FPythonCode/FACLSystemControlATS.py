""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLSystemControlATS.py"


from contextlib import contextmanager

import acm, time
from datetime import datetime

import FOperationsATSRoutines
from FOperationsATSRoutines import FOperationsATSRoutines
from FOperationsATSRoutines import FOperationsATSEngine

@contextmanager
def Cursor(connection):
    cursor = connection.cursor()
    try:
        yield cursor
        cursor.commit()
    except:
        raise
    finally:
        cursor.close()

class FACLSQLLoggingService:
    
    def __init__(self, connectionString):
        import pypyodbc as pyodbc
        self.connection = pyodbc.connect(connectionString)
    
    def GetProcessId(self, processName, activity, source):
        query = '''
BEGIN
    SELECT TOP 1 ProcessID FROM dbo.ProcessStatus 
    WHERE Process  = ?
    AND   Activity = ?
    AND   Source   = ?
    AND   EndTime IS NULL
END   
        '''
        
        with Cursor(self.connection) as cursor:
            row = cursor.execute(query, (processName, activity, source)).fetchone()
            if row:
                result = row[0]
            else:
                result = None
            return result
    
    def CreateProcess(self, processName, activity, source, userId, machine):
        query = '''
BEGIN
    SET NOCOUNT ON

    INSERT INTO dbo.ProcessStatus (Process, UserID, Machine, Activity, StatusClassID, Source, StartTime, Total, Success, Fail)
    VALUES (?, NULL, ?, ?, 622, ?, GETDATE(), 0, 0, 0)

    SELECT SCOPE_IDENTITY()
END
        '''

        with Cursor(self.connection) as cursor:
            row = cursor.execute(query, (processName, machine, activity, source))
            if row:
                return row.fetchone()[0]
            else:
                return None
    
    def UpdateProcess(self, processId, failed):
        query = '''
BEGIN
    SET NOCOUNT ON
    
    UPDATE dbo.ProcessStatus SET Total = Total + 1 
    WHERE ProcessID = ?
    
    UPDATE dbo.ProcessStatus SET %s = %s + 1 
    WHERE ProcessID = ?     
END
        '''
        if failed:
            query = query % ('Fail', 'Fail')
        else:
            query = query % ('Success', 'Success')
            
        with Cursor(self.connection) as cursor:
            if failed:
                cursor.execute(query, (processId, processId))
            else:
                cursor.execute(query, (processId, processId))
    
    def LogEvent(self, processId, event):
        query = '''
BEGIN
    SET NOCOUNT ON

    DECLARE @UserID INT

    SELECT @UserID = dbo.GetUserID(?)
    IF (@UserID = -1)
    BEGIN
        SET @UserID = NULL
    END

    INSERT INTO dbo.Events (ProcessID, DateStamp, Machine, Source, UserID, TypeID, Message) 
    VALUES (?, ?, ?, ?, @UserID, ?, ?)
END
        '''
        
        with Cursor(self.connection) as cursor:
            cursor.execute(query, (event.userId, processId, event.timestamp, event.machine, event.source, event.eventType, event.message))


class FACLLogEvent:
    
    def __init__(self, timestamp, userId, machine, eventType, source, message):
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        self.userId = userId
        self.machine = machine
        self.eventType = eventType
        self.source = source
        self.message = message 

class FACLPinger:

    def __init__(self, router, pingMsg, sleep, lastPing):
        self.router = router
        self.pingMsg = pingMsg
        self.sleep = sleep
        self.lastPing = lastPing
    
    def Ping(self):
        self.DoPing(time.time())
    
    def DoPing(self, now):
        if (now - self.lastPing) > self.sleep:
            try:
                status = self.router.RouteMessage(None, self.pingMsg)
                if status:
                    print('PING Status:', status)
            except Exception as e:
                print('PING Error:', e)
            finally:
                self.lastPing = now

class FACLSystemControlATSEngine(FOperationsATSEngine):

    def __init__(self, parameters, requestBuilder, responseBuilder, loggingService):
        super(FACLSystemControlATSEngine, self).__init__('SystemControlATS', ['FACL_STATS'], parameters, 'FACLParametersTemplate')
        self.parameters = parameters
        self.requestBuilder = requestBuilder
        self.responseBuilder = responseBuilder
        self.loggingService = loggingService

    def IsCreateObjectFromAMBAMessage(self, msg):
        return False    
        
    def Start(self):
        pass
        
    def GetProcessName(self, action, flags, adminType):
        return 'Interface Processing'    

    def GetActivity(self, action, flags, adminType):
        if action in ['Admin.Push', 'Deal.PostUpdates']:
            return 'Online'
        elif action.startswith('Deal.'):
            return 'Online Trades'
        
        return None
    
    def GetSource(self, action, flags, adminType):
        if action in ['Deal.Add', 'Deal.Modify', 'Deal.Reverse']:
            if 'ConfirmRequired' in flags:
                return 'Pre-Save Checks'
            elif 'TRIALCHECK' in flags:
                return 'Trial Checks'
            else:
                return 'Trade Save'
        elif action == 'Deal.Availability':
            return 'Availability Checks'
        elif action == 'Deal.Confirm':
            return 'Pre-Save Confirms'
        elif action == 'Deal.Reject':
            return 'Pre-Save Rejects'
        elif action == 'Deal.PostUpdates':
            return 'Trade MtM Save'
        elif action == 'Admin.Push':
            if adminType in ['Customer\Legal Entity', 'Customer\Customer Branch']:
                return 'Party Save'
            elif adminType in ['Asset Security\Equity', 'Asset Security\Fixed Income']:
                return 'Security Save'
            elif adminType == 'Currency\Currency':
                return 'FX Rate Save'
            
        return None
    
    def GetUserIdAndMachine(self, mbf_object):
        armlSource = mbf_object.mbf_find_object('SOURCE').mbf_get_value()
        return tuple(armlSource.split('::'))

    def Work(self, mbf_object, obj):
        try:
            self.DoWork(mbf_object)
        except Exception as e:
            print(e)
    
    def DoWork(self, mbf_object):
        armlRequest = mbf_object.mbf_find_object('ARML_REQUEST').mbf_get_value()
        request = self.requestBuilder(armlRequest)
        
        armlResponse = mbf_object.mbf_find_object('ARML_RESPONSE').mbf_get_value()
        response = self.responseBuilder(armlResponse)
        
        userId, machine = self.GetUserIdAndMachine(mbf_object)
        processName = self.GetProcessName(request.Action(), request.Flags(), request.AdminType())
        activity = self.GetActivity(request.Action(), request.Flags(), request.AdminType())
        source = self.GetSource(request.Action(), request.Flags(), request.AdminType())
                
        if processName and activity and source:
            datestamp = mbf_object.mbf_find_object('TIME').mbf_get_value()
            
            processId = self.loggingService.GetProcessId(processName, activity, source)
            if not processId:
                processId = self.loggingService.CreateProcess(processName, activity, source, userId, machine)
            self.loggingService.UpdateProcess(processId, response.ExceptionOccurred())
    
            if response.ExceptionOccurred():
                eventTypeException = 771
                event = FACLLogEvent(datestamp,
                                     userId,
                                     machine,
                                     eventTypeException,
                                     'Interface Processing',
                                     response.ExceptionDescription() + ' ' + request.RequestID()) 
                self.loggingService.LogEvent(processId, event)
        
        if (self.parameters.armlLogInclude == 'All') or \
           (self.parameters.armlLogInclude == 'Exception' and response.ExceptionOccurred()): 
            self.LogArMLToFile(armlRequest, armlResponse, request.RequestID())
    
    def LogArMLToFile(self, armlRequest, armlResponse, requestID):
        import os
        if self.parameters.armlLogDir:
            try:
                os.mkdir(self.parameters.armlLogDir)
            except:
                pass
            requestDir = os.path.join(self.parameters.armlLogDir, requestID)
            os.mkdir(requestDir)
            
            requestFile = os.path.join(requestDir, 'ArMLRequest.xml')
            with open(requestFile, 'w') as f:
                f.write(armlRequest)
            
            responseFile = os.path.join(requestDir, 'ArMLResponse.xml')
            with open(responseFile, 'w') as f:
                f.write(armlResponse)

def InitATS():
    from FACLParameters import CommonSettings
    from FACLParameters import SystemControlATSSettings
    from FACLArMLResponse import FACLArMLResponse
    from FACLArMLRequest import FACLArMLRequest
    
    responseBuilder = FACLArMLResponse
    requestBuilder = FACLArMLRequest
    loggingService = FACLSQLLoggingService(SystemControlATSSettings.dbConnectionString)
    
    engine = FACLSystemControlATSEngine(SystemControlATSSettings, requestBuilder, responseBuilder, loggingService)
    return FOperationsATSRoutines(engine)
    
def InitPinger():
    from FACLParameters import SystemControlATSSettings as parameters
    from FACLMessageRouter import FACLMessageRouter
    from FACLArMLMessageBuilder import FACLArMLMessageBuilder
    
    sender = parameters.senderMBName
    source = parameters.senderSource
    timeout = parameters.timeoutForReplyInSeconds
    router = FACLMessageRouter(sender, source, timeout, None)
    builder = FACLArMLMessageBuilder()
    sleep = parameters.pingInterval

    pingMsg = builder.CreatePing()
    lastPing = time.time()
    return FACLPinger(router, pingMsg, sleep, lastPing)
    
def work():
    global ats, pinger
    if ats:
        ats.Work()
    if pinger:
        pinger.Ping()

def start():
    global ats, pinger
    ats = InitATS()
    ats.Start()
    pinger = InitPinger()
