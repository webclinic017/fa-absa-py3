import ael, acm

from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

ael_variables.add(
    'trades',
    label = 'Trade numbers',
    cls = 'FTrade',
    collection = None,
    default = None,
    mandatory = False,
    multiple = True,
    alt = 'Trade numbers to Touch'
    )
    
ael_gui_parameters = {'windowCaption':'Trades Touched'}

def ael_main(ael_dict):
    msg_box = acm.GetFunction('msgBox', 3)
    trades = ael_dict['trades']
    for trd in trades:
        try: 
            trd.Touch()
            trd.Commit()
            result = 'Trade %s touched successfully' % trd.Oid()
            print result
            msg_box('Information', result, 0)

        except:
            result = 'could not touch trade %s' % trd.Oid()
            print result
            msg_box('TouchTrade', result, 0)        

