""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/FIntegration.py"

"""--------------------------------------------------------------------------
MODULE
    FIntegration -
    This module contains the class definition of FIntegration which forms the center
    of any AMI. With setters you can form your instance of FIntegration to fit the
    needs of a specific integration.

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-----------------------------------------------------------------------------"""
import inspect
import tempfile
import datetime
import acm
import FExportUtils
import FFileTransporter

class IntegrationTypeEnum():
    """
    Enums for
    """
    PRIMEBROKER = 0
    FUNDADMIN = 1
    #You must set your own PartyFinderFunction if you use any other


class FIntegration:

    FTP_CONTACT_NAME = 'FTP Server'
    def __init__(self, integrationId, tradeTransitions, integrationType = IntegrationTypeEnum.PRIMEBROKER):
        self._id = str(integrationId)
        self._integrationType = integrationType
        self._tradeTransitions = None
        self._templateName = None
        self._tradeACMQueryPrefix = None
        self._linkedExportObjects = None
        self._chartId = self.Id()
        self._sheetTemplateFinderFunction = lambda ACMQueryId: ACMQueryId
        self.ExportEventId("Export Executed")
        self.TradeTransitions(tradeTransitions)
        self.TradeACMQueryPrefix(self.Id() + '_')
        self._linkedExportObjects = []
        self._partyFinderFunctionHook = None
        self._enableGUI = 'false'
        self._expParty = ''

    def _exportEventId(self):
        # pylint: disable-msg=E0202
        return FExportUtils.StandardExportEventId()

    def _postTransformationFunction(self, filepath):
        return

    def _XSLTTemplateFinderFunction(self, singleExportIdentifier):
        # pylint: disable-msg=E0202
        return 'FCSVTemplateFormatedDataNoHeader'

    def _partyFinderFunction(self, trade):
        """
        if generating an empty report in case when there is no trades nor BPs is needed,
        then use a party that is not bound to a trade
        """
        if self._enableGUI == 'true' and self._expParty != '':
            return FExportUtils.ExportParty(self._expParty).GetPartyObj(trade)
        elif self._partyFinderFunctionHook != None:
            return self._partyFinderFunctionHook(trade)

        if self._integrationType is IntegrationTypeEnum.PRIMEBROKER:
            return trade.Broker()
        elif self._integrationType is IntegrationTypeEnum.FUNDADMIN:
            return trade.Acquirer()
        return None

    def _contactFinderFunction(self, singleExportIdentifier):
        # pylint: disable-msg=E0202
        party = acm.FParty[singleExportIdentifier.PartyId()]
        for contact in party.Contacts():
            if contact.Name() == self.FTP_CONTACT_NAME:
                return contact
        return None

    def _fileTransferFunction(self, singleExportIdentifier):
        # pylint: disable-msg=E0202
        contact = self._contactFinderFunction(singleExportIdentifier)
        if contact:
            transfers = list()
            #Set up FTP transport
            ftpServer = FFileTransporter.FFTPTransfer.FTPServer.createFromPartyOrContact(contact)
            transfers.append(FFileTransporter.FFTPTransfer(ftpServer))

            #Set up email/SMTP transport
            try:
                userOptions = singleExportIdentifier.ExportProcess().AdditionalParameters()
                if userOptions.SendEmail == 'true':

                    recipients = self.Split(userOptions.EmailRecipient, [',', ';', ' '])
                    sender = userOptions.EmailSender
                    subject = self.GetEmailField(userOptions.EmailSubject, singleExportIdentifier, recipients)
                    body = self.GetEmailField(userOptions.EmailBody, singleExportIdentifier, recipients)

                    ai = contact.AdditionalInfo()
                    smtpServer = FFileTransporter.FEmailTransfer.SMTPServer(ai.SMTP_Server(), ai.SMTP_Port(), ai.SMTP_Username(), ai.SMTP_Password())
                    smtpMessage = FFileTransporter.FEmailTransfer.Message(recipients, subject, sender, body)
                    smtpTransfer = FFileTransporter.FEmailTransfer(smtpServer, smtpMessage)
                    if recipients:
                        transfers.append(smtpTransfer)
            except (AttributeError):
                print('Email Settings not added to GUI')

            return transfers
        raise LookupError('Could not find an recipient contact for party ' + str(singleExportIdentifier.PartyId()))

    def _filenameFunction(self, singleExportIdentifier):
        # pylint: disable-msg=E0202
        try:
            userOptions = singleExportIdentifier.ExportProcess().AdditionalParameters()
            if userOptions.EnableFileSettings == 'true':
                fileName = self.GetFileNameField(userOptions.FileName, singleExportIdentifier)
                return fileName + '.txt'
        except (AttributeError):
            print('File Settings not added to GUI')
        return self.GetFileNameField('trades_%EXPORT_DATE%.txt', singleExportIdentifier)

    def _filePathFunction(self, singleExportIdentifier):
        # pylint: disable-msg=E0202
        try:
            userOptions = singleExportIdentifier.ExportProcess().AdditionalParameters()
            if userOptions.EnableFileSettings == 'true':
                return userOptions.FilePath
        except (AttributeError):
            print('File Settings not added to GUI')
        return tempfile.gettempdir()

    def Id(self):
        return self._id

    def SetEnableGUI(self, enableGUI):
        self._enableGUI = enableGUI

    def SetPartyFunction(self, expParty):
        self._expParty = expParty

    def TradeACMQueryPrefix(self, tradeACMQueryPrefix = None):
        if tradeACMQueryPrefix is None:
            return self._tradeACMQueryPrefix
        self._tradeACMQueryPrefix = tradeACMQueryPrefix

    def ChartId(self, chartId = None):
        if chartId is None:
            return self._chartId
        assert(acm.FStateChart[chartId]), "No FStateChart exists with name " + chartId
        self._chartId = chartId

    def StateChart(self):
        stateChart = acm.FStateChart[self.ChartId()]
        assert(stateChart), "No FStateChart exists with name " + self.ChartId()
        return stateChart

    def LinkedExportObjects(self, listOfLinkData = None):
        """
        This method gives an integration the possibility of including additional objects,
        linked to the trade, to be exported. You must also supply the state chart that is associated.
        Lastly you must append an identifier that corresponds to the selected queries sent to
        the FExportProcess instance which might come from a runscript GUI.
        Example: To include prices and instruments in an export you would call this function thus:
        LinkedExportObjects( ( lambda t: t.Price(), 'PriceExport', 'Prices' ),
        ( lambda t: t.Instrument(), 'InstrumentExport', 'Instruments' ) )
        """
        if listOfLinkData is None:
            return self._linkedExportObjects
        for func, chartId, _linkedExportObjectId in listOfLinkData:
            assert(acm.FStateChart[chartId]), "No FStateChart exists with name " + chartId
            self._ValidateCallbackFunction(func, 1)
        self._linkedExportObjects = listOfLinkData

    def TradeTransitions(self, tradeTransitions = None):
        if tradeTransitions is None:
            return self._tradeTransitions
        self._tradeTransitions = tradeTransitions

    def Split(self, txt, seps):
        default_sep = seps[0]
        for sep in seps[1:]: # we skip seps[0] because that's the default seperator
            txt = txt.replace(sep, default_sep)
        return [i.strip() for i in txt.split(default_sep) if i]

    def GetEmailField(self, txt, singleExportIdentifier, recipients):
     # Replace variable placeholders in email fields with values for this export
        now = datetime.datetime.now()

        variables = {
            '%EXPORT_DATE%': now.strftime('%Y-%m-%d'),
            '%EXPORT_TIME%': now.strftime('%H:%M:%S'),
            '%FILENAME%': self._filenameFunction(singleExportIdentifier),
            '%SHEET_TEMPLATE%': singleExportIdentifier.SheetTemplateId(),
            '%PARTY%': singleExportIdentifier.PartyId(),
            '%RECIPIENTS%': str(recipients),
        }
        for variable, value in variables.items():
            txt = txt.replace(variable, value)
        return txt

    def GetFileNameField(self, txt, singleExportIdentifier):
        now = datetime.datetime.now()
        variables = {
            '%EXPORT_DATE%': now.strftime('%Y%m%d'),
            '%EXPORT_TIME%': now.strftime('%H%M%S'),
            '%SHEET_TEMPLATE%': singleExportIdentifier.SheetTemplateId(),
            '%PARTY%': singleExportIdentifier.PartyId(),
        }
        for variable, value in variables.items():
            txt = txt.replace(variable, value)
        return txt

    @staticmethod
    def _ValidateCallbackFunction(function, numberArgsRequired=0):
        try:
            functionName = function.__name__
        except AttributeError:
            functionName = str(function)
        assert(callable(function)), \
            "Callback function '%s' must be callable" % functionName
        functionArgs = inspect.getargspec(function)
        assert(len(functionArgs.args) == numberArgsRequired or
                functionArgs.varargs or functionArgs.keywords), \
            "Callback function '%s' has incorrect number of arguments (expected %d)" % \
            (functionName, numberArgsRequired)

    ############################################
    # Hook function getter and setters here:
    ############################################

    def ExportEventId(self, eventId = None):
        if eventId is None:
            return self._exportEventId
        self._exportEventId = eventId

    def PartyFinderFunction(self, function = None):
        """
        Supply the function that given a FTrade returns the relevant FParty
        """
        if function is None:
            return self._partyFinderFunction
        self._ValidateCallbackFunction(function, 1)
        self._partyFinderFunctionHook = function

    def ContactFinderFunction(self, function = None):
        """
        Supply the function that given a FSingleExportIdentifier returns the relevant FContact
        """
        if function is None:
            return self._contactFinderFunction
        self._ValidateCallbackFunction(function, 1)
        self._contactFinderFunction = function

    def PostTransformationFunction(self, function = None):
        """
        Supply the function that transforms the file after creation
        """

        if function is None:
            return self._postTransformationFunction

        self._ValidateCallbackFunction(function, 1)
        self._postTransformationFunction = function


    def FileTransferFinderFunction(self, function = None):
        """
        Supply the function that given an FSingleExportIdentifier
        returns an FFileTransfer, or a list of FFileTransfer objects when
        sending to multiple recipients.
        """
        if function is None:
            return self._fileTransferFunction
        self._ValidateCallbackFunction(function, 1)
        self._fileTransferFunction = function

    def SheetTemplateFinderFunction(self, function = None):
        """
        Supply the function that given a ACMQuery id returns a SheetTemplate id
        """
        if function is None:
            return self._sheetTemplateFinderFunction
        self._ValidateCallbackFunction(function, 1)
        self._sheetTemplateFinderFunction = function

    def XSLTTemplateFinderFunction(self, function = None):
        """
        Supply the function that given a FSingleExportIdentifier returns a XSLTTemplate id
        """
        if function is None:
            return self._XSLTTemplateFinderFunction
        self._ValidateCallbackFunction(function, 1)
        self._XSLTTemplateFinderFunction = function

    def FilenameFunction(self, function = None):
        """
        Supply the function that given a FSingleExportIdentifier returns a SheetTemplate id
        """
        if function is None:
            return self._filenameFunction
        self._ValidateCallbackFunction(function, 1)
        self._filenameFunction = function

    def FilePathFunction(self, function = None):
        """
        Supply the function that given a FSingleExportIdentifier returns a SheetTemplate id
        """
        if function is None:
            return self._filePathFunction
        self._ValidateCallbackFunction(function, 1)
        self._filePathFunction = function

