"""
    The violation class is used to model a mandate breach violation.
"""
import re
import json

import acm
import GenericMandatesRunScriptSetup
from GenericMandatesLogger import getLogger, printTraceBack
from GenericMandatesDefinition import Mandate
from ViolationReasonAnalyser import ViolationBreachAnalyser


PREFIX = "TMP2/"


class Violation:
    def __init__(self, limit, acmTrade, tradeUuid, mandateType, mandatedEntity, mandateVersion, tradeVersion,
                 breachComment):
        self.acmTrade = acmTrade
        self.loggedOnUser = acm.User().Name()
        self.loggedOnUserName = acm.User().FullName() if acm.User().FullName() else ''
        self.tradeNumber = acmTrade.Oid() if 'Oid' in dir(acmTrade) and acmTrade.Oid() > 0 else 'New Trade'
        self.tradeOptionalKey = tradeUuid
        self.mandateType = mandateType
        self.mandatedEntity = mandatedEntity
        self.mandateVersion = mandateVersion
        self.tradeVersion = tradeVersion
        self.breachComment = breachComment
        self.tradeBreachNotes = []
        self.limit = limit
        self.tradeBreachParams = {}
        self.mandateRuleQueryFolders = []
        self.breachReasonsList = []

        self.BuildViolationEventParams()
        self.GetViolationReason()
        self.BuildViolationNotes()
        self.AddAdditionalTradeParams(acmTrade)


    def GetViolationReason(self):
        """
            Retrieve the reason for the mandate violation
        """
        for mandateRuleQueryfolder in self.mandateRuleQueryFolders:
            violationAnalyser = ViolationBreachAnalyser(self.acmTrade, mandateRuleQueryfolder)
            self.breachReasonsList = violationAnalyser.FindBreachReason() 


    def BuildViolationNotes(self):
        """
            Prepare the note for the business process
        """
        self.tradeBreachNotes.append(self.breachComment)
        self.tradeBreachNotes.append('-----------------------------------------------------')
        self.tradeBreachNotes.append('Trader not mandated to trade {0}''s with:'.format(self.acmTrade.Instrument().InsType()))

        for breachReason in self.breachReasonsList:
            getLogger().info(breachReason)
            self.tradeBreachNotes.append('    - {0}'.format(breachReason))


    def BuildViolationEventParams(self):
        """
        Add parameters containing violation detail to the Business Process.
        """
        self.tradeBreachParams['LoggedOnUser'] = '%s' % self.loggedOnUser
        self.tradeBreachParams['LoggedOnUserName'] = '%s' % self.loggedOnUserName
        self.tradeBreachParams['TradeNumber'] = '%s' % self.tradeNumber
        self.tradeBreachParams['TradeOptionalKey'] = '%s' % self.tradeOptionalKey
        self.tradeBreachParams['MandateType'] = '%s' % self.mandateType
        self.tradeBreachParams['MandatedEntity'] = '%s' % self.mandatedEntity
        self.tradeBreachParams['MandateVersion'] = '%s' % self.mandateVersion
        self.tradeBreachParams['TradeVersion'] = '%s' % self.tradeVersion
        
        try:
            mandate = Mandate(self.limit)
            for folderName in mandate.QueryFolders():
                qf = acm.FStoredASQLQuery[folderName]
                self.mandateRuleQueryFolders.append(qf)

            self.tradeBreachParams['QueryFolders'] ='%s' % ",".join(str(id) for id in mandate.QueryFolders())
        except Exception as e:
            getLogger().error('[ERROR] %s' % e)


    def AddAdditionalTradeParams(self, trade):
        """
        Add additional parameters to the Business Process containing detail about the trade.
        :param trade: FTrade
        """
        instrument = trade.Instrument()
        underlyingIns = trade.Instrument().Underlying()

        insName = instrument.Name()
        insType = instrument.InsType()
        insCurrency = instrument.Currency().Name()

        # Set the parameters for the instrument
        self.tradeBreachParams['Instrument Name'] = '%s' % insName
        self.tradeBreachParams['Instrument Type'] = '%s' % insType
        self.tradeBreachParams['Instrument Currency'] = '%s' % insCurrency

        if underlyingIns:
            # Set the parameters for the underlying instrument
            undInsName = underlyingIns.Name()
            undInsType = underlyingIns.InsType()
            undInsCurrency = underlyingIns.Currency().Name()

            self.tradeBreachParams['Underlying Instrument Name'] = '%s' % undInsName
            self.tradeBreachParams['Underlying Instrument Type'] = '%s' % undInsType
            self.tradeBreachParams['Underlying Instrument Currency'] = '%s' % undInsCurrency

        violationCount = 0
        for mandateRuleQueryfolder in self.mandateRuleQueryFolders:
            violationAnalyser = ViolationBreachAnalyser(self.acmTrade, mandateRuleQueryfolder)
            breachReasonsList = violationAnalyser.FindBreachReason() 
            
            for breachReason in breachReasonsList:
                violationCount = violationCount + 1
                self.tradeBreachParams['Violation' + str(violationCount)] = breachReason
                getLogger().info("Violation Param{0} = {1}".format(violationCount, breachReason))


    def CreateBPFromViolation(self):
        state_chart = GenericMandatesRunScriptSetup.StateChartMandateViolation.NAME
        event = GenericMandatesRunScriptSetup.StateChartMandateViolation.EVENT_LIMIT_BREACH
        bp = acm.BusinessProcess.InitializeProcess(self.limit, state_chart)
        bp.HandleEvent(event, self.tradeBreachParams, self.tradeBreachNotes)
        bp.Commit()
        return bp


