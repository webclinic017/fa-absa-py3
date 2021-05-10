
import acm
from CVAUtils import CVAStateChartConstants, IsSwapDesk, IsCVADesk
import CVAHooksHelper as hooks

EVENTS       = CVAStateChartConstants.EVENTS
PAYMENT_KEYS = CVAStateChartConstants.PAYMENT_KEYS

# The context parameter is an instance of FBusinessProcessCallbackContext

# Conditions return True or False
#
# Name convention is 
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
def condition_entry_state_ready(context):
    subject = context.Subject()
    
    if subject.IsKindOf(acm.FTrade):
        return hooks.IsCVACandidate(subject) and IsSwapDesk()

    return False

def condition_exit_state_ready(context):
    subject = context.Subject()
    
    if subject.IsKindOf(acm.FTrade):
        return hooks.IsCVACandidate(subject) and IsSwapDesk()
        
    return False

def condition_entry_state_pending_cva(context):
    return IsSwapDesk()

def condition_exit_state_pending_cva(context):
    return IsCVADesk()
    
def condition_entry_state_pending_confirmation(context):
    return IsCVADesk()
    
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

def on_entry_state_pending_cva(context):
    subject = context.Subject()
    subject.Changed()
    
def on_exit_state_pending_cva(context):
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


"""
def on_entry_state_pending_confirmation(context):
    subject = context.Subject()
    if subject.IsKindOf(acm.FTrade):
        paymentsDict = context.Parameters()
        
        for paymentType in paymentsDict.Keys():
            payment = None
            updateOld = False
            
            for p in subject.Payments():
                if str(p.Type()) == str(paymentType):
                    payment = p
                    updateOld = True
                    break
                            
            if not updateOld:
                payment = acm.FPayment()
                payment.Trade(subject)
            
            amount = -1 * paymentsDict[paymentType]
            payment.Type(paymentType)
            payment.Amount(amount)
            payment.Currency(subject.CreditBalance().Currency())
            payment.Party(hooks.CreditDeskCounterParty())
            payment.PayDay(subject.AcquireDay() )
            payment.ValidFrom(subject.TradeTime())
            
            if not updateOld:
                payment.Commit()
"""
    
def on_exit_state_pending_confirmation(context):
    event = context.Event()
    
    if event.Name() == EVENTS.CVA_RE_REQUEST:
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
