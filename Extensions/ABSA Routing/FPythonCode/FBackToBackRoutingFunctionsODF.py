'''================================================================================================
================================================================================================'''
import acm, FRoutingCommon
from at import  TP_FX_SPOT, TP_FX_FORWARD,  TP_SPOT_COVER_PARENT, TP_DRAWDOWN_CHILD, TP_DRAWDOWN_OFFSET, TP_SALES_COVER_CHILD, TP_SALES_COVER_PARENT, TP_PROLONG_PARENT, TP_PROLONG_CHILD
from FBackToBackRoutingUtilsODF import CreateMirrorTrade, PortfolioSpt, PortfolioFwd, AddInfoOrTriangulate, AddInfoOrFxRate, GetDrawdownOffsetTrade, TpBreakdown 
from FRoutingExtensions import InitialExerciseEventValueDate
ZAR = acm.FCurrency['ZAR']
USD = acm.FCurrency['USD']
USDZAR = USD.CurrencyPair(ZAR)
'''================================================================================================
Example:
    CURRENCY_PAIR   = GBP/ZAR
    STRIKE          = 14.5
    B2BAcquirerFwd  = USD/ZAR:FWD|GBP/USD:HDG
    B2BAcquirerSpt  = USD/ZAR:AGG|GBP/USD:JDY
    B2BCrossMktPr   = 14.51
    B2BAllInPr      = 9.477124
    B2BSptMktPr     = 9.2763
    B2BSplitAllInPr = 1.53
    B2BSplitSptMktPr= 1.52
Notes:
    This function is also used for close ( the trade process for the close will be the TP_DRAWDOWN_OFFSET )
    This function creataes  FX Cash trades
Parameters:
    trade           =   NB: WILL ALWAYS BE AN ODF INSTRUMENT
                        This will either be the the original ODF or in the case of a DRWDOWN_OFFSET it will be the ODF drwdown trade  
    close           =   only to decide what we should set the TradeProcess()    
================================================================================================'''
def FXODFSpotCover( trade , addInfoProxy , operationParameters , close = False):

    origTrade = acm.FTrade[trade.ContractTrdnbr()]   
    origOdf = origTrade.Instrument()  
    assert origOdf.InsType() == 'FXOptionDatedFwd', 'FXODFSpotCover can only process ODF instruments'
    tradeCurrencyPair = trade.CurrencyPair()
    dealtCurrency = origOdf.Underlying()
   
    usdzarSpotPortfolio = PortfolioSpt( origTrade.AdditionalInfo(), USDZAR, operationParameters )
    usdzarFwdPortfolio = PortfolioFwd(  origTrade.AdditionalInfo(), USDZAR, operationParameters, False )        
    
    if tradeCurrencyPair != USDZAR: 
    
        NONUSD = tradeCurrencyPair.Currency2() if tradeCurrencyPair.Currency1() == ZAR else tradeCurrencyPair.Currency1()    
        splitCurrencyPair = USD.CurrencyPair(NONUSD)

        splitSpotPortfolio = PortfolioSpt( addInfoProxy, splitCurrencyPair, operationParameters )
        splitFwdPortfolio = PortfolioFwd( addInfoProxy, splitCurrencyPair, operationParameters, True )
        
        B2BSplitSptMktPr = AddInfoOrFxRate( addInfoProxy.B2BSplitSptMktPr(), splitCurrencyPair )   
        B2BCrossSptMktPr = addInfoProxy.B2BCrossSptMktPr()
        SpotCoverRate = AddInfoOrTriangulate( addInfoProxy.B2BSptMktPr(), USDZAR, tradeCurrencyPair, B2BCrossSptMktPr, splitCurrencyPair, B2BSplitSptMktPr)     
        
        splitTrade = acm.FTrade() # Create a trade in the split currency pair
        splitTrade.Instrument( splitCurrencyPair.Currency1() )     
        splitTrade.Currency( splitCurrencyPair.Currency2() )
        splitTrade.TradeTime( trade.TradeTime() ) 
        splitTrade.GroupTrdnbr( origTrade )                                     
        splitTrade.ValueDay( trade.ValueDay() )                          
        splitTrade.AcquireDay( trade.AcquireDay() )
        splitTrade.MirrorPortfolio( splitSpotPortfolio )  
        splitTrade.Portfolio( splitFwdPortfolio )    
        splitTrade.Counterparty( trade.Counterparty() ) 
        splitTrade.Acquirer(  splitFwdPortfolio.PortfolioOwner() ) 
        splitTrade.Price( B2BSplitSptMktPr )                             
        splitTrade.ReferencePrice( splitTrade.Price() )
        splitTrade.DiscountingType( origOdf.DiscountingType() )
        splitTrade.TradeProcess( TP_FX_SPOT )
        if dealtCurrency == ZAR: #funtion to do this  
            if origOdf.Currency() == splitCurrencyPair.Currency2():         
                splitTrade.Quantity( -1 * ( trade.ODFQuantity() / SpotCoverRate ) ) # Original ODF : (ZAR/JPY OR CAD/ZAR)
            else:                                                               
                splitTrade.Quantity( ( trade.ODFQuantity() / SpotCoverRate) / B2BSplitSptMktPr ) # Original ODF : (ZAR/BWP OR GBP/ZAR)
        else:
            # Scenario : (***/USD OR USD/***)
            if dealtCurrency == splitCurrencyPair.Currency1(): 
                splitTrade.Quantity( -1 * trade.ODFQuantity() ) # Original ODF : (GBP/ZAR OR ZAR/BWP) splitCurrencyPair : (GBP/USD OR BWP/USD)
            else:
                splitTrade.Quantity( trade.ODFQuantity() / B2BSplitSptMktPr )
        splitTrade.UpdatePremium( True )
        
        usdZarTrade = acm.FTrade() # Create a trade in the USD/ZAR currency pair
        usdZarTrade.Instrument( USD )     
        usdZarTrade.Currency( ZAR )
        usdZarTrade.TradeTime( trade.TradeTime() ) 
        usdZarTrade.GroupTrdnbr( origTrade )                                     
        usdZarTrade.ValueDay( trade.ValueDay() )                          
        usdZarTrade.AcquireDay( trade.AcquireDay() )
        usdZarTrade.MirrorPortfolio( usdzarSpotPortfolio )
        usdZarTrade.Portfolio( usdzarFwdPortfolio )  
        usdZarTrade.Counterparty( usdzarFwdPortfolio.PortfolioOwner() )   
        usdZarTrade.Acquirer( usdzarSpotPortfolio.PortfolioOwner() )  
        usdZarTrade.DiscountingType( origOdf.DiscountingType() )
        usdZarTrade.Price( SpotCoverRate )                       
        usdZarTrade.ReferencePrice( usdZarTrade.Price() )
        usdZarTrade.TradeProcess( TP_FX_SPOT )
        if dealtCurrency == ZAR:  
            usdZarTrade.Quantity( trade.ODFQuantity() / SpotCoverRate ) 
        else: 
            if dealtCurrency != splitCurrencyPair.Currency1():
                usdZarTrade.Quantity( -1* ( trade.ODFQuantity() / B2BSplitSptMktPr )) # GBP/ZAR : ZAR/BWP   
            else:
                usdZarTrade.Quantity( -1* ( trade.ODFQuantity() * B2BSplitSptMktPr )) # CAD/ZAR : ZAR/JPY
        usdZarTrade.UpdatePremium(True)
  
    else:  #tradeCurrencyPair == USDZAR:
        B2BSptMktPr = AddInfoOrFxRate( addInfoProxy.B2BSptMktPr(), tradeCurrencyPair ) 
        usdZarTrade = acm.FTrade() # Create a trade in the USD/ZAR currency pair
        usdZarTrade.Instrument( USD )     
        usdZarTrade.Currency( ZAR )
        usdZarTrade.TradeTime( trade.TradeTime() ) 
        usdZarTrade.GroupTrdnbr( origTrade )                                     
        usdZarTrade.ValueDay( trade.ValueDay() )                          
        usdZarTrade.AcquireDay( trade.AcquireDay() )
        usdZarTrade.MirrorPortfolio( usdzarSpotPortfolio )
        usdZarTrade.Portfolio( usdzarFwdPortfolio )  
        usdZarTrade.Counterparty( usdzarSpotPortfolio.PortfolioOwner() )   
        usdZarTrade.Acquirer( usdzarFwdPortfolio.PortfolioOwner() ) 
        usdZarTrade.DiscountingType( origOdf.DiscountingType() )
        usdZarTrade.Price( B2BSptMktPr )                  
        usdZarTrade.ReferencePrice( usdZarTrade.Price() )
        usdZarTrade.TradeProcess( TP_FX_SPOT )        
        usdZarTrade.Quantity( trade.ODFQuantity() / B2BSptMktPr ) if origOdf.Quotation().Name() == 'Per Unit Inverse' else usdZarTrade.Quantity(-1*( trade.ODFQuantity() ))
        usdZarTrade.UpdatePremium(True)

    if close == False: trade.TradeProcess( trade.TradeProcess() + TP_SPOT_COVER_PARENT )
    return [usdZarTrade, splitTrade] if tradeCurrencyPair != USDZAR else [usdZarTrade]
    
