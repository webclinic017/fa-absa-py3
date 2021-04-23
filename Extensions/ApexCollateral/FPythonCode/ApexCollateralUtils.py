testMode = False

import amb
import acm
import socket
import smtplib
import at_addInfo
import traceback

from time import time
from datetime import datetime
from xml.etree import ElementTree
from collections import deque
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import ApexParameters
Params = ApexParameters.load()


class FunctionalError(Exception):
    pass


class MessageBrokerType:
    ActiveMQ = "ActiveMQ"
    WebSphereMQ = "WebSphereMQ"


metrics = {
    "TotalMessageCount":0, "ProcessedMessageCount":0,
    "LongestMessageDuration":None, "LongestMessageDurationTrade":None,
    "TotalDuration":None, "TotalProcessedMessageDuration":None,
    "FirstProcessedMessageDuration":None
}

def captureMetrics(duration, processed, tradeNo):
    metrics["TotalMessageCount"] = metrics["TotalMessageCount"] + 1
    if (metrics["LongestMessageDuration"] is None or
            duration > metrics["LongestMessageDuration"]):
        metrics["LongestMessageDuration"] = duration
        if processed is not None:
            metrics["LongestMessageDurationTrade"] = tradeNo
    if metrics["TotalDuration"] is None:
        metrics["TotalDuration"] = duration
    else:
        metrics["TotalDuration"] = metrics["TotalDuration"] + duration
    if processed == True:
        metrics["ProcessedMessageCount"] = metrics["ProcessedMessageCount"] + 1
        if metrics["TotalProcessedMessageDuration"] is None:
            metrics["TotalProcessedMessageDuration"] = duration
        else:
            metrics["TotalProcessedMessageDuration"] = (
                metrics["TotalProcessedMessageDuration"] + duration
            )
        if metrics["FirstProcessedMessageDuration"] is None:
            metrics["FirstProcessedMessageDuration"] = duration

    logMetrics(duration)


def logMetrics(duration):
    print "Duration:", duration
    print "TotalMessageCount:", metrics["TotalMessageCount"]
    print "ProcessedMessageCount:", metrics["ProcessedMessageCount"]
    print (
        "AverageMessageDuration:",
        metrics["TotalDuration"] / metrics["TotalMessageCount"]
    )
    if metrics["ProcessedMessageCount"] > 0:
        print (
            "AverageProcessedMessageDuration:",
            (metrics["TotalProcessedMessageDuration"] /
                metrics["ProcessedMessageCount"]
            )
        )
    print "LongestMessageDuration:", metrics["LongestMessageDuration"]
    print (
        "LongestMessageDurationTrade:", metrics["LongestMessageDurationTrade"]
    )
    print (
        "FirstProcessedMessageDuration:",
        metrics["FirstProcessedMessageDuration"]
    )


latestSentMailsDurationInSec = Params.LatestSentMailsDurationInSec
latestSentMailsDepth = Params.LatestSentMailsDepth
latestSentMails = deque(maxlen=latestSentMailsDepth)


