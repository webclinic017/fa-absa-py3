import acm
from collections import defaultdict, namedtuple
from at_time import *

context = acm.GetDefaultContext()
sheet_type = 'FPortfolioSheet'
calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )
 
cash_posting_instrument = acm.FInstrument['CASH_PAYMENT_OPTION_CURR_OTCTRUE']

for t in list(cash_posting_instrument.Trades()):
    if t.Status() in ('Simulated', 'Void'):
        t.Delete()

def create_named_param( vector, currency ): 
    param = acm.FNamedParameters();
    param.AddParameter( 'currency', acm.FCurrency[ currency ] ) 
    vector.Add( param ) 

with open(r'C:\temp\option_curr_otc.csv', 'w') as f:
    column_id = 'Portfolio Cash Vector' 
    vector = acm.FArray() 
    currencies = acm.FCurrency.Select('')
    trades_per_aggregate = defaultdict(list)
    header = '%s;%s;%s;%s;%s;%s\n' % ('Portfolio',
                        'Counterparty', 'Instrument', 'Trade Number', 'Status',	'Cash Posting Trade Number')
    f.write(header)
    
    for curr in currencies:
        create_named_param( vector, curr.Name() ) 
        
    column_config = acm.Sheet.Column().ConfigurationFromVector( vector ) 

    trades = acm.FStoredASQLQuery['Cash_Posting_CURR_OPTIONS_OTC'].Query().Select()
    
    with open(r'C:\temp\all_trades_option_curr_otc.csv', 'w') as all_f:
        header = '%s;%s;%s;%s;%s\n' % ('Portfolio',
                        'Counterparty', 'Instrument', 'Trade Number', 'Status')
        all_f.write(header)
        
        for trade in trades:
            portf = trade.Portfolio().Name()
            line = '%s;%s;%s;%s\n' % (portf, trade.Instrument().Name(), trade.Oid(), trade.Status())
            all_f.write(line)
            
    for trade in trades:
        if trade.Status() in ['Simulated', 'Void']:
            continue
            
        portf = trade.Portfolio().Name()
        cp = trade.Counterparty().Name()
        
        trades_per_aggregate[(portf, cp)].append(trade)


    for portf, cp in trades_per_aggregate:
        virtual_portf = acm.FAdhocPortfolio()
        for trade in trades_per_aggregate[(portf, cp)]:
            virtual_portf.Add(trade)
        
        calculation = calc_space.CreateCalculation(virtual_portf, column_id, column_config)
        
        acm.BeginTransaction()
        try:
            cash_posting = acm.FTrade()
            cash_posting.Instrument(cash_posting_instrument)
            cash_posting.Counterparty(cp)
            cash_posting.Acquirer('FMAINTENANCE')
            cash_posting.Trader('FMAINTENANCE')
            cash_posting.Portfolio(portf)
            cash_posting.Type('Cash Posting')
            cash_posting.Quantity(0)
            cash_posting.Status('Simulated')
            cash_posting.Currency('ZAR')
            cash_posting.TradeTime(acm_datetime('-90d'))
            cash_posting.AcquireDay(acm_date('-90d'))
            cash_posting.ValueDay(acm_date('-90d'))
            cash_posting.Commit()
            
            for v in calculation.Value():
                if v.Number():
                    payment = acm.FPayment()
                    payment.Type('Cash')
                    payment.Trade(cash_posting)
                    payment.Amount(v.Number())
                    payment.Currency(v.Unit())
                    payment.Party(cp)
                    payment.ValidFrom(acm_date('-90d'))
                    payment.PayDay(acm_date('-90d'))
                    payment.Commit()
                
            acm.CommitTransaction()
            
            
            for trade in trades_per_aggregate[(portf, cp)]:
                line = '%s;%s;%s;%s;%s;%s\n' % (portf, cp, trade.Instrument().Name(), trade.Oid(), trade.Status(), cash_posting.Oid())
                f.write(line)
        except Exception, e:
            print(e)
            acm.AbortTransaction()
