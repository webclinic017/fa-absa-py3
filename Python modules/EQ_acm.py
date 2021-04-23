import ael, acm
def getvalend(t,*rest):
    t = acm.FTrade[t.trdnbr]
    tr = acm.CreateTradeRow(t, 1)
    tag = acm.CreateEBTag()
    v = acm.GetCalculatedValueFromString(tr, 'Standard', 'object:*"valPLEnd"', tag)
    return v.Value()
    
def getColumnForStartandEnd(p,start,end,value,context,*rest):
    port = acm.FPhysicalPortfolio[p.prfnbr]
    pr = acm.CreatePortfolioInstrumentAndTradeRows(port, 1, 0)
    tag = acm.CreateEBTag()
    d = '"' + start.to_string() + '"'
    d2 = '"' + end.to_string() + '"'
    print d, d2
    #List of Possible values for showWhatStartDate
    #[Inception, First Of Year, First Of Month, Two Days Ago, Yesterday, Custom Date]
    evaluator = acm.GetCalculatedValueFromString(0, context, "showWhatStartDate", tag)
    evaluator.Simulate(6, 0)
    #List of Possible values for showWhatEndDate
    #[Now, TwoDaysAgo, Yesterday, Custom Date] 
    evaluator = acm.GetCalculatedValueFromString(0, context, "showWhatEndDate", tag)
    evaluator.Simulate(4, 0)
    evaluator = acm.GetCalculatedValueFromString(0, context, "customPLStartDate", tag)
    evaluator.Simulate(d, 0)
    evaluator = acm.GetCalculatedValueFromString(0, context, "customPLEndDate", tag)
    evaluator.Simulate(d2, 0)
    v = []
    for s in value:
        v.append(acm.GetCalculatedValueFromString(pr, context, s, tag).Value())
    #To get the Valuation Viewer open
    #acm.StartApplication("Valuation Viewer",v)
    #acm.CloseApplication("Valuation Viewer")
    return v


#print getColumnForStartandEnd(ael.Portfolio['EQTESTFUND'],ael.date('2008-08-03'),ael.date('2008-08-05'),'object:*"cash"','Standard')
#print getColumnForStartandEnd(ael.Portfolio['EQTESTFUND'],ael.date('2008-08-03'),ael.date('2008-08-05'),'object:*"valPLEnd"','Standard')