def sendEmail(message, exception, stackTrace, logMessages):
    host = Params.EmailHost
    subject = None
    fromText = Params.EmailFrom
    toText = Params.EmailToFunctional

    xmlMessage = """<?xml version="1.0" encoding="UTF-8"?>
    <message>
        <type></type>
        <description>
        </description>
        <logMessages>
        </logMessages>
        <stackTraces>
        </stackTraces>
        <hostname>
        </hostname>
        <environmentName>
        </environmentName>
    </message>
    """

    root = ElementTree.fromstring(xmlMessage)

    if exception is not None:
        if isinstance(exception, FunctionalError):
            subject = "[%s] Front/Apex Integration Functional Error" % Params.EnvironmentSettingName
            toText = Params.EmailToFunctional
            root.find("type").text = "Functional"
        else:
            subject = "[%s] Front/Apex Integration Technical Error" % Params.EnvironmentSettingName
            toText = Params.EmailToTechnical
            root.find("type").text = "Technical"

        if stackTrace is not None:
            stackTraceLines = stackTrace.splitlines()
            if len(stackTraceLines) > 0:
                message = message + " - " + stackTraceLines[-1]
            stackTracesElement = root.find("stackTraces")
            for st in stackTraceLines:
                newNode = ElementTree.Element("stackTrace")
                newNode.text = st
                stackTracesElement.append(newNode)

    if logMessages is not None and len(logMessages) > 0:
        message = message + " - " + logMessages[-1]
    logMessagesElement = root.find("logMessages")
    for lm in logMessages:
        newNode = ElementTree.Element("logMessage")
        newNode.text = lm
        logMessagesElement.append(newNode)


    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromText
    msg['To'] = toText

    root.find("description").text = message
    root.find("hostname").text = socket.gethostname()
    root.find("environmentName").text = Params.EnvironmentSettingName

    context = acm.GetDefaultContext()
    xslExtension = context.GetExtension("FXSLTemplate", "FObject", "Email_XSL")
    transformer = acm.FXSLTTransform(xslExtension.Value())
    html = transformer.Transform(ElementTree.tostring(root))

    part = MIMEText(html, 'html')

    msg.attach(part)

    try:
        print "Sending email to %s from host %s" % (
            toText, socket.gethostname()
        )
        server = smtplib.SMTP(host)
        server.sendmail(fromText, toText.split(','), msg.as_string())
        server.quit()
    except Exception:
        traceback.print_exc()


def totalSeconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6


def log(message, logMessages=None):
    print message
    if logMessages is not None:
        logMessages.append(message)


def logError(message):
    print message


def handleException(message, exception, stackTrace, logMessages):
    print "Received Exception at %s: %s" % (acm.Time.TimeNow(), message)
    try:
        latestSentMails.append((time(), message))
        startTime = datetime.fromtimestamp(latestSentMails[0][0])
        endTime = datetime.fromtimestamp(
            latestSentMails[len(latestSentMails) - 1][0]
        )
        duration = endTime - startTime
        print "Last %s email durations: %s" % (len(latestSentMails), duration)
        if (len(latestSentMails) == latestSentMailsDepth and
                totalSeconds(duration) < latestSentMailsDurationInSec):
            print ("Not sending email as last %s messages were sent "
                   "in less than %s seconds" %
                   (latestSentMailsDepth, latestSentMailsDurationInSec))
        else:
            if not testMode:
                sendEmail(message, exception, stackTrace, logMessages)
            else:
                print "In test mode so not sending email"
    except Exception:
        traceback.print_exc()


def getStoredQuery(storedQueryName):
    storedQuery = acm.GetClass("FStoredASQLQuery").Select01(
        "name=%s" % storedQueryName,
        'Error selecting "%s" ASQL Query' % storedQueryName
    )
    if not storedQuery:
        raise Exception('Cannot find "%s" ASQL Query' % storedQueryName)
    return storedQuery


def getObject(mbf_object, tag):
    if mbf_object:
        return mbf_object.mbf_find_object(tag, 'MBFE_BEGINNING')


def getObjectValue(mbf_object, tag):
    if mbf_object:
        obj = getObject(mbf_object, tag)
        if obj:
            return obj.mbf_get_value()
    return None


def setObjectValue(obj, tag_name, tag_value):
    tag = obj.mbf_find_object(tag_name, 'MBFE_BEGINNING')
    if tag:
        obj.mbf_replace_string(tag_name, tag_value)
    return


def removeCashflows(buffer):
    i = getObject(buffer, 'INSTRUMENT')
    leg = getObject(i, 'LEG')
    while getObject(leg, 'CASHFLOW'):
        leg.mbf_remove_object()


def generateMessage(entity):
    generator = acm.FAMBAMessageGenerator(entity)
    message = generator.Generate(entity)
    messageString = str(message)
    tmp = amb.mbf_create_buffer_from_data(messageString)
    tmpMessage = tmp.mbf_read()
    removeCashflows(tmpMessage)
    setObjectValue(tmpMessage, "SOURCE", Params.MessageSource)
    return tmpMessage


