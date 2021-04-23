import acm
from at_ael_variables import AelVariableHandler

FOLDERS = acm.FStoredASQLQuery.Select('subType="FTrade"')

ael_variables = AelVariableHandler()
ael_variables.add(
    'queryFolder',
    label = 'Query Folder',
    cls = 'FStoredASQLQuery',
    collection = FOLDERS,
    default = None,
    mandatory = True,
    multiple = False,
    alt = 'Query folder for trades to update.'
    )
ael_variables.add(
    'trade_status',   
    label = 'Trade Status',
    cls = 'string',
    collection = ['FO Confirmed', 'BO Confirmed', 'Void'],
    default = 'BO Confirmed',
    mandatory = True,
    alt = 'Trade Status for update'
    )

ael_gui_parameters = {'windowCaption':'Update Trade Status'}

def ael_main(ael_dict):
    try:
        trade_set = ael_dict['queryFolder'].Query().Select()
        acm.Log('Process will update %s trades' %len(trade_set))
    except Exception as e:
        acm.Log('Error with query folder: %s' %e)
        return
    new_status = ael_dict['trade_status']
    
    for t in trade_set:
        try:
            t.Status(new_status)
            t.Commit()
            acm.Log('Trade %s updated to %s' %(t.Oid(), new_status))
        except Exception as e:
            acm.Log('Error updating trade: %s, %s' %(t.Oid(), e))
    acm.Log('Run completed')