'''================================================================================================
Parameters
    trade               = FXCash trade representing the draw-down child    
    operationParameters = 
Example
    B2BAcquirerFwd      = USD/ZAR:FWD|GBP/USD:HDG
    B2BAcquirerSpt      = USD/ZAR:AGG|GBP/USD:JDY
    B2BMktPr            = 9.477124
    B2BSplitMktPr       = 1.53
================================================================================================'''
def FXODFDrawdownCash( trade, addInfoProxy, operationParameters ):

    assert trade.Instrument().InsType() == 'Curr', 'FXODFDrawdownCash can only handle currency instuments'
    origTrade = acm.FTrade[trade.ContractTrdnbr()]  
    origOdf =  origTrade.Instrument()
    tradeCurrencyPair = trade.CurrencyPair()
    usdzarFwdPortfolio = PortfolioFwd( origTrade.AdditionalInfo(), USDZAR, operationParameters, False )   #original trade addinfo proxy ???
    constellation = []
    #print usdzarFwdPortfolio.Name()  #returning FLO
    
    if tradeCurrencyPair != USDZAR: 
        assert addInfoProxy.B2BCrossMktPr() != None, 'The additional info B2BCrossMktPr must be supplied for the draw-down child cash cross trade' 
    
        NONUSD = tradeCurrencyPair.Currency2() if tradeCurrencyPair.Currency1() == ZAR else tradeCurrencyPair.Currency1()    
        splitCurrencyPair = USD.CurrencyPair(NONUSD)
        splitFwdPortfolio = PortfolioFwd( addInfoProxy, splitCurrencyPair, operationParameters, True )

        B2BCrossSptMktPr = addInfoProxy.B2BCrossMktPr()
        B2BSplitMktPr = AddInfoOrFxRate( addInfoProxy.B2BSplitMktPr(), splitCurrencyPair, trade.ValueDay() ) 
        B2BMktPr = AddInfoOrTriangulate( addInfoProxy.B2BMktPr(), USDZAR, tradeCurrencyPair, B2BCrossSptMktPr, splitCurrencyPair, B2BSplitMktPr)   

        splitOdf = acm.FOdf[str(ExternalId1.Oid()) + '_' + splitCurrencyPair.Name()]
        usdZarOdf = acm.FOdf[str(ExternalId1.Oid()) + '_' + USDZAR.Name()] 
        
        usdZarSales = GetDrawdownOffsetTrade( usdZarOdf, trade.Portfolio())
        usdZarFwd = GetDrawdownOffsetTrade( usdZarOdf, usdzarFwdPortfolio )
        splitSales = GetDrawdownOffsetTrade( splitOdf, trade.Portfolio())
        splitFwd = GetDrawdownOffsetTrade( splitOdf, splitFwdPortfolio ) #there are two trades  ???
        
        splitTrade = acm.FTrade() # Create a trade in the split currency pair
        splitTrade.Instrument( splitCurrencyPair.Currency1() )     
        splitTrade.Currency( splitCurrencyPair.Currency2() )
        splitTrade.GroupTrdnbr( origTrade )
        splitTrade.TradeTime( trade.TradeTime() )    
        splitTrade.AcquireDay( trade.AcquireDay() )
        splitTrade.ValueDay( trade.ValueDay() ) 
        splitTrade.Trader( trade.Trader() )
        splitTrade.DiscountingType( trade.DiscountingType() )  
        splitTrade.TradeProcess( TP_FX_SPOT + TP_DRAWDOWN_CHILD ) 
        splitTrade.Price( B2BSplitMktPr )                             
        splitTrade.ReferencePrice( splitTrade.Price() )   
        splitTrade.Status('Internal') 
        splitTrade.Type( trade.Type() )
        splitTrade.ContractTrdnbr( splitFwd )
        splitTrade.Portfolio( splitFwd.Portfolio() ) 
        splitTrade.Acquirer( splitFwd.Acquirer() )
        splitTrade.Counterparty( splitFwd.Counterparty() )
        
        if tradeCurrencyPair.Currency1() != ZAR:
            if tradeCurrencyPair.Currency1() == splitCurrencyPair.Currency1():
                splitTrade.Quantity( trade.Quantity() ) # (tradeCurrencyPair GBP/ZAR - splitCurrencyPair GBP/USD)           
            else:
                splitTrade.Quantity( -1 * trade.Quantity() / B2BSplitMktPr ) # (tradeCurrencyPair CAD/ZAR - splitCurrencyPair USD/CAD)    
        else:
            if tradeCurrencyPair.Currency2() == splitCurrencyPair.Currency1():
                splitTrade.Quantity( trade.Premium() ) # tradeCurrencyPair ZAR/BWP splitCurrencyPair 
            else:
                splitTrade.Quantity( -1 * (trade.Premium() / B2BSplitMktPr ) ) # tradeCurrencyPair ZAR/JPY splitCurrencyPair  

        splitTrade.UpdatePremium( True )
        splitTrade_mirror = CreateMirrorTrade( splitTrade, trade.Portfolio(), splitSales ) # Create the mirror trade of the split trade  
        constellation.extend( [splitTrade_mirror, splitTrade] ) # Add the split trade and mirror split trade to the constellation   
        
        usdZarTrade = acm.FTrade() # Create a trade in the USD/ZAR currency pair
        usdZarTrade.Instrument( USD )     
        usdZarTrade.Currency( ZAR )    
        usdZarTrade.GroupTrdnbr( origTrade )
        usdZarTrade.TradeTime( trade.TradeTime() )  
        usdZarTrade.AcquireDay( trade.AcquireDay() )        
        usdZarTrade.ValueDay( trade.ValueDay() )          
        usdZarTrade.Trader( trade.Trader() ) 
        usdZarTrade.DiscountingType( trade.DiscountingType() )  
        usdZarTrade.TradeProcess( TP_FX_SPOT + TP_DRAWDOWN_CHILD ) 
        usdZarTrade.Portfolio( USDZAR.ForwardPortfolio()  )    
        usdZarTrade.Status('Internal')
        usdZarTrade.Type( trade.Type() )        
        usdZarTrade.Price( B2BMktPr )                  
        usdZarTrade.ReferencePrice( B2BMktPr ) 
        usdZarTrade.Acquirer( usdZarFwd.Acquirer() )
        usdZarTrade.Counterparty( usdZarFwd.Counterparty() )
        usdZarTrade.ContractTrdnbr( usdZarFwd )
        if tradeCurrencyPair.Currency1() == ZAR:  
            if tradeCurrencyPair.Currency2() == splitCurrencyPair.Currency1(): 
                usdZarTrade.Quantity( ( trade.Premium() * B2BSplitMktPr ) ) # Scenario ZAR/BWP splitCurrencyPair BWP/USD 
            else:
                usdZarTrade.Quantity( ( trade.Premium() / B2BSplitMktPr ) ) # Scenario ZAR/JPY splitCurrencyPair USD/JPY 
        else:        
            if tradeCurrencyPair.Currency1() == splitCurrencyPair.Currency1():
                usdZarTrade.Quantity( ( trade.Quantity() * B2BSplitMktPr ) )# Scenario GBP/ZAR    
            else:
                usdZarTrade.Quantity( ( trade.Quantity() / B2BSplitMktPr ) )# Scenario CAD/ZAR 
        usdZarTrade.UpdatePremium( True )

    elif tradeCurrencyPair == USDZAR:

        usdZarOdf = origOdf 
        usdZarSales = GetDrawdownOffsetTrade( usdZarOdf, trade.Portfolio() )
        usdZarFwd = GetDrawdownOffsetTrade( usdZarOdf, usdzarFwdPortfolio )  #what trade we getting here   
        #print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        #why it not in the correct portfolio
        #for t in usdZarOdf.Trades():
        #    print t.Portfolio().Name() , t.TradeProcessesToString()
        #print usdzarFwdPortfolio.Name()
        #print usdZarSales.Oid()
        #print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'

        usdZarTrade = acm.FTrade() # Create a trade in the USD/ZAR currency pair
        usdZarTrade.Instrument( USD )     
        usdZarTrade.Currency( ZAR )    
        usdZarTrade.GroupTrdnbr( origTrade )
        usdZarTrade.TradeTime( trade.TradeTime() )  
        usdZarTrade.AcquireDay( trade.AcquireDay() )        
        usdZarTrade.ValueDay( trade.ValueDay() )          
        usdZarTrade.Trader( trade.Trader() ) 
        usdZarTrade.DiscountingType( trade.DiscountingType() )  
        usdZarTrade.TradeProcess( TP_FX_SPOT + TP_DRAWDOWN_CHILD ) 
        usdZarTrade.Status('Internal')
        usdZarTrade.Type( trade.Type() )
        usdZarTrade.Quantity( origTrade.ODFQuantity() )   
        usdZarTrade.Price( origOdf.InitialExerciseEventStrike() )                  
        usdZarTrade.ReferencePrice( usdZarTrade.Price() ) 
        usdZarTrade.UpdatePremium( True )
        usdZarTrade.Portfolio( usdzarFwdPortfolio ) 
        usdZarTrade.Acquirer( usdZarFwd.Acquirer() )                   
        usdZarTrade.Counterparty( usdZarFwd.Counterparty() )             
        usdZarTrade.ContractTrdnbr( usdZarSales )
        
    usdZarTrade_mirror = CreateMirrorTrade( usdZarTrade, trade.Portfolio(), usdZarSales ) # Create a mirror trade in the USD/ZAR trade
    constellation.extend( [ usdZarTrade_mirror, usdZarTrade] ) # Add USD/ZAR + mirror trades to constellation
    return [constellation]
