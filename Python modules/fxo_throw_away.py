import ael, acm


def listOfFilters():
    return acm.FTradeSelection.Select('')

def set_fxswaps(tlist, val):
    acm.BeginTransaction()
    try:
        for t in tlist:
            t.OptKey4(val)
            t.Commit()
        acm.CommitTransaction()
    except:
        print 'Not commited for ', tlist[0].Oid(), tlist[1].Oid()
        acm.AbortTransaction()

# =============================================================================

def setCPKey(tf):
    keys =  acm.FChoiceList.Select('list = "TradeKey4"')
    CurrDict = {}
    for k in keys:
        CurrDict[k.Name()] = k.Oid()
        
    for t in tf.Trades():
        if not t.OptKey4():
            cp =  t.CurrencyPair()
            print t.Oid(), cp.Name()
            if cp and cp.Name() in CurrDict.keys():
                if t.TradeInstrumentType() == 'Curr':
                    if t.TradeProcessesToString() in ['Swap Near Leg', 'Swap Far Leg']:
                        if t.Oid() != t.ConnectedTrade().Oid():
                            tlist = [t, t.ConnectedTrade()]
                            set_fxswaps(tlist, CurrDict[cp.Name()])
                    else:
                        try:
                            t.OptKey4(CurrDict[cp.Name()])
                            t.Commit()
                        except:
                            print 'Error on Trade : ', t.Oid(), cp.Name()
                elif t.TradeInstrumentType() == 'Option' and t.Instrument().UnderlyingType() == 'Curr':
                   
                    try:
                        t.OptKey4(CurrDict[cp.Name()])
                        t.Commit()
                    except:
                        print 'Error on Trade : ', t.Oid(), cp.Name()
                        
ael_gui_parameters = {'windowCaption':'Set Currency Pair on Trade Filter'}

ael_variables = [
['filter', 'Trade Filter', acm.FTradeSelection, listOfFilters(), None, 1, 0, 'Trade Filters to set trade key', None, 1]]

def ael_main(dict):
    if dict['filter']:
        setCPKey(dict['filter'])
