import ael, acm, at_time
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
    alt = 'Trade numbers to assess archive status'
    )

ael_gui_parameters = {'windowCaption':'Check Archive Status'}
   
def ael_main(ael_dict):
    msg_box = acm.GetFunction('msgBox', 3)
    trades = ael_dict['trades']
    for trade in trades:
        result = 'TradeNr: %s \nArchived: %s \nStatus: %s \nUpdated at %s \nType: %s \nAggregate: %s \nMirrorTrade: %s' \
        % (trade.Oid(), trade.IsArchived(), trade.Status(), str(at_time.to_datetime(trade.UpdateTime()))\
            , trade.Type(), trade.Aggregate(), 'None' if not trade.MirrorTrade() else trade.MirrorTrade().Oid() )
        print result
        msg_box('Trade Info', result, 0)


