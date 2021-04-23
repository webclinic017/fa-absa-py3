""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FExportBaseConfiguration.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExportBaseConfiguration
 
    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


import FIntegration
import FFileTransporter
import FBDExport
import FExportUtils
import datetime
import base64
import acm
import FTransactionHistoryReader
import FLogger
logger = FLogger.FLogger.GetLogger("BD Export")

STATUS_CHECK = 'FO Amend'

def EnviromenatSetuprCheck(name):
    CheckTradeStatus()
    CheckTransactionHistory(name)
    FExportUtils.create_add_info("StateChart", 'Export')


def CheckContactInfo():
    sftp_list = ['SFTP Host Name', 'SFTP Port', 'SFTP Path', 'SFTP UserName', 'SFTP Password']
    for l in sftp_list:
        FExportUtils.create_add_info('Contact', l)
    ftp_list = ['FTP Username', 'FTP Hostname', 'FTP Port', 'FTP Path', 'FTP Password', 'SMTP User Name', 'SMTP Password']
    for l in ftp_list:
        FExportUtils.create_add_info('Contact', l)



def CheckTradeStatus():
    # Trade status 'FO Amend' must exist to monitor corrected trades
    global STATUS_CHECK
    customTradeStatus = STATUS_CHECK
    try:
        if not acm.FEnumeration['enum(TradeStatus)'].Enumeration(customTradeStatus):
            raise RuntimeError('No enum!')
        ts_value = acm.FTradeStatusValue.Select('')
        ts = [t for t in ts_value if t.SystemName() ==  STATUS_CHECK]
        if ts == []:
            raise RuntimeError('No Trade Status Value')
        logger.info("FO Amend status exist")
    except Exception as e:
        assert(False),  "Trade status '%s' does not exist: %s" % (customTradeStatus, e)

      
def CheckTransactionHistory(integrationId):
    # Check transaction history and subscription functionality is available.
    # This is not strictly required, so only log a warning on failure.
    try:
        subscriber = FTransactionHistoryReader.FTransactionHistorySubscriber(integrationId)
        subscription = subscriber.TransHistSubscription()
        if not subscription:
			logger.warn("Subscription to transaction history does not exist")
    except Exception as e:
		logger.warn("Failed to get transaction history subscription: %s", str(e))

def StandardExportEventId():
    return 'Export Executed'


def TradeTransitions():
    # Define a set of trade status transitions that may result in a state change in the export
    # business process.
    return (
        # A trade entering any of these statuses
        #'BO Confirmed', 'Exchange', 'FO Confirmed', 'BO-BO Confirmed' is a potential new candidate
        # for export. This will result in an export business process being created
        # for the trade, which will be processed on the next export run.
        FIntegration.FTradeStatusTransition(
            eventId=FIntegration.FTransition.CREATE_EVENT_ID,
            #toStatus=['BO Confirmed', 'Exchange', 'FO Confirmed', 'BO-BO Confirmed']),
            toStatus=['BO Confirmed']),

        # A trade entering the 'FO Amend' status via the 'Correct Trade' event.
        FIntegration.FTradeStatusTransition(
            eventId='Correct Trade',
            toStatus=['FO Amend']),

        # A trade entering the 'BO Confirmed' via the 'Correction Confirmed' event.
        FIntegration.FTradeStatusTransition(
            eventId='Correction Confirmed',
            toStatus=['BO Confirmed']),

        # A voided trade will move the export business process via a 'Void Trade' event, such that
        # the counterpart will be notified on the next export run.
        FIntegration.FTradeStatusTransition(
            eventId='Void Trade',
            toStatus=['Void']),
    )


def FileTransferFinderFunction(params):
    transfers = []
    if params.EnableEmail == 'true':
        transfers.append(EmailTransfer(params))
    if params.EnableFTP == 'true':
        transfers.append(FTPTransfer(params))
    if params.EnableSFTP == 'true':
        transfers.append(SFTPTransfer(params))
    return transfers

