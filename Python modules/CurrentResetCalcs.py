import acm
import ael
import itertools
import csv
from at_ael_variables import AelVariableHandler

calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
today = ael.date_today()

ael_variables = AelVariableHandler()
ael_variables.add('trd_filter',
    label='Trade Filter',
    cls='FTradeSelection',
    mandatory=True,   
    default='JibarLinkedTrades')

ael_variables.add('path',
    label='Export Path',
    mandatory=True, 
    default=r'C:\temp\Jibar_resets.csv')

def getResetInfo(index_ref, date):
    for price in itertools.chain(index_ref.Prices(), index_ref.HistoricalPrices()):       
        if str(price.Day()) == str(date) and price.Market().Name() in ('SPOT_MID', 'SPOT'):          
            return price.Settle()

def getCurrentResetRate(trade, currency):    
    for leg in trade.Instrument().Legs():
       
        if leg.LegType() in ('Call Float', 'Float') and  leg.Currency().Name() == currency:            
            for cashflow in leg.CashFlows():
                
                for reset in cashflow.Resets():
                    if str(reset.Day()) == str(today) and reset.ResetType() in ('Compound', 'Single', 'Unweighted', 'Weighted'):                        
                        index_ref = leg.FloatRateReference()
                        float_value = getResetInfo(index_ref, today)
                        return float_value, str(reset.Day()), index_ref.Name()


def getDateBasedNominal(trade, date): 
    nom = trade.Nominal()
    for leg in trade.Instrument().Legs():
        if leg.LegType() in ('Call Float', 'Float'):
            for cashflow in leg.CashFlows():            
                if str(cashflow.StartDate()) <= str(date) and str(cashflow.EndDate()) >= str(date):
                    calc = cashflow.Calculation()                
                    nom =  calc.Nominal(calc_space, trade).Number()    
    return nom

def ael_main(config):   
    data = []    
    trade_filter = config['trd_filter']
    for t in trade_filter.Trades():
        try:
            yesterday = today.add_period('-1d')
            trade = t.Oid()
            instype = t.Instrument().InsType()
            portfolio = t.Portfolio().Name()
            acquirer = t.Acquirer().Name()
            counterparty = t.Counterparty().Name()   
            reset_rate = getCurrentResetRate(t, 'ZAR')[0]
            reset_day = getCurrentResetRate(t, 'ZAR')[1]
            index_ref = getCurrentResetRate(t, 'ZAR')[2]
            zero_exposure = getDateBasedNominal(t, yesterday)            
        except Exception as e:
            print trade, e
        
        line = [ trade, instype, portfolio, acquirer,
                        counterparty, reset_rate, reset_day, index_ref,
                            zero_exposure]
        data.append(line)

    header = ['Trade', 'Ins Type', 'Portfolio', 'Acquirer', 'Counterparty', 'Reset Rate', 'Reset Day',
                'Reset Reference', 'Nominal']
    with open(config['path'], 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL) 
        #filewriter.writerow(['Trade', 'Curve', 'PV', 'TPL'])
        filewriter.writerow(header)
        for row in data:        
            filewriter.writerow(row)