def getCounterparty(SDSID):
    parties = acm.FCounterParty.Select('').AsSet()
    parties.Union(acm.FClient.Select(''))
    for party in parties:
        if (party.AdditionalInfo().BarCap_SMS_CP_SDSID() == SDSID and
                party.AdditionalInfo().BarCap_SMS_LE_SDSID() == SDSID):
            return party


def getFXRate(currency, market, date):
    usdCurrency = acm.FCurrency["USD"]
    baseCurrency = acm.FCurrency[Params.BaseCurrency]
    quoteCurrency = currency

    if date is None:
        query = 'instrument={0} and currency={1} and market={2}'
    else:
        query = 'instrument={0} and currency={1} and market={2} and day={3}'

    if date is None:
        basePricesInUSD = acm.FPrice.Select(
            query.format(usdCurrency.Oid(), baseCurrency.Oid(), market.Oid())
        )
    else:
        basePricesInUSD = acm.FPrice.Select(
            query.format(usdCurrency.Oid(), baseCurrency.Oid(),
            market.Oid(), str(date))
        )
    if len(basePricesInUSD) > 0:
        if len(basePricesInUSD) > 1:
            logError("Error found more than one price for base currency")
        else:
            if quoteCurrency == usdCurrency:
                return basePricesInUSD[0].Settle()

            if date is None:
                quotePricesInUSD = acm.FPrice.Select(
                    query.format(usdCurrency.Oid(), quoteCurrency.Oid(),
                    market.Oid())
                )
            else:
                quotePricesInUSD = acm.FPrice.Select(
                    query.format(usdCurrency.Oid(), quoteCurrency.Oid(),
                    market.Oid(), str(date))
                )
            if len(quotePricesInUSD) > 0:
                if len(quotePricesInUSD) > 1:
                    logError(
                        "Error found more than one USD price for quote " +
                        "currency"
                    )
                else:
                    return (
                        basePricesInUSD[0].Settle() /
                        quotePricesInUSD[0].Settle()
                    )
            else:
                if date is None:
                    quotePrices = acm.FPrice.Select(
                        query.format(quoteCurrency.Oid(), usdCurrency.Oid(),
                        market.Oid())
                    )
                else:
                    quotePrices = acm.FPrice.Select(
                        query.format(quoteCurrency.Oid(), usdCurrency.Oid(),
                        market.Oid(), str(date))
                    )
                if len(quotePrices) > 0:
                    if len(quotePricesInUSD) > 1:
                        logError(
                            "Error found more than one price for quote " +
                            "currency"
                        )
                    else:
                        return (
                            basePricesInUSD[0].Settle() *
                            quotePrices[0].Settle()
                        )


class ActiveMQMessageSender(object):
    connection = None
    session = None
    queue = None
    producer = None

    def __init__(self, queueName):
        import pyactivemq
        brokerURL = Params.ActiveMQBrokerURL
        log("Opening ActiveMQ connection: %s" % brokerURL)
        f = pyactivemq.ActiveMQConnectionFactory(brokerURL)
        self.connection = f.createConnection()
        log("Opened ActiveMQ connection: %s" % self.connection)
        self.session = self.connection.createSession()
        self.queue = self.session.createQueue(queueName)
        self.producer = self.session.createProducer(self.queue)

    def close(self):
        log("Closing ActiveMQ connection: %s" % self.connection)
        self.connection.close()

    def handle(self, message):
        log("Message: %s" % message)
        textMessage = self.session.createTextMessage()
        textMessage.text = message
        log("Sending to queue: %s" % self.queue)
        self.producer.send(textMessage)


