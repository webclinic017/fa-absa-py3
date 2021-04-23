import acm

ael_variables = []
ael_variables.append(['Trades', 'Trades:', 'string', None, '', 1, 1])
ael_variables.append(['Portfolio', 'New Portfolio:', 'string', None, '', 1])

def ael_main(data):

    trade_set = data['Trades']
    new_port = data['Portfolio']
    
    for t in trade_set:
        trd = acm.FTrade[t]
        print(trd.Oid())
        trd.Portfolio(new_port)
        trd.Commit()
