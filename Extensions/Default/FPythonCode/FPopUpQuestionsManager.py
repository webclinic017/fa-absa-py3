import acm

"""
FPopUpQuestionsManager hook template 

The hook is enabled by setting 'Manage Pop-Up Questions' in Application Settings (found in Users, 
Group & Organisation in the Administration Console) to the value 'Hook'. Once enabled, Save, SaveNew 
and Delete operations from, e.g. the Instrument Definition window or the Apply operation from the 
editable sheets will call the hook as below. In order to suppress the different pop-up dialogs, like 
the question "Do you really want to save the trade as BO Confirmed?" - filter out the question id and 
specify the answer id. By doing so, the applications will not pop the dialog (since the question is 
already set. 
  
Example:
def Save(qnA, object, *args):
    if object:
        if object.IsKindOf(acm.FInstrument):
            if qnA.QuestionId() == 'RegenerateCashFlows':
                qnA.AnswerId('all')
        elif object.IsKindOf(acm.FTrade):
            if qnA.QuestionId() == 'SaveTradeInStatus':
                qnA.AnswerId('ok')
"""

def Save(qnA, object, *args):
    pass

def SaveNew(qnA, object, *args):
    pass

def Delete(qnA, object, *args):
    pass
