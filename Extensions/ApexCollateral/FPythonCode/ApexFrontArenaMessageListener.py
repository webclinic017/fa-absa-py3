"""
Entry point for FA -> Apex integration.

This job takes data from AMB and places them on MQ if the trade satisfies
a filter definition.

Contact mail group: CIB Africa MAPEX BTB
"""

import amb
import acm
import socket
import ApexParameters
import FOperationsUtils as Utils
from ApexCollateralUtils import log, getObjectValue, getObject, getStoredQuery, captureMetrics, handleException, MessageHandler
from ApexEntityProcessors import BondPositionProcessor, PositionAmountType
from datetime import datetime
from time import time
import traceback

Params = ApexParameters.load()

dbTables = ['TRADE']

def receiverCallback(channel, event, arg):
    messageStr = None
    logMessages = []
    try:
        start_time = datetime.fromtimestamp(time())
        eventString = amb.mb_event_type_to_string(event.event_type)
        processed = None
        trade = None
        if eventString == 'Message':
            log("Receiver got message at %s" % acm.Time.TimeNow())
            buf = amb.mbf_create_buffer_from_data(event.message.data_p)
            message = buf.mbf_read()
            messageStr = message.mbf_object_to_string()

            messageType = getObjectValue(message, 'TYPE')

            if messageType == 'INSERT_TRADE' or messageType == 'UPDATE_TRADE':
                if messageType == 'INSERT_TRADE':
                    tradeObject = getObject(message, '+TRADE')
                if messageType == 'UPDATE_TRADE':
                    tradeObject = getObject(message, '!TRADE')
                insType = getObjectValue(tradeObject, 'INSADDR.INSTYPE')
                log('insType: %s' % insType)
                if insType in ['Bond', 'IndexLinkedBond']:
                    trade = acm.AMBAMessage().CreateObjectFromMessage(
                        message.mbf_object_to_string()
                    )
                    instrument = trade.Instrument()
                    inventoryTradesStoredQuery = getStoredQuery(
                        Params.CollateralBondInventoryTradesStoredQuery
                    )
                    inventoryTradesQuery = inventoryTradesStoredQuery.Query()
                    if inventoryTradesQuery.IsSatisfiedBy(trade):
                        log(
                            "Trade %s satisfies query %s" %
                            (trade.Oid(), inventoryTradesStoredQuery.Name())
                        )
                        amount = (
                            trade.Quantity() *
                            instrument.ContractSize()
                        )
                        with MessageHandler(Params.BondPositionQueueName) as messageHandler:
                            positionProcessor = BondPositionProcessor(messageHandler, PositionAmountType.Movement)
                            positionProcessor.process(
                                (trade.Portfolio(), instrument,
                                amount, trade.AcquireDay()), trade.TradeTime(), 0
                            )
                            processed = True
                    else:
                        log(
                            "Trade %s does not satisfy query %s" %
                            (trade.Oid(), inventoryTradesStoredQuery.Name())
                        )

        amb.mb_queue_accept(channel, event.message, 'ok')
        end_time = datetime.fromtimestamp(time())
        duration = end_time - start_time

        if processed:
            captureMetrics(duration, processed, trade.Oid())
        else:
            captureMetrics(duration, processed, None)

    except Exception as e:
        traceback.print_exc()
        handleException(
            "Receiver Got Error", e, traceback.format_exc(), logMessages
        )
        if messageStr:
            log("The message we received was: %s" % messageStr)
        raise


def start():
    Utils.Log(True, "Starting %s at %s on %s" % (__name__, acm.Time.TimeNow(), socket.gethostname()))
    initString = "%s:%s" % (Params.AmbHost, Params.AmbPort)
    Utils.Log(True, "Initialising: %s" % initString)
    amb.mb_init(initString)
    reader = amb.mb_queue_init_reader(Params.ReceiverName, receiverCallback, None)
    Utils.Log(True, "reader: %s" % reader)
    for dbTable in dbTables:
        subscriptionString = Params.ReceiverSource + '/' + dbTable
        amb.mb_queue_enable(reader, subscriptionString)

    Utils.Log(True, "Waiting for events...")

    amb.mb_main_loop()

def stop():
    Utils.Log(True, "Stopping %s at %s on %s" % (__name__, acm.Time.TimeNow(), socket.gethostname()))

def status():
    Utils.Log(True, "Running %s at %s on %s" % (__name__, acm.Time.TimeNow(), socket.gethostname()))
    return status

