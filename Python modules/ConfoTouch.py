import ael, acm

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

ael_variables.add(
    'Confirmations',
    label = 'Confirmations',
    cls = 'FConfirmation',
    collection = None,
    default = None,
    mandatory = False,
    multiple = True,
    alt = 'Confirmation query to selct confirmations'
    )
    
ael_gui_parameters = {'windowCaption':'Confos Touched'}

def ael_main(ael_dict):
    msg_box = acm.GetFunction('msgBox', 3)
    confos = ael_dict['Confirmations']
    
    for confo in confos:
        try: 
            confo.Touch()
            confo.Commit()
            print 'Confo %s touched successfully' % confo.Oid()
            
        except:
            print 'could not touch confo %s' % confo.Oid()

    msg_box('Information', 'Completed, check console for result', 0)

