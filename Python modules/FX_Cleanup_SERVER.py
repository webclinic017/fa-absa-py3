import acm
import FBDPCommon

def del_acquirers():
    '''================================================================================================
    #ReferencesIn()
    #ReferencesOut()
    ================================================================================================'''
    for ro in acm.FRoutingOperationParameters.Select(''):
        ro.Acquirer1(None)
        ro.Acquirer2(None)
        ro.Acquirer3(None)
        ro.Acquirer4(None)
        ro.Acquirer5(None)
        ro.Acquirer6(None)
        ro.Commit()
    for to in acm.FRoutingTradeParameters.Select(''):
        to.Acquirer(None)
        to.Commit()
    '''================================================================================================
    ================================================================================================'''
    Compoundports = ['FX_SPOT', 'FX_FORWARD']
    
    for port in Compoundports:
        
        coumpoundport = acm.FPhysicalPortfolio[port]
        
        if coumpoundport != None:
        
            portfoliolist = coumpoundport.AllPhysicalPortfolios()
            
            for portfolio in portfoliolist:
                for trade in portfolio.Trades():
                    if trade.Status() == 'Simulated':
                        print 'Trade Deleted', trade.Oid() 
                        FBDPCommon.delete_object(trade, False)  # this deosnt seem to handle swaps ???
                try:
                    Mem =  portfolio.MemberLinks()
                    if Mem: Mem.Delete()
                    portfolio.Delete()
                except Exception, err:
                    print portfolio.Name(),  len(portfolio.Trades()), err, portfolio.ReferencesIn()
                    print err
                    
                    
            # delete compount port if no trades        
            if len(portfoliolist) == 0:
                try:
                    Mem =  coumpoundport.MemberLinks()
                    if Mem: Mem.Delete()
                    coumpoundport.Delete()
                except Exception, err:
                    print coumpoundport.Name(),  len(coumpoundport.Trades()), err, coumpoundport.ReferencesIn()
                    print err
                
    '''================================================================================================
    ================================================================================================'''

    Acquirerlist = ['AGG', 'HDG', 'RND', 'FLO', 'FWT', 'FWD', 'CAT', 'JOL']
    for acquirer in Acquirerlist:

        Acq = acm.FInternalDepartment[acquirer] 
        if Acq != None:

            Delete = True
            for t in acm.FTrade.Select('acquirer = "%s"' % acquirer): #there still are trades
                print 'Trade Deleted', t.Oid() 
                if t.Status() == 'Simulated':
                    t.Acquirer(None)
                    t.Commit()
                    FBDPCommon.delete_object(t, False)

            #diconnect portfolios
            for p in acm.FPhysicalPortfolio.Select('portfolioOwner = %i' % Acq.Oid()):
                p.PortfolioOwner(None)
                p.Commit()

            #finally delete acquirers
            print acquirer
            if Delete == True:
                Acq.Delete()


ael_variables = []

def ael_main(parameters):   
    del_acquirers()




