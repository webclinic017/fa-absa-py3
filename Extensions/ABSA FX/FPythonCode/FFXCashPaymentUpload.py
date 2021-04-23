import acm
'''================================================================================================
can't convert 'BON' to FPhysicalPortfolio object
can't convert 'BTB' to FPhysicalPortfolio object
can't convert 'DAN' to FPhysicalPortfolio object
can't convert 'DCM' to FPhysicalPortfolio object
can't convert 'DOX' to FPhysicalPortfolio object
can't convert 'ETA' to FPhysicalPortfolio object
can't convert 'EUF' to FPhysicalPortfolio object
can't convert 'JCB' to FPhysicalPortfolio object
can't convert 'LTX' to FPhysicalPortfolio object
can't convert 'SML' to FPhysicalPortfolio object
================================================================================================'''
current_portfolio = None
currency_pair = None          
column_config = None

vector = acm.FArray()
date_today = acm.Time.DateNow()
simulate = True 

#buckets = acm.FStoredTimeBuckets['FX_Spot_Ladder'].TimeBuckets()
buckets = acm.FStoredTimeBuckets.Select01("name = 'FX_Spot_Ladder'", '').TimeBuckets()
config = acm.Report().CreatePortfolioSheetGridConfiguration(buckets)
csc = acm.Calculations().CreateCalculationSpaceCollection()
calcSpace = csc.GetSpace('FPortfolioSheet', 'Standard', config)

pos_pair = acm.Risk().GetGrouperFromName('Position Pair')
default = acm.Risk().GetGrouperFromName('Default')

#trade_port = acm.Risk().GetGrouperFromName('Trade Portfolio')
#ch_grouper = acm.FChainedGrouper([trade_port,pos_pair])

TODAY = acm.Time.DateToday()
PREBUSDAY = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(TODAY, -1)
'''================================================================================================
================================================================================================'''
def CreatePayment(Portfolio, Currency, Quantity, ValueDay, Text1, PosPair):
    try:
        trade = acm.FTrade()
        trade.Portfolio(Portfolio)
        trade.Acquirer(trade.Portfolio().PortfolioOwner())
        trade.Counterparty('FMAINTENANCE')
        trade.TradeTime(PREBUSDAY)
        trade.Currency(Currency)
        trade.Instrument(Currency)
        trade.Status('BO Confirmed')
        trade.Quantity(Quantity)
        trade.ValueDay(ValueDay)
        trade.AcquireDay(ValueDay)
        trade.Text1(Text1)
        trade.PositionPair(PosPair)
        #trade.Type('Cash Entry') #was failing with this
        trade.TradeCategory('Cash')
        if simulate == False:
            trade.Commit()
        print trade
    except Exception, e:
        print e
'''================================================================================================
================================================================================================'''
def create_named_param(vector, currency ):
    param = acm.FNamedParameters();
    param.AddParameter('currency', acm.FCurrency[currency])
    vector.Add( param )

for currency in acm.FCurrency.Select(''):
    create_named_param(vector, currency.Name())
column_config = acm.Sheet.Column().ConfigurationFromVector(vector)
'''================================================================================================
================================================================================================'''
def recurse_tree(node, port, calc_space, group):
    
    row = node.Item()
    row_name = row.StringKey()
    global vector
    global currency_pair
    global column_config

    if row.Class() == acm.FMultiInstrumentAndTrades: 
        currency_pair = acm.FCurrencyPair[row_name]

    if row_name == 'Rest': 
    
       if group == True  and currency_pair != None:
           print port.Name(), row_name, group, currency_pair.Name()
           calculation = calc_space.CreateCalculation(node, 'Portfolio Projected Payments', column_config) 
           for calc in calculation.Value(): 
                if abs(calc.Number()) > 0:
                    CreatePayment(port, calc.Unit(), -1*calc.Number(), PREBUSDAY, 'ClearCashBalance', currency_pair)

       if group == False:
           print port.Name(), row_name, group, currency_pair
           calculation = calc_space.CreateCalculation(node, 'Portfolio Projected Payments', column_config) 
           for calc in calculation.Value(): 
                if abs(calc.Number()) > 0:
                    CreatePayment(port, calc.Unit(), -1*calc.Number(), PREBUSDAY, 'ClearCashBalance', None) 
           
    #recurse tree
    if node.NumberOfChildren():
        child_iter = node.Iterator().FirstChild()
        while child_iter:
            recurse_tree(child_iter.Tree(), port, calc_space, group)
            child_iter = child_iter.NextSibling()
'''================================================================================================
must this run for portfolios under FX Salses
================================================================================================'''
ApplyGrouper = ['AGG', 'CAT', 'HDG', 'FWT', 'FLO', 'JOL', 'RND']
Ports = acm.FSet()
Ports.AddAll(ApplyGrouper)
for x in acm.FPhysicalPortfolio['FX_SALES'].AllPhysicalPortfolios():
    Ports.Add(x.Name())
Ports = []
for object in Ports:
    object = acm.FPhysicalPortfolio[object]
    top_node = calcSpace.InsertItem(object)
    if object.Name() in ApplyGrouper:
        top_node.ApplyGrouper(pos_pair)
        Group = True
    else:
        Group = False
        top_node.ApplyGrouper(default)
        
    calcSpace.Refresh()
    recurse_tree(top_node, object, calcSpace, Group)
    calcSpace.Clear()
    
SPACE = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()    
USD = acm.FCurrency['USD']    
'''================================================================================================
================================================================================================'''
def GetDollarAmount(Currency, Quantity):
    if Currency == 'USD':
        return Quantity, 1
    else:
        OtherCurr = acm.FCurrency[Currency]
        CurrPair = USD.CurrencyPair(OtherCurr)
        spotDate = CurrPair.SpotDate(acm.Time.DateNow())
        rate = CurrPair.Currency1().Calculation().FXRate(SPACE, CurrPair.Currency2(), spotDate).Value().Number()
        if rate != 0 and rate not in (float('nan'), float('inf')):
            if CurrPair.Currency1() == USD:
                return Quantity / rate, rate
            else:
                return Quantity * rate, rate
        else:
            return Quantity, rate
'''================================================================================================
================================================================================================'''
def UploadCashPayments():
    with open(r"C:\Users\klimkemi\Desktop\frontdkc.csv", "r") as f:
        for line in f.readlines():
            print line
            properties = line.split(',')
            Portfolio = properties[0].replace('"', '')
            Quantity = float(properties[2])
            Currency = properties[1].replace('"', '')

            if Currency == 'USD':
                PostionPair = acm.FCurrencyPair['USD/ZAR']
            else:
                PostionPair = acm.FCurrency[Currency].CurrencyPair(USD)
            
            dollaramount, rate  = GetDollarAmount(Currency, Quantity)
            
            print dollaramount, rate, PostionPair.Name() 
            if abs(dollaramount) > 1:
                CreatePayment(Portfolio, Currency, Quantity, PREBUSDAY, 'MidasTakeOnBalance', PostionPair)
            else:
                print 'Wont create payment for %s Portfolio and Currency %s amount less than 1 USD' % (Portfolio, Currency)

UploadCashPayments()
'''================================================================================================
================================================================================================'''
