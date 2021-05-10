"""----------------------------------------------------------------------------
MODULE:
    FSwiftSecuritySettlementIn

DESCRIPTION:
    OPEN EXTENSION MODULE
    Business process state callbacks.

FUNCTIONS:
    For sample state xxx there are always the four standard extension points:
        condition_entry_state_xxx():
            To control if all the pre-requisites to performing the action and
            entering the state are defined.
        on_entry_state_xxx():
            Is the place to perform the action.
            For example, the on_ entry_state_settled is the place to set the
            settlement status to Settled
        condition_exit_state_xxx():
            To control that all pre-requisites for performing the next action
            are fulfilled.
        on_exit_state_xxx():
             Is the place to reset values that you set in the state entry, if
             you are leaving the state to go backwards in the workflow.
             For example if you exit from the "Settled" state to go and re-pair,
             or to manually cancel, then you would want to remove the Settled
             status

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
from FSecuritySettlementInCallbacks import FSecuritySettlementInCallbacks

securitySettlementConfMsgCallbacks = FSecuritySettlementInCallbacks()

# The context parameter is an instance of FBusinessProcessCallbackContext
# Conditions return True or False
# Name convention is
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
def condition_entry_state_ready(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_ready(context)

def condition_entry_state_paired(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_paired(context)

def condition_entry_state_settled(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_settled(context)

def condition_entry_state_unpaired(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_unpaired(context)

def condition_entry_state_ignored(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_ignored(context)

def condition_entry_state_difference(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_difference(context)

def condition_entry_state_tradegenerated(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_tradegenerated(context)

def condition_entry_state_partialmatch(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_partialmatch(context)

def condition_entry_state_manuallycancelled(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_manuallycancelled(context)

def condition_entry_state_manuallycorrected(context):
    return securitySettlementConfMsgCallbacks.condition_entry_state_manuallycorrected(context)

# Entry/Exit callbacks do not return anything
#
# Name convention is
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
def on_entry_state_ready(context):
    securitySettlementConfMsgCallbacks.on_entry_state_ready(context)

def on_entry_state_paired(context):
    securitySettlementConfMsgCallbacks.on_entry_state_paired(context)

def on_entry_state_settled(context):
    securitySettlementConfMsgCallbacks.on_entry_state_settled(context)

def on_entry_state_unpaired(context):
    securitySettlementConfMsgCallbacks.on_entry_state_unpaired(context)

def on_entry_state_ignored(context):
    securitySettlementConfMsgCallbacks.on_entry_state_ignored(context)

def on_entry_state_difference(context):
    securitySettlementConfMsgCallbacks.on_entry_state_difference(context)

def on_entry_state_partialmatch(context):
    securitySettlementConfMsgCallbacks.on_entry_state_partialmatch(context)

def on_entry_state_manuallycancelled(context):
    securitySettlementConfMsgCallbacks.on_entry_state_manuallycancelled(context)

def on_entry_state_manuallycorrected(context):
    securitySettlementConfMsgCallbacks.on_entry_state_manuallycorrected(context)

def on_entry_state_tradegenerated(context):
    securitySettlementConfMsgCallbacks.on_entry_state_tradegenerated(context)
    '''
    print 'on entry state trade generated'
    test_trade = create_test_trade()
    # put subject of ext item to trade
    ext_item = context.Subject()
    ext_item.Subject(test_trade)
    ext_item.Commit()
    '''
'''
def create_test_trade():
    """ create test trade to generate settlement """
    trd = acm.FTrade[500] # Put example trade number
    trdClone = trd.Clone()
    trdClone = set_trade_status(trdClone, 'Simulated')
    trdClone.Commit()
    trdClone = set_trade_status(trdClone, 'FO Confirmed')
    trdClone.Commit()
    trdClone = set_trade_status(trdClone, 'BO-BO Confirmed')
    trdClone.Commit()
    print 'Created trade %d'%(trdClone.Oid())
    return trdClone

def set_trade_status(trd, status):
    """ set the trade status """
    acm.FEnumeration['enum(TradeStatus)'].Enumeration(status)
    trd.Status(status)
    return trd
'''


