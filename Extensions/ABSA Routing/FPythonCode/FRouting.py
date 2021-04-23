'''================================================================================================
MODULE
    FRouting - Module that subscribes to AMB messages.
    (c) Copyright 2011 by SunGard Front ARENA. All rights reserved.
DESCRIPTION
================================================================================================'''
import collections, time
import acm, amb, FLogger
import FRoutingExtensions
import FOperationsUtils as Utils
from FOperationsUtils import Log
from FOperationsExceptions import AMBConnectionException 
from FRoutingCommon import FOP_PORTFOLIO, route

ambMsgNbr = 0
eventDeque = collections.deque()
dbTables = ['TRADE', 'ROUTINGREDIRECTION']
logger = FLogger.FLogger.GetLogger('ROUTING')
logger.Reinitialize(level=2) # Level 2 is debug , level 1 is for production
'''================================================================================================
================================================================================================'''
class DictionaryWrapper:
    def __init__(self, dict):
        self.dict = dict
    def __getattr__(self, name):
        s = str(self.dict.At(name))
        try:
            import ast
            return ast.literal_eval(s)
        except:
            return s
'''================================================================================================
================================================================================================'''
# AMB specific code
def event_cb(channel, event, arg):
    """
    Main callback function for AMB messages. The events are placed in a
    queue that is then processed by work.
    """
    global ambMsgNbr
    eventString = amb.mb_event_type_to_string(event.event_type)
    if eventString == 'Status':
        try:
            ambMsgNbr = int(event.status.status)
        except ValueError:
            ambMsgNbr = 0

    elif eventString == 'Message':
        ambMsgNbr += 1
        eventDeque.append((amb.mb_copy_message(event.message), channel, ambMsgNbr))
        Log(False, 'Added event with mid %d (%d in queue).' % (event.message.id, len(eventDeque)))
    else:
        Log(True, 'Unknown event %s' % eventString)

'''================================================================================================
================================================================================================'''
def work():
    """Process the event queue. """
    if not len(eventDeque):
        return
      
    (eventCopy, channel, msgNbr) = eventDeque.popleft()
    Log(True, '>>> Processing event with mid %d (%d in queue).' % (eventCopy.id, len(eventDeque)))

    buf = amb.mbf_create_buffer_from_data(eventCopy.data_p)     # mbf_buffer
    msg = buf.mbf_read()                                        # mbf_object
    process_message(msg.mbf_object_to_string())

    amb.mb_queue_accept(channel, eventCopy, str(msgNbr))
    msg.mbf_destroy_object()
    buf.mbf_destroy_buffer()
    print('>>> Waiting for events...\n')
    
'''================================================================================================
================================================================================================'''
def start():
    """Set up AMB connection."""
    Utils.InitFromParameters(routing_parameters_as_object())
    try:
        Utils.InitAMBConnection(event_cb, dbTables) #mklimke - call_back when there is a new message?      
    except AMBConnectionException, e:
        errStr = 'RBRR ATS start-up failed. %s' % e
        Log(True, errStr)
        raise

    Log(False, 'RBRR ATS start-up completed')
    print('>>> Waiting for events...\n')
    amb.mb_poll()

'''================================================================================================
================================================================================================'''
def stop(): pass
def status(): pass
'''================================================================================================
================================================================================================'''
# AMB Routing specific code
def routing_parameters_as_object():
    ctx = acm.GetDefaultContext()
    extensions = ctx.GetAllExtensions('FParameters', acm.FObject, True, True)
    for ext in extensions:
        if str(ext.Name()) == 'FRoutingParameters':
            return DictionaryWrapper(ext.Value())
'''================================================================================================
================================================================================================'''
def process_message(message):
    logger.debug('Processing message')
    obj = acm.AMBAMessage.CreateSimulatedObject(message) #do we need this ?
    if obj and obj.IsKindOf(acm.FTrade): 
        handle_trade_message(obj, message)
    elif obj and obj.IsKindOf(acm.FRoutingRedirection):
        handle_redirection_message(obj)
    else:
        logger.debug('Cannot handle message %s' % message)
'''================================================================================================
================================================================================================'''
def handle_trade_message(trade, message):
    try:
        route(trade)
    except Exception, e:
        logger.ELOG('Routing of trade %d failed: %s', trade.Oid(), str(e))    
        # Recreating the trade from the AMBA message to revert any changes
        # done during the failed operation execution
        reverted_trade = acm.AMBAMessage.CreateSimulatedObject(message)
        handle_failure(reverted_trade)
'''================================================================================================
# handle_failure does not make sense for infant trades as it's unlikely an exception would be raised
# inside a transaction. Also, there is no trade to revert to.
================================================================================================'''
def handle_failure(trade):
    def move_trade(trade):
        trade.Portfolio(FOP_PORTFOLIO)
        trade.Commit()
        logger.debug('Trade %d moved to failed operation portfolio', trade.Oid())

    def find_near_leg(far_leg):
        assert far_leg.IsFxSwapFarLeg()
        near_leg = far_leg.ConnectedTrade()
        assert near_leg.IsFxSwapNearLeg()
        return near_leg

    if trade and trade.Class() is acm.FTrade and trade.IsFxSwapFarLeg():

        far_leg = trade
        near_leg = find_near_leg(far_leg)
        # Reverts transformation
        near_leg.Undo()
        try:
            acm.BeginTransaction()
            move_trade(far_leg)
            move_trade(near_leg)
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise
    else:
        move_trade(trade)
'''================================================================================================
================================================================================================'''
def handle_redirection_message(redirection):
    if redirection.Status() == 'Enabled':
        acm.Routing.SendRedirectionMessage(redirection)
'''================================================================================================
================================================================================================'''