def TradeTransitions():
    return (
        FTradeStatusTransition(
            eventId=FTransition.CREATE_EVENT_ID,
            toStatus='BO Confirmed'),
        FTradeStatusTransition(
            eventId='Correct Trade',
            toStatus='FO Amend'),
        FTradeStatusTransition(
            eventId='Correction Confirmed',
            toStatus='BO Confirmed'),
        FTradeStatusTransition(
            eventId='Void Trade',
            toStatus='Void'),
    )

def GetFileNameField(txt, singleExportIdentifier):
    now = datetime.datetime.now()
    variables = {
        '%EXPORT_DATE%': now.strftime('%Y%m%d'),
        '%EXPORT_TIME%': now.strftime('%H%M%S'),
        '%SHEET_TEMPLATE%': singleExportIdentifier.SheetTemplateId(),
        '%PARTY%': singleExportIdentifier.PartyId(),
    }
    for variable, value in variables.items():
        txt = txt.replace(variable, value)
    return txt

class FTransition():
    """
    Base class
    """
    CREATE_EVENT_ID = "Create Business Process"

    def __init__(self, eventId):
        self.eventId = str(eventId)

    def EventId(self):
        return self.eventId

class FTradeStatusTransition(FTransition):
    """
    Class for modeling a trade status change event
    E.g. a trade that goes from Simulated into FO Confirmed
    But also from any state into some specific state.
    You may give each instance an Id, like "void trade"
    """
    def __init__(self, eventId, toStatus):

        tradeStatuses = acm.FEnumeration['enum(TradeStatus)'].Enumerators()
        assert(toStatus in tradeStatuses), \
            "To status is not valid (%s) for event %s" % (toStatus, eventId)

        self.toStatus = toStatus
        id_string = str(eventId) if eventId else "into %s" % toStatus
        FTransition.__init__(self, id_string)

    def TransactionHistoryTag(self):
        integer = acm.FEnumeration['enum(TradeStatus)'].Enumeration(self.toStatus)
        if integer > 20:
            return str(integer)
        else:
            return self.toStatus

    def ToStatus(self):
        return self.toStatus
