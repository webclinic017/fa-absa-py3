'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Reads messages from AMB and places them on the 
						   Markets Message Gateway
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX    Francois Truter           Initial Implementation
'''

import acm
import amb
import time
import collections
import ps_gen_swift_mt515_client_trade

from gen_absa_xml_config_settings import AmbaXmlConfig
from gen_absa_xml_config_settings import AmbaType
from gen_amb_helper import SwiftMtAmbaMessageConstants
from gen_mq import MqMessenger

SCRIPT_NAME = 'Markets Message Gateway ATS'
AMBA_NODE = 'MarketsMessageGatewayAmba'
MQ_NODE = 'MarketsMessageGatewayMq'

ambMessageNumber = 0
numberOfTries  = 0
maxNumberOfTries = 5
eventDeque = collections.deque()
subscriptions = []

DB_TABLES = [
    'TRADE',
    'SWIFT_MT'
]


class TradeStatus:
    BoConfirmed = 'TRADE_STATUS_BO_CONF'
    BoBoConfirmed = 'TRADE_STATUS_BO_BO_CONF'
    ConfirmedVoid = 'TRADE_STATUS_CONF_VOID'
    Exchange = 'TRADE_STATUS_EXCHANGE'
    FoConfirmed = 'TRADE_STATUS_FO_CONF'
    Internal = 'TRADE_STATUS_INTERNAL'
    LegallyConfirmed = 'TRADE_STATUS_LEGALLY_CONF'
    Reserved = 'TRADE_STATUS_RESERVED'
    Simulated = 'TRADE_STATUS_SIMULATED'
    Terminated = 'TRADE_STATUS_TERMINATED'
    Void = 'TRADE_STATUS_VOID'

class Event:
    
    def __init__(self, message, channel, messageNumber):
        self._message = message
        self._channel = channel
        self._messageNumber = messageNumber
        
    @property
    def Message(self):
        return self._message
        
    @property
    def Channel(self):
        return self._channel
        
    @property
    def MessageNumber(self):
        return self._messageNumber
        
class Subscription:

    def __init__(self, reader, subject):
        self._reader = reader
        self._subject = subject
        
    @property
    def Reader(self):
        return self._reader
    
    @property
    def Subject(self):
        return self._subject

def event_cb(channel, event, arg):
    global ambMessageNumber

    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == 'Status':
        try:
            ambMessageNumber = int(event.status.status)
        except ValueError:
            ambMessageNumber = 0
    elif eventString == 'Message':
        ambMessageNumber += 1
        eventDeque.append(Event(amb.mb_copy_message(event.message), channel, ambMessageNumber))
        print '%s: Added event to event queue' % SCRIPT_NAME
    else:
        print '%s: Unknown event %s' % (SCRIPT_NAME, eventString)
        
def _getSwiftMessage(message):
    list = message.mbf_find_object(SwiftMtAmbaMessageConstants.SwiftMtList, 'MBFE_BEGINNING')
    swiftMessageTag = list.mbf_find_object(SwiftMtAmbaMessageConstants.ContentTag, 'MBFE_BEGINNING')
    if not swiftMessageTag:
        raise Exception('Could not find SWIFT message content')
    
    return swiftMessageTag.mbf_get_value()
    
def _placeOnMq(message):
    print 'Connecting to MQ'
    mqMessenger = MqMessenger(MQ_NODE)
    print 'Placing message on MQ'
    mqMessenger.Put(message)
    
def _updateMt940StatementNumber(oid, date, number):
    account = acm.FDeposit[oid]
    if not account:
        print 'Error: Could not load call account [%s] to advance statement number' % oid
    else:
        account.Mt940SetStatementNumber(date, number)
        print 'Statement number for account [%(account)s] advanced to [%(statement)s] for [%(date)s]' % \
            {'account': account.Name(), 'statement': number, 'date': date}

def _updateMt535StatementNumber(oid, date, number):
    party = acm.FParty[oid]
    if not party:
        print 'Error: Could not load party [%s] to advance statement number' % oid
    else:
        party.Mt535SetStatementNumber(date, number)
        print 'Statement number for party [%(party)s] advanced to [%(statement)s] for [%(date)s]' % \
            {'party': party.Name(), 'statement': number, 'date': date}

def _postProcessSwiftMessage(ambaMessage):
    list = ambaMessage.mbf_find_object(SwiftMtAmbaMessageConstants.SwiftMtList, 'MBFE_BEGINNING')
    mtTypeTag = list.mbf_find_object(SwiftMtAmbaMessageConstants.TypeTag, 'MBFE_BEGINNING')
    if mtTypeTag and mtTypeTag.mbf_get_value() in ('MT940', 'MT535'):
        statementList = list.mbf_find_object(SwiftMtAmbaMessageConstants.StatementList, 'MBFE_BEGINNING')
        if statementList:
            oidTag = statementList.mbf_find_object(SwiftMtAmbaMessageConstants.OidTag, 'MBFE_BEGINNING')
            numberTag = statementList.mbf_find_object(SwiftMtAmbaMessageConstants.NumberTag, 'MBFE_BEGINNING')
            dateTag = statementList.mbf_find_object(SwiftMtAmbaMessageConstants.DateTag, 'MBFE_BEGINNING')
            
            if oidTag and numberTag and dateTag:
                oid = oidTag.mbf_get_value()
                number = numberTag.mbf_get_value()
                date = dateTag.mbf_get_value()
                mtType = mtTypeTag.mbf_get_value()
                if mtType == 'MT940':
                    _updateMt940StatementNumber(oid, date, number)
                elif mtType == 'MT535':
                    _updateMt535StatementNumber(oid, date, number)
    
def _getTradeStatusBefore(message):
    trade = message.mbf_find_object('!TRADE', 'MBFE_BEGINNING')
    if not trade:
        raise Exception('Could not find the TRADE list')
    status = trade.mbf_find_object('!STATUS', 'MBFE_BEGINNING')
    if status:
        return status.mbf_get_value()
    else:
        return None
    
def _getVersionId(message):
    trade = message.mbf_find_object('!TRADE', 'MBFE_BEGINNING')
    if not trade:
        raise Exception('Could not find the TRADE list')
    version = trade.mbf_find_object('VERSION_ID', 'MBFE_BEGINNING')
    if version:
        return version.mbf_get_value()
    else:
        return None
        
def PlaceMt515OnMQ(trade, version, isDuplicate):
    swiftMessage = ps_gen_swift_mt515_client_trade.CreateMt515GatewayMessageFromTrade(trade, None, version, isDuplicate)
    _placeOnMq(swiftMessage)

def work():
    if len(eventDeque) == 0:
        return

    global numberOfTries
    
    event = eventDeque.popleft()
    if len(eventDeque) > 0:
        print 'Processing event, %d in queue.' % len(eventDeque)
    else:
        print 'Processing event.'
    if numberOfTries == maxNumberOfTries:
        print 'Maximum number of tries [%i] reached for event [%i] - event removed from queue.' % (maxNumberOfTries, event.MessageNumber)
        numberOfTries = 0
        return
    
    try:
        buffer = amb.mbf_create_buffer_from_data(event.Message.data_p)
        message = buffer.mbf_read()
        
        messageType = message.mbf_find_object('TYPE', 'MBFE_BEGINNING').mbf_get_value()        
        if messageType == SwiftMtAmbaMessageConstants.NewSwiftMtAmbaMessage:
            print 'Parsing message for SWIFT message content'
            swiftMessage = _getSwiftMessage(message)
            _placeOnMq(swiftMessage)
            _postProcessSwiftMessage(message)
        
        elif messageType in ('INSERT_TRADE', 'UPDATE_TRADE'):
            trade = acm.AMBAMessage.CreateSimulatedObject(message.mbf_object_to_string())
            tradeStatus = trade.Status()
            processTrade = False
            version = None
            if (messageType == 'INSERT_TRADE' and tradeStatus == 'BO Confirmed'):
                processTrade = True
            elif messageType == 'UPDATE_TRADE':
                tradeStatusBefore = _getTradeStatusBefore(message)
                if tradeStatusBefore and ((tradeStatusBefore != TradeStatus.BoConfirmed and tradeStatus == 'BO Confirmed') or \
                    (tradeStatusBefore in (TradeStatus.BoConfirmed, TradeStatus.BoBoConfirmed, TradeStatus.LegallyConfirmed) and tradeStatus == 'Void')):
                    processTrade = True
                    version = _getVersionId(message)
            if processTrade:
                instrument = trade.Instrument()
                if instrument.Otc():
                    print 'Not processing trades for OTC instruments. Trade [%i], Instrument [%s]' % (trade.Oid(), instrument.Name())
                else:
                    PlaceMt515OnMQ(trade, version, False)
                    print '%s trade message processed' % ('New' if tradeStatus == 'BO Confirmed' else 'Cancel')
        else:
            print 'Not processing message type: %s' % messageType
        
    except Exception, ex:
        eventDeque.appendleft(event)
        numberOfTries += 1
        print 'Exception while processing event: %s' % ex
        print 'Event re-entered in the queue (try #%i). %i members in the queue.' % (numberOfTries, len(eventDeque))
    else:
        numberOfTries = 0
        amb.mb_queue_accept(event.Channel, event.Message, str(event.MessageNumber))
    
    message.mbf_destroy_object()
    buffer.mbf_destroy_buffer()
    
    print('Waiting for events...\n')

def start():
    try:
        print '%s start-up commenced on %s' % (SCRIPT_NAME, time.ctime())
        print 'Reading configuration'
        config = AmbaXmlConfig(AMBA_NODE, AmbaType.Receiver)
        
        print 'Setting up AMB subscriptions...'
        amb.mb_init(config.InitString)
        reader = amb.mb_queue_init_reader(config.ReceiverName, event_cb, None)
        for table in DB_TABLES:
            subject = '%s/%s' % (config.SenderSource, table)
            amb.mb_queue_enable(reader, subject)
            subscriptions.append(Subscription(reader, subject))
            print 'Subscribed to %s on %s:%s' % (subject, config.Host, config.Port)
        
        print '%s start-up completed at %s' % (SCRIPT_NAME, time.ctime())
        
        print('Waiting for events...\n')
        amb.mb_poll()
        
    except Exception, ex:
        print 'The following error occurred during %s start-up: %s' % (SCRIPT_NAME, ex)

def stop():   
    print 'Stopping %s on %s' % (SCRIPT_NAME, time.ctime())
    if subscriptions:
        print 'Removing subscriptions'
    else:
        print 'No subscriptions'
    for subscription in subscriptions:
        amb.mb_queue_disable(subscription.Reader, subscription.Subject)
        print 'Removed subscription %s' % subscription.Subject
        
    print '%s stopped on %s' % (SCRIPT_NAME, time.ctime())

def status():
    print 'Not implemented'