'''================================================================================================
Example:
    CURRENCY_PAIR   = GBP/ZAR
    STRIKE          = 14.5
    B2BAcquirerFwd  = USD/ZAR:FWD|GBP/USD:HDG
    B2BAcquirerSpt  = USD/ZAR:AGG|GBP/USD:JDY
    B2BCrossMktPr   = 14.51
    B2BAllInPr      = 9.477124
    B2BSptMktPr     = 9.2763
    B2BSplitAllInPr = 1.53
    B2BSplitSptMktPr= 1.52
    B2BMktPr

    Its looking athe wrong place for forwards trads
    but must look at iteslef for 
================================================================================================'''
def FXODFDrawdownODF( trade , operationParameters , close = False):

    constellation = []
    origOdf = trade.Instrument() 
    assert origOdf.InsType() == 'FXOptionDatedFwd', 'FXODFDrawdownODF can only process ODF instruments'
    origTrade = acm.FTrade[trade.ContractTrdnbr()] 
    #addInfoProxy = acm.FAdditionalInfoProxy( origTrade )
    quotation = origOdf.Quotation().Name()
    dealtCurrency = origOdf.Underlying()
    tradeCurrencyPair = trade.CurrencyPair()
    usdzarFwdPortfolio = PortfolioFwd( origTrade.AdditionalInfo(), USDZAR )   
    
    if tradeCurrencyPair != USDZAR: 
    
        NONUSD = tradeCurrencyPair.Currency2() if tradeCurrencyPair.Currency1() == ZAR else tradeCurrencyPair.Currency1() 
        
        splitCurrencyPair = USD.CurrencyPair( NONUSD )
        splitFwdPortfolio = PortfolioFwd( origTrade.AdditionalInfo(), splitCurrencyPair, None, True )    
        splitOdf = acm.FOdf[ str( origTrade.ExternalId1() ) + '_' + splitCurrencyPair.Name() ]        
        usdZarOdf = acm.FOdf[ str( origTrade.ExternalId1() ) + '_' + USDZAR.Name() ] 
        
        splitSales = GetDrawdownOffsetTrade( splitOdf, trade.Portfolio() ) #GetDrawdownOffsetTrade should be called SalesCoverChild
        splitFwd = GetDrawdownOffsetTrade( splitOdf, splitFwdPortfolio ) 
        usdZarSales = GetDrawdownOffsetTrade( usdZarOdf, trade.Portfolio())
        usdZarFwd = GetDrawdownOffsetTrade(usdZarOdf, usdzarFwdPortfolio )
        
        splitTrade = acm.FTrade()                       # Create a trade in the split ODF
        splitTrade.Instrument( splitOdf )    
        splitTrade.TradeTime( trade.TradeTime() )  
        splitTrade.GroupTrdnbr( origTrade.Oid() )  
        splitTrade.ValueDay( trade.ValueDay() )           
        splitTrade.AcquireDay( trade.ValueDay() )
        splitTrade.Type( trade.Type())                  
        splitTrade.ContractTrdnbr( splitSales )
        splitTrade.Portfolio( trade.Portfolio() ) 
        splitTrade.Acquirer( trade.Acquirer() ) 
        splitTrade.Counterparty( trade.Counterparty() ) 
        splitTrade.TradeProcess( TP_DRAWDOWN_OFFSET + TP_SALES_COVER_CHILD ) if close == False else  splitTrade.TradeProcess( trade.TradeProcess() + TP_SALES_COVER_CHILD )
        
        if quotation == 'Per Unit':
            if dealtCurrency != ZAR:
                if splitCurrencyPair.Currency1()  == origOdf.Underlying():
                    splitTrade.Quantity( trade.Quantity() )
                    splitTrade.Currency( splitCurrencyPair.Currency2() ) 
                else:
                    splitTrade.Quantity( trade.Quantity() )
                    splitTrade.Currency( splitCurrencyPair.Currency1() ) 
            else: 
                if splitCurrencyPair.Currency1()  == origOdf.Currency(): # Scenario ZAR/BWP (split BWP/
                    splitTrade.Quantity( trade.Quantity() * origOdf.InitialExerciseEventStrike() )
                    splitTrade.Currency( splitCurrencyPair.Currency2() ) 
                else:                                             
                    splitTrade.Quantity( -1 * ( trade.Quantity() * origOdf.InitialExerciseEventStrike() ))  # Scenario ZAR/JPY   
                    splitTrade.Currency( splitCurrencyPair.Currency1() ) 
        else: 
            if dealtCurrency != ZAR:
                if splitCurrencyPair.Currency1() == dealtCurrency: # Scenario ZAR/BWP (splitCurrencyPair BWP/USD ) 
                    splitTrade.Quantity( trade.Quantity() )
                    splitTrade.Currency( splitCurrencyPair.Currency2() ) 
                else:                                               
                    splitTrade.Quantity( -1 * (trade.Quantity() )) # Scenario ZAR/JPY (splitCurrencyPair USD/JPY )      
                    splitTrade.Currency( splitCurrencyPair.Currency1() ) 
            else: 
                splitTrade.Quantity( trade.Quantity() / origOdf.InitialExerciseEventStrike() )
                if splitCurrencyPair.Currency1() == origOdf.Currency():    
                    splitTrade.Currency( splitCurrencyPair.Currency2() ) # GBP/ZAR
                else:                                               
                    splitTrade.Currency( splitCurrencyPair.Currency1() ) # CAD/ZAR
        
        splitTrade_mirror = CreateMirrorTrade( splitTrade, splitCurrencyPair.ForwardPortfolio(), splitFwd ) # Create the mirror trade of the split trade  
        constellation.extend( [splitTrade, splitTrade_mirror] ) # Add the split trade and mirror split trade to the constellation
        
        B2BAllInPr = usdZarOdf.InitialExerciseEventStrike()         # Retreive the B2B allin price     
        B2BSplitAllInPr = splitOdf.InitialExerciseEventStrike()         
        
        usdZarTrade = acm.FTrade()                          
        usdZarTrade.Instrument( usdZarOdf )    
        usdZarTrade.TradeTime( trade.TradeTime() ) 
        usdZarTrade.GroupTrdnbr( origTrade.Oid() )
        usdZarTrade.ValueDay( trade.ValueDay() )           
        usdZarTrade.AcquireDay( trade.ValueDay() )
        usdZarTrade.Portfolio( trade.Portfolio() ) 
        usdZarTrade.Acquirer( trade.Acquirer() ) 
        usdZarTrade.Counterparty( usdzarFwdPortfolio.PortfolioOwner() ) 
        usdZarTrade.Currency( USD )
        usdZarTrade.Type( trade.Type() )
        usdZarTrade.TradeProcess( TP_DRAWDOWN_OFFSET + TP_SALES_COVER_CHILD ) if close == False else usdZarTrade.TradeProcess( trade.TradeProcess() + TP_SALES_COVER_CHILD  )
        usdZarTrade.ContractTrdnbr( usdZarSales )
        
        if quotation == 'Per Unit': 
            usdZarTrade.Currency( ZAR )
            if tradeCurrencyPair.Currency2() == ZAR: 
                if splitCurrencyPair.Currency2() == USD: 
                    usdZarTrade.Quantity( -1 * trade.Quantity() *  B2BSplitAllInPr) # GBP/ZAR 
                else:    
                    usdZarTrade.Quantity( -1 * trade.Quantity() /  B2BSplitAllInPr) # CAD/ZAR  
            else:
                usdZarTrade.Quantity( -1 * trade.Quantity() /  B2BAllInPr)            
        else:  
            usdZarTrade.Currency( USD )
            if tradeCurrencyPair.Currency2()  == ZAR: 
                usdZarTrade.Quantity( -1 * trade.Quantity() ) # CAD/ZAR - GBP/ZAR
            else:
                usdZarTrade.Quantity( -1 * trade.Quantity() / origOdf.InitialExerciseEventStrike() )  # ZAR/JPY - ZAR/BWP 
        
    else: #tradeCurrencyPair == USDZAR:
       
        usdZarOdf = origOdf  # Retreive the USD/ZAR ODF
        usdZarSales = GetDrawdownOffsetTrade( usdZarOdf, trade.Portfolio() )           
        usdZarFwd = GetDrawdownOffsetTrade( usdZarOdf, usdzarFwdPortfolio )           
      
        usdZarTrade = acm.FTrade()  # Create a trade in the original ODF
        usdZarTrade.Instrument( usdZarOdf )    
        usdZarTrade.TradeTime( trade.TradeTime() ) 
        usdZarTrade.GroupTrdnbr( origTrade.Oid() )
        usdZarTrade.ValueDay( trade.ValueDay() )           
        usdZarTrade.AcquireDay( trade.ValueDay() )
        usdZarTrade.Portfolio(trade.Portfolio() ) 
        usdZarTrade.Acquirer( usdZarFwd.Acquirer() ) 
        usdZarTrade.Counterparty( usdZarFwd.Counterparty() ) 
        usdZarTrade.Currency( USD )
        usdZarTrade.Type( trade.Type() )
        usdZarTrade.TradeProcess( TP_DRAWDOWN_OFFSET + TP_SALES_COVER_CHILD ) if close == False else usdZarTrade.TradeProcess( trade.TradeProcess() + TP_SALES_COVER_CHILD  )
        usdZarTrade.Quantity( -1 * trade.Quantity() )
        usdZarTrade.Currency( trade.Currency() )
        usdZarTrade.ContractTrdnbr( usdZarSales )
        
    usdZarTrade_mirror = CreateMirrorTrade( usdZarTrade, USDZAR.ForwardPortfolio(), usdZarFwd ) # Create the mirror trade of the USD/ZAR trade  
    constellation.extend( [ usdZarTrade, usdZarTrade_mirror ] ) # Add USD/ZAR + mirror trades to constellation
    return constellation