def EmailTransfer(params):
    smtpServer = FFileTransporter.FEmailTransfer.SMTPServer(params.EmailHostName)
    message = FFileTransporter.FEmailTransfer.Message([params.EmailRecipient],
                                                      EmailVariablesToValues(params, params.EmailSubject),
                                                      params.EmailSender,
                                                      EmailVariablesToValues(params, params.EmailBody))
    return FFileTransporter.FEmailTransfer(smtpServer, message)
    
def EmailVariablesToValues(params, freeText):
    emailVariables = FBDExport.emailVariables()
    for key, value in emailVariables.items():
        try:
            freeText = freeText.replace(key, getattr(params, value))
        except (AttributeError):
            freeText = freeText.replace(key, value)
    return freeText

def TransformFileName(filename):
    now = datetime.datetime.now()
    variables = {
        '%EXPORT_DATE%': now.strftime('%Y%m%d'),
        '%EXPORT_TIME%': now.strftime('%H%M%S'),
    }
    
    for variable, value in variables.items():
        filename = filename.replace(variable, value)
    return filename

def decrypt_password(password):
    if password and password[:3] == "0Ox":
        decrypted_pwd = password[3: len(password)]
        decrypted_pwd = base64.b64decode(str(decrypted_pwd))
        return decrypted_pwd
    return password
    
def FTPTransfer(params):
    ftpServer = FFileTransporter.FFTPTransfer.FTPServer(params.FTPHostName,
                                                        params.FTPPortNumber,
                                                        params.FTPUserName,
                                                        decrypt_password(params.FTPPasswordSecret),
                                                        params.FTPPath)
    return FFileTransporter.FFTPTransfer(ftpServer)
    
    
def SFTPTransfer(params):
    sftpServer = FFileTransporter.FFTPTransfer.FTPServer(params.SFTPHostName,
                                                        params.SFTPPortNumber,
                                                        params.SFTPUserName,
                                                        decrypt_password(params.SFTPPasswordSecret),
                                                        params.SFTPPath)
    return FFileTransporter.FSFTPTransfer(sftpServer)
    
def ExportEventId():
    return FExportUtils.StandardExportEventId()
    
def PartyFinderFunction(_trade):
    
    class Dummy(object):
        def Name(self):
            return 'NoName'
        
    return Dummy()
    
def InstrumentACMQueryPrefix(insquery):
    return insquery
    
def InstrumentChartId(ChartId):
    return ChartId
    
def _GetObjectTypeFromExportIdentifier(singleExportIdentifier):
    # TODO: This should maybe be accessible directly from FSingleExportIdentifier
    objectTypeMap = {
        'FTradeSheet': 'Trade',
        'FDealSheet': 'Instrument',
    }
    sheetTemplate = acm.FTradingSheetTemplate[singleExportIdentifier.SheetTemplateId()]
    assert(sheetTemplate), 'Failed to load sheet template: ' + str(singleExportIdentifier.SheetTemplateId())
    sheetType = str(sheetTemplate.SheetClass())
    return objectTypeMap.get(sheetType, None)

def FilenameFunction(singleExportIdentifier):
    userOptions = singleExportIdentifier.ExportProcess().AdditionalParameters()
    exportObjectType = _GetObjectTypeFromExportIdentifier(singleExportIdentifier)
    try:
        if exportObjectType == 'Trade':
            filename = FIntegration.GetFileNameField(userOptions.FileName, singleExportIdentifier)
            return filename
        elif exportObjectType == 'Instrument':
            filename = FIntegration.GetFileNameField(userOptions.Instrument_iFileName, singleExportIdentifier)
            return filename
    except (AttributeError):
		logger.error('File Settings not added to GUI')

class TestModeAlAndaluz():
    def __init__(self, mode):
        self._mode = mode
        
    def IsEnabled(self):
        return self._mode
        
    def IsFileTransferEnabled(self):
        return True