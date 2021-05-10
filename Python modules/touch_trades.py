import acm, ael

ael_variables = []

def ael_main(ael_variables):
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')

    query.AddAttrNodeString('Instrument.InsType', 'Stock', 'EQUAL')
    query.AddAttrNodeString('Type', 'Aggregate', 'EQUAL')
    query.AddAttrNodeString('Status', ['Simulated', 'Void'], 'NOT_EQUAL')

    ael.log('Aggregate Trades to be recommitted: %s' % query.Select().Size())

    for t in query.Select():
        ael.log('Touched trade %s' % t.Oid())
        t.Touch()
        t.Commit()
