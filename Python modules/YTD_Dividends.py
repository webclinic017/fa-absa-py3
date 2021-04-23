import acm, ael

ael_variables = [('todate', 'To Date:', 'string', ael.date_today(), ael.date_today(), 0)]

global portList
portList = acm.FDictionary()


def get_links(name):
    port = acm.FCompoundPortfolio['%s' %name]
    if port:
        ports = acm.FPortfolioLink.Select('ownerPortfolio="%s"' %name)
        return ports

def get_port_struc(name):
    if name:
        pl = get_links(name)  
        
        if pl:
            portList[name] = 0
            for p in pl:
                get_port_struc(p.MemberPortfolio().Name())
        else:
            portList[name] = 0
    
def ASQL(*rest):
    acm.RunModuleWithParameters( 'YTD_Dividends', 'Standard' )
    return 'SUCCESS'
    
def ael_main(dict, *rest):   
    portList.Clear()
    get_port_struc('9806')
    
    header = 'Instrument,Portfolio,Position,Pay Date,Ex Date,Dividend,Payout\n'
    fileName = 'F:\Dividend.csv'
    outfile=  open(fileName, 'w')
    outfile.write(header)
    
    toDate = dict['todate']
    fromDate = ael.date(toDate).first_day_of_year()
    
    query = "exDivDay >= '%s' and exDivDay <= '%s'" %(fromDate, toDate)   
    dividends = acm.FDividend.Select(query)
    for dividend in dividends:
        if (dividend.Instrument().InsType() == 'Stock'):
            tradeQuery = "instrument = '%s' and tradeTime <= '%s' and status <> 'Simulated' and status <> 'Void' and status <> 'Reserved' and status <> 'Confirmed Void'" %(dividend.Instrument().Oid(), dividend.ExDivDay())
            trades = acm.FTrade.Select(tradeQuery)
            if trades:
                for trade in trades:                
                    portfolio = trade.Portfolio().Name()
                    if portList.HasKey(portfolio):                    
                        portList[portfolio] += trade.Quantity()
                
                for key in portList.Keys():                    
                    if portList[key] != 0:
                        outfile.write(dividend.Instrument().Name() + ',' + key + ',' + str(portList[key]) + ',' + dividend.PayDay() + ',' + dividend.ExDivDay() + ',' + str(dividend.Amount()) + ',' + str(dividend.Amount() * portList[key]) + '\n')

    func=acm.GetFunction('msgBox', 3)
    func("Information", "Completed - saved as " + fileName, 0)
    outfile.close()