'''================================================================================================
================================================================================================'''
def FXODFSalesCoverPayment( originaltrade, trade, inverse, operationParameters, addInfoProxy ):
    payment = acm.FPayment()  
    payment.Trade( trade )              
    payment.PayDay( trade.TradeTime() )          
    payment.ValidFrom( trade.TradeTime() )
    payment.Party( trade.Counterparty() )  #Acquirer
    payment.Type('Cash')            
    payment.Text('Sales Margin')          
    payment.Currency( ZAR)
    quantity = originaltrade.ODFQuantity()  
    B2BMktPr = addInfoProxy.B2BMktPr() if originaltrade.CurrencyPair() == USDZAR else addInfoProxy.B2BCrossMktPr()  
    amount = ( (quantity * originaltrade.Instrument().InitialExerciseEventStrike() ) - (quantity * B2BMktPr) )
    if inverse == True: amount = amount * -1
    payment.Amount( amount ) 
    return payment
'''================================================================================================
Example:
    CURRENCY_PAIR   = GBP/ZAR
    STRIKE          = 14.5
    B2BAcquirerFwd  = USD/ZAR:FWD|GBP/USD:HDG
    B2BAcquirerSpt  = USD/ZAR:AGG|GBP/USD:JDY
    B2BCrossMktPr   = 14.51
    B2BAllInPr      = 9.477124
    B2BSptMktPr     = 9.2763
    B2BSplitAllInPr = 1.53
    B2BSplitSptMktPr= 1.52
If cross we will create two new ODF istrument in the cross currencyies    
================================================================================================'''
def FXODFSalesCover( trade, addInfoProxy, operationParameters):

    origOdf = trade.Instrument() 
    assert origOdf.InsType() == 'FXOptionDatedFwd', 'FXODFSalesCover can only process ODF instruments'

    quotation = origOdf.Quotation().Name()
    dealtCurrency = origOdf.Underlying()
    tradeCurrencyPair = trade.CurrencyPair()
    constellation = []
    
    if tradeCurrencyPair != USDZAR: 
    
        NONUSD = tradeCurrencyPair.Currency2() if tradeCurrencyPair.Currency1() == ZAR else tradeCurrencyPair.Currency1()    
        splitCurrencyPair = USD.CurrencyPair( NONUSD )   
        splitFwdPortfolio = PortfolioFwd( addInfoProxy, splitCurrencyPair, operationParameters, True )
        usdZarFwdPortfolio = PortfolioFwd( addInfoProxy, USDZAR, operationParameters, False )
        B2BSplitAllInPr = AddInfoOrFxRate( addInfoProxy.B2BSplitAllInPr(), splitCurrencyPair, InitialExerciseEventValueDate(trade) )
        
        splitOdf = acm.FOdf() # Create the ODF of the split currency
        splitOdf.SpotBankingDaysOffset(0)
        splitOdf.ExternalId1( str( origOdf.ExternalId1() ) + '_' + splitCurrencyPair.Name() )
        splitOdf.Name( NONUSD.Name() + '/USD/' + NONUSD.Name() + '/' + str( trade.Oid() ) ) 
        splitOdf.DiscountingType( origOdf.DiscountingType() )
        
        splitEv = acm.FExerciseEvent() # Add draw-down period to split ODF
        splitEv.Instrument( splitOdf )
        splitEv.Type( 'DrawdownPeriod' )
        splitEv.Start_day( origOdf.InitialExerciseEventStartDate() )   
        splitEv.End_day( origOdf.InitialExerciseEventEndDate() )    
        splitEv.Strike( B2BSplitAllInPr )                      
        splitEv.Strike2( splitEv.Strike() ) 
        
        splitTrade = acm.FTrade() # Create a trade in the split ODF (make a function for this)
        splitTrade.GroupTrdnbr( trade )
        splitTrade.Instrument( splitOdf )    
        splitTrade.TradeTime( trade.TradeTime() )  
        splitTrade.ValueDay( trade.ValueDay() )           
        splitTrade.AcquireDay( trade.ValueDay() )
        splitTrade.Trader( acm.User() )
        splitTrade.Portfolio( trade.Portfolio() ) 
        splitTrade.Acquirer( trade.Acquirer() ) 
        splitTrade.Counterparty( trade.Counterparty() )  
        splitTrade.TradeProcess( TP_SALES_COVER_CHILD )
        
        if quotation == 'Per Unit':
            if dealtCurrency == ZAR:
                splitOdf.Underlying( origOdf.Currency() )  
                if splitCurrencyPair.Currency1()  == origOdf.Currency(): 
                    # Scenario ZAR/BWP 
                    splitOdf.IsCallOption( origOdf.IsCallOption() )     
                    splitOdf.Quotation('Per Unit') 
                    splitOdf.Currency( splitCurrencyPair.Currency2() )                                    
                    splitTrade.Quantity( ( trade.Quantity() * origOdf.InitialExerciseEventStrike() ) )
                else:                                             
                    # Scenario ZAR/JPY      
                    splitOdf.IsCallOption( origOdf.IsCallOption() == False )     
                    splitOdf.Quotation( 'Per Unit Inverse' )      
                    splitOdf.Currency( splitCurrencyPair.Currency1() )                                    
                    splitTrade.Quantity( -1 * ( trade.Quantity() * origOdf.InitialExerciseEventStrike() ) )
            else:
                splitOdf.IsCallOption( origOdf.IsCallOption() == False )     
                splitOdf.Underlying( dealtCurrency ) 
                if splitCurrencyPair.Currency1() == dealtCurrency:
                    splitOdf.Quotation('Per Unit')
                    splitOdf.Currency( splitCurrencyPair.Currency2() )                                    
                    splitTrade.Quantity( trade.Quantity() )
                else: 
                    # Scenario CAD/ZAR 
                    splitOdf.Quotation( 'Per Unit Inverse' )     
                    splitOdf.Currency( splitCurrencyPair.Currency1() )                                    
                    splitTrade.Quantity( trade.Quantity() )
        else: 
            if dealtCurrency == ZAR:
                splitOdf.IsCallOption( origOdf.IsCallOption() )  
                splitOdf.Underlying( origOdf.Currency() )  
                splitTrade.Quantity( trade.Quantity() / origOdf.InitialExerciseEventStrike() )
                if splitCurrencyPair.Currency1() == origOdf.Currency():
                    # Scenario GBP/ZAR splitCurrencyPair
                    splitOdf.Quotation( 'Per Unit' )
                    splitOdf.Currency( splitCurrencyPair.Currency2() )                                    
                else:
                     # Scenario CAD/ZAR splitCurrencyPair                                       
                    splitOdf.Quotation( 'Per Unit Inverse' ) 
                    splitOdf.Currency( splitCurrencyPair.Currency1() )                                    
            else:
                splitOdf.Underlying( dealtCurrency ) 
                if splitCurrencyPair.Currency1() == dealtCurrency:
                    # Scenario ZAR/BWP splitCurrencyPair BWP/USD
                    splitOdf.IsCallOption( origOdf.IsCallOption() == False )  
                    splitOdf.Quotation( 'Per Unit' ) 
                    splitOdf.Currency( splitCurrencyPair.Currency2() )                                    
                    splitTrade.Quantity( trade.Quantity() )
                else:  
                    # Scenario ZAR/JPY       
                    splitOdf.IsCallOption( origOdf.IsCallOption() )                              
                    splitOdf.Quotation( 'Per Unit Inverse' )
                    splitOdf.Currency( splitCurrencyPair.Currency1() )                                    
                    splitTrade.Quantity( -1* trade.Quantity() )   
                    
        splitTrade.Currency( splitOdf.Currency() )  #set the trade currency to the instrument currency 
        mirrorSplitTrade = CreateMirrorTrade( splitTrade, splitFwdPortfolio )          # Create the mirror trade of the split trade
        constellation.extend( [splitOdf, splitEv, splitTrade, mirrorSplitTrade] )    # Add the split ODF, exercise event, split trade and mirror split trade to the constellation
        
        usdZarOdf = acm.FOdf() # Create the ODF of the USD/ZAR currency pair
        usdZarOdf.SpotBankingDaysOffset(0)
        usdZarOdf.ExternalId1( str(origOdf.ExternalId1()) + '_USD/ZAR' ) 
        usdZarOdf.Name( 'USD/ZAR/USD/' + str( trade.Oid() ) )
        usdZarOdf.Quotation( quotation ) 
        usdZarOdf.DiscountingType( origOdf.DiscountingType() )
        usdZarOdf.IsCallOption( origOdf.IsCallOption() ) if tradeCurrencyPair.Currency2() == ZAR else usdZarOdf.IsCallOption( origOdf.IsCallOption() == False )
        
        if addInfoProxy.B2BAllInPr() != None: # Retreive the B2B allin price
            B2BAllInPr = addInfoProxy.B2BAllInPr()    
        else:
            B2BAllInPr = origOdf.InitialExerciseEventStrike() if tradeCurrencyPair == USDZAR else USDZAR.TriangulateRate( splitCurrencyPair, B2BSplitAllInPr, tradeCurrencyPair, origOdf.InitialExerciseEventStrike() )
        
        usdZarEv = acm.FExerciseEvent() # Add draw-down period to the USD/ZAR ODF
        usdZarEv.Instrument( usdZarOdf )
        usdZarEv.Type('DrawdownPeriod')
        usdZarEv.Start_day( origOdf.InitialExerciseEventStartDate() )
        usdZarEv.End_day( origOdf.InitialExerciseEventEndDate() )    
        usdZarEv.Strike( B2BAllInPr )                        
        usdZarEv.Strike2( usdZarEv.Strike() )
       
        usdZarTrade = acm.FTrade() # Create a trade in the USD/ZAR ODF
        usdZarTrade.GroupTrdnbr( trade )
        usdZarTrade.Instrument( usdZarOdf )    
        usdZarTrade.TradeTime( trade.TradeTime()) 
        usdZarTrade.ValueDay( trade.ValueDay() )           
        usdZarTrade.AcquireDay( trade.ValueDay() )
        usdZarTrade.Trader( acm.User() ) 
        usdZarTrade.Portfolio( trade.Portfolio() ) 
        usdZarTrade.Acquirer( trade.Counterparty() ) 
        usdZarTrade.Counterparty( usdZarFwdPortfolio.PortfolioOwner() ) 
        usdZarTrade.TradeProcess( TP_SALES_COVER_CHILD )
        constellation.extend( [ usdZarOdf, usdZarEv ] ) # Add the USD/ZAR ODF and exercise event to the constellation

        if quotation == 'Per Unit':
            usdZarOdf.Currency( ZAR )          
            usdZarOdf.Underlying( USD )                 
            if tradeCurrencyPair.Currency2() == ZAR: 
                if splitCurrencyPair.Currency2() == USD:
                    usdZarTrade.Quantity( -1 * trade.Quantity() *  B2BSplitAllInPr) # tradeCurrencyPair GBP/ZAR  
                else:    
                    usdZarTrade.Quantity( -1 * trade.Quantity() /  B2BSplitAllInPr) # tradeCurrencyPair CAD/ZAR   
            else:
                usdZarTrade.Quantity( -1 * trade.Quantity() /  B2BAllInPr)            
        else:  
            usdZarOdf.Currency( USD )          
            usdZarOdf.Underlying( ZAR )
            if tradeCurrencyPair.Currency2() == ZAR:
                usdZarTrade.Quantity( -1 * trade.Quantity() )  # tradeCurrencyPair CAD/ZAR:GBP/ZAR
            else:
                usdZarTrade.Quantity( -1 * trade.Quantity() / origOdf.InitialExerciseEventStrike() ) # tradeCurrencyPair ZAR/JPY:ZAR/BWP         
        usdZarTrade.Currency( usdZarOdf.Currency() )
        
    else: #tradeCurrencyPair == USDZAR: 
        usdZarFwdPortfolio = PortfolioFwd( addInfoProxy, USDZAR, operationParameters, False )
        usdZarOdf = origOdf         # Retreive the original USD/ZAR ODF
        usdZarTrade = acm.FTrade()  # Create a trade in the original ODF
        usdZarTrade.GroupTrdnbr( trade )
        usdZarTrade.Instrument( usdZarOdf )    
        usdZarTrade.TradeTime( trade.TradeTime()) 
        usdZarTrade.ValueDay( trade.ValueDay() )           
        usdZarTrade.AcquireDay( trade.ValueDay() )
        usdZarTrade.PositionPair( USDZAR )
        usdZarTrade.Acquirer( usdZarFwdPortfolio.PortfolioOwner() ) 
        usdZarTrade.Counterparty( trade.Acquirer() ) 
        usdZarTrade.Portfolio( trade.Portfolio() ) 
        usdZarTrade.Trader( acm.User() )
        usdZarTrade.TradeProcess( TP_SALES_COVER_CHILD )
        usdZarTrade.Quantity( -1 * trade.Quantity() )
        usdZarTrade.Currency( usdZarOdf.Currency() )
    
    mirrorTrade = CreateMirrorTrade( usdZarTrade, usdZarFwdPortfolio ) # Create the mirror trade of the USD/ZAR trade
    usdZarPayment = FXODFSalesCoverPayment( trade, usdZarTrade, True, operationParameters, addInfoProxy)  # Create payments for USD/ZAR + mirror trades
    mirrorPayment = FXODFSalesCoverPayment( trade, mirrorTrade, False, operationParameters, addInfoProxy)
    constellation.extend( [usdZarTrade, usdZarPayment, mirrorTrade, mirrorPayment] ) # Add USD/ZAR + mirror trades and payments to constellation
    trade.TradeProcess( trade.TradeProcess() + TP_SALES_COVER_PARENT )  # Update trade process of original trade
    return constellation
