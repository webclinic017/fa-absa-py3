""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/HedgingCostWorkflow.py"
import acm
from HedgingCostUtils import HedgingCostStateChartConstants, IsSwapDesk, IsHedgingCostDesk
import HedgingCostHooksHelper as hooks

EVENTS       = HedgingCostStateChartConstants.EVENTS
PAYMENT_KEYS = HedgingCostStateChartConstants.PAYMENT_KEYS

# The context parameter is an instance of FBusinessProcessCallbackContext

# Conditions return True or False
#
# Name convention is 
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
def condition_entry_state_ready(context):
    subject = context.Subject()
    
    if subject.IsKindOf(acm.FTrade):
        return hooks.IsHedgingCostCandidate(subject) and IsSwapDesk()

    return False

def condition_exit_state_ready(context):
    subject = context.Subject()
    
    if subject.IsKindOf(acm.FTrade):
        return hooks.IsHedgingCostCandidate(subject) and IsSwapDesk()
        
    return False

def condition_entry_state_pending_hedgingcost(context):
    return IsSwapDesk()

def condition_exit_state_pending_hedgingcost(context):
    return IsHedgingCostDesk()
    
def condition_entry_state_pending_confirmation(context):
    return IsHedgingCostDesk()
    
def condition_exit_state_pending_confirmation(context):
    return IsSwapDesk()
    
def condition_entry_state_confirmed(context):
    return IsSwapDesk()

# Entry/Exit callbacks do not return anything
#
# Name convention is 
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
def on_exit_state_ready(context):
    subject = context.Subject()
    subject.Changed()

def on_entry_state_pending_hedgingcost(context):
    subject = context.Subject()
    subject.Changed()
    
def on_exit_state_pending_hedgingcost(context):
    subject = context.Subject()
    subject.Changed()

def on_entry_state_pending_confirmation(context):
    subject = context.Subject()
    if subject.IsKindOf(acm.FTrade):
        paymentsDict = context.Parameters()
        paymentAmount   = paymentsDict.At( PAYMENT_KEYS.PAYMENT_TYPE )
        paymentCurrency = paymentsDict.At( PAYMENT_KEYS.PAYMENT_CURRENCY )
        
        payment = None
        
        for p in subject.Payments():
            if str( p.Type() ) == str( PAYMENT_KEYS.PAYMENT_TYPE ):
                payment = p
                break

        if not payment:
            payment = acm.FPayment()
            payment.Trade(subject)
            subject.Payments().Add( payment )

        payment.Type( PAYMENT_KEYS.PAYMENT_TYPE )
        payment.Amount( -1.0 * paymentAmount )
        payment.Currency( paymentCurrency )
        payment.Party(hooks.CreditDeskCounterParty())
        payment.PayDay(subject.AcquireDay() )
        payment.ValidFrom(subject.TradeTime())

    
def on_exit_state_pending_confirmation(context):
    event = context.Event()
    
    if event.Name() == EVENTS.HEDGINGCOST_REQUESTED:
        reRequestReason = context.Parameters().At('reRequestReason', '')
        if reRequestReason:
            context.AddNote(reRequestReason)
            
    subject = context.Subject()
    subject.Changed()
    
def on_entry_state_confirmed(context):
    subject = context.Subject()
    
    if subject.IsKindOf(acm.FTrade):
        subject.Status(hooks.ConfirmedTradeStatus())
        
    subject.Changed()

