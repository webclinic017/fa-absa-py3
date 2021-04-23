

import acm

# The context_clone parameter is a cloned instance of FBusinessProcessCallbackContext
# 
# In order to access the non-cloned version of a subject, for instance to access collection methods,
# please use method Originator().
# For example, the following will retrieve all trades in an instrument:
#     if subject.IsKindOf(acm.FInstrument):
#         trades = context_clone.Subject().Originator().Trades()



# Conditions return True or False
#
# Name convention is 
# 'condition_' + 'entry'/'exit' + '_state_' + state name in lowercase and underscore 
#
def condition_entry_state_a(context_clone):
    return True

    
def condition_exit_state_b(context_clone):
    return context_clone.Parameters().At('x') == 'y'
    

# Entry/Exit callbacks do not return anything
#
# Name convention is 
# 'on_' + 'entry'/'exit' + '_state_' + state name in lowercase and underscore 
#
def on_entry_state_a(context_clone):
    print ('Subject', context_clone.Subject())
    
    
def on_exit_state_b(context_clone):
    print ('Parameters', context_clone.Parameters())

