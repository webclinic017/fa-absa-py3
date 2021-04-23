import acm

mkt = acm.FParty[ 'internal' ]
acq = acm.FParty[ 'FMAINTENANCE' ]

def add_mtm_on_expiry(o, closeprice, date):
    trades=o.Trades()
    if trades:

        price = acm.FPrice.Select("instrument = %i and market = %i and day = %s" %(o.Oid(), mkt.Oid(), date))
        if not price:
            prcN = acm.FPrice()           
            prcN.Settle( closeprice )
            prcN.Instrument( o ) 
            prcN.Day( date )
            prcN.Market( mkt )
            prcN.Currency( o.Currency() )
            prcN.Commit()
            print '%-40s --added price' % o.Name()
            return 0.0
        else:
            if price[0].Settle() <> price[0].Settle():
                return 0.0
            else:
                return price[0].Settle()
    else:
        return 0.0


def close_single_option(o, q, price, port):
    trade = acm.FTrade()
    trade.Instrument( o)
    trade.Price( price )
    trade.Portfolio( acm.FPhysicalPortfolio[port] )
    trade.Acquirer( acq )
    trade.Counterparty( acq )
    trade.Quantity( q )
    trade.Premium( -1*q*price * o.Quotation().QuotationFactor())
    trade.ValueDay( o.ExpiryDate() )
    trade.AcquireDay( o.ExpiryDate() )
    trade.TradeTime( o.ExpiryDate() )
    trade.Currency( o.Currency() )
    trade.Status( 'BO-BO Confirmed' )
    trade.Trader( acm.User() )
    trade.Text1 = 'Closed2CleanUp'
    trade.Commit()
      

def delete_simulated_void(t):
    try:
        t.Delete()
        print '%-40s --deleted trade --%s --%s' % (t.Instrument().Name(), str(t.Oid()), t.Status())
    except:
        print '%-40s --ERROR deleting trade --%s --%s' % (t.Instrument().Name(), str(t.Oid()), t.Status())


def check_and_update_acquire_day(t):
    exp = t.Instrument().ExpiryDate()
    acq = t.AcquireDay()
    val = t.ValueDay()
    tim = t.TradeTime()
    
    if acq > exp or val > exp or tim > exp:
        t.AcquireDay(exp)
        t.ValueDay(exp)
        t.TradeTime(exp)
        t.Commit()
        print '%-40s --update val(%s)/acquire(%s)/trdtime(%s) to exp(%s) --%s' % (t.Instrument().Name(), val, acq, tim, exp, str(t.Oid()))
          
def close_open_positions(o, price):
    dict={}
   
    for t in o.Trades().AsList(): 
        if t.Status() not in ['Void', 'Simulated']:
            key = '%s:::%s' % (o.Name(), t.Portfolio().Name())
            dict.setdefault(key, []).append(t.Quantity()) 

            if t.Portfolio().Name() == 'VOE':
                check_and_update_acquire_day(t)
            
        #else:
        #    delete_simulated_void(t)
        #try and run commod futures without first deleting void.

    for k in dict:
        sum=0.0
        for q in dict[k]:
            sum+=q

        if round(sum, 8) <> 0.0:
            ins, port = k.split(':::')
            if port == 'VOE':
                close_single_option(o, -1*sum, price, port)
                print '%-40s --closed pos --%f' % (o.Name(), sum)
            
            
            
opts = acm.FOption.Select('underlyingType = "Curr" and expiryDate <"2012-08-31" ' )
def do_fxoptions():
    for opt in opts:
        
        if opt.Name() == 'ZAR/FX/USD/P/110518/7.50':
            print '******************************Special handling for problem position', opt.Name()
            #close_open_positions(opt,0.0)
            
        elif opt.Name() == 'ZAR/FX/AUD/C/120406/8.065':
            print '******************************Special handling for ITM position', opt.Name()
            #ignore = add_mtm_on_expiry(opt,0.128700,opt.ExpiryDate())
            #close_open_positions(opt,0.128700)
            
        elif opt.Name() == 'ZAR/FX/EUR/P/101225/7.004633':
            print '******************************Special handling for ITM position', opt.Name()
            #ignore = add_mtm_on_expiry(opt,625.900,opt.ExpiryDate())
            #close_open_positions(opt,625.900)            
            
        elif opt.Name() == 'ZAR/FX/USD/P/110502/7.13':
            print '******************************Special handling for ITM position', opt.Name()
            #ignore = add_mtm_on_expiry(opt,5499,opt.ExpiryDate())
            #close_open_positions(opt,5499) 
            
        elif opt.Name() == 'ZAR/FX/USD/P/120409/7.35/#1':
            print '******************************Special handling for ITM position', opt.Name()
            #ignore = add_mtm_on_expiry(opt,0.000001,opt.ExpiryDate())
            #close_open_positions(opt,0.5) 
            
        else:
            last_mtm = add_mtm_on_expiry(opt, 0.000001, opt.ExpiryDate())
            close_open_positions(opt, last_mtm)
            
         
def get_nottrading_cpties():
    not_trading=[]
    for opt in opts:
        trades = opt.Trades()
        for t in trades.AsList():
            if t.Counterparty() and t.Counterparty().NotTrading():
                not_trading.append(t.Counterparty().Name())
        
    return list(set(not_trading))

   
cpties = ['IRD INTERNAL', 'ZZZ DO NOT USE STANDARD CHARTERED LON', 'LEHMAN BROS INTL EUROPE LONDON', 'CITIBANK NA', 
'LEHMAN BROTHERS COMM CORP', 'MORGAN STANLEY CAP SERVICES NY', 'HSBC BANK USA', 'MORGAN STANLEY CAPITAL SERV NY']


def update_cpties(boo):
    for cpty in cpties:
        print 'Updating: ', cpty
        p = acm.FParty[cpty]
        p.NotTrading(boo) 
        p.Commit()
    print 'done updating cpties'
    



ael_variables = []    
def ael_main(dict):
    print '...starting'
    update_cpties(False)
    do_fxoptions()
    
    #print get_nottrading_cpties()
    
    print '...done'
