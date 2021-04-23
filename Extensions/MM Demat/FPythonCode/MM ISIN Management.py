import acm

def on_entry_state_ready(context):
    print 'Instrument has been added to the ISIN Management process'
 
def on_entry_state_new_isin_request_to_be_sent(context):
    print 'New ISIN request to be sent - waiting for outgoing ATS to pick up'   
    
def on_entry_state_topup_reduce_request_to_be_sent(context):
    print 'Amend request to be sent - waiting for outgoing ATS to pick up'
    
def on_entry_state_deissue_request_to_be_sent(context):
    print 'Deissue request to be sent - waiting for outgoing ATS to pick up'

def hasNonNullParam(paramDict, key):
    if paramDict.HasKey(key):
        if paramDict.At(key) != None:
            return True
    return False
    
def condition_entry_state_topup_reduce_request_to_be_sent(context):
    return hasNonNullParam(context.Parameters(), 'Amend Amount')

def condition_entry_state_new_isin_request_to_be_sent(context):
    return hasNonNullParam(context.Parameters(), 'Initial Amount')
    
def condition_entry_state_active(context):
    return hasNonNullParam(context.Parameters(), 'Amount')