class WebSphereMQMessageSender(object):
    queueManager = None
    queueName = None

    def __init__(self, queueName):
        import sys 
        #sys.path.append(r'/opt/front/arena/lib64/pythonextensionlib27/pymqi')
        import pymqi
        from pymqi import CMQC
        client = "%s(%s)" % (Params.WebSphereMQHost, Params.WebSphereMQPort)
        cd = pymqi.cd()
        cd.ChannelName = Params.WebSphereMQChannel
        cd.ConnectionName = client
        cd.ChannelType = CMQC.MQCHT_CLNTCONN
        cd.TransportType = CMQC.MQXPT_TCP
        '''
        if Params.WebSphereChannelSecured.lower() == 'true':
            log('Using security exit channel %s' %Params.WebSphereMQChannel)
            cd.SecurityExit = "BCPKIJCExit_70R(SECSEND)"
        else:
            log('Using unsecured exit channel %s' %Params.WebSphereMQChannel)
        '''
        self.queueName = queueName

        log("Opening WebSphereMQ connection: %s" % client)
        self.queueManager = pymqi.QueueManager(None)
        self.queueManager.connectWithOptions(
            Params.WebSphereMQQueueManager, cd
        )
        log("Opened WebSphereMQ connection: %s" % self.queueManager)

    def close(self):
        log("Closing WebSphereMQ connection: %s" % self.queueManager)
        self.queueManager.disconnect()

    def handle(self, message):
        try:
            log("Message: %s" % message)
            log("Sending to queue: %s" % self.queueName)
            self.queueManager.put1(self.queueName, message)
        except Exception:
            traceback.print_exc()
            self.queueManager.disconnect()
            raise


class MessageHandler(object):

    def __init__(self, destination):
        if Params.MessageBroker == MessageBrokerType.ActiveMQ:
            self.sender = ActiveMQMessageSender(destination)

        if Params.MessageBroker == MessageBrokerType.WebSphereMQ:
            self.sender = WebSphereMQMessageSender(destination)

    def handle(self, message, recordNumber=None):
        self.sender.handle(message)

    def close(self):
        self.sender.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.close()


def process(storedQueryName, date, processor, filter=None):
    log("Processing")
    start_time = datetime.fromtimestamp(time())
    storedQuery = getStoredQuery(storedQueryName)
    log("Executing query %s" % storedQuery.Name())
    records = storedQuery.Query().Select()
    log("Found %s records" % len(records))
    if filter is not None:
        log("Filtering...")
        records = filter(records, date)
        log("Filtered to %s records" % len(records))
    for idx, record in enumerate(records):
        processor.process(record, date, idx)
    end_time = datetime.fromtimestamp(time())
    duration = end_time - start_time
    log("Processed %s records in %s" % (len(records), duration))


def positionFilter(trades, date):
    log("Position Filter")
    positions = []
    if date is None:
        date = acm.Time.DateNow()
    positionDict = calculatePositions(trades, date)
    for (portfolio, instrument) in positionDict:
        positions.append(
            (portfolio, instrument, positionDict[(portfolio, instrument)],
            date)
        )
    return positions


def calculatePositions(trades, date):
    log("Calculating Positions")

    start_time = datetime.fromtimestamp(time())
    positionDict = {}
    for trade in trades:
        key = (trade.Portfolio(), trade.Instrument())
        if key not in positionDict:
            positionDict[key] = 0

        ins = trade.Instrument()

        if (ins.IsKindOf(acm.FBond) or
                ins.IsKindOf(acm.FIndexLinkedBond)):

            if (ins.Isin() != '' and ins.maturity_date() > date and
                    date >= trade.AcquireDay()):
                leg = ins.Legs().At(0)
                legInfo = leg.LegInformation(date)
                staticLegInfo = leg.StaticLegInformation(ins, date, None)
                nominalValue = staticLegInfo.NominalValue(
                    date, legInfo).Number()

                nominal = (
                    trade.Quantity() * ins.ContractSize() * nominalValue
                )
                positionDict[key] = positionDict[key] + nominal

        elif (ins.IsKindOf(acm.FStock) or ins.IsKindOf(acm.FETF)):
            if ins.Isin() != '':
                nominal = (
                    trade.Position()
                )
                positionDict[key] = positionDict[key] + nominal

    end_time = datetime.fromtimestamp(time())
    duration = end_time - start_time
    log("Found %s positions in %s" % (len(positionDict), duration))
    return positionDict


