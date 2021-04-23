import ael, acm

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

ael_variables.add(
    'cashflows',
    label = 'Cashflow numbers',
    cls = 'FCashFlow',
    collection = None,
    default = None,
    mandatory = False,
    multiple = True,
    alt = 'Cashflow numbers to Delete'
    )
    
ael_gui_parameters = {'windowCaption':'Delete Cashflows'}

def ael_main(ael_dict):
    msg_box = acm.GetFunction('msgBox', 3)
    cashFlows = ael_dict['cashflows']
    for cf in cashFlows:
        delNumber = cf.Oid()
        try: 
            cf.Delete()
            result = 'Cashflow %s deleted successfully' %delNumber
            print result
            msg_box('Information', result, 0)

        except:
            result = 'Could not delete cashflow %s' %delNumber
            print result
            msg_box('Information', result, 0)        