def CreateViolation(limit, acmTrade, tradeUuid, mandateType, mandatedEntity, mandateVersion, tradeVersion,
                    breachComment):
    if breachComment:
        try:
            violation = Violation(limit, acmTrade, tradeUuid, mandateType, mandatedEntity, mandateVersion,
                                  tradeVersion, breachComment)
            bp = violation.CreateBPFromViolation()
            StoreTradeData(acmTrade, bp)
            return violation
        except Exception, ex:
            getLogger().error('Exception occurred when saving mandate breach business process. Exception: %s' % ex)
            printTraceBack()


def StoreTradeData(trade, bp):
    CreateTextObject(trade, bp)


def GetTradeAMBA(trade):
    """
    Get a string representation of the AMBA message generated from a Trade.
    :param trade: FTrade
    :return: string
    """
    gen = acm.FAMBAMessageGenerator()

    newTrade = acm.FTrade()
    newTrade.Apply(trade.Clone())
    newTrade.OptionalKey('')
    newTrade.ConnectedTrdnbr(None)
    newTrade.ContractTrdnbr(None)
    newTrade.TrxTrade(None)
    newTrade.MirrorTrade(None)
    message = gen.Generate(newTrade)

    trdMessage = message.FindMessages("TRADE")
    trdMessage[0].RemoveKeyString("INSADDR.INSID")
    trdMessage[0].AtPut("INSADDR.INSID", "%s%s" % (PREFIX, trade.Instrument().Name()))
    return "%s" % message


def GetInstrumentAMBA(trade):
    """
    Get a string representation of the instrument linking to the trade in AMBA string format.
    :param trade: FTrade
    :return: string
    """
    gen = acm.FAMBAMessageGenerator()
    newIns = acm.DealCapturing.CreateNewInstrument('%s' % trade.Instrument().InsType())
    message = gen.Generate(trade.Instrument().Clone())

    insMessage = message.FindMessages('INSTRUMENT')
    insMessage[0].RemoveKeyString("INSID")
    insMessage[0].AtPut("INSID", "%s%s" % (PREFIX, trade.Instrument().Name()))
    return "%s" % message


def CreateTextObject(trade, bp):
    """
    Create a text object in the database and store the AMBA messages in the text field.
    :param trade: FTrade
    :param bp:
    """
    blob = GetInstrumentAMBA(trade)
    blob += GetTradeAMBA(trade)
    bpParams = bp.CurrentStep().DiaryEntry().Parameters()
    blobName = bpParams.At('TradeOptionalKey')
    selection = acm.FCustomTextObject.Select('subType="Mandates" name="Violations"')

    if not selection:
        getLogger().error('[ERROR] Violation text object does not exist')
    else:
        getLogger().debug('Updating violation text object with new violation.')
        to = selection[0]

        obj = json.loads(to.Text())
        obj[blobName] = blob
        to.Text(json.dumps(obj))
        to.Commit()


def GetTradeFromViolation(businessProcess):
    bpParams = businessProcess.CurrentStep().DiaryEntry().Parameters()
    instrument = None
    trade = None
    blobName = bpParams.At('TradeOptionalKey')

    print bpParams

    if bpParams.At('TradeNumber') != "New Trade":
        print 'Select trade using Trade ID'
        print bpParams.At('TradeNo')
        trade = acm.FTrade['%s' % bpParams.At('TradeNo')]
    elif bpParams.At('TradeOptionalKey'):
        print 'Select trade using Optional Key'
        optionalKey = bpParams.At('TradeOptionalKey')
        trade = acm.FTrade.Select('optionalKey="%s"' % optionalKey)[0]
    else:
        msg = '[ERROR] Business Process does not have an optional key or trade no. (BP Oid: %s)' % businessProcess.Oid()
        getLogger().error(msg)

    selection = acm.FCustomTextObject.Select('subType="Mandates" name="Violations"')
    if not selection:
        raise Exception("Violations object does not exist")

    to = acm.FCustomTextObject["Violations"]
    obj = json.loads(to.Text())
    blob = obj[blobName]
    messages = GetMessagesFromBlob(blob)

    for message in messages:
        with open("C:\Temp\\amba.txt", "wb") as fp:
            fp.write(message)

        fp = open("C:\Temp\\amba.txt", "r")
        message = fp.read()

        obj = GetAcmObjectFromMessage(message)

        # Trade Message
        if obj.ClassName().AsString() == 'FTrade':
            getLogger().debug('Processing TRADE AMBA message')
            obj.Instrument(instrument)
            trade = obj

        # Instrument Message
        else:
            getLogger().debug('Processing INSTRUMENT AMBA message')
            instrument = obj

    return trade, instrument


def GetMessagesFromBlob(blob):
    """ Read AMBA messages from text file and return an array containing messages in text format
    """
    messages = re.findall(r"\[MESSAGE\].*?\[/MESSAGE\]", blob, flags=re.DOTALL)
    return messages


def GetAcmObjectFromMessage(message):
    """ Convert AMBA text message to ACM object
    """
    acmObject = acm.AMBAMessage.CreateObjectFromMessage(message)
    return acmObject
