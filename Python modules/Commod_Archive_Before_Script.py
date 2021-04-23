# BYPASS FValidation.


import acm

mkt = acm.FParty[ 'internal' ]
acq = acm.FParty[ 'FMAINTENANCE' ]

def add_mtm_on_expiry(o, closeprice, date):
    
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


          
def close_open_positions(o, price):
    dict={}
   
    for t in o.Trades().AsList(): 
        if t.Status() not in ['Void', 'Simulated']:
            key = '%s:::%s' % (o.Name(), t.Portfolio().Name())
            dict.setdefault(key, []).append(t.Quantity())   
            
        else:
            delete_simulated_void(t)

    for k in dict:
        sum=0.0
        for q in dict[k]:
            sum+=q

        if round(sum, 8) <> 0.0:
            ins, port = k.split(':::')
            close_single_option(o, -1*sum, price, port)
            print '%-40s --closed pos --%f' % (o.Name(), sum)
            
 


stock_und_list = ['SUNS_SAFEX_MAY02', 'WMAZ_SAFEX_DEC01', 'YMAZ_SAFEX_JUL01', 'SUNS_SAFEX_JUL02', 'WMAZ_SAFEX_MAR03', 'YMAZ_SAFEX_DEC02', 'YMAZ_SAFEX_MAR03', 'WMAZ_SAFEX_SEP02', 'WMAZ_SAFEX_JUL02', 'WMAZ_SAFEX_DEC02', 'WEAT_SAFEX_MAR03', 'WEAT_SAFEX_JUL01', 'WEAT_SAFEX_DEC02', 'YMAZ_SAFEX_JUL02', 'YMAZ_SAFEX_SEP02', 'WMAZ_SAFEX_JUL01']

def get_opts_on_fut_on_commod():
    stop = False
    futs = acm.FFuture.Select('expiryDate <"2012-01-31"') # later than 2011, will block options more exactly.
    for fut in futs:
        if (fut.Underlying().InsType() == 'Commodity' or fut.Name() in stock_und_list)and not stop:
            opts = acm.FOption.Select('underlying = "%s" and expiryDate <"2011-12-31" ' % fut.Name())
        
            for o in opts:
                if o.Name() == 'ZAR/FUT/YMAZ/SAFEX/MAY03/P/1100.00':
                    print '******************************Special handling for ITM position', o.Name()
                    add_mtm_on_expiry(o, 0.000001, '30/12/2011')
                    close_open_positions(o, 180.0)
                else:
                    add_mtm_on_expiry(o, 0.000001, '30/12/2011')
                    close_open_positions(o, 0.0)
                    
    print 'done closing and adding mtm'
 
def get_opts_on_commod():
    opts = acm.FOption.Select('underlyingType = "Commodity" and expiryDate <"2011-12-31" ' )
    
    for o in opts:
        
        if o.Name() == 'ZAR/GOL/C/2675/031231':
            print '******************************Special handling for ITM position', o.Name()
            add_mtm_on_expiry(o, 0.000001, '30/12/2011')
            close_open_positions(o, 101.084245)
        else:
            add_mtm_on_expiry(o, 0.000001, '30/12/2011')
            close_open_positions(o, 0.0)
    
    
               

cpties = ['SAFEX_CLIENT',
'ZZZ DO NOT USE ABSA INSURANCE COMPANY L',
'ZZZ DO NOT USE ACBB SPECIALISED FINANCE',
'ZZZ DO NOT USE AGRI JB RHEEDER EN SEUNS',
'ZZZ DO NOT USE EZOLIMO NEMFUYO AGRICULT',
'ZZZ DO NOT USE NDALLEN BOERDERY VENNOOT',

'ZZZ DO NOT USE N3 TOLL CONCESSION',
'ZZZ DO NOT USE TELKOM',
'DEUTSCHE BANK AG NEW YORK',
'HSBC BANK USA',
'GOLD DESK.',
'MORGAN STAN CAP SER NY'
]


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
    get_opts_on_fut_on_commod()
    get_opts_on_commod()
    update_cpties(False)
    print '...done'



