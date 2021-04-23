'''
Purpose               : To populate price table on instrument with theoretically calculated price
Department and Desk   : EQ 
Requester             : Khunal Ramesar
Developer             : Rohan vd Walt
CR Number             : 654242

History:
Date       Who                   CR NR     What
2011-05-12 Rohan vd Walt         654242    Initial Dev - To populate price table on instrument with theoretically calculated price
2011-11-16 Rohan vd Walt         829813    Update to get instruments from a trade filter instead of seperately from parameters
'''

import acm, ael

def listOfTradeFilters():
    return acm.FTradeSelection.Select('')
    
ael_variables = [['TradeFilter', 'Trade Filter', acm.FTradeSelection, listOfTradeFilters(), None, 1, 0, 'Trade filter to specify ONE trade per Future Instruments where Theoretical value will be copied to price table', None, 1],
                 ['verbose', 'Verbose', 'string', ['No', 'Yes'], 'No', 1, 0, 'Verbose output', None, 1],
                 ]
    
def ael_main(dict):
    verbose = dict['verbose']
    if verbose:
        print 'Setting Market Price to Theoretical Price for instruments' 
    for ins in [t.Instrument() for t in dict['TradeFilter'].Trades()]:
        if verbose:
            print 'Instrument:', ins.Name()
        aelIns = ael.Instrument[ins.Name()]
        if ael.date_today() <= aelIns.maturity_date():
            for p in aelIns.prices():
                if p.ptynbr != None:
                    if p.ptynbr.ptyid == 'SPOT':
                        if verbose:
                            print '\tFound existing SPOT price in table', p.last
                        p_clone = p.clone()
                        theorPrice = getTheoreticalPrice(ins)
                        p_clone.bid = theorPrice
                        p_clone.ask = theorPrice
                        p_clone.settle = theorPrice
                        p_clone.last = theorPrice
                        if p.day != ael.date_today():
                            p_clone.day = ael.date_today()  
                        try:                            
                            if verbose:
                                print '\tTrying to set prices to', theorPrice
                            p_clone.commit()
                            if verbose:
                                print '\t', '-'*10, 'COMMITED', '-'*10
                        except:
                            print 'Could not update price table with theorPrice on', ins.Name()

def getTheoreticalPrice(ins):
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    calc = ins.Calculation()
    TheoPrice = calc.TheoreticalPrice(cs)
    return TheoPrice.Number()