def adjustDeposit(
        accountNumber, valueDate, direction, quantity, externalReference,
        logMessages=None):

    if accountNumber is None or accountNumber == "":
        log("Must specify an account number", logMessages)
        raise FunctionalError(logMessages[-1])

    callDeposit = None
    callDepositTrade = None

    callDeposit = acm.FDeposit[accountNumber]
    if not callDeposit:
        log(
            'Call account "{0}" cannot be found in Front Arena'.format(
            accountNumber), logMessages
        )
        raise FunctionalError(logMessages[-1])
    else:
        log('CallDeposit found: ' + callDeposit.Name())
        statuses = ('BO-BO Confirmed', 'BO Confirmed', 'FO Confirmed')

        trades = [trade for trade in callDeposit.Trades()
            if trade.Status() != 'Void']

        for status in statuses:
            if not callDepositTrade:
                for trade in trades:
                    if trade.Status() == status:
                        callDepositTrade = trade
                        break

        if callDepositTrade is not None:
            log(
                'Found callDepositTrade: %s' % callDepositTrade.Oid(),
                logMessages
            )
            log(
                'Counterparty: %s' % callDepositTrade.Counterparty().Name(),
                logMessages
            )
        else:
            log(
                'A confirmed trade was not found for {0}.'.format(
                callDeposit.Name()), logMessages
            )
            raise FunctionalError(logMessages[-1])

        adjustDate = valueDate
        adjustment = direction * abs(quantity)

        log(
            "Adjusting Deposit for amount: %s on date: %s " % (adjustment,
            adjustDate), logMessages
        )

        if (adjustDate > callDeposit.EndDate()):
            log(
                (
                    "Warning: the adjust date %s is greater than the end "
                    "date %s of the call call account, this adjustment is "
                    "likely to fail!"
                ) % (adjustDate, callDeposit.EndDate()),
                    logMessages
            )

        leg = callDeposit.Legs()[0]
        for cashflow in leg.CashFlows():
            if (cashflow.PayDate() == adjustDate
                    and cashflow.CashFlowType() == 'Fixed Amount'
                    and cashflow.FixedAmount() == adjustment):
                log(
                    (
                        'There is already a cashflow with the specified '
                        'nominal and date: {0} on {1}'
                    ).format(adjustDate, callDeposit.Name()), logMessages
                )
                raise FunctionalError(logMessages[-1])

        if (abs(adjustment) < 0.00000001):
            log('The adjustment value is 0, we will not adjust, because it will fail', logMessages)
            raise FunctionalError(logMessages[-1])

        adjustResult = callDeposit.AdjustDeposit(
            adjustment, adjustDate, callDepositTrade.Quantity()
        )
        log("adjustResult: %s" % adjustResult)

        if adjustResult == True:
            acm.PollDbEvents()
            cashflows = callDeposit.Legs()[0].CashFlows()
            lastCashflow = max(cashflows, key=lambda cashflow: cashflow.Oid())

            # This addinfo is required for filtering in Settlement Manager.
            at_addInfo.save_or_delete(lastCashflow, 'Settle_Type', 'Settle')

            lastCashflowClone = lastCashflow.Clone()
            lastCashflowClone.ExternalId = externalReference
            lastCashflow.Apply(lastCashflowClone)
            lastCashflow.Commit()

            print lastCashflow
        else:
            log(
                (
                    "Adjusting deposit %s (Trade No.:%s) failed, "
                    "see the log for details."
                ) % (callDeposit.Name(), callDepositTrade.Oid()), logMessages
            )
            raise FunctionalError(logMessages[-1])

        return callDepositTrade


def setAddInfo(name, object, value):
    try:
        ai=getattr(object.AdditionalInfo(), name)
        if not ai():
            ais = acm.FAdditionalInfoSpec[name]
            ai = acm.FAdditionalInfo()
            ai.Recaddr(object.Oid())
            ai.AddInf(ais)
            ai.FieldValue(value)
            ai.Commit()
        else:
            ai(value)
        return True
    except Exception as ex:
        log (str(ex) + str(object.Oid())+ ' ' + name + ' '+ value)
        return False