'''================================================================================================
268435456 TP_DRAWDOWN_OFFSET
536870912 TP_DRAWDOWN_CHILD (shifted value)
536879104 TP_DRAWDOWN_CHILD (xml value)
================================================================================================'''
def FXStandard( trade, operationParameters , cover = True):
    
    constellation = acm.FArray()
    tradeProcess = trade.TradeProcess()
    tradeProcessList = TpBreakdown(tradeProcess)
    
    assert FRoutingCommon.TradeAIproxyInstance != None, 'TradeAIProxy cannot be None'
    assert FRoutingCommon.TradeAIproxyInstance.Trade() == trade, 'TradeAiProxy trade must be equal to routed trade'
    assert trade.CurrencyPair().IncludesCurrency(ZAR), 'ZAR must be included in the traded currency pair'
    
    if trade.Instrument().InsType() == 'FXOptionDatedFwd':
        assert len(trade.Instrument().ExerciseEvents()) == 1, 'No Draw Down period supplied' 
        ev = trade.Instrument().ExerciseEvents()[0]
        assert ev.Strike() == ev.Strike2(), 'Strike Price for Start and End Period should be the same'
        #assert acm.Time.DateDifference( trade.Instrument().InitialExerciseEventEndDate(),acm.Time.DateToday()) > 0 , 'Exercise event end date has expired and instrument should be closed.'
    
    if trade.Type() == 'Closing':
        constellation.AddAll( FXODFDrawdownODF( trade, operationParameters, True ))
        if TP_PROLONG_PARENT not in tradeProcessList:
           constellation.AddAll( FXODFSpotCover( trade, FRoutingCommon.TradeAIproxyInstance, operationParameters, True )) 
    elif tradeProcess == TP_DRAWDOWN_OFFSET: #268435456
        print '1'
        constellation.AddAll( FXODFDrawdownODF( trade, operationParameters )) 
    elif tradeProcess == (TP_FX_FORWARD + TP_DRAWDOWN_CHILD): #536879104
        print '2'
        constellation.AddAll( FXODFDrawdownCash( trade, FRoutingCommon.TradeAIproxyInstance, operationParameters )) 
    else:
        print '3'
        trade.ContractTrdnbr( trade )
        SalesCover = FXODFSalesCover( trade, FRoutingCommon.TradeAIproxyInstance, operationParameters )
        constellation.AddAll(SalesCover)
        TextArray = trade.Text1().split('|')
        Type = 'None'
        if len(TextArray) == 3:
            Type = TextArray[2]
        if Type != 'C5': #MIGRATION ONLY 
            if cover == True and TP_PROLONG_CHILD not in tradeProcessList:  
                constellation.AddAll( FXODFSpotCover( trade, FRoutingCommon.TradeAIproxyInstance, operationParameters ))
    trade.GroupTrdnbr(acm.FTrade[trade.ContractTrdnbr()])
    for item in constellation:
        if item.Class() == acm.FTrade:
           if item.Status() != 'Simulated': item.Status('Internal')    

    if trade.Instrument().InsType() == 'FXOptionDatedFwd': trade.Instrument().SpotBankingDaysOffset(0)
    return constellation
'''================================================================================================
================================================================================================'''
def FXStandardNoCover( trade, operationParameters ):
    return FXStandard( trade, operationParameters, False)
'''================================================================================================
================================================================================================'''
